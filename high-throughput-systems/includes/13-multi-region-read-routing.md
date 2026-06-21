# Multi-Region Read Routing

Multi-region adds throughput and availability — at the cost of **consistency complexity**. Design the write path first; reads follow.

> **Related:** Consistency → [postgresql-performance/includes/14-consistency-promises-and-costs.md](../../postgresql-performance/includes/14-consistency-promises-and-costs.md) · Stateless API(Application Programming Interface) → [api-design-and-protection/includes/11-stateless-architecture.md](../../api-design-and-protection/includes/11-stateless-architecture.md#consistency-and-read-routing) · DR → [database-connection-and-security/includes/12-credential-rotation-and-dr.md](../../database-connection-and-security/includes/12-credential-rotation-and-dr.md)

---

## At a glance

| Pattern | Writes | Reads | Complexity |
|---------|--------|-------|------------|
| **Single region** | One primary | Local replica/cache | Low |
| **Active-passive DR** | One active region | Failover region standby | Medium |
| **Active-active reads** | One write region (or Cockroach/Spanner) | Local replica per region | Medium–high |
| **True multi-master** | Multiple write regions | Local | Very high |

**Rule of thumb:** Default to **one write region + read replicas per region**. Add multi-master only with a clear conflict model.

---

## Active-passive (DR)

```mermaid
flowchart LR
    Users[Global users] --> R1[Region A primary]
    R1 --> RepB[Region B replica async]
    RepB -.->|Failover| Promote[Promote B on disaster]
```

| Metric | Typical target |
|--------|----------------|
| **RPO(Recovery Point Objective)** | Replication lag window (seconds–minutes) |
| **RTO(Recovery Time Objective)** | DNS + promote + app config (minutes–hours) |

Run DR drill quarterly → [database-connection-and-security §12](../../database-connection-and-security/includes/12-credential-rotation-and-dr.md).

---

## Read-local, write-global

| Request type | Route to |
|--------------|----------|
| **Session / read-your-writes** | Write region primary or sticky session |
| **Public catalog** | Regional replica + CDN(Content Delivery Network) |
| **Analytics** | Regional replica; stale OK |
| **All writes** | Single primary region |

API contract must document per-endpoint consistency → [api-design §1](../../api-design-and-protection/includes/01-api-design.md).

---

## Latency and routing

| Mechanism | Use |
|-----------|-----|
| **GeoDNS / latency routing** | Send user to nearest healthy region |
| **Global load balancer** | Health checks per region |
| **CDN** | Cache static and semi-static GET |
| **`X-Read-Region` header (internal)** | Debug which replica served read |

Avoid cross-region DB round trips on hot paths — cache in region.

---

## Data plane options

| Stack | Multi-region story |
|-------|-------------------|
| **PostgreSQL + async replica** | Read replicas in region B; writes to region A |
| **RDS cross-region read replica** | Managed; watch lag |
| **CockroachDB / Spanner** | Built-in global consistency; different ops model |
| **DynamoDB global tables** | Active-active at item level |

PostgreSQL details → [postgresql-performance §11](../../postgresql-performance/includes/11-read-scaling-and-caching.md).

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Read replica in region B for write-after-read UX | Route writes and immediate reads to primary |
| No lag monitoring per region | Alert on `pg_stat_replication` / cloud metric |
| Failover untested | Scheduled DR drill |
| Multi-region before single-region optimized | Fix primary hot path first |

---

## Pros and cons

**Pros:** Lower read latency globally; regional failure isolation.

**Cons:** Staleness, failover runbooks, cost duplication, harder debugging.