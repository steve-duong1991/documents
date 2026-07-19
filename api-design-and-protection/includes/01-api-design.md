# API Design Best Practices

> **Scope:** **General REST(Representational State Transfer)/HTTP(Hypertext Transfer Protocol) API design** — resources, errors, pagination, contracts. Event-sourced command/query APIs → [ES §4 API design implications](../../event-sourcing-and-cqrs/includes/04-api-design-implications.md).

> **Related:** Protection layers → [§2 API protection](02-api-protection.md) · OpenAPI contract → [§7 OpenAPI / Swagger](07-openapi-swagger.md) · Idempotency → [§13 Idempotency](13-idempotency.md) · Versioning → [§14 API versioning](14-api-versioning-and-deprecation.md)

## What it is

API design defines **how clients interact with your system**: URLs, HTTP methods, request/response shapes, errors, pagination, and versioning. Good design is **predictable**, **consistent**, and **hard to misuse**.

## Core principles

### 1. Design around resources, not actions

Use **nouns** in paths; let HTTP verbs express behavior.

```http
GET    /v1/users/123
POST   /v1/users
PATCH  /v1/users/123
DELETE /v1/users/123
```

When CRUD does not fit, use a **sub-resource command** sparingly:

```http
POST /v1/orders/123/cancel
POST /v1/payments/456/refund
```

### 2. Be consistent

- Plural resource names: `/users`, `/orders`
- One JSON casing convention (`snake_case` or `camelCase`) everywhere
- ISO 8601 UTC dates: `2026-06-14T18:30:00Z`
- Same pagination and error shape on every endpoint
- Same wrapper pattern (either always `{ "data": ... }` or never)

### 3. Use HTTP methods and status codes correctly

| Method | Use for |
|--------|---------|
| `GET` | Read (safe, idempotent) |
| `POST` | Create or non-idempotent actions |
| `PUT` | Full replace |
| `PATCH` | Partial update |
| `DELETE` | Remove |

| Code | Meaning |
|------|---------|
| `200` | Success with body |
| `201` | Created |
| `204` | Success, no body |
| `400` | Malformed request |
| `401` | Not authenticated |
| `403` | Authenticated but not allowed |
| `404` | Resource not found |
| `409` | Conflict (duplicate, stale state) |
| `422` | Semantically invalid input |
| `429` | Rate limited |
| `500` | Server error |

**Do not** return `200` with `{ "success": false }`. **Do not** use `404` to hide authorization failures when existence leakage matters.

### 4. Standard response shapes

**List success:**

```json
{
  "data": [
    { "id": "ord_123", "status": "open", "created_at": "2026-06-14T10:00:00Z" }
  ],
  "pagination": {
    "next_cursor": "abc",
    "has_more": true
  }
}
```

**Error (same shape everywhere):**

```json
{
  "error": {
    "code": "invalid_email",
    "message": "Email must be a valid address.",
    "request_id": "req_9f2a",
    "details": [
      { "field": "email", "issue": "format" }
    ]
  }
}
```

### 5. Pagination, filtering, sorting

```http
GET /v1/orders?status=open&sort=-created_at&limit=20&cursor=abc
```

- Document supported filters explicitly
- Cap `limit` (e.g. max 100)
- Prefer **cursor pagination** for large or frequently changing datasets
- Offset pagination is simpler but performs poorly at scale

### 6. Versioning

| Approach | Example | Pros | Cons |
|----------|---------|------|------|
| **URL path** | `/v1/users` | Visible, easy to route | URLs change per version |
| **Header** | `Accept: application/vnd.app.v1+json` | Clean URLs | Harder to test in browser |
| **Query param** | `/users?version=1` | Easy to add | Messy, easy to forget |

**Rules:**

- Add optional fields freely; removing or renaming fields is **breaking**
- Deprecate with `Deprecation` and `Sunset` headers
- Never make breaking changes in place on a stable version

### 7. Write safety

```http
POST /v1/orders
Authorization: Bearer ...
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7
Content-Type: application/json
```

- **Idempotency keys** on POST with side effects (payments, orders) — full guide → [Idempotency](13-idempotency.md)
- **Optimistic concurrency** with `ETag` / `If-Match` on updates — maps to aggregate version checks; return `409 Conflict` on stale writes
- Whitelist writable fields — prevent mass assignment

For operations that may run longer than ~30 seconds (exports, batch jobs), use async job resources — see [Async patterns](10-async-patterns.md).

Event-sourced write models use the same headers for command APIs — see [Event Sourcing & CQRS](../../event-sourcing-and-cqrs/includes/04-api-design-implications.md).

### 8. Modeling tips

- Stable IDs: prefixed strings (`usr_`, `ord_`) or UUIDs — avoid exposing auto-increment integers publicly
- Money: minor units + currency code, or decimal string — **never floats**
- Enums as strings, not magic numbers
- Relationships via sub-resources: `GET /v1/users/123/orders`

## REST vs RPC-style HTTP

| Style | Pros | Cons | When to use |
|-------|------|------|-------------|
| **REST (resource-oriented)** | Predictable, cacheable, standard tooling | Awkward for complex actions | Default for most HTTP APIs |
| **RPC-style** (`POST /createOrder`) | Familiar to some teams | Inconsistent, poor cache semantics | Legacy integrations only |
| **GraphQL** | Flexible queries, one endpoint | Complexity, caching, authorization per field | Mobile/apps with varied data needs |
| **gRPC(Google Remote Procedure Call)** | Performance, strong contracts | Not browser-native | Internal microservices |

## Common mistakes

- Verbs in every URL (`/getUser`, `/deleteUser`)
- Inconsistent pluralization (`/user` vs `/orders`)
- Returning entire DB rows (password hashes, internal flags)
- Undocumented query parameters
- Giant response objects with 80+ fields
- Silent breaking changes without version bump

## Pros of strong API design

- Faster partner and client integration
- Fewer support tickets and misuse bugs
- Easier to add gateway policies and contract tests
- Clear evolution path via versioning

## Cons / trade-offs

- Contract-first design slows initial prototyping
- Strict consistency requires discipline across teams
- Over-versioning creates maintenance burden (`/v1` … `/v5`)
- REST purity can fight natural business language — pragmatic command endpoints are OK in moderation