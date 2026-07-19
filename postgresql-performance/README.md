# PostgreSQL Performance Guide

A practical reference for PostgreSQL performance — measurement, indexing, query design, maintenance, configuration, scaling, multi-tenant isolation (RLS and silos), and when to use each strategy.

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Measurement — start here](includes/01-measurement.md) |
| 2 | [Indexing](includes/02-indexing.md) |
| 3 | [Query design](includes/03-query-design.md) |
| 4 | [Schema design](includes/04-schema-design.md) |
| 5 | [Statistics and the planner](includes/05-statistics-and-planner.md) |
| 6 | [Vacuum, bloat, and maintenance](includes/06-vacuum-and-bloat.md) |
| 7 | [Connection management](includes/07-connection-management.md) |
| 8 | [Memory and configuration](includes/08-memory-and-config.md) |
| 9 | [Views, functions, and scale-out terminology](includes/09-views-functions-and-scale-out-terminology.md) |
| 10 | [Partitioning](includes/10-partitioning.md) |
| 11 | [Read scaling, caching & materialized views](includes/11-read-scaling-and-caching.md) |
| 12 | [Bulk operations and concurrency](includes/12-bulk-operations-and-concurrency.md) |
| 13 | [Decision guide and common mistakes](includes/13-decision-guide-and-common-mistakes.md) |
| 14 | [Strong consistency — promises and costs](includes/14-consistency-promises-and-costs.md) |
| 15 | [Schema migration checklist](includes/15-schema-migration-checklist.md) |
| 16 | [Backup, restore, and PITR](includes/16-backup-restore-and-pitr.md) |
| 17 | [Row-level security for multi-tenant data](includes/17-row-level-security-multi-tenant.md) |
| 18 | [Schema and database per tenant](includes/18-schema-and-database-per-tenant.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Guide | Topics |
|-------|--------|
| [high-throughput-systems](../high-throughput-systems/README.md) | System-wide throughput order: cache, scale, async, backpressure |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | B+ vs LSM(Log-Structured Merge) storage engines for write-heavy workloads |
| [database-connection-and-security](../database-connection-and-security/README.md) | Production credentials, IAM(Identity and Access Management), PgBouncer |
| [api-rate-limiting](../api-rate-limiting/README.md) | Limiter algorithms and deployment layers |
| [deployment-strategies](../deployment-strategies/README.md) | Safe rollout during schema and API(Application Programming Interface) changes |
| [deployment-strategies §12](../deployment-strategies/includes/12-schema-migrations-and-deploy.md) | Expand/contract with rolling deploy |
| [apache-kafka](../apache-kafka/README.md) | Read models and search indexes fed by Kafka consumers; Connect credentials |
| [data-platforms](../data-platforms/README.md) | Warehouse/search/Redis roles; analytics off primary; org-scale migration coordination |
| [finops-and-cost](../finops-and-cost/README.md) | Right-size DB before horizontal sprawl; retention and backup cost |