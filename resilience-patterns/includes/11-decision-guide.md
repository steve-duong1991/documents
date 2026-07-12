# Decision Guide — Resilience

When to apply which pattern — and common mistakes that cause cascades.

> **Related:** Overview stack → [00-overview.md](00-overview.md) · Architecture failure domains → [architecture §11](../../architecture-decisions/includes/11-failure-domains.md) · Overload → [HTS §9](../../high-throughput-systems/includes/09-backpressure-and-limits.md) · Rate limits → [api-rate-limiting §10](../../api-rate-limiting/includes/10-decision-guide.md)

---

## Master decision flow

```mermaid
flowchart TD
    Start[Resilience gap] --> TO{Timeouts set?}
    TO -->|No| T[Add deadlines §1]
    TO -->|Yes| Id{Retries needed?}
    Id -->|Yes| Idem{Idempotent?}
    Idem -->|No| I[Add idempotency §6 or don't retry]
    Idem -->|Yes| R[Backoff + jitter §2]
    Id -->|No| BH[Bulkhead §4]
    I --> BH
    R --> BH
    BH --> CB{Sustained dep failure?}
    CB -->|Yes| Br[Circuit breaker §3]
    CB -->|No| Ov{Overload?}
    Br --> Ov
    Ov -->|Yes| Sh[Shed / degrade §5]
    Ov -->|No| As{Async path?}
    Sh --> As
    As -->|Yes| Del[Delivery + dedup §8]
    As -->|No| Ch[Chaos validate §10]
    Del --> Ch
```

---

## Scenario recommendations

| Scenario | Recommended approach |
|----------|----------------------|
| New outbound HTTP(Hypertext Transfer Protocol) client | Timeouts + bulkhead; retries only if idempotent |
| Payments dependency flaky | Tight timeout, breaker, **no** blind retry; idempotent keys |
| Browse page with recs + cart | Bulkhead recs; degrade recs; protect cart T0 |
| Queue floods after outage | Jittered consumer backoff; DLQ(Dead Letter Queue); replay rate limit |
| Partner webhook duplicates | Dedup by event ID — [§6](06-idempotency-systemwide.md) |
| “Exactly once” stakeholder ask | At-least-once + idempotency; Kafka EOS(Exactly-Once Semantics) only in scope — [§8](08-delivery-semantics.md) |
| Singleton cron overlap | Lock/lease **or** `SKIP LOCKED` jobs — [§7](07-distributed-locks.md) |
| Site-wide brownout | Shed + breakers + reduce retries — [§9](09-cascading-failure.md) |
| Unknown if patterns work | Game day — [§10](10-chaos-and-failure-injection.md) |
| Edge abuse | Rate limit first — [api-rate-limiting](../../api-rate-limiting/README.md) |

---

## Priority checklist

- [ ] Every dependency has connect + request timeouts
- [ ] End-to-end deadline ≥ sum of child budgets
- [ ] Retry policy documented (including “none”)
- [ ] Unsafe writes covered by idempotency
- [ ] Per-dependency concurrency caps
- [ ] Breakers on T0/T1 sync deps
- [ ] Degrade/shed plan agreed with product
- [ ] Consumers: dedup + DLQ + alert
- [ ] Dashboards for pool wait, breaker state, retry rate
- [ ] At least one chaos/game-day per critical journey

---

## Common mistakes

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| Infinite client timeouts | Thread/pool meltdown | Explicit deadlines |
| Retry POST without keys | Double charges | Idempotency or no retry |
| No jitter | Thundering herd | Equal/full jitter |
| Shared executor | Cascade across features | Bulkheads |
| Breaker without timeout | Still hangs | Always both |
| Unbounded queues | Delayed meltdown | Cap + shed |
| Distributed lock over HTTP call | Deadlocks / expiry hell | Redesign |
| Trusting broker EOS alone | Duplicate side effects | Dedup effects |
| Never injecting failure | False confidence | Chaos drills |

---

## Quick decision summary

| Question | Default answer |
|----------|----------------|
| First control to add? | Timeouts |
| Retry writes? | Only if idempotent |
| Breaker when? | Sustained errors/latency with min volume |
| Overload tool? | Shed/degrade + rate limits |
| Async duplicates? | Expect them; dedup |
| Need a lock? | Prefer ownership/idempotency first |
| How to verify? | Fault tests + game days |

---

## See also

| Guide | Topics |
|-------|--------|
| [architecture-decisions](../../architecture-decisions/README.md) | Hop budget, failure domains |
| [high-throughput-systems](../../high-throughput-systems/README.md) | Saturation and backpressure |
| [api-design-and-protection](../../api-design-and-protection/README.md) | HTTP idempotency |
| [apache-kafka](../../apache-kafka/README.md) | Delivery guarantees |
| [sre-and-incidents](../../sre-and-incidents/README.md) | Incident response |
| [api-rate-limiting](../../api-rate-limiting/README.md) | Admission at the edge |