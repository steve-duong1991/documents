# Apache Kafka Guide

A practical deep dive into Apache Kafka — commit log internals, topics and replication, producers and consumers, schema formats, cluster setup, operations, integration patterns, retry/DLQ(Dead Letter Queue), failure recovery, and testing. Platform angle: topic governance and event catalog SLOs, client quotas, tiered storage, and multi-region DR(Disaster Recovery) / active-active.

Related: [high-throughput-systems](../high-throughput-systems/README.md) (when to stream, system throughput) · [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) (outbox, sagas, domain schema evolution) · [enterprise-security-compliance](../enterprise-security-compliance/README.md) (audit/PII(Personally Identifiable Information) on the bus)

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
| 13 | [Failure modes, troubleshooting, and recovery](includes/13-failure-modes-troubleshooting-and-recovery.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **New to Kafka** | Overview → [§1 commit log](includes/01-commit-log-and-internals.md) → [§2 topics](includes/02-topics-partitions-and-replication.md) → [§3 producers](includes/03-producers-and-delivery-guarantees.md) → [§4 consumers](includes/04-consumers-and-consumer-groups.md) |
| **Platform / ops** | [§9 cluster setup](includes/09-cluster-setup-and-requirements.md) → [§10 ops/DR](includes/10-operations-dr-security-and-observability.md) → [§13 failure modes](includes/13-failure-modes-troubleshooting-and-recovery.md) → [§5 retention](includes/05-retention-compaction-and-storage.md) |
| **App integration** | [§8 integration](includes/08-integration-patterns.md) → [§6 schema](includes/06-serialization-and-schema-evolution.md) → [ES §5A outbox/inbox](../event-sourcing-and-cqrs/includes/05A-outbox-and-inbox.md) → [§12 testing](includes/12-testing-and-verification.md) |
| **Choosing vs queues** | [§11 decision guide](includes/11-decision-guide-and-common-mistakes.md) → [HTS §14 brokers](../high-throughput-systems/includes/14-message-brokers-and-queues.md) |

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
| [data-platforms](../data-platforms/README.md) | CDC/search pipelines; retention and ownership of derived stores |
| [finops-and-cost](../finops-and-cost/README.md) | Kafka retention/storage cost; managed vs self-hosted TCO(Total Cost of Ownership) |
| [enterprise-security-compliance](../enterprise-security-compliance/README.md) | Audit/PII on the bus; classification; compliance evidence tied to stream retention |