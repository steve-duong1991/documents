# API Rate Limiting Guide

A practical reference for rate limiters in API protection — how they work, pros and cons, when to use each, and production architecture patterns.

Related: [api-design-and-protection](../api-design-and-protection/README.md) (gateway, rate-limit tiers, async escape hatch) · [high-throughput-systems](../high-throughput-systems/README.md) (backpressure and overload protection)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Fixed Window Counter](includes/01-fixed-window.md) |
| 2 | [Sliding Window Log](includes/02-sliding-window-log.md) |
| 3 | [Sliding Window Counter](includes/03-sliding-window-counter.md) |
| 4 | [Token Bucket](includes/04-token-bucket.md) |
| 5 | [Leaky Bucket](includes/05-leaky-bucket.md) |
| 6 | [Scope & identity limiters](includes/06-scope-identity.md) |
| 7 | [Deployment layers](includes/07-deployment-layers.md) |
| 8 | [Specialized limiters](includes/08-specialized-limiters.md) |
| 9 | [Response strategies](includes/09-response-strategies.md) |
| 10 | [Decision guide](includes/10-decision-guide.md) |
| 11 | [Common mistakes & production architecture](includes/11-common-mistakes-and-architecture.md) |
| 12 | [Distributed rate limiting](includes/12-distributed-rate-limiting.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Operating limits in production** | [§7 Deployment layers](includes/07-deployment-layers.md) → [§12 Distributed rate limiting](includes/12-distributed-rate-limiting.md) → [§6 Scope and identity](includes/06-scope-identity.md) → [§9 Response strategies](includes/09-response-strategies.md) → [§11 Common mistakes](includes/11-common-mistakes-and-architecture.md) |
| **Choosing an algorithm** | [§10 Decision guide](includes/10-decision-guide.md) → [§1 Fixed window](includes/01-fixed-window.md) → [§2 Sliding window log](includes/02-sliding-window-log.md) → [§3 Sliding window counter](includes/03-sliding-window-counter.md) → [§4 Token bucket](includes/04-token-bucket.md) → [§5 Leaky bucket](includes/05-leaky-bucket.md) |
| **B2B(Business-to-Business) / multi-tenant quotas** | [§6 Scope and identity](includes/06-scope-identity.md) → [api-design §5 tiers](../api-design-and-protection/includes/05-rate-limit-tiers.md) → [§8 Specialized limiters](includes/08-specialized-limiters.md) |
| **429 UX and client behavior** | [§9 Response strategies](includes/09-response-strategies.md) → [fullstack](../fullstack-bff-and-clients/README.md) → [resilience §2 retries](../resilience-patterns/includes/02-retries-backoff-jitter.md) |

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | Gateway enforcement, rate-limit tiers, scope identity |
| [high-throughput-systems](../high-throughput-systems/README.md) | Backpressure, circuit breakers, system-wide overload order |
| [deployment-strategies](../deployment-strategies/README.md) | Edge vs app-layer limit rollout during deploys |
| [postgresql-performance](../postgresql-performance/README.md) | Connection storms and pool saturation |
| [database-connection-and-security](../database-connection-and-security/README.md) | Edge identity vs DB credentials |
| [apache-kafka](../apache-kafka/README.md) | Consumer-side rate limits and overload when event ingress saturates |