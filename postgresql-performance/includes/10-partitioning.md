# Partitioning

Partitioning splits one logical table into smaller physical pieces. Queries that filter on the **partition key** can skip irrelevant partitions (**partition pruning**).

> **Related:** Partitioning vs sharding vs replication vs clustering → [09-views-functions-and-scale-out-terminology.md](09-views-functions-and-scale-out-terminology.md)

## Partition strategies

| Strategy | Key type | Example |
|----------|----------|---------|
| **Range** | Ordered values | `created_at` by month |
| **List** | Discrete values | `region IN ('us', 'eu')` |
| **Hash** | Even distribution | `user_id` hash for sharding-like split |

Use **declarative partitioning** (PostgreSQL 10+):

```sql
CREATE TABLE events (
  id bigint GENERATED ALWAYS AS IDENTITY,
  org_id int NOT NULL,
  created_at timestamptz NOT NULL,
  payload jsonb
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_06 PARTITION OF events
  FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
```

## Pros and cons

| Pros | Cons |
|------|------|
| Faster queries with partition pruning | Queries without partition key scan all partitions |
| Drop old data by dropping partition | More complex migrations and monitoring |
| Smaller indexes per partition | Unique constraints must include partition key |
| Targeted vacuum/maintenance | Wrong key choice is hard to fix |

## When to use

- Tables with **millions+ rows** where queries **always filter** on the partition key
- **Time-series** data with retention policies
- Need to **drop** old data regularly (compliance, cost)
- Maintenance windows — vacuum/reindex one partition at a time

## When NOT to use

- Small or medium tables
- Queries that don't filter on the partition key
- "Might need it someday" without a pruning-friendly access pattern

## Retention pattern

```sql
-- Drop June 2025 data instantly (vs DELETE millions of rows)
DROP TABLE events_2025_06;
```

Schedule partition creation ahead of time (cron, pg_partman extension).

## Verify pruning

```sql
EXPLAIN SELECT * FROM events
WHERE created_at >= '2026-06-01' AND created_at < '2026-06-15';
```

Look for **`Partition Prune`** or scans on a single child table only — not all partitions.

## Index strategy

Index each partition the same way, or use partitioned indexes:

```sql
CREATE INDEX ON events (org_id, created_at DESC);
-- Creates matching indexes on all partitions
```

## Best practices

- Choose partition granularity so each partition is **manageable** (often monthly or weekly for events)
- Automate partition creation and old partition drops
- Include partition key in unique constraints and PKs
- Combine with **BRIN** on time column inside very large partitions if appropriate

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Partition without partition key in queries | Scans all partitions | Match schema to query patterns |
| Monthly partitions for 10k-row table | Unnecessary complexity | Wait until millions+ rows |
| Unique constraint without partition key | Invalid or awkward constraints | Include partition key in PK/unique |
| Mass DELETE for retention | Bloat and long vacuum | `DROP TABLE` old partition |
| Skip verifying prune in EXPLAIN | Silent full scan across children | Confirm `Partition Prune` in plan |
