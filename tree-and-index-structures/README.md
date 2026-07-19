# Trees and Index Structures Guide

A practical reference for tree data structures and storage indexes — B-Trees, B+ Trees, in-memory balanced trees, specialized trees, LSM(Log-Structured Merge) trees, and when to use each.

Related: [postgresql-performance](../postgresql-performance/README.md) (PostgreSQL index types and tuning) · [high-throughput-systems](../high-throughput-systems/README.md) (LSM write path at scale)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [B-Trees and B+ Trees](includes/01-b-trees-and-b-plus.md) |
| 2 | [In-memory balanced trees](includes/02-in-memory-trees.md) |
| 3 | [Specialized trees](includes/03-specialized-trees.md) |
| 4 | [LSM Trees](includes/04-lsm-trees.md) |
| 5 | [Decision guides and cheat sheets](includes/05-decision-guides.md) |
| 6 | [Amplification, complexity, and related topics](includes/06-amplification-and-related-topics.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **PostgreSQL index theory** | Overview → [§1 B+](includes/01-b-trees-and-b-plus.md) → [PG §2 indexing](../postgresql-performance/includes/02-indexing.md) → [§5 decision](includes/05-decision-guides.md) |
| **Write-heavy / LSM** | [§4 LSM](includes/04-lsm-trees.md) → [§6 amplification](includes/06-amplification-and-related-topics.md) → [HTS DB throughput](../high-throughput-systems/README.md) → [nosql](../nosql-and-key-value-stores/README.md) |
| **In-memory / specialized** | [§2 in-memory](includes/02-in-memory-trees.md) → [§3 specialized](includes/03-specialized-trees.md) → [§5](includes/05-decision-guides.md) |

## See also

| Guide | Topics |
|-------|--------|
| [postgresql-performance](../postgresql-performance/README.md) | B-tree, GIN(Generalized Inverted Index), partial, and covering indexes; vacuum/planner when engine choice meets SQL(Structured Query Language) |
| [high-throughput-systems](../high-throughput-systems/README.md) | Database throughput layer; write amplification when LSM vs B+ matters |
| [api-design-and-protection](../api-design-and-protection/README.md) | API(Application Programming Interface) caching and read-path design |
| [nosql-and-key-value-stores](../nosql-and-key-value-stores/README.md) | Access patterns that prefer LSM / wide-column engines |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Event store and append-heavy write paths |
| [database-connection-and-security](../database-connection-and-security/README.md) | Connection security is independent of index choice |
| [api-rate-limiting](../api-rate-limiting/README.md) | Overload protection when storage read path saturates |
| [deployment-strategies](../deployment-strategies/README.md) | Deploy when changing index strategy at scale |
| [apache-kafka](../apache-kafka/README.md) | LSM in Kafka Streams state stores; log-segment storage |
| [VISUAL-INDEX](../VISUAL-INDEX.md) | Request / async spines that sit above storage engines |