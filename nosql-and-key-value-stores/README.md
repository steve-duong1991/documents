# NoSQL & Key-Value Stores Guide

Choosing and modeling non-relational stores — DynamoDB, Cassandra, and MongoDB — against a PostgreSQL default: query-shape-first decisions, access-pattern modeling, multi-tenant isolation, and the anti-patterns that cause the most production pain.

Related: [postgresql-performance](../postgresql-performance/README.md) · [data-platforms](../data-platforms/README.md) · [architecture-decisions](../architecture-decisions/README.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [When to choose NoSQL vs PostgreSQL](includes/01-when-to-choose.md) |
| 2 | [Access-pattern modeling](includes/02-access-pattern-modeling.md) |
| 3 | [Dynamo-style vs SQL for multi-tenant SaaS](includes/03-dynamo-style-multi-tenant.md) |
| 4 | [Cassandra wide-column](includes/04-cassandra-wide-column.md) |
| 5 | [MongoDB document model](includes/05-mongodb-document.md) |
| 6 | [Decision guide](includes/06-decision-guide.md) |
| 7 | [Day-2 operations](includes/07-day-2-operations.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Deciding SQL(Structured Query Language) vs NoSQL for a new service** | Overview → §1 Decision matrix → §6 Decision guide |
| **Designing a DynamoDB table** | §2 Access-pattern modeling → §3 Multi-tenant (if SaaS(Software as a Service)) |
| **Evaluating Cassandra for write-heavy telemetry** | §1 Decision matrix → §4 Cassandra |
| **Comparing MongoDB to PostgreSQL JSONB** | §1 Decision matrix → §5 MongoDB |
| **Building multi-tenant SaaS on a key-value store** | §3 Multi-tenant → [PG §17 RLS](../postgresql-performance/includes/17-row-level-security-multi-tenant.md) |
| **Auditing an existing NoSQL table for hot partitions** | §2 Access-pattern modeling → §6 Decision guide (anti-patterns) |

---

## See also

| Guide | Topics |
|-------|--------|
| [postgresql-performance](../postgresql-performance/README.md) | The relational default this guide compares against — indexing, RLS(Row-Level Security), consistency costs |
| [data-platforms](../data-platforms/README.md) | Where a key-value store fits alongside warehouse, search, and cache in a wider data platform |
| [architecture-decisions](../architecture-decisions/README.md) | Data ownership and multi-tenant system models — the product-level framing behind §3 |
| [distributed-systems-primitives](../distributed-systems-primitives/README.md) | Consistent hashing, quorum reads/writes, and unique IDs that underpin DynamoDB/Cassandra internals |
| [high-throughput-systems](../high-throughput-systems/README.md) | CDC(Change Data Capture)/search indexing off a NoSQL source; database throughput order |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | LSM(Log-Structured Merge) tree internals behind Cassandra and RocksDB-based stores |
| [finops-and-cost](../finops-and-cost/README.md) | TCO(Total Cost of Ownership) comparisons between managed NoSQL and self-hosted PostgreSQL |
| [resilience-patterns](../resilience-patterns/README.md) | Idempotency and retry patterns for eventually consistent writes |