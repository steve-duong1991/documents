# Resilience Patterns Guide

A practical reference for keeping systems useful under partial failure — timeouts, retries with backoff and jitter, circuit breakers, bulkheads, load shedding, idempotency as a system rule, locks, delivery semantics, cascading failure, chaos testing, policy placement, and operating the patterns in production.

Related: [High Throughput Systems](../high-throughput-systems/README.md) · [API Rate Limiting](../api-rate-limiting/README.md) · [API Design & Protection](../api-design-and-protection/README.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Timeouts](includes/01-timeouts.md) |
| 2 | [Retries, backoff, and jitter](includes/02-retries-backoff-jitter.md) |
| 3 | [Circuit breakers](includes/03-circuit-breakers.md) |
| 4 | [Bulkheads](includes/04-bulkheads.md) |
| 5 | [Load shedding and degradation](includes/05-load-shedding-and-degradation.md) |
| 6 | [Idempotency systemwide](includes/06-idempotency-systemwide.md) |
| 7 | [Distributed locks](includes/07-distributed-locks.md) |
| 8 | [Delivery semantics](includes/08-delivery-semantics.md) |
| 9 | [Cascading failure](includes/09-cascading-failure.md) |
| 10 | [Chaos and failure injection](includes/10-chaos-and-failure-injection.md) |
| 11 | [Policy placement (app / gateway / mesh)](includes/11-policy-placement.md) |
| 12 | [Worked example — checkout](includes/12-worked-example-checkout.md) |
| 13 | [Observability for resilience](includes/13-observability-for-resilience.md) |
| 14 | [Graceful shutdown and drain](includes/14-graceful-shutdown-and-drain.md) |
| 15 | [Implementation map](includes/15-implementation-map.md) |
| 16 | [Decision guide](includes/16-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Hardening a sync call path** | Overview → §1 Timeouts → §2 Retries → §3 Breakers → §4 Bulkheads → §11 Placement |
| **Surviving overload** | §5 Load shedding → [HTS §9](../high-throughput-systems/includes/09-backpressure-and-limits.md) → [api-rate-limiting](../api-rate-limiting/README.md) |
| **Async / messaging** | §6 Idempotency → §8 Delivery → [apache-kafka](../apache-kafka/README.md) |
| **Seeing the full stack** | §12 Checkout worked example → §16 Decision guide |
| **Choosing where policy lives** | §11 Policy placement → §15 Implementation map |
| **Operating patterns** | §13 Observability → §14 Graceful shutdown → [sre-and-incidents](../sre-and-incidents/README.md) |
| **Stopping cascade incidents** | §9 Cascading → §16 Decision guide → [architecture §11](../architecture-decisions/includes/11-failure-domains.md) |
| **Proving resilience** | §10 Chaos → §13 Observability → [sre-and-incidents](../sre-and-incidents/README.md) |

---

## See also

| Guide | Topics |
|-------|--------|
| [high-throughput-systems](../high-throughput-systems/README.md) | Backpressure, overload, observability, connection draining |
| [api-rate-limiting](../api-rate-limiting/README.md) | Limits, 429, retry-storm prevention at edge |
| [api-design-and-protection](../api-design-and-protection/README.md) | HTTP(Hypertext Transfer Protocol) idempotency, async, protection |
| [architecture-decisions](../architecture-decisions/README.md) | Failure domains, integration style, sync hop budget |
| [apache-kafka](../apache-kafka/README.md) | Producer/consumer delivery guarantees |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Outbox, saga idempotency |
| [deployment-strategies](../deployment-strategies/README.md) | Safe rollout while hardening |
| [postgresql-performance](../postgresql-performance/README.md) | Pool exhaustion under retry storms |
| [database-connection-and-security](../database-connection-and-security/README.md) | Connection limits as a bulkhead |
| [sre-and-incidents](../sre-and-incidents/README.md) | Incident response when patterns fail |
| [cicd-and-environments](../cicd-and-environments/README.md) | Health probes, game-day environments |
| [testing-strategy](../testing-strategy/README.md) | Fault-injection tests in CI(Continuous Integration) |
| [enterprise-security-compliance](../enterprise-security-compliance/README.md) | Fail-closed requirements |
| [finops-and-cost](../finops-and-cost/README.md) | Cost of retries and over-provisioning |
| [payments-and-fintech](../payments-and-fintech/README.md) | Money-specific double-charge classes on top of §6 |