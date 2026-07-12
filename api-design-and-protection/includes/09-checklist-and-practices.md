# Checklist & Cross-Cutting Practices

> **Related:** Threat model → [§6 Threat model](06-threat-model.md) · Lifecycle → [§8 Lifecycle](08-lifecycle-and-architecture.md) · Rate limiting → [api-rate-limiting](../../api-rate-limiting/README.md)

## Pre-launch checklist

| Area | Check |
|------|-------|
| **Design** | `/v1` resources, plural nouns, standard error shape |
| **Design** | Cursor pagination with max `limit` |
| **Design** | Idempotency-Key on POST with side effects — [§13](13-idempotency.md) |
| **Design** | Long work uses `202` + job resource, not held connections |
| **Design** | Separate rate limits for expensive POST vs job status GET |
| **Design** | Webhook `callback_url` SSRF(Server-Side Request Forgery)-protected; outbound HMAC(Hash-based Message Authentication Code) signed |
| **OpenAPI** | Spec published; Swagger UI or portal live |
| **OpenAPI** | CI(Continuous Integration) contract tests pass; Spectral lint clean |
| **Auth** | OAuth(Open Authorization) + PKCE(Proof Key for Code Exchange) for user apps; scoped API(Application Programming Interface) keys for partners |
| **AuthZ** | Object ownership on every `{id}` route (BOLA(Broken Object-Level Authorization)) |
| **AuthZ** | Writable field whitelist on PATCH/POST |
| **Gateway** | Rate tiers configured; `429` + headers returned |
| **Load balancer** | Health checks enabled; targets only healthy instances |
| **Architecture** | App tier stateless — no sticky sessions; durable state in DB/Redis/S3 |
| **Architecture** | Identity from validated JWT(JSON Web Token)/API key, not server memory or request body alone |
| **Edge** | HTTPS only; WAF(Web Application Firewall) enabled; DDoS protection on |
| **Protection** | Payload size capped; request timeouts set |
| **Protection** | Secrets in vault; not in git or logs |
| **Threats** | OWASP(Open Worldwide Application Security Project) API Top 10 reviewed for new endpoints |
| **Ops** | Correlation IDs end-to-end |
| **Ops** | Alerts on 401/403/429 spikes and 5xx error rate |
| **Ops** | Runbook for key rotation and incident response |

## HTTP status code quick reference

| Code | Use | Do not use for |
|------|-----|----------------|
| `200` | Success with body | Errors |
| `201` | Resource created | Updates |
| `204` | Success, no body | Errors |
| `400` | Malformed syntax | Business rule violations |
| `401` | Missing/invalid auth | Permission denied |
| `403` | Authenticated, not allowed | Missing auth |
| `404` | Resource not found | Hiding auth failures (when sensitive) |
| `409` | Conflict / duplicate | Generic validation |
| `422` | Valid JSON, invalid semantics | Malformed JSON |
| `429` | Rate limited | Generic errors |
| `500` | Unexpected server fault | Client mistakes |

## Common mistakes

| Mistake | Why it hurts | Fix |
|--------------|--------------|-----|
| `200` + `{ success: false }` | Breaks HTTP semantics, caching, monitoring | Proper status codes |
| AuthN only at gateway | BOLA(Broken Object-Level Authorization) vulnerabilities | Object checks in app |
| IP-only rate limits | Bypassed via distributed IPs; unfair shared NAT | Identity-based tiers |
| Logging Authorization header | Credential leak in logs | Redact sensitive headers |
| Undocumented breaking changes | Broken clients, angry partners | Version bump + Sunset |
| Swagger spec neglected | Docs lie | CI contract tests |
| Fail-open rate limiter on writes | Abuse during Redis outage | Fail closed on expensive routes |
| Sync POST for multi-minute work | 504 timeouts, slot exhaustion | Job + poll or webhook ([§10](10-async-patterns.md)) |
| Sticky sessions with in-memory state | Scale/deploy breaks user sessions | Externalize state; token auth ([§11](11-stateless-architecture.md)) |
| `200` + pending on async POST | Breaks HTTP semantics | `202` + `Location` + `Retry-After` |

## Cross-cutting best practices

### Documentation

- OpenAPI as source of truth for public APIs
- Document rate tiers, auth scopes, and error codes in portal
- Provide curl examples and idempotency guidance — see [Idempotency](13-idempotency.md)

### Testing

- Unit tests for AuthZ and validation
- Contract tests against OpenAPI
- Load tests on list and search endpoints
- Periodic OWASP ZAP / API security scans

### Observability

- Structured JSON logs with `request_id`, `client_id`, `route`, `status`, `latency_ms`
- Metrics: RPS, p99 latency, error rate, 429 rate per tier
- Distributed tracing across gateway → service → DB

### Secret and key management

- Rotate API keys on schedule and after incidents
- Support two active keys during rotation window
- Never commit `.env` or credentials to git

## Other guides in this repo

| Guide | Topics |
|-------|--------|
| [api-rate-limiting](../../api-rate-limiting/README.md) | Algorithms, deployment layers, common mistakes |
| [event-sourcing-and-cqrs](../../event-sourcing-and-cqrs/README.md) | Event store, CQRS(Command Query Responsibility Segregation), outbox, audit APIs |
| [database-connection-and-security](../../database-connection-and-security/README.md) | DB credentials, IAM(Identity and Access Management), vault patterns |
| [deployment-strategies](../../deployment-strategies/README.md) | Safe rollout of API changes |
| [high-throughput-systems](../../high-throughput-systems/README.md) | End-to-end throughput: measure, cache, async, streaming, backpressure |
| [tree-and-index-structures](../../tree-and-index-structures/README.md) | B+ vs LSM(Log-Structured Merge) storage engines for write-heavy workloads |

## Quick decision summary

| Question | Default answer |
|----------|----------------|
| REST(Representational State Transfer) or GraphQL? | REST for public APIs unless strong client flexibility need |
| URL or header versioning? | URL `/v1` for simplicity |
| Gateway required? | Yes for public; optional for internal mTLS(Mutual Transport Layer Security) mesh |
| User auth? | OAuth 2.0 + PKCE → JWT |
| Partner auth? | Scoped API key + optional mTLS |
| Rate limit algorithm? | Sliding window counter + token bucket for bursts |
| Spec tooling? | OpenAPI + Swagger UI + Spectral + contract CI |
| Where is AuthZ? | Always in application code |

## Pros of using this checklist

- Catches gaps before launch (especially BOLA and rate limits)
- Repeatable across teams and services
- Audit-friendly evidence of security review

## Cons

- Checkbox fatigue if treated as bureaucracy only
- Must be updated when architecture or threats evolve
- Does not replace pen testing or production monitoring

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Checklist as one-time paperwork | Re-run before each major release |
| BOLA unchecked on new `{id}` routes | Ownership test in CI or review gate |
| Idempotency only on payments | All side-effect POSTs that clients retry |
| Webhook `callback_url` without SSRF guard | Allowlist or validate outbound URLs |
| Sticky sessions on "stateless" API | Externalize session to Redis/DB |