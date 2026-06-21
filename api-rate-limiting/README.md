# API Rate Limiting Guide

A practical reference for rate limiters in API protection — how they work, pros and cons, when to use each, and production architecture patterns.

Related: [api-design-and-protection](../api-design-and-protection/README.md) (gateway, rate-limit tiers, async escape hatch) · [high-throughput-systems](../high-throughput-systems/README.md) (backpressure and overload protection)

---

## Table of contents

| # | Topic | Include file |
|---|-------|--------------|
| — | [Overview](#overview) | [includes/00-overview.md](includes/00-overview.md) |
| 1 | [Fixed Window Counter](#1-fixed-window-counter) | [includes/01-fixed-window.md](includes/01-fixed-window.md) |
| 2 | [Sliding Window Log](#2-sliding-window-log) | [includes/02-sliding-window-log.md](includes/02-sliding-window-log.md) |
| 3 | [Sliding Window Counter](#3-sliding-window-counter-hybrid) | [includes/03-sliding-window-counter.md](includes/03-sliding-window-counter.md) |
| 4 | [Token Bucket](#4-token-bucket) | [includes/04-token-bucket.md](includes/04-token-bucket.md) |
| 5 | [Leaky Bucket](#5-leaky-bucket) | [includes/05-leaky-bucket.md](includes/05-leaky-bucket.md) |
| 6 | [Scope & identity limiters](#6-scope--identity-based-limiters) | [includes/06-scope-identity.md](includes/06-scope-identity.md) |
| 7 | [Deployment layers](#7-deployment-layers) | [includes/07-deployment-layers.md](includes/07-deployment-layers.md) |
| 8 | [Specialized limiters](#8-specialized-limiters) | [includes/08-specialized-limiters.md](includes/08-specialized-limiters.md) |
| 9 | [Response strategies](#9-response-strategies) | [includes/09-response-strategies.md](includes/09-response-strategies.md) |
| 10 | [Decision guide](#10-decision-guide--choosing-a-limiter) | [includes/10-decision-guide.md](includes/10-decision-guide.md) |
| 11 | [Common mistakes & production architecture](#11-common-mistakes--production-architecture) | [includes/11-common-mistakes-and-architecture.md](includes/11-common-mistakes-and-architecture.md) |

> **Tip:** Open [GUIDE.md](GUIDE.md) for the full combined document in one file.

---

## Overview

Rate limiting protects availability, cost, and fairness. It is not authentication on its own — combine it with auth, WAF, and abuse detection.

See full details → [includes/00-overview.md](includes/00-overview.md)

---

## 1. Fixed Window Counter

Counts requests in fixed time buckets. Simple and fast, but suffers from boundary burst at window edges.

See full details → [includes/01-fixed-window.md](includes/01-fixed-window.md)

---

## 2. Sliding Window Log

Stores a timestamp per request for true sliding-window accuracy. Best for strict fairness on sensitive endpoints.

See full details → [includes/02-sliding-window-log.md](includes/02-sliding-window-log.md)

---

## 3. Sliding Window Counter (Hybrid)

Weighted overlap of previous and current windows. The default choice for most production APIs.

See full details → [includes/03-sliding-window-counter.md](includes/03-sliding-window-counter.md)

---

## 4. Token Bucket

Refills tokens at a steady rate; allows controlled bursts up to bucket capacity.

See full details → [includes/04-token-bucket.md](includes/04-token-bucket.md)

---

## 5. Leaky Bucket

Queues requests and drains to the backend at a fixed rate. Protects slow downstream systems.

See full details → [includes/05-leaky-bucket.md](includes/05-leaky-bucket.md)

---

## 6. Scope & Identity-Based Limiters

Global, per-IP, per API key, per user, per endpoint — layer from cheapest to most specific.

See full details → [includes/06-scope-identity.md](includes/06-scope-identity.md)

---

## 7. Deployment Layers

CDN/edge, API gateway, reverse proxy, app middleware — where to enforce limits in the stack.

See full details → [includes/07-deployment-layers.md](includes/07-deployment-layers.md)

---

## 8. Specialized Limiters

Concurrent limits, quotas, cost-based weighting, adaptive limits, and bandwidth caps.

See full details → [includes/08-specialized-limiters.md](includes/08-specialized-limiters.md)

---

## 9. Response Strategies

Hard reject, throttle, queue, graduated tiers — and the headers clients need (`429`, `Retry-After`).

See full details → [includes/09-response-strategies.md](includes/09-response-strategies.md)

---

## 10. Decision Guide — Choosing a Limiter

Algorithm decision flow, scenario recommendations, and common stack combinations.

See full details → [includes/10-decision-guide.md](includes/10-decision-guide.md)

---

## 11. Common Mistakes & Production Architecture

Common mistakes, fail-open vs fail-closed, observability, and a minimal production architecture diagram.

See full details → [includes/11-common-mistakes-and-architecture.md](includes/11-common-mistakes-and-architecture.md)

---

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | Gateway enforcement, rate-limit tiers, scope identity |
| [high-throughput-systems](../high-throughput-systems/README.md) | Backpressure, circuit breakers, system-wide overload order |
| [deployment-strategies](../deployment-strategies/README.md) | Edge vs app-layer limit rollout during deploys |
| [postgresql-performance](../postgresql-performance/README.md) | Connection storms and pool saturation |
| [database-connection-and-security](../database-connection-and-security/README.md) | Edge identity vs DB credentials |
