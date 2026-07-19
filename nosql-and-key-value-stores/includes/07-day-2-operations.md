# Day-2 Operations

Day-2 for DynamoDB-style, Cassandra, and MongoDB is **backups, TTL(Time To Live), repair/compaction, and capacity** — the work that keeps NoSQL fast after launch. Modeling → [§2](02-access-pattern-modeling.md); this section is **cross-cutting ops**.

> **Scope:** Operational checklist across Dynamo-style, Cassandra wide-column, and MongoDB document stores. Engine-specific modeling → [§3](03-dynamo-style-multi-tenant.md) · [§4](04-cassandra-wide-column.md) · [§5](05-mongodb-document.md). PostgreSQL day-2 → [postgresql-performance](../../postgresql-performance/README.md).
>
> **Related:** RPO(Recovery Point Objective)/RTO(Recovery Time Objective) → [sre §12 DR](../../sre-and-incidents/includes/12-disaster-recovery.md) · [DB §12](../../database-connection-and-security/includes/12-credential-rotation-and-dr.md) · Capacity → [architecture §13](../../architecture-decisions/includes/13-capacity-estimation.md) · FinOps(Cloud Financial Operations) → [HTS §1](../../high-throughput-systems/includes/01-measurement-and-slo.md)

---

## At a glance

| Concern | Dynamo-style | Cassandra | MongoDB |
|---------|--------------|-----------|---------|
| **Backup** | PITR(Point-in-Time Recovery) + on-demand | Snapshots + incremental | Continuous backup / snapshots |
| **TTL** | Native per-item | TTL column + compaction | TTL index |
| **Repair** | N/A (managed) | `nodetool repair` schedule | Resync replica set |
| **Capacity** | RCU/WCU or on-demand | Nodes + RF(Replication Factor) | Tier + shard keys |
| **Restore drill** | Table restore to sandbox | Restore + repair verify | Point-in-time restore |

**Rule of thumb:** NoSQL day-2 fails in **silent ways** — throttling, compaction lag, repair debt — not loud query errors. Monitor saturation, not just errors.

---

## Backup and restore

```mermaid
flowchart LR
    Prod[Production cluster] --> Snap[Automated snapshots / PITR]
    Snap --> Store[Cross-region / vault]
    Store --> Drill[Quarterly restore drill]
    Drill --> App[App smoke on restored data]
```

| Practice | All engines |
|----------|-------------|
| **RPO/RTO named** | Match product tier — [sre §12](../../sre-and-incidents/includes/12-disaster-recovery.md) |
| **Cross-region copy** | Region loss survivability |
| **Restore ≠ prod** | Scrub PII(Personally Identifiable Information); separate account |
| **Test application** | Restore proves backup, not just snapshot existence |

Dynamo-style: enable PITR before you need it. Cassandra: snapshot before major schema change. MongoDB: verify oplog window covers restore target.

---

## TTL and lifecycle

| Use TTL for | Avoid TTL for |
|-------------|---------------|
| Sessions, idempotency keys | Financial records (use archive tier) |
| Ephemeral cache rows | Legal hold data |
| IoT(Internet of Things) telemetry roll-off | Anything needing audit WORM(Write Once Read Many) |

TTL deletion is **eventually consistent** — do not rely on instant purge for compliance. Pair with ILM(Index Lifecycle Management) export to cold storage if needed.

---

## Repair, compaction, and health

| Engine | Scheduled work |
|--------|----------------|
| **Cassandra** | Repair (rf coverage), cleanup snapshots, compaction strategy review — [§4](04-cassandra-wide-column.md) |
| **MongoDB** | Compact (rare), index rebuild plan, replica lag alerts |
| **Dynamo-style** | Watch hot partitions; GSI(Global Secondary Index) backpressure |

Alerts: **disk > 70%**, **repair overdue**, **compaction pending**, **consumer lag** on change streams.

---

## Capacity and noisy neighbor

| Signal | Action |
|--------|--------|
| Throttled reads/writes | Raise caps or fix hot key — [§3](03-dynamo-style-multi-tenant.md) |
| Node CPU / heap high | Scale out or fix queries |
| p99 latency up, errors flat | Saturation — [HTS §1](../../high-throughput-systems/includes/01-measurement-and-slo.md) |
| One tenant dominates | Partition key redesign or dedicated table |

Review on-demand vs provisioned monthly — FinOps tie-in.

---

## Common mistakes

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| Backups never restored | False confidence | Quarterly drill |
| TTL on compliance data | Audit gap | Archive path |
| Skip Cassandra repair | Data inconsistency | Automated repair window |
| Ignore GSI costs | Bill shock | Project only needed attributes |
| No cross-region backup | Region loss = data loss | Copy snapshots |

---

## Pros and cons

| Ops model | Pros | Cons |
|-----------|------|------|
| **Fully managed** | Less repair burden | Less tuning control |
| **Self-hosted Cassandra** | Cost at scale | Repair/compaction ops mandatory |
| **On-demand capacity** | Simple | Expensive at steady high load |
