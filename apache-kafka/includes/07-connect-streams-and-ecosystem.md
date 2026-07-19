# Connect, Streams, and Ecosystem

Beyond custom producers/consumers, **Kafka Connect** integrates external systems and **Kafka Streams** builds stream processing with embedded state.

> **Related:** LSM(Log-Structured Merge) state stores → [tree §4 LSM](../../tree-and-index-structures/includes/04-lsm-trees.md) · CDC(Change Data Capture) → [§8 integration](08-integration-patterns.md) · Mirror/DR(Disaster Recovery) → [§10 DR](10-operations-dr-security-and-observability.md#disaster-recovery) · Active-active → [§10](10-operations-dr-security-and-observability.md#active-active-multi-region)

---

## At a glance

| Tool | Best for |
|------|----------|
| **Custom consumer/producer** | Full control; simple one-off |
| **Kafka Connect** | JDBC, S3, Debezium CDC, Elasticsearch sinks |
| **Kafka Streams** | Stateful transforms, joins, aggregations in JVM |
| **MirrorMaker 2** | Cross-cluster replication |
| **ksqlDB / Flink** | SQL(Structured Query Language) or large-scale stream processing (external) |

**Rule of thumb:** Use **Connect** for **integration** (DB ↔ Kafka). Use **Streams** when processing stays in Kafka and needs **local state**. Use **Flink** when Connect/Streams cannot scale the logic.

---

## Kafka Connect

```mermaid
flowchart LR
    PG[(PostgreSQL)] -->|Debezium_source| Connect[Connect_worker]
    Connect --> Kafka[(Kafka_topics)]
    Kafka --> Connect2[Connect_worker]
    Connect2 -->|ES_sink| OS[(OpenSearch)]
```

| Concept | Role |
|---------|------|
| **Connector** | Source or sink plugin (Debezium, S3, JDBC) |
| **Task** | Parallel units of connector work |
| **Worker** | JVM running connectors |
| **SMT(Simple Message Transform)** | Lightweight map/filter in pipeline |
| **Dead letter queue** | Route failed records to DLQ(Dead Letter Queue) topic — config detail in [§8 DLQ](08-integration-patterns.md#retry-and-dlq-deep-dive) |

### When Connect

| Scenario | Connect? |
|----------|----------|
| Debezium CDC | Yes — standard path — [HTS §15](../../high-throughput-systems/includes/15-cdc-and-search-indexing.md) |
| Copy topic → S3 archive | Yes — S3 sink |
| Complex business rules | Custom consumer often clearer |
| Non-JVM team owns logic | Custom consumer in their language |

Run Connect workers **separate from brokers** in production — [§9 setup](09-cluster-setup-and-requirements.md).

---

## Kafka Streams

| Feature | Detail |
|---------|------|
| **Topology** | DAG(Directed Acyclic Graph) of processors |
| **State stores** | RocksDB-backed changelog topics (LSM) — [tree §4](../../tree-and-index-structures/includes/04-lsm-trees.md) |
| **Exactly-once** | `processing.guarantee=exactly_once_v2` (broker + Streams cooperation) |
| **Repartition topics** | Created automatically for key changes |

### When Streams

| Fit | Misfit |
|-----|--------|
| Join two Kafka topics | Heavy ML(Machine Learning) inference |
| Session windows, aggregations | Non-JVM stack requirement |
| Compact changelog for KTable | Cross-region active-active (prefer Flink + careful design) |

---

## MirrorMaker 2 (MM2)

| Capability | Use |
|------------|-----|
| Topic replication | DR standby cluster — [§10 DR](10-operations-dr-security-and-observability.md) |
| Offset sync | Consumer failover planning |
| Bidirectional | Multi-region active-active (complex — see below) |

MM2 is **async** — RPO(Recovery Point Objective) > 0; not a synchronous dual-write.

### Topologies

| Topology | Flow | Prefer when |
|----------|------|-------------|
| **Active → passive (DR)** | Primary produces; MM2 mirrors to standby; consumers failover on disaster | Most enterprises; clearest ownership |
| **Active → active (multi-region)** | Each region produces locally; MM2 (or equivalent) replicates topics both ways | Latency needs local produce; team can own conflict rules |
| **Fan-in hub** | Edge clusters → central analytics cluster | Analytics isolation; do not reverse-fan domain writes |

```mermaid
flowchart LR
    subgraph DR[Active_passive]
        P1[Primary] -->|MM2| S1[Standby]
    end
    subgraph AA[Active_active]
        R1[Region_A] <-->|MM2| R2[Region_B]
    end
```

### Active-active hard requirements

| Requirement | Why |
|-------------|-----|
| **Idempotent consumers** | Same event may arrive from local produce and remote mirror |
| **Stable event ids** | Dedup key = producer `event_id` / outbox id — not broker offset |
| **Conflict policy** | Last-write-wins by timestamp, region preference, or domain merge — document per topic |
| **No dual-write of the same command** | Route a given aggregate to one home region when possible |
| **Schema Registry parity** | Subjects and compatibility modes match across regions — [§6](06-serialization-and-schema-evolution.md) |
| **Lag SLO(Service Level Objective) per link** | Treat inter-region lag as user-visible staleness, not just ops metric |

**Rule of thumb:** Default to **active-passive DR**. Choose active-active only when product latency requires local produce **and** you have a written conflict/idempotency design — full ops playbook → [§10 active-active](10-operations-dr-security-and-observability.md#active-active-multi-region).

---

## Ecosystem map

| Component | Purpose |
|-----------|---------|
| **Schema Registry** | Schemas for Connect converters — [§6](06-serialization-and-schema-evolution.md) |
| **REST(Representational State Transfer) Proxy** | HTTP(Hypertext Transfer Protocol) produce/consume (limited; not primary API(Application Programming Interface)) |
| **Cruise Control** | Rebalance partitions, broker maintenance |
| **Redpanda / WarpStream** | Kafka-compatible APIs; different ops model |

---

## Connect vs custom consumer

| Factor | Connect | Custom |
|--------|---------|--------|
| Time to integrate DB/ES | Fast | Slower |
| Operational surface | Connector version + worker | Your code only |
| Transform logic | SMTs (limited) | Full language |
| Team skills | Config-heavy | Code-heavy |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Connect on broker JVM | Dedicated worker cluster |
| Streams state without changelog backup | Monitor changelog topics; RF=3 |
| MM2 as active-active without idempotency | Design consumers idempotent; accept lag — [§10](10-operations-dr-security-and-observability.md#active-active-multi-region) |
| Bidirectional MM2 without home-region routing | Pin aggregates to a region; document conflict policy |
| SMT doing heavy enrichment | Stream processing app or consumer |

---

## Pros and cons

### Kafka Connect

**Pros:** Reusable connectors; ops model for integrations; Debezium maturity.

**Cons:** Worker scaling and connector bugs; SMTs tempt logic in config.