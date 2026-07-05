# Response Strategies

> **Scope:** **Behavior lens** — hard reject vs throttle vs queue, retry-storm prevention. Canonical `429` headers and tier contract → [api-design §5 Response headers](../../api-design-and-protection/includes/05-rate-limit-tiers.md#response-headers).
>
> **Related:** Standard headers → [api-design §5 Response headers](../../api-design-and-protection/includes/05-rate-limit-tiers.md#response-headers) · Async escape hatch → [api-design §5 Async escape hatch](../../api-design-and-protection/includes/05-rate-limit-tiers.md#async-escape-hatch) · Retry storms → [HTS §9 Backpressure](../../high-throughput-systems/includes/09-backpressure-and-limits.md)

How you respond when a limit is hit is as important as the algorithm itself.

---

## At a glance

| Strategy | HTTP(Hypertext Transfer Protocol) | Client experience | Default? |
|----------|------|-------------------|----------|
| **Hard reject** | `429` + `Retry-After` | Must backoff | Yes — public APIs |
| **Throttle** | `200` after delay | Slower but succeeds | Partner/scrape deterrence |
| **Queue** | `202` or delayed `200` | Async wait | Job ingestion only |
| **Graduated** | Warn headers → throttle → `429` | Escalating pressure | Enterprise SaaS |

---

## Comparison

| Strategy | Behavior | Pros | Cons | When to use |
|----------|----------|------|------|-------------|
| **Hard reject** | Immediate `429 Too Many Requests` | Simple, protects fast | Bad UX for legitimate retries | Default for abuse prevention |
| **Throttle / delay** | Slow down responses | Softer on clients | Ties up connections | Partner APIs, scraping deterrence |
| **Queue** | Buffer then process | No immediate loss | Latency, memory risk | Async job ingestion |
| **Graduated** | Warn → throttle → block | Better UX for good users | More logic to maintain | Enterprise SaaS |
| **Priority tiers** | Premium bypasses limits | Revenue-aligned | Complexity, fairness debates | Paid vs free tiers |

## Standard response headers

Canonical `429` example and header names for product tiers → [api-design §5 Response headers](../../api-design-and-protection/includes/05-rate-limit-tiers.md#response-headers).

| Header | Purpose |
|--------|---------|
| `Retry-After` | Seconds (or HTTP(Hypertext Transfer Protocol)-date) until client should retry |
| `X-RateLimit-Limit` | Max requests allowed in the window |
| `X-RateLimit-Remaining` | Requests left in current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

Optional warning before hard block (graduated):

```http
X-RateLimit-Warning: 90% of quota consumed
```

## Retry storm prevention

Clients that retry aggressively on `429` amplify load. Mitigate with:

1. Document exponential backoff in your API(Application Programming Interface) docs
2. Return accurate `Retry-After` values
3. Use jitter in client SDKs
4. Consider a separate, stricter limit for rapid retries from the same client — key: `ratelimit:key:{id}:retry:{window}` ([§6](06-scope-identity.md))

## JSON error body

Return structured errors so clients distinguish tier limits from abuse blocks:

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Monthly quota exhausted",
    "retry_after": 3600
  }
}
```

Use distinct `code` values: `rate_limit_exceeded` vs `abuse_blocked` vs `concurrent_limit`.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `429` without `Retry-After` | Always set seconds or HTTP-date |
| Same error body for tier vs abuse blocks | Distinct `code` in JSON for client handling |
| Throttling without closing idle connections | Time out slow clients; see [§5 Leaky bucket](05-leaky-bucket.md) for queue caps |
| Retry storm from your own SDK | Exponential backoff + respect `Retry-After`; cap internal retries |