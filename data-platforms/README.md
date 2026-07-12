# Data Platforms Guide

When one OLTP(Online Transaction Processing) database is no longer enough — warehouses, lakes, search, Redis roles, caching coherence, ownership/lineage, migration coordination, and analytics that do not starve production.

Related: [postgresql-performance](../postgresql-performance/README.md) · [high-throughput-systems](../high-throughput-systems/README.md) (CDC(Change Data Capture)/search) · [apache-kafka](../apache-kafka/README.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [OLTP vs OLAP](includes/01-oltp-vs-olap.md) |
| 2 | [Search systems](includes/02-search-systems.md) |
| 3 | [Redis and in-memory](includes/03-redis-and-in-memory.md) |
| 4 | [Caching end to end](includes/04-caching-end-to-end.md) |
| 5 | [Data ownership, lineage, retention](includes/05-data-ownership-lineage-retention.md) |
| 6 | [Migration coordination](includes/06-migration-coordination.md) |
| 7 | [Analytics without harming OLTP](includes/07-analytics-without-harming-oltp.md) |
| 8 | [Decision guide](includes/08-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Guide | Topics |
|-------|--------|
| [postgresql-performance](../postgresql-performance/README.md) | Indexes, replicas, expand/contract migrations ([§15](../postgresql-performance/includes/15-schema-migration-checklist.md)) |
| [high-throughput-systems](../high-throughput-systems/README.md) | Caching layers ([§4](../high-throughput-systems/includes/04-caching-layers.md)), CDC(Change Data Capture) and search ([§15](../high-throughput-systems/includes/15-cdc-and-search-indexing.md)), batch/ETL(Extract, Transform, Load) |
| [apache-kafka](../apache-kafka/README.md) | Event bus, Connect, CDC pipelines, retention |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Outbox, projections, read models |
| [api-rate-limiting](../api-rate-limiting/README.md) | Redis-backed limits and distributed quotas |
| [database-connection-and-security](../database-connection-and-security/README.md) | Credentials, IAM(Identity and Access Management), DR vocabulary |
| [finops-and-cost](../finops-and-cost/README.md) | Storage retention cost, managed-service spend |
| [deployment-strategies](../deployment-strategies/README.md) | Schema + deploy order, blue/green index swaps |
| [nosql-and-key-value-stores](../nosql-and-key-value-stores/README.md) | DynamoDB/Cassandra/Mongo when OLTP is not PostgreSQL |
| [specialized-data-systems](../specialized-data-systems/README.md) | Time-series, graph, vector/RAG(Retrieval-Augmented Generation) beyond warehouse/search |