# Overview — Resilience Patterns

Resilience is the ability to **stay useful when dependencies fail or overload** — not the absence of failure.

**Rule of thumb:** Every outbound call needs a **deadline**, a **retry policy** (or explicit none), and a **isolation boundary**. Missing any one invites cascading outage.

> **Related:**
> - Backpressure and limits → [HTS §9](../../high-throughput-systems/includes/09-backpressure-and-limits.md)
> - Rate limits and 429 → [api-rate-limiting](../../api-rate-limiting/README.md)
> - HTTP(Hypertext Transfer Protocol) contracts → [api-design-and-protection](../../api-design-and-protection/README.md)
> - Failure domains → [architecture-decisions §11](../../architecture-decisions/includes/11-failure-domains.md)
> - Policy placement → [11-policy-placement.md](11-policy-placement.md)
> - Worked example → [12-worked-example-checkout.md](12-worked-example-checkout.md)
> - Capstone → [16-decision-guide.md](16-decision-guide.md)

---

## At a glance

| Pattern | Job |
|---------|-----|
| **Timeouts** | Bound wait time; free resources |
| **Retries + jitter** | Survive transient faults without stampedes |
| **Circuit breakers** | Stop calling a sick dependency |
| **Bulkheads** | Limit blast radius of one dependency |
| **Load shedding / degrade** | Protect core journeys under overload |
| **Idempotency** | Make retries safe |
| **Delivery semantics** | Define async truth (at-least-once + dedup) |
| **Policy placement** | One owner per control across app/gateway/mesh |
| **Observability** | See retry ratio, breakers, pool wait, shed |
| **Graceful drain** | Survive deploys without partial writes |
| **Chaos** | Prove the above before customers do |

---

## Defense in depth

```mermaid
flowchart TD
    In[Incoming load] --> Shed[Shed / rate limit]
    Shed --> App[App concurrency cap]
    App --> BH[Bulkhead per dependency]
    BH --> TO[Timeout]
    TO --> RT[Retry with jitter]
    RT --> CB[Circuit breaker]
    CB --> Dep[Dependency]
```

Pair edge limits ([api-rate-limiting](../../api-rate-limiting/README.md)) with in-process patterns here. Decide **which layer owns** retries and timeouts — [§11](11-policy-placement.md).

---

## Document map

| # | Topic | File |
|---|-------|------|
| 1 | Timeouts | [01-timeouts.md](01-timeouts.md) |
| 2 | Retries, backoff, jitter | [02-retries-backoff-jitter.md](02-retries-backoff-jitter.md) |
| 3 | Circuit breakers | [03-circuit-breakers.md](03-circuit-breakers.md) |
| 4 | Bulkheads | [04-bulkheads.md](04-bulkheads.md) |
| 5 | Load shedding and degradation | [05-load-shedding-and-degradation.md](05-load-shedding-and-degradation.md) |
| 6 | Idempotency systemwide | [06-idempotency-systemwide.md](06-idempotency-systemwide.md) |
| 7 | Distributed locks | [07-distributed-locks.md](07-distributed-locks.md) |
| 8 | Delivery semantics | [08-delivery-semantics.md](08-delivery-semantics.md) |
| 9 | Cascading failure | [09-cascading-failure.md](09-cascading-failure.md) |
| 10 | Chaos and failure injection | [10-chaos-and-failure-injection.md](10-chaos-and-failure-injection.md) |
| 11 | Policy placement | [11-policy-placement.md](11-policy-placement.md) |
| 12 | Worked example — checkout | [12-worked-example-checkout.md](12-worked-example-checkout.md) |
| 13 | Observability for resilience | [13-observability-for-resilience.md](13-observability-for-resilience.md) |
| 14 | Graceful shutdown and drain | [14-graceful-shutdown-and-drain.md](14-graceful-shutdown-and-drain.md) |
| 15 | Implementation map | [15-implementation-map.md](15-implementation-map.md) |
| 16 | Decision guide | [16-decision-guide.md](16-decision-guide.md) |

---

## Default stack (sync dependency)

1. Set connect + request timeouts shorter than caller budget — [§1](01-timeouts.md)
2. Retry only idempotent / explicitly safe calls; **one** retry owner — [§2](02-retries-backoff-jitter.md) + [§6](06-idempotency-systemwide.md) + [§11](11-policy-placement.md)
3. Trip a breaker on sustained errors — [§3](03-circuit-breakers.md)
4. Cap concurrency per dependency — [§4](04-bulkheads.md)
5. Degrade T1 features before failing T0 (with a fallback contract) — [§5](05-load-shedding-and-degradation.md)
6. Instrument and drain cleanly — [§13](13-observability-for-resilience.md), [§14](14-graceful-shutdown-and-drain.md)

End-to-end example → [§12 checkout](12-worked-example-checkout.md).

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Infinite waits on HTTP clients | Explicit timeouts everywhere |
| Eager retries without jitter | Exponential backoff + jitter |
| Retries on non-idempotent POSTs | Idempotency keys or no retry |
| Retries at mesh **and** app | Single owner — [§11](11-policy-placement.md) |
| One shared thread pool for all deps | Bulkheads |
| Patterns without dashboards | [§13](13-observability-for-resilience.md) |
| No game days | Chaos drills — [§10](10-chaos-and-failure-injection.md) |