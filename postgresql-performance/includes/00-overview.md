# Overview — PostgreSQL Performance

PostgreSQL performance work follows a predictable order: **measure first**, then fix queries and schema, tune the server, and scale out only when a single node is truly exhausted.

> **Related:** System-wide throughput order → [HTS README](../../high-throughput-systems/README.md) · B+ vs LSM(Log-Structured Merge) storage → [tree-and-index-structures](../../tree-and-index-structures/README.md) · Production credentials → [database-connection-and-security](../../database-connection-and-security/README.md)

## Layers at a glance

| Layer | Focus | Typical tools |
|-------|-------|---------------|
| **Measurement** | Find slow queries and bad plans | `EXPLAIN ANALYZE`, `pg_stat_statements` |
| **Query & schema** | Indexes, query shape, data types | B-tree, partial, composite indexes |
| **Maintenance** | Bloat, dead tuples, statistics | Autovacuum, `ANALYZE`, `pg_repack` |
| **Connections** | Too many clients | PgBouncer, RDS Proxy |
| **Configuration** | Memory, planner costs, parallelism | `shared_buffers`, `work_mem` |
| **Scale-out** | Read load, large tables, retention | Replicas, partitioning, caching |
| **Backup / PITR(Point-in-Time Recovery)** | Recovery drills, WAL(Write-Ahead Log) restore | Managed backups, [§16](16-backup-restore-and-pitr.md) |

## Strategy quick comparison

| Strategy | Effort | Impact | When to use first |
|----------|--------|--------|-------------------|
| `EXPLAIN ANALYZE` | Low | High | Always — before any other change |
| Targeted indexes | Low–Medium | High | Seq scans on large tables |
| Query rewrite | Medium | High | Expensive joins, N+1, `SELECT *` |
| Autovacuum tuning | Medium | Medium | High-churn tables, bloat |
| Connection pooling | Low | High | Many app servers / connections |
| Memory tuning | Medium | Medium | Sort/hash-heavy workloads |
| Partitioning | High | High | Time-series at millions+ rows |
| Read replicas | Medium | Medium | Read-heavy after query optimization |
| App caching | Medium | High | Repeated identical hot reads |

## Default recommendation

For most OLTP workloads:

1. Enable **`pg_stat_statements`** and find the top queries by total time
2. Run **`EXPLAIN (ANALYZE, BUFFERS)`** on each slow query
3. Add **targeted indexes** (partial or composite where appropriate)
4. Put **PgBouncer** in front of the database before raising `max_connections`
5. Tune **`shared_buffers`** and **`effective_cache_size`** at deploy time
6. Read **[§9 scale-out terminology](09-views-functions-and-scale-out-terminology.md)** before choosing partitioning, replicas, or sharding
7. Only then consider **partitioning**, **replicas**, or **caching**

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Skip measurement and buy bigger hardware | `pg_stat_statements` + EXPLAIN first |
| Replicas before query tuning | Optimize primary, then scale reads |
| Partition without pruning-friendly queries | Match partition key to filters |
| Raise `max_connections` instead of pooling | PgBouncer or RDS Proxy |
| Tune many config knobs at once | One change; re-measure each time |

## Performance decision flow

Full decision flowchart, scenario table, and common mistakes → **[§13 Decision guide and common mistakes](13-decision-guide-and-common-mistakes.md)**.

## Priority order

1. **Measure** — never optimize blind
2. **Index correctly** — partial, composite, covering where needed
3. **Fix queries and schema** — fewer round trips, right types
4. **Vacuum/analyze health** — especially on churny tables
5. **Connection pooling** — before raising `max_connections`
6. **Config tuning** — memory and SSD-aware planner costs
7. **Understand scale-out terms** — [§9](09-views-functions-and-scale-out-terminology.md): partitioning vs replication vs sharding
8. **Partitioning / replicas / caching** — when single-node fixes aren't enough
9. **Backup and PITR drills** — [§16 Backup, restore, and PITR](16-backup-restore-and-pitr.md) with [database-connection §12](../../database-connection-and-security/includes/12-credential-rotation-and-dr.md)
