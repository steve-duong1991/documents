# Operations, DR, Security, and Observability

Running Kafka in production means monitoring **lag and replication**, securing clients, planning **disaster recovery**, and tying alerts to runbooks.

> **Related:** DR vocabulary → [database-connection §12 DR](../../database-connection-and-security/includes/12-credential-rotation-and-dr.md) · Observability patterns → [HTS §11](../../high-throughput-systems/includes/11-observability.md) · Runbook template → [RUNBOOK-TEMPLATE.md](../../RUNBOOK-TEMPLATE.md) · Setup baseline → [§9](09-cluster-setup-and-requirements.md) · **Failure catalog and runbooks** → [§13](13-failure-modes-troubleshooting-and-recovery.md) · Audit/PII on streams → [ESC §6](../../enterprise-security-compliance/includes/06-audit-logging-and-retention.md) · [ESC §7](../../enterprise-security-compliance/includes/07-pii-and-data-classification.md) · MM2 topologies → [§7 MirrorMaker](07-connect-streams-and-ecosystem.md#mirrormaker-2-mm2)

---

## At a glance

| Signal | Severity |
|--------|----------|
| **Consumer lag growing** | Capacity or slow handler |
| **Under-replicated partitions** | Broker failure or network |
| **Offline partitions** | No leader in ISR(In-Sync Replicas) |
| **ISR shrink** | Follower lag or broker down |
| **Disk usage > 80%** | Retention or sizing issue |

**Rule of thumb:** Alert on **lag derivative** (rate of growth) and **under-replicated partitions** — not lag alone on low-traffic topics.

---

## Key metrics

| Metric | Source | Action |
|--------|--------|--------|
| `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec` | JMX / Prometheus | Capacity |
| Consumer lag per partition | Burrow, Kafka exporter, MSK metrics | Scale consumers |
| `UnderReplicatedPartitions` | Broker JMX | Check broker / network |
| `OfflinePartitionsCount` | Cluster | Incident — leader election |
| Request latency produce/fetch | Broker | Hot disk or network |
| Connect task failures | Connect REST(Representational State Transfer) | Connector config / DLQ(Dead Letter Queue) |

---

## Consumer lag operations

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Lag flat, high | Steady overload | Add consumers to partition limit; optimize handler |
| Lag spike after deploy | Regression or poison pill | Roll back; inspect DLQ — [§13 poison pill](13-failure-modes-troubleshooting-and-recovery.md#runbook-poison-pill) |
| One partition hot lag | Skewed key | Rekey strategy — [§2](02-topics-partitions-and-replication.md) |
| All groups lag | Broker or disk | Broker ops — disk, network |

Runbook row → [RUNBOOK-TEMPLATE.md](../../RUNBOOK-TEMPLATE.md) consumer lag section. Detailed runbooks → [§13](13-failure-modes-troubleshooting-and-recovery.md).

---

## Broker tuning (day-2)

| Area | Guidance |
|------|----------|
| **Heap** | 4–6 GB typical; avoid consuming RAM needed for page cache |
| **Disk** | Monitor log dirs; expand or reduce retention |
| **Network** | 10 GbE+ for heavy replication cross-AZ |
| **Thread pools** | Tune under sustained high fetch/produce |
| **Cruise Control** | Automated partition rebalance on broker add/remove |

Details build on [§9 setup](09-cluster-setup-and-requirements.md) — do not duplicate checklist here.

---

## Security

| Layer | Practice |
|-------|----------|
| **Wire encryption** | TLS(Transport Layer Security) between clients and brokers; inter-broker TLS |
| **Authentication** | SASL SCRAM, OAuth (OIDC), or mTLS(Mutual Transport Layer Security) |
| **Authorization** | ACLs (open source) or RBAC (Confluent); least privilege per principal |
| **Quotas** | Byte rate per client id / user — multi-tenant fairness — [#client-quotas-and-noisy-neighbor](#client-quotas-and-noisy-neighbor) |
| **Admin access** | Separate admin principals; audit topic delete |
| **Broker / ACL audit** | Log authorization denials and admin API(Application Programming Interface) calls — feed security audit pipeline ([ESC §6](../../enterprise-security-compliance/includes/06-audit-logging-and-retention.md)) |

| Principal | Typical ACL(Access Control List) |
|-----------|-------------|
| Service producer | `WRITE` on specific topics |
| Service consumer | `READ` + `GROUP` on specific group |
| Connect | `READ`/`WRITE` on internal + target topics |
| Human admin | Restricted; break-glass only |

Classify topic payloads (PII vs internal) in the event catalog — [§9 catalog](09-cluster-setup-and-requirements.md#event-catalog-and-ownership-slos) · [ESC §7](../../enterprise-security-compliance/includes/07-pii-and-data-classification.md).

---

## Client quotas and noisy-neighbor

On a **shared enterprise cluster**, one hot producer or catch-up consumer can starve everyone else. Kafka **client quotas** cap produce/fetch rates per `user` and/or `client.id`.

| Quota type | Typical config intent | Protects against |
|------------|----------------------|------------------|
| **Producer byte rate** | Cap inbound MB/s per principal | Runaway producer, bad batching, load test against prod |
| **Consumer byte rate** | Cap fetch MB/s per principal | Catch-up storm after deploy / new group `earliest` |
| **Request rate** | Cap request/s | Metadata / Produce flood |
| **Controller mutation** | Cap topic create/alter (where available) | Self-service abuse |

### Default platform policy

| Practice | Detail |
|----------|--------|
| **Defaults on** | New principals inherit org default quotas — not unlimited |
| **Raise by ticket / PR** | Documented capacity request; tie to catalog owner |
| **Separate client.id** | One service → one `client.id`; never share across teams |
| **Monitor throttling** | Alert when a principal is throttled sustained (> N minutes) |
| **Multi-tenant apps** | Quotas bound the **service**, not each end-customer — still enforce tenant in app ([§2](02-topics-partitions-and-replication.md#multi-tenant-isolation)) |

```mermaid
flowchart TD
    Produce[Producer_burst] --> Q{Within_quota?}
    Q -->|Yes| Broker[Accepted]
    Q -->|No| Throttle[Broker_throttles]
    Throttle --> Backpressure[Client_backs_off]
```

**Rule of thumb:** Quotas are **fairness and blast-radius control**, not a substitute for capacity planning or partition sizing. Pair with lag SLOs from the [event catalog](09-cluster-setup-and-requirements.md#event-catalog-and-ownership-slos).

### Pros and cons

**Pros:** Stops one team from melting a shared cluster; predictable multi-tenant behavior.

**Cons:** Mis-tuned quotas look like "Kafka is broken"; raises need clear capacity process.

---

## Disaster recovery

Link RPO(Recovery Point Objective)/RTO(Recovery Time Objective) definitions → [database-connection §12](../../database-connection-and-security/includes/12-credential-rotation-and-dr.md).

| Scenario | Pattern | Stream RPO note |
|----------|---------|-----------------|
| **Single broker loss** | RF=3, auto leader election | RPO ≈ 0 if `acks=all` and ISR healthy |
| **AZ / region loss** | MirrorMaker 2 to standby cluster | RPO = replication lag (seconds–minutes) |
| **Accidental topic delete** | Restrict DELETE ACLs; mirror cluster backup | Replay from mirror if within retention |
| **Consumer rebuild** | New group `earliest` or reset offsets | Bounded by topic retention |
| **Schema Registry loss** | Registry HA; backup subjects | Consumers cache schema id → schema |
| **Corrupt partition** | Restore from mirror; rebuild consumers | Coordinate offset reset |

```mermaid
flowchart LR
    Primary[Primary_cluster] -->|MM2| DR[DR_cluster]
    DR --> StandbyConsumers[Standby_consumer_groups]
```

**Stream RPO ≠ DB PITR(Point-in-Time Recovery):** Kafka retention and replication define how far back you can replay — not PostgreSQL WAL(Write-Ahead Log) recovery.

Failover checklist:

1. Confirm mirror lag acceptable
2. Point consumers to DR bootstrap servers (or DNS(Domain Name System) cutover)
3. Reset or sync consumer groups per runbook
4. Verify Schema Registry subject parity

---

## Active-active multi-region

Use when **local produce latency** matters in more than one region. Prefer **active-passive MM2 DR** (above) unless product requirements force otherwise — topologies → [§7 MM2](07-connect-streams-and-ecosystem.md#mirrormaker-2-mm2).

| Pattern | Behavior | Main risk |
|---------|----------|-----------|
| **Home-region routing** | Aggregate keyed to a home region; other regions read via mirror | Cross-region write latency for "away" aggregates |
| **Local write + async converge** | Both regions produce; consumers dedup by `event_id` | Conflicts; duplicate side effects if not idempotent |
| **Region-scoped topics** | `us.orders…` / `eu.orders…`; merge in analytics only | Harder global projections |

### Decision flow

```mermaid
flowchart TD
    Need[Multi_region_produce?] -->|No| AP[Active_passive_DR]
    Need -->|Yes| Conflict{Documented_conflict_and_idempotency?}
    Conflict -->|No| AP
    Conflict -->|Yes| Home{Can_pin_aggregate_home?}
    Home -->|Yes| HR[Home_region_routing]
    Home -->|No| AA[Active_active_with_dedup]
```

### Ops checklist (active-active)

| Check | Detail |
|-------|--------|
| **Idempotent sinks** | Inbox / unique `event_id` before side effects — [§8](08-integration-patterns.md) |
| **Inter-region lag SLO** | Page when mirror lag exceeds freshness budget from catalog |
| **Schema + ACL parity** | Same subjects, compatibility, and principals in every region |
| **Failover drill** | Kill region or pause MM2 link quarterly; verify no double charge / double email |
| **Avoid Streams stateful active-active** | Prefer Flink or single-region state — [§7 Streams](07-connect-streams-and-ecosystem.md#kafka-streams) |

**Rule of thumb:** If you cannot answer "what happens when the same order event appears twice, five minutes apart, from two regions?" — you are not ready for active-active.

---

## Observability integration

| Practice | Detail |
|----------|--------|
| **OpenTelemetry** | Propagate `traceparent` in headers — [§3 headers](03-producers-and-delivery-guarantees.md#message-headers) |
| **Structured logs** | topic, partition, offset, key hash, correlation_id |
| **Dashboards** | Lag by group; broker disk; produce/consume rate; **quota throttle** by principal |
| **SLO(Service Level Objective) example** | 99% of events consumed within 60s of publish — per topic from [catalog](09-cluster-setup-and-requirements.md#event-catalog-and-ownership-slos) |
| **Mirror lag** | Per MM2 link; treat as freshness for remote readers |

---

## Incident triage order

1. **Offline / under-replicated partitions** — cluster health
2. **Disk full** — retention or expansion
3. **Lag growth** — consumer capacity or downstream DB
4. **Auth failures** — cert expiry, ACL change
5. **Schema errors** — incompatible deploy — [§6](06-serialization-and-schema-evolution.md)

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Lag alert without rate | Derivative alert |
| TLS enabled, ACLs open | Principle of least privilege |
| No DR drill | Failover test to mirror cluster quarterly |
| Delete topic ACL for apps | Admin-only |
| Ignore Connect DLQ | Monitor connector dead letter topics — [§8 DLQ](08-integration-patterns.md#detection-and-alerting) |
| Unlimited client quotas on shared cluster | Defaults + raise-by-request — [#quotas](#client-quotas-and-noisy-neighbor) |
| Active-active without dedup | Event ids + idempotent consumers — [#active-active](#active-active-multi-region) |

---

## Pros and cons

### MirrorMaker DR cluster

**Pros:** Geographic redundancy; replay buffer.

**Cons:** Async lag; active-active complexity; cost of second cluster.

### Active-active multi-region

**Pros:** Local produce latency; regional isolation for some failures.

**Cons:** Duplicate delivery and conflict handling; harder drills; higher ops cost than active-passive.