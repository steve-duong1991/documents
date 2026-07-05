# Apache Kafka Guide

A practical deep dive into Apache Kafka — commit log internals, topics and replication, producers and consumers, schema formats, cluster setup, operations, integration patterns, and testing.

Related: [high-throughput-systems](../high-throughput-systems/README.md) (when to stream, system throughput) · [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) (outbox, sagas, domain schema evolution)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Commit log and internals](includes/01-commit-log-and-internals.md) |
| 2 | [Topics, partitions, and replication](includes/02-topics-partitions-and-replication.md) |
| 3 | [Producers and delivery guarantees](includes/03-producers-and-delivery-guarantees.md) |
| 4 | [Consumers and consumer groups](includes/04-consumers-and-consumer-groups.md) |
| 5 | [Retention, compaction, and storage](includes/05-retention-compaction-and-storage.md) |
| 6 | [Serialization and schema evolution](includes/06-serialization-and-schema-evolution.md) |
| 7 | [Connect, Streams, and ecosystem](includes/07-connect-streams-and-ecosystem.md) |
| 8 | [Integration patterns](includes/08-integration-patterns.md) |
| 9 | [Cluster setup and requirements](includes/09-cluster-setup-and-requirements.md) |
| 10 | [Operations, DR, security, and observability](includes/10-operations-dr-security-and-observability.md) |
| 11 | [Decision guide and common mistakes](includes/11-decision-guide-and-common-mistakes.md) |
| 12 | [Testing and verification](includes/12-testing-and-verification.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Guide | Topics |
|-------|--------|
| [high-throughput-systems](../high-throughput-systems/README.md) | Streaming pipelines, message brokers, CDC(Change Data Capture) overview, observability |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Transactional outbox, sagas, domain event schema evolution |
| [api-design-and-protection](../api-design-and-protection/README.md) | Async patterns, idempotency, multi-tenant APIs, contract testing |
| [postgresql-performance](../postgresql-performance/README.md) | Row-level security, read models fed by Kafka consumers |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | LSM(Log-Structured Merge) trees in Kafka Streams state stores |
| [database-connection-and-security](../database-connection-and-security/README.md) | DR vocabulary (RPO/RTO(Recovery Time Objective)), credentials for Connect |
| [deployment-strategies](../deployment-strategies/README.md) | Safe deploy when consumers lag or schemas change |
