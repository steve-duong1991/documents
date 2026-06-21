# Scope & Identity-Based Limiters

> **Related:** Product tier definitions → [api-design §5 Rate-limit tiers](../../api-design-and-protection/includes/05-rate-limit-tiers.md) · Gateway identity → [api-design §3 Gateway](../../api-design-and-protection/includes/03-api-gateway.md) · Layer order → [§7 Deployment layers](07-deployment-layers.md)

Rate limits can be keyed by different dimensions. Layer them from cheapest to most specific.

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

## Layered check order

Run cheapest checks first:

```text
1. Global limit        → stop volumetric attacks early
2. Per-IP limit        → catch unauthenticated abuse
3. Per identity limit  → API key / user / tenant
4. Per-endpoint limit  → protect expensive operations
```

## Best practices

- **Combine IP + identity** — per-IP alone punishes corporate NAT and mobile carriers
- **Different limits per tier** — free vs paid vs enterprise
- **Stricter limits on auth endpoints** — login, password reset, OTP
- **Looser limits on read, tighter on write** — `GET` vs `POST`/`DELETE`

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Per-IP only on authenticated API | Add per API key / user / tenant ([§6 table](#comparison)) |
| Trusting `X-Forwarded-For` without trusted proxy config | Strip/spoof at edge; only trust from load balancer |
| Same limit for `GET /health` and `POST /export` | Per-endpoint multipliers → [api-design §5](../../api-design-and-protection/includes/05-rate-limit-tiers.md#per-endpoint-multipliers) |
