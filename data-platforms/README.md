# Data Platforms Guide

When one OLTP(Online Transaction Processing) database is no longer enough — warehouses, lakes, search, Redis roles, caching coherence, ownership/lineage, migration coordination, and analytics that do not starve production.

Related: [postgresql-performance](../postgresql-performance/README.md) · [high-throughput-systems](../high-throughput-systems/README.md) (CDC(Change Data Capture)/search) · [apache-kafka](../apache-kafka/README.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [OLTP vs OLAP](includes/01-oltp-vs-olap.md) |
| 1A | [Columnar OLAP operations](includes/01A-columnar-olap-operations.md) |
| 1B | [Lakehouse table formats and ops](includes/01B-lakehouse-table-formats-and-ops.md) |
| 2 | [Search systems](includes/02-search-systems.md) |
| 2A | [Search cluster operations](includes/02A-search-cluster-operations.md) |
| 3 | [Redis and in-memory](includes/03-redis-and-in-memory.md) |
| 3A | [Redis operations](includes/03A-redis-operations.md) |
| 4 | [Caching end to end](includes/04-caching-end-to-end.md) |
| 5 | [Data ownership, lineage, retention](includes/05-data-ownership-lineage-retention.md) |
| 5A | [Data contracts and registries](includes/05A-data-contracts-and-registries.md) |
| 5B | [Data quality and pipeline testing](includes/05B-data-quality-and-pipeline-testing.md) |
| 6 | [Migration coordination](includes/06-migration-coordination.md) |
| 7 | [Analytics without harming OLTP](includes/07-analytics-without-harming-oltp.md) |
| 8 | [Decision guide](includes/08-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Adding analytics off OLTP** | [§1 OLTP vs OLAP](includes/01-oltp-vs-olap.md) → [§1A Columnar OLAP](includes/01A-columnar-olap-operations.md) → [§1B Lakehouse](includes/01B-lakehouse-table-formats-and-ops.md) → [§7 Analytics without harming OLTP](includes/07-analytics-without-harming-oltp.md) |
| **Search and discovery** | [§2 Search systems](includes/02-search-systems.md) → [§2A Search cluster ops](includes/02A-search-cluster-operations.md) → [high-throughput §15 CDC/search](../high-throughput-systems/includes/15-cdc-and-search-indexing.md) |
| **Data contracts and quality** | [§5A Data contracts](includes/05A-data-contracts-and-registries.md) → [§5B Data quality](includes/05B-data-quality-and-pipeline-testing.md) → [§5 Ownership/lineage](includes/05-data-ownership-lineage-retention.md) |
| **Platform migration** | [§6 Migration coordination](includes/06-migration-coordination.md) → [PG §15](../postgresql-performance/includes/15-schema-migration-checklist.md) → [§8 Decision guide](includes/08-decision-guide.md) |

## See also

| Guide | Topics |
|-------|--------|
| [postgresql-performance](../postgresql-performance/README.md) | Indexes, replicas, expand/contract migrations ([§15](../postgresql-performance/includes/15-schema-migration-checklist.md)) |
| [high-throughput-systems](../high-throughput-systems/README.md) | Caching layers ([§4](../high-throughput-systems/includes/04-caching-layers.md)), CDC(Change Data Capture) and search ([§15](../high-throughput-systems/includes/15-cdc-and-search-indexing.md)), batch/ETL(Extract, Transform, Load) |
| [apache-kafka](../apache-kafka/README.md) | Event bus, Connect, CDC pipelines, retention, [event catalog / freshness SLOs](../apache-kafka/includes/09-cluster-setup-and-requirements.md#event-catalog-and-ownership-slos) |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Outbox, projections, read models |
| [api-rate-limiting](../api-rate-limiting/README.md) | Redis-backed limits and distributed quotas |
| [database-connection-and-security](../database-connection-and-security/README.md) | Credentials, IAM(Identity and Access Management), DR(Disaster Recovery) vocabulary |
| [finops-and-cost](../finops-and-cost/README.md) | Storage retention cost, managed-service spend |
| [deployment-strategies](../deployment-strategies/README.md) | Schema + deploy order, blue/green index swaps |
| [nosql-and-key-value-stores](../nosql-and-key-value-stores/README.md) | DynamoDB/Cassandra/Mongo when OLTP is not PostgreSQL |
| [specialized-data-systems](../specialized-data-systems/README.md) | Time-series, graph, vector/RAG(Retrieval-Augmented Generation) beyond warehouse/search |