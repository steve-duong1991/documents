# Read Scaling, Replication, and Caching

When query optimization and indexing aren't enough for read load, scale reads horizontally — but only **after** fixing slow queries on the primary.

> **Related:** Replication vs sharding vs partitioning → [09-views-functions-and-scale-out-terminology.md](09-views-functions-and-scale-out-terminology.md) · What strong consistency promises, what it costs, and when to require it → [Strong consistency — promises and costs](14-consistency-promises-and-costs.md)

## Read replicas

Streaming replication sends WAL(Write-Ahead Log) changes to one or more standby servers.

| Pros | Cons |
|------|------|
| Offload SELECT traffic from primary | Replication lag |
| Simple mental model | Replicas don't fix bad queries |
| Managed on all major clouds | No automatic query routing |

### When to use

- Read-heavy workloads: dashboards, search, reporting
- Primary CPU or IO saturated by **SELECT** after optimization
- Geographic read locality (read replica in another region)

### Caveats

- **Read-your-writes:** after an INSERT, a read from replica may be stale — route session-critical reads to primary
- Replicas replay writes too — very write-heavy primaries can lag replicas
- Run the same `EXPLAIN ANALYZE` on replica — bad plans are bad everywhere

## Caching layers

| Layer | Tool | When to use |
|-------|------|-------------|
| **Application cache** | Redis, Memcached | Hot keys, session data, idempotent reads |
| **Materialized view** | PostgreSQL native | Expensive SQL(Structured Query Language) aggregations refreshed periodically |
| **Query result cache** | ORM / CDN(Content Delivery Network) | Identical repeated API(Application Programming Interface) responses |
| **Unlogged tables** | PostgreSQL | Staging/bulk temp data (not crash-safe) |

### Materialized views

```sql
CREATE MATERIALIZED VIEW daily_revenue AS
SELECT date_trunc('day', created_at) AS day, sum(amount) AS total
FROM orders
GROUP BY 1;

CREATE UNIQUE INDEX ON daily_revenue (day);

REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue;
```

**When to use:** Dashboards tolerating minutes of staleness; heavy aggregations over millions of rows.

### Application cache (Redis)

**When to use:**

- Same key read thousands of times per second
- Computed values expensive to derive
- Rate limit counters, feature flags

**Cache invalidation patterns:** TTL, delete-on-write, and event-driven invalidation — full patterns, CDN layer, cache-aside vs write-through, and stampede mitigation → [high-throughput-systems §4 Caching layers](../../high-throughput-systems/includes/04-caching-layers.md).

## Layered read path

End-to-end flow (Redis → primary vs replica routing, plus CDN for public GETs) lives in [high-throughput-systems §4 — Layered read path](../../high-throughput-systems/includes/04-caching-layers.md#layered-read-path). This section focuses on **PostgreSQL-specific** pieces: replicas, materialized views, and `pg_stat_replication`.

## When to use what

| Scenario | Recommendation |
|----------|----------------|
| Single slow report query | Materialized view or pre-aggregation table |
| Hot product page | Redis cache with TTL |
| 10× read vs write ratio | Read replica + app routing |
| Search autocomplete | Dedicated index (GIN(Generalized Inverted Index)) + cache; not replica alone |
| Global low-latency reads | Replicas per region + CDN for static API responses |

## Best practices

- Optimize on primary first — replicas multiply cost of bad queries
- Monitor **replication lag** (`pg_stat_replication` on primary)
- Document which endpoints require strong consistency
- Set cache TTLs based on business tolerance for staleness

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Add replicas before tuning primary | 10× the same bad query | Optimize on primary first |
| Read-after-write from replica | User sees stale data | Route session writes to primary |
| Cache without invalidation strategy | Stale reads until TTL | Delete-on-write or event-driven invalidation |
| Ignore replication lag alerts | Growing stale read window | Monitor `pg_stat_replication` |
| Materialized view without CONCURRENT refresh | Blocks readers during refresh | Unique index + `REFRESH CONCURRENTLY` |