# High Throughput Systems Guide

A practical reference for building systems that handle high request, event, and write rates — measurement, optimization order, caching, async, streaming, batch, backpressure, and operations.

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Measurement and SLOs](includes/01-measurement-and-slo.md) |
| 2 | [Entry and edge](includes/02-entry-and-edge.md) |
| 3 | [Stateless app tier](includes/03-stateless-app-tier.md) |
| 4 | [Caching layers](includes/04-caching-layers.md) |
| 5 | [Database throughput](includes/05-database-throughput.md) |
| 6 | [Async, queues, and workers](includes/06-async-queues-workers.md) |
| 7 | [Streaming pipelines](includes/07-streaming-pipelines.md) |
| 8 | [Batch and ETL](includes/08-batch-and-etl.md) |
| 9 | [Backpressure and limits](includes/09-backpressure-and-limits.md) |
| 10 | [Scale and deploy](includes/10-scale-and-deploy.md) |
| 11 | [Observability](includes/11-observability.md) |
| 12 | [Decision guide and common mistakes](includes/12-decision-guide-and-common-mistakes.md) |
| 13 | [Multi-region read routing](includes/13-multi-region-read-routing.md) |
| 14 | [Message brokers and queues](includes/14-message-brokers-and-queues.md) |
| 15 | [CDC and search indexing](includes/15-cdc-and-search-indexing.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | Gateway, stateless architecture, async API(Application Programming Interface) patterns |
| [api-rate-limiting](../api-rate-limiting/README.md) | Limiter algorithms, deployment layers |
| [postgresql-performance](../postgresql-performance/README.md) | DB measurement, indexing, replicas, bulk writes |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | B+ vs LSM(Log-Structured Merge) storage engines |
| [deployment-strategies](../deployment-strategies/README.md) | Rolling, canary, blue/green deploys |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Event log, outbox, projections |
| [database-connection-and-security](../database-connection-and-security/README.md) | DB credentials, IAM(Identity and Access Management), PgBouncer |