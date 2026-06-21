# Statistics and the Query Planner

PostgreSQL's planner chooses join order, scan types, and parallel workers based on **table statistics**. Bad statistics lead to bad plans.

> **Related:** When plans go wrong after bulk load → [§6 Vacuum and bloat](06-vacuum-and-bloat.md) · SSD planner costs → [§8 Memory and configuration](08-memory-and-config.md) · Measurement workflow → [§1 Measurement](01-measurement.md)

## How statistics work

- **`ANALYZE`** samples rows and stores histograms, null fractions, and distinct counts in `pg_stats`
- **Autovacuum** runs `ANALYZE` automatically when enough rows change
- The planner compares **estimated rows** vs what you see as **actual rows** in `EXPLAIN ANALYZE`

## When estimates are wrong

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Nested loop on huge set | Underestimated rows | `ANALYZE`; increase statistics target |
| Seq scan when index exists | Overestimated index cost | `ANALYZE`; lower `random_page_cost` on SSD |
| Bad join order | Correlated columns not captured | Extended statistics |
| Plan changed after bulk load | Stale stats | `ANALYZE` after load |

## default_statistics_target

Default is **100**. Increase for columns where the planner makes poor choices:

```sql
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
ANALYZE orders;
```

Higher values = better estimates but slower `ANALYZE` and slightly more planner time.

## Extended statistics

For correlated columns the planner treats as independent:

```sql
CREATE STATISTICS orders_status_created (dependencies)
  ON status, created_at FROM orders;

ANALYZE orders;
```

Types: `dependencies`, `ndistinct`, `mcv` (most common values).

## When to use

| Situation | Action |
|-----------|--------|
| After bulk INSERT/UPDATE/DELETE | `ANALYZE table_name` |
| Plan flip-flops between deploys | Check autovacuum; increase statistics target |
| Multi-column filters with skew | Extended statistics or partial indexes |
| New index not being used | `ANALYZE`; verify selectivity with `EXPLAIN` |

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Skip `ANALYZE` after bulk load | Stale row estimates, bad plans | `ANALYZE` table after large INSERT/UPDATE/DELETE |
| Raise `default_statistics_target` globally | Slower ANALYZE and planning everywhere | Per-column statistics target only |
| Ignore estimated vs actual rows in EXPLAIN | Miss planner regression | Compare in every `EXPLAIN ANALYZE` |
| Assume correlated columns are independent | Wrong join order | Extended statistics or partial indexes |
| Disable autovacuum on busy tables | Stats never refresh | Tune per-table autovacuum, don't disable |

## Best practices

- Trust autovacuum for steady-state OLTP — manual `ANALYZE` mainly after bulk changes
- Compare estimated vs actual rows in every `EXPLAIN ANALYZE`
- Don't raise statistics target globally — per-column is enough
- On PostgreSQL 14+, consider **`pg_stat_statements`** + auto-explain for plan regression detection

## Check current stats

```sql
SELECT schemaname, tablename, last_analyze, last_autoanalyze, n_live_tup, n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
```
