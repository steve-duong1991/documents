# Idempotency

How to design writes that are safe to retry: HTTP(Hypertext Transfer Protocol) semantics, `Idempotency-Key` headers, storage patterns, and how idempotency fits async jobs, webhooks, and stateless app tiers.

> **Related:** Write safety contract → [API design §7](01-api-design.md#7-write-safety) · Webhook replay → [API protection §6](02-api-protection.md#6-idempotency-and-replay-protection) · Async job retries → [Async patterns](10-async-patterns.md) · Shared stores → [Stateless architecture](11-stateless-architecture.md) · Event-sourced commands → [Event Sourcing & CQRS](../../event-sourcing-and-cqrs/includes/04-api-design-implications.md) · Multi-step sagas → [Sagas and distributed workflows](../../event-sourcing-and-cqrs/includes/07B-sagas-compensation-idempotency.md#idempotency-patterns-specific-to-sagas)

## Articles in this section

| Article | Topics |
|---------|--------|
| [Client contract and server flow](13A-idempotency-client-and-server-flow.md) | Key scope, response replay, claim-before-side-effects sequence |
| [Storage patterns](13B-idempotency-storage.md) | Redis, PostgreSQL, natural domain keys, TTL(Time To Live) |
| [Async, webhooks, and OpenAPI](13C-idempotency-integrations.md) | `202` jobs, inbound webhook dedup, spec modeling, observability |

---

## At a glance

| Question | Answer |
|----------|--------|
| **What is it?** | Repeating the same operation has the same effect as doing it once |
| **Who enforces it?** | **Application layer** — not gateway or load balancer ([entry architecture](03B-api-gateway-stacks-and-selection.md#what-the-gateway-should-do)) |
| **When is a key required?** | `POST` (and some `PATCH`) with side effects: payments, orders, provisioning, external calls |
| **Where to store keys?** | Shared **Redis** or **PostgreSQL** — never per-instance memory ([stateless checklist](11A-stateless-auth-operations.md#checklist-is-your-app-tier-stateless)) |
| **Updates to existing resources?** | Use `ETag` / `If-Match`, not idempotency keys |
| **Inbound webhooks?** | HMAC(Hash-based Message Authentication Code) + timestamp + dedup by event ID — see [API protection §6](02-api-protection.md#6-idempotency-and-replay-protection) |

**Rule of thumb:** If a client might retry on timeout and a duplicate would charge money, create a row, or send a notification — require `Idempotency-Key`.

---

## What it is

**Idempotent** means calling an operation multiple times does not change state beyond the first successful application.

| Term | Meaning |
|------|---------|
| **Safe** | No side effects (reads) |
| **Idempotent** | Side effects happen at most once; repeats are no-ops or return the same outcome |

### HTTP methods (default semantics)

| Method | Idempotent? | Safe? | Notes |
|--------|-------------|-------|-------|
| `GET` | Yes | Yes | Cache-friendly reads |
| `PUT` | Yes | No | Full replace — same payload → same final state |
| `DELETE` | Yes | No | Second call → `404` or `204`; still idempotent |
| `PATCH` | Design-dependent | No | Use version checks for safe updates |
| `POST` | **No** | No | Creates or triggers actions — **needs explicit protection** |

Examples:

- `GET /orders/123` twice → same order, no extra writes.
- `DELETE /orders/123` twice → gone after first call; second is harmless.
- `POST /orders` twice with the same JSON body → **two orders** unless you implement idempotency.

---

## When to use what

### Natural idempotency (no header)

Design these to be idempotent by HTTP semantics or resource identity:

- **`GET`** — all reads
- **`PUT /resources/{id}`** — client-known ID; same body → same state
- **`DELETE /resources/{id}`** — delete is naturally repeatable

### `Idempotency-Key` header (explicit)

Require on **`POST`** when the operation:

- Moves money (charges, refunds, transfers)
- Creates durable resources (orders, subscriptions, tickets)
- Triggers external side effects (email, SMS, partner API(Application Programming Interface) calls)
- Enqueues async work the client may retry ([Async patterns](10-async-patterns.md))
- Runs on unreliable networks (mobile, partner integrations)

```http
POST /v1/orders
Authorization: Bearer ...
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7
Content-Type: application/json
```

### Optimistic concurrency (updates, not creates)

For **`PATCH`** / **`PUT`** on existing resources, prefer **`ETag`** / **`If-Match`**:

```http
PATCH /v1/orders/123
If-Match: "v5"
Content-Type: application/json
```

Return **`409 Conflict`** on stale version. This prevents lost updates; it is complementary to idempotency keys, not a replacement.

### When you can skip idempotency keys

- Pure reads
- `PUT` / `DELETE` with stable resource IDs already designed for repeat calls
- Fire-and-forget events where duplicates are harmless
- Domain models with a **natural dedup key** (e.g. `client_reference_id` on payments with a unique constraint)

---

## Decision checklist

| Question | Action |
|----------|--------|
| Is it a read? | Rely on `GET`; no key needed |
| Is it `PUT`/`DELETE` with stable ID? | Design for natural idempotency |
| Is it `POST` with money, creation, or external effects? | Require `Idempotency-Key` |
| Can the client retry on timeout? | Idempotency is mandatory |
| Is it an update to existing resource? | Use `ETag` / `If-Match` |
| Is it async (`202` + job)? | Key dedupes enqueue; worker dedupes processing |
| Is it a multi-step saga across services? | Per-step idempotency keys + saga state — see [Sagas §7](../../event-sourcing-and-cqrs/includes/07B-sagas-compensation-idempotency.md#idempotency-patterns-specific-to-sagas) |
| Is it an inbound webhook? | HMAC + timestamp + event ID dedup |
| Multiple app instances? | Shared Redis or DB store |

---

## Pre-launch checklist

| Check | Pass? |
|-------|-------|
| Side-effecting `POST`s document `Idempotency-Key` in OpenAPI | |
| Keys scoped to `(tenant, endpoint, key)` | |
| Claim happens before external side effects | |
| Same key + different body returns error | |
| Replays return identical status and body | |
| Storage is shared (Redis or DB), not in-memory | |
| TTL and processing-lock expiry documented | |
| Concurrent duplicate requests handled | |
| Async enqueue deduped on retry | |
| Metrics/logs distinguish fresh vs replay | |