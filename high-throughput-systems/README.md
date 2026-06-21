# High Throughput Systems Guide

A practical reference for building systems that handle high request, event, and write rates — measurement, optimization order, caching, async, streaming, batch, backpressure, and operations.

---

## Table of contents

| # | Topic | Include file |
|---|-------|--------------|
| — | [Overview](#overview) | [includes/00-overview.md](includes/00-overview.md) |
| 1 | [Measurement and SLOs](#1-measurement-and-slos) | [includes/01-measurement-and-slo.md](includes/01-measurement-and-slo.md) |
| 2 | [Entry and edge](#2-entry-and-edge) | [includes/02-entry-and-edge.md](includes/02-entry-and-edge.md) |
| 3 | [Stateless app tier](#3-stateless-app-tier) | [includes/03-stateless-app-tier.md](includes/03-stateless-app-tier.md) |
| 4 | [Caching layers](#4-caching-layers) | [includes/04-caching-layers.md](includes/04-caching-layers.md) |
| 5 | [Database throughput](#5-database-throughput) | [includes/05-database-throughput.md](includes/05-database-throughput.md) |
| 6 | [Async, queues, and workers](#6-async-queues-and-workers) | [includes/06-async-queues-workers.md](includes/06-async-queues-workers.md) |
| 7 | [Streaming pipelines](#7-streaming-pipelines) | [includes/07-streaming-pipelines.md](includes/07-streaming-pipelines.md) |
| 8 | [Batch and ETL](#8-batch-and-etl) | [includes/08-batch-and-etl.md](includes/08-batch-and-etl.md) |
| 9 | [Backpressure and limits](#9-backpressure-and-limits) | [includes/09-backpressure-and-limits.md](includes/09-backpressure-and-limits.md) |
| 10 | [Scale and deploy](#10-scale-and-deploy) | [includes/10-scale-and-deploy.md](includes/10-scale-and-deploy.md) |
| 11 | [Observability](#11-observability) | [includes/11-observability.md](includes/11-observability.md) |
| 12 | [Decision guide and common mistakes](#12-decision-guide-and-common-mistakes) | [includes/12-decision-guide-and-common-mistakes.md](includes/12-decision-guide-and-common-mistakes.md) |
| 14 | [Multi-region read routing](#14-multi-region-read-routing) | [includes/14-multi-region-read-routing.md](includes/14-multi-region-read-routing.md) |

> **Tip:** Open [GUIDE.md](GUIDE.md) for the full combined document in one file.

---

## Overview

Measure first, reduce work per request, optimize the database hot path, then cache, scale horizontally, async deferrable work, and protect under load.

See full details → [includes/00-overview.md](includes/00-overview.md)

---

## 1. Measurement and SLOs

Define throughput targets, load test realistic paths, and find the bottleneck layer.

See full details → [includes/01-measurement-and-slo.md](includes/01-measurement-and-slo.md)

---

## 2. Entry and Edge

CDN, WAF, API gateway, and load balancer — absorb traffic early and route efficiently.

See full details → [includes/02-entry-and-edge.md](includes/02-entry-and-edge.md)

---

## 3. Stateless App Tier

Horizontal scaling, bounded concurrency, connection pooling, and reducing per-request cost.

See full details → [includes/03-stateless-app-tier.md](includes/03-stateless-app-tier.md)

---

## 4. Caching Layers

Redis, CDN, read paths, hot keys, and consistency trade-offs.

See full details → [includes/04-caching-layers.md](includes/04-caching-layers.md)

---

## 5. Database Throughput

Priority order for PostgreSQL throughput — links to the full DB performance guide.

See full details → [includes/05-database-throughput.md](includes/05-database-throughput.md)

---

## 6. Async, Queues, and Workers

Decouple accept rate from process rate; scale workers on queue depth.

See full details → [includes/06-async-queues-workers.md](includes/06-async-queues-workers.md)

---

## 7. Streaming Pipelines

Event streams, partitions, consumer groups, and backpressure for high-volume data.

See full details → [includes/07-streaming-pipelines.md](includes/07-streaming-pipelines.md)

---

## 8. Batch and ETL

COPY, staging tables, chunked backfills, and idempotent bulk jobs.

See full details → [includes/08-batch-and-etl.md](includes/08-batch-and-etl.md)

---

## 9. Backpressure and Limits

Layered rate limits, semaphores, circuit breakers, and fail-open vs fail-closed.

See full details → [includes/09-backpressure-and-limits.md](includes/09-backpressure-and-limits.md)

---

## 10. Scale and Deploy

Autoscaling triggers, safe deploys, multi-region, and cold-start avoidance.

See full details → [includes/10-scale-and-deploy.md](includes/10-scale-and-deploy.md)

---

## 11. Observability

RPS, p99, saturation signals, tracing, and alerts that fire before users notice.

See full details → [includes/11-observability.md](includes/11-observability.md)

---

## 12. Decision Guide and Common Mistakes

Master decision flow, scenario table, priority checklist, and common mistakes.

See full details → [includes/12-decision-guide-and-common-mistakes.md](includes/12-decision-guide-and-common-mistakes.md)

---

## 14. Multi-region read routing

Active-passive DR, read-local/write-global, geo routing, and consistency trade-offs.

See full details → [includes/14-multi-region-read-routing.md](includes/14-multi-region-read-routing.md)

---

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | Gateway, stateless architecture, async API patterns |
| [api-rate-limiting](../api-rate-limiting/README.md) | Limiter algorithms, deployment layers |
| [postgresql-performance](../postgresql-performance/README.md) | DB measurement, indexing, replicas, bulk writes |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | B+ vs LSM storage engines |
| [deployment-strategies](../deployment-strategies/README.md) | Rolling, canary, blue/green deploys |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Event log, outbox, projections |
| [database-connection-and-security](../database-connection-and-security/README.md) | DB credentials, IAM, PgBouncer |
