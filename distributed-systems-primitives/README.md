# Distributed Systems Primitives Guide

The mechanisms underneath the architectural choices — CAP(Consistency, Availability, Partition Tolerance)/PACELC, consistent hashing, unique ID generation, consensus and leader election, service discovery, probabilistic data structures, and clocks/ordering. This guide goes deep on **how**; [architecture-decisions](../architecture-decisions/README.md) covers **when a product should care**.

Related: [architecture-decisions](../architecture-decisions/README.md) · [nosql-and-key-value-stores](../nosql-and-key-value-stores/README.md) · [apache-kafka](../apache-kafka/README.md) · [tree-and-index-structures](../tree-and-index-structures/README.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [CAP and PACELC](includes/01-cap-and-pacelc.md) |
| 2 | [Consistent hashing](includes/02-consistent-hashing.md) |
| 3 | [Unique IDs](includes/03-unique-ids.md) |
| 4 | [Consensus and leader election](includes/04-consensus-and-leader-election.md) |
| 5 | [Service discovery](includes/05-service-discovery.md) |
| 6 | [Probabilistic structures](includes/06-probabilistic-structures.md) |
| 7 | [Clocks and ordering](includes/07-clocks-and-ordering.md) |
| 8 | [Decision guide](includes/08-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Deepening a CAP/PACELC decision from architecture-decisions** | [architecture-decisions §6](../architecture-decisions/includes/06-tradeoff-frameworks.md) → §1 CAP and PACELC |
| **Sharding a cache, CDN(Content Delivery Network), or database** | §2 Consistent hashing → [nosql-and-key-value-stores §2](../nosql-and-key-value-stores/includes/02-access-pattern-modeling.md) |
| **Choosing a primary key / ID strategy** | §3 Unique IDs → §8 Decision guide |
| **Evaluating etcd/ZooKeeper/KRaft or "should we build our own lock service"** | §4 Consensus and leader election |
| **Debugging service-to-service discovery failures** | §5 Service discovery → [resilience-patterns](../resilience-patterns/README.md) |
| **Sizing a Bloom filter, HyperLogLog counter, or rate approximator** | §6 Probabilistic structures |
| **Reasoning about event ordering across services** | §7 Clocks and ordering → [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) |

---

## See also

| Guide | Topics |
|-------|--------|
| [architecture-decisions](../architecture-decisions/README.md) | Product-level CAP/PACELC framing ([§6](../architecture-decisions/includes/06-tradeoff-frameworks.md)), when to decide vs defer |
| [nosql-and-key-value-stores](../nosql-and-key-value-stores/README.md) | DynamoDB/Cassandra/MongoDB — where these primitives show up in a real store |
| [apache-kafka](../apache-kafka/README.md) | KRaft(Kafka Raft) metadata consensus, ISR(In-Sync Replicas) quorum, partition assignment |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | LSM(Log-Structured Merge) trees — where Bloom filters do their heaviest lifting |
| [postgresql-performance](../postgresql-performance/README.md) | Single-primary consistency baseline these primitives generalize beyond |
| [high-throughput-systems](../high-throughput-systems/README.md) | Multi-region read routing, caching layers that lean on consistent hashing |
| [resilience-patterns](../resilience-patterns/README.md) | Distributed locks, health checks, and failure handling around these primitives |
| [api-rate-limiting](../api-rate-limiting/README.md) | Approximate counting (Count-Min/HyperLogLog) applied to distributed rate limits |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Causal ordering of events across aggregates and services |