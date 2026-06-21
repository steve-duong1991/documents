# PostgreSQL Performance Guide

A practical reference for PostgreSQL performance — measurement, indexing, query design, maintenance, configuration, scaling, and when to use each strategy.

---

## Table of contents

| # | Topic | Include file |
|---|-------|--------------|
| — | [Overview](#overview) | [includes/00-overview.md](includes/00-overview.md) |
| 1 | [Measurement — start here](#1-measurement--start-here) | [includes/01-measurement.md](includes/01-measurement.md) |
| 2 | [Indexing](#2-indexing) | [includes/02-indexing.md](includes/02-indexing.md) |
| 3 | [Query design](#3-query-design) | [includes/03-query-design.md](includes/03-query-design.md) |
| 4 | [Schema design](#4-schema-design) | [includes/04-schema-design.md](includes/04-schema-design.md) |
| 5 | [Statistics and the planner](#5-statistics-and-the-planner) | [includes/05-statistics-and-planner.md](includes/05-statistics-and-planner.md) |
| 6 | [Vacuum, bloat, and maintenance](#6-vacuum-bloat-and-maintenance) | [includes/06-vacuum-and-bloat.md](includes/06-vacuum-and-bloat.md) |
| 7 | [Connection management](#7-connection-management) | [includes/07-connection-management.md](includes/07-connection-management.md) |
| 8 | [Memory and configuration](#8-memory-and-configuration) | [includes/08-memory-and-config.md](includes/08-memory-and-config.md) |
| 9 | [Views, functions, and scale-out terminology](#9-views-functions-and-scale-out-terminology) | [includes/09-views-functions-and-scale-out-terminology.md](includes/09-views-functions-and-scale-out-terminology.md) |
| 10 | [Partitioning](#10-partitioning) | [includes/10-partitioning.md](includes/10-partitioning.md) |
| 11 | [Read scaling and caching](#11-read-scaling-and-caching) | [includes/11-read-scaling-and-caching.md](includes/11-read-scaling-and-caching.md) |
| 12 | [Bulk operations and concurrency](#12-bulk-operations-and-concurrency) | [includes/12-bulk-operations-and-concurrency.md](includes/12-bulk-operations-and-concurrency.md) |
| 13 | [Decision guide and common mistakes](#13-decision-guide-and-common-mistakes) | [includes/13-decision-guide-and-common-mistakes.md](includes/13-decision-guide-and-common-mistakes.md) |
| 14 | [Strong consistency — promises and costs](#14-strong-consistency--promises-and-costs) | [includes/14-consistency-promises-and-costs.md](includes/14-consistency-promises-and-costs.md) |
| 15 | [Schema migration checklist](#15-schema-migration-checklist) | [includes/15-schema-migration-checklist.md](includes/15-schema-migration-checklist.md) |

> **Tip:** Open [GUIDE.md](GUIDE.md) for the full combined document in one file.

---

## Overview

Measure first, then fix queries and indexes, tune the server, and scale out only when needed.

See full details → [includes/00-overview.md](includes/00-overview.md)

---

## 1. Measurement — Start Here

Use `EXPLAIN ANALYZE` and `pg_stat_statements` before any other optimization.

See full details → [includes/01-measurement.md](includes/01-measurement.md)

---

## 2. Indexing

B-tree, partial, composite, covering, GIN, and BRIN — when each type pays off.

See full details → [includes/02-indexing.md](includes/02-indexing.md)

---

## 3. Query Design

N+1 elimination, pagination, JOINs, and query common mistakes.

See full details → [includes/03-query-design.md](includes/03-query-design.md)

---

## 4. Schema Design

Types, JSONB, foreign keys, soft deletes, and when to denormalize.

See full details → [includes/04-schema-design.md](includes/04-schema-design.md)

---

## 5. Statistics and the Planner

Keep statistics fresh; use extended statistics when estimates are wrong.

See full details → [includes/05-statistics-and-planner.md](includes/05-statistics-and-planner.md)

---

## 6. Vacuum, Bloat, and Maintenance

Autovacuum tuning, dead tuples, long transactions, and bloat recovery.

See full details → [includes/06-vacuum-and-bloat.md](includes/06-vacuum-and-bloat.md)

---

## 7. Connection Management

PgBouncer, pooling modes, and why not to raise `max_connections` blindly.

See full details → [includes/07-connection-management.md](includes/07-connection-management.md)

---

## 8. Memory and Configuration

`shared_buffers`, `work_mem`, SSD planner costs, and WAL tuning.

See full details → [includes/08-memory-and-config.md](includes/08-memory-and-config.md)

---

## 9. Views, Functions, and Scale-Out Terminology

Read this before partitioning, replicas, or sharding — defines views, materialized views, partitioning vs replication vs sharding vs clustering.

See full details → [includes/09-views-functions-and-scale-out-terminology.md](includes/09-views-functions-and-scale-out-terminology.md)

---

## 10. Partitioning

Range, list, and hash partitioning — retention, pruning, and when it helps.

See full details → [includes/10-partitioning.md](includes/10-partitioning.md)

---

## 11. Read Scaling and Caching

Read replicas, materialized views, Redis, and consistency trade-offs.

See full details → [includes/11-read-scaling-and-caching.md](includes/11-read-scaling-and-caching.md)

---

## 12. Bulk Operations and Concurrency

COPY, upserts, locking, job queues, and write-heavy patterns.

See full details → [includes/12-bulk-operations-and-concurrency.md](includes/12-bulk-operations-and-concurrency.md)

---

## 13. Decision Guide and Common Mistakes

Scenario recommendations, priority checklist, and common mistakes to avoid.

See full details → [includes/13-decision-guide-and-common-mistakes.md](includes/13-decision-guide-and-common-mistakes.md)

---

## 14. Strong Consistency — Promises and Costs

Definitions (ACID, linearizability, read-your-writes), CAP trade-offs, PostgreSQL replication modes, and when to require strong reads vs accept staleness.

See full details → [includes/14-consistency-promises-and-costs.md](includes/14-consistency-promises-and-costs.md)

---

## 15. Schema migration checklist

Expand/contract phases, `CREATE INDEX CONCURRENTLY`, batched backfills, and lock-risk table for rolling deploys.

See full details → [includes/15-schema-migration-checklist.md](includes/15-schema-migration-checklist.md)

---

## See also

| Guide | Topics |
|-------|--------|
| [high-throughput-systems](../high-throughput-systems/README.md) | System-wide throughput order: cache, scale, async, backpressure |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | B+ vs LSM storage engines for write-heavy workloads |
| [database-connection-and-security](../database-connection-and-security/README.md) | Production credentials, IAM, PgBouncer |
| [api-rate-limiting](../api-rate-limiting/README.md) | Limiter algorithms and deployment layers |
| [deployment-strategies](../deployment-strategies/README.md) | Safe rollout during schema and API changes |
| [deployment-strategies §12](../deployment-strategies/includes/12-schema-migrations-and-deploy.md) | Expand/contract with rolling deploy |
