# Scope & Identity-Based Limiters

> **Related:** Product tier definitions → [api-design §5 Rate-limit tiers](../../api-design-and-protection/includes/05-rate-limit-tiers.md) · Gateway identity → [api-design §3 Gateway](../../api-design-and-protection/includes/03-api-gateway.md) · Layer order → [§7 Deployment layers](07-deployment-layers.md) · Shared Redis keys → [§12 Distributed rate limiting](12-distributed-rate-limiting.md)

Rate limits can be keyed by different dimensions. Layer them from cheapest to most specific.

---

## At a glance

| Scope | Typical Redis key fragment | Counter cardinality |
|-------|---------------------------|---------------------|
| Global | `ratelimit:global:api:global` | 1 |
| Per IP | `ratelimit:ip:203.0.113.42` | ~unique IPs/day |
| Per API(Application Programming Interface) key | `ratelimit:key:key_abc123` | ~active keys |
| Per user | `ratelimit:user:usr_9f2a` | ~MAU |
| Per tenant | `ratelimit:org:org_acme` | ~tenant count |
| Per endpoint | `ratelimit:key:key_abc:export` | keys × endpoint classes |
| Per resource | `ratelimit:user:42:proj:789:upload` | **high** — cap key space |

**Rule of thumb:** Pick the **coarsest scope that still stops abuse** — per-resource keys only where object-level fairness matters (uploads, shared project quotas).

---

## Comparison

| Type | Key | Pros | Cons | When to use |
|------|-----|------|------|-------------|
| **Global** | Single counter for entire API(Application Programming Interface) | Simple DDoS brake | One noisy client affects everyone | Emergency circuit, small APIs |
| **Per IP** | Source IP / `X-Forwarded-For` | Easy, no auth needed | Shared NAT, VPN, mobile carriers; spoofable behind bad proxies | Public unauthenticated endpoints |
| **Per API Key** | `Authorization` header | Ties to billing and plan | Key sharing, leaked keys | B2B APIs, developer portals |
| **Per User / Account** | User ID from JWT(JSON Web Token)/session | Fair per customer | Requires auth on every request | Logged-in SaaS APIs |
| **Per Tenant / Org** | `org_id` | Multi-tenant fairness | Large tenants may need custom limits | B2B multi-tenant platforms |
| **Per Endpoint** | `method + path` | Protects expensive ops only | Many rules to maintain | Search, export, ML inference |
| **Per Resource** | `user:123:project:456` | Fine-grained abuse control | Key explosion, storage cost | File uploads, object CRUD |

---

## Redis key patterns by scope

When counters live in Redis (multi-instance APIs), encode **scope + identity + bucket** in the key. Full topology, hot-key mitigations, and Lua scripts → [§12](12-distributed-rate-limiting.md).

### Key template

```text
ratelimit:{scope}:{identity}:{bucket}:{window_start}
```

| Field | Meaning | Example |
|-------|---------|---------|
| `scope` | Limit dimension | `global`, `ip`, `key`, `user`, `org`, `ep` |
| `identity` | Who or what is limited | `key_abc123`, `usr_9f2a`, `203.0.113.42` |
| `bucket` | Endpoint class or `global` | `read`, `write`, `export`, `auth` |
| `window_start` | Fixed UTC minute/hour, or omit when using TTL buckets | `1735689600` |

**Global scope special case:** identity is always `api`, bucket is always `global` — full key `ratelimit:global:api:global:{window}`. Do not omit the bucket segment for global; it keeps parsing consistent with other scopes.

Use **endpoint classes** (read / write / export) instead of raw paths — avoids unbounded key cardinality from query strings.

### Examples by scope

| Scope | Redis key (sliding window, 1-minute) | Notes |
|-------|--------------------------------------|-------|
| **Global** | `ratelimit:global:api:global:1735689660` | Single key; identity `api`, bucket `global` |
| **Per IP** | `ratelimit:ip:203.0.113.42:global:1735689660` | Normalize IPv6; trust IP only from edge |
| **Per API key** | `ratelimit:key:key_abc123:global:1735689660` | Map key → tier from DB/cache at check time |
| **Per user** | `ratelimit:user:usr_9f2a:write:1735689660` | Separate read/write buckets |
| **Per tenant** | `ratelimit:org:org_acme:global:1735689660` | Enterprise custom limits override tier default |
| **Per endpoint** | `ratelimit:key:key_abc123:export:1735689660` | Stricter bucket for `POST /v1/reports/export` |
| **Per resource** | `ratelimit:user:usr_9f2a:proj:789:upload:1735689660` | Cap uploads per project, not per API key |

### Layered keys in one request

A single authenticated `POST /v1/reports/export` might increment **four** counters in order (cheapest first):

```text
1. ratelimit:global:api:global:{window}
2. ratelimit:ip:{client_ip}:global:{window}
3. ratelimit:org:{org_id}:global:{window}
4. ratelimit:key:{api_key}:export:{window}
```

Stop at the first limit exceeded — do not burn Redis round trips on lower-priority checks after a 429.

### TTL bucket variant (no window_start in key)

For simpler ops, anchor the window with Redis TTL instead of embedding `window_start`:

```text
ratelimit:key:key_abc123:export
```

On first `INCR`, set `EXPIRE 60`. Same key for the whole minute — fewer keys, slightly fuzzier boundaries at rollover. See [§12 clock skew](12-distributed-rate-limiting.md#clock-skew-and-window-boundaries).

### Key explosion and storage

| Risk | Cause | Mitigation |
|------|-------|------------|
| **Millions of keys** | Per-resource limits on every object ID | Limit to coarse resources (project, bucket) — not every row |
| **Hot key** | One viral tenant or integration user | Sub-shard or local bucket + sync → [§12 hot key](12-distributed-rate-limiting.md#key-design) |
| **Stale keys** | Fixed windows without TTL | Always `EXPIRE` or use sliding window with bounded key count |

Cardinality rule: if `keys ≈ requests × resources`, move quota to **tenant or tier** level and use application-level checks for object abuse.

---

## Layered check order

Run cheapest checks first:

```text
1. Global limit        → stop volumetric attacks early
2. Per-IP limit        → catch unauthenticated abuse
3. Per identity limit  → API key / user / tenant
4. Per-endpoint limit  → protect expensive operations
```

Gateway can enforce global + IP; app or gateway plugin enriches with API key / tenant from JWT. Layer diagram → [§7](07-deployment-layers.md).

---

## Best practices

- **Combine IP + identity** — per-IP alone punishes corporate NAT and mobile carriers
- **Different limits per tier** — free vs paid vs enterprise ([api-design §5 tiers](../../api-design-and-protection/includes/05-rate-limit-tiers.md))
- **Stricter limits on auth endpoints** — login, password reset, OTP
- **Looser limits on read, tighter on write** — `GET` vs `POST`/`DELETE`
- **Hash tags for cluster affinity** — `{org_acme}` in key when org counters need same slot for multi-key Lua
- **Document identity fallback** — if JWT missing `org_id`, fall back to user scope, not unlimited

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Per-IP only on authenticated API | Add per API key / user / tenant ([comparison table](#comparison)) |
| Trusting `X-Forwarded-For` without trusted proxy config | Strip/spoof at edge; only trust from load balancer |
| Same limit for `GET /health` and `POST /export` | Per-endpoint multipliers → [api-design §5](../../api-design-and-protection/includes/05-rate-limit-tiers.md#per-endpoint-multipliers) |
| Raw path in Redis key (`GET_/v1/orders?page=…`) | Bucket by endpoint **class** — read, write, export |
| Per-resource key on every database row | Coarse resource (project, workspace) or tenant-level cap |
| Checking all layers after first 429 | Short-circuit; return `Retry-After` from the tightest exceeded limit |