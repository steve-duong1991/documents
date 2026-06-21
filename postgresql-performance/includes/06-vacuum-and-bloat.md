# Vacuum, Bloat, and Maintenance

PostgreSQL uses MVCC — updated and deleted rows leave **dead tuples** until vacuum reclaims space. Neglected maintenance causes bloat, slower scans, and blocked index-only scans.

> **Related:** Statistics refresh after vacuum → [§5 Statistics and the planner](05-statistics-and-planner.md) · Retention without mass DELETE → [§10 Partitioning](10-partitioning.md) · Online maintenance → [§15 Schema migration checklist](15-schema-migration-checklist.md)

## What autovacuum does

| Task | Purpose |
|------|---------|
| **Dead tuple cleanup** | Reclaim space; keep tables lean |
| **Freeze** | Prevent transaction ID wraparound |
| **Visibility map update** | Enable index-only scans |
| **Statistics update** | Runs `ANALYZE` when enough rows change |

## Signs you need attention

| Signal | Where to look |
|--------|---------------|
| Growing table size despite deletes | `pg_total_relation_size`; bloat estimates |
| Queries slowing over time | Dead tuple accumulation |
| Index-only scans not happening | Stale visibility map |
| `autovacuum` constantly behind | High-churn tables; long transactions |
| `xid_wraparound` warnings | Critical — vacuum not keeping up |

## Monitoring

```sql
SELECT
  relname,
  n_live_tup,
  n_dead_tup,
  round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
  last_autovacuum,
  last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;
```

## Tuning autovacuum (per table)

For high-churn tables:

```sql
ALTER TABLE events SET (
  autovacuum_vacuum_scale_factor = 0.02,
  autovacuum_analyze_scale_factor = 0.01
);
```

Lower scale factor = vacuum triggers sooner (more aggressive).

## Long-running transactions

Idle or long transactions **block vacuum** from reclaiming tuples they can still "see."

```sql
SELECT pid, state, xact_start, query
FROM pg_stat_activity
WHERE state != 'idle'
  AND xact_start < now() - interval '5 minutes';
```

Fix at the application layer: short transactions, connection pool timeouts, kill idle-in-transaction sessions.

## Manual maintenance

```sql
VACUUM (ANALYZE) orders;          -- routine after large deletes
VACUUM FULL orders;               -- rewrites table — locks exclusively; avoid in prod peak
REINDEX INDEX CONCURRENTLY idx_orders_user_id;
```

## pg_repack

For large tables with heavy bloat without long `VACUUM FULL` locks — rewrites the table online (extension).

## When to use

| Situation | Action |
|-----------|--------|
| High UPDATE/DELETE rate | Per-table autovacuum tuning |
| Bulk delete of old data | `VACUUM ANALYZE` or drop partitions instead |
| Table 2× expected size | Investigate bloat; consider `pg_repack` |
| Index-only scans never appear | Ensure autovacuum is running; check visibility map |

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Long idle-in-transaction sessions | Block vacuum, dead tuples accumulate | Pool timeouts; short transactions |
| `VACUUM FULL` during peak hours | Exclusive lock on table | `pg_repack` or maintenance window |
| Disable autovacuum globally | Wraparound risk, unbounded bloat | Tune per-table; never disable cluster-wide |
| Mass `DELETE` for retention | Bloat and long vacuum cycles | Drop partitions instead |
| Ignore dead tuple ratio alerts | Queries degrade gradually | Monitor `n_dead_tup` on churny tables |

## Best practices

- Never disable autovacuum globally
- Prefer **partition drops** over mass `DELETE` for retention
- Schedule heavy `REINDEX`/`VACUUM FULL` in maintenance windows
- Monitor dead tuple ratio on your busiest tables
