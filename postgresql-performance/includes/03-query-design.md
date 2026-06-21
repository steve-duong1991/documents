# Query Design

Even perfect indexes cannot fix a fundamentally expensive query shape. Query design reduces work before it hits the storage layer.

> **Related:** Index support for filters and sorts → [§2 Indexing](02-indexing.md) · Measurement first → [§1 Measurement](01-measurement.md) · System-wide latency → [HTS §5 Database throughput](../../high-throughput-systems/includes/05-database-throughput.md)

## Core strategies

| Strategy | Why it helps | Example |
|----------|--------------|---------|
| **Select only needed columns** | Less IO, smaller rows | `SELECT id, name` not `SELECT *` |
| **Limit early** | Stop after enough rows | `LIMIT 20` with index supporting sort |
| **Avoid functions on indexed columns** | Index cannot be used | `created_at >= '2024-01-01'` not `date(created_at) = ...` |
| **Use EXISTS over IN** | Better for correlated large sets | `WHERE EXISTS (SELECT 1 FROM ...)` |
| **Batch writes** | Fewer round trips | Multi-row `INSERT`, `COPY` |
| **Eliminate N+1** | One round trip vs hundreds | JOIN or `WHERE id = ANY($1)` |

## N+1 problem

**Bad — one query per row:**

```text
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
... (N times)
```

**Good — single query:**

```sql
SELECT * FROM orders WHERE user_id = ANY($1::int[]);
-- or
SELECT o.* FROM orders o JOIN users u ON u.id = o.user_id WHERE u.org_id = $1;
```

## Pagination

**Offset pagination** (`LIMIT 20 OFFSET 100000`) gets slower as offset grows — PostgreSQL must scan and discard rows.

**Keyset pagination** (cursor-based) scales:

```sql
SELECT id, created_at, title
FROM posts
WHERE (created_at, id) < ($last_created_at, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Requires an index on `(created_at DESC, id DESC)`.

## Aggregations

- Pre-filter with `WHERE` before `GROUP BY`
- Use **`HAVING`** only when filtering aggregates — not as a substitute for `WHERE`
- For repeated expensive aggregates, consider [materialized views](11-read-scaling-and-caching.md#materialized-views)

## JOINs

- Join on **indexed columns** (usually PK/FK)
- Avoid joining wide tables when only a few columns are needed — select early or use covering indexes
- `LEFT JOIN` where you filter the right table in `WHERE` often behaves like an inner join — put filters in `ON` when appropriate

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `SELECT *` on wide rows | Excess IO | Select needed columns |
| `OR` across different columns | Often prevents index use | `UNION ALL` of two indexed queries |
| Implicit cast mismatch | Index not used | Match column and parameter types |
| `NOT IN (subquery)` with NULLs | Surprising empty results | `NOT EXISTS` |
| Unbounded queries in APIs | Memory and timeout risk | Always paginate |
| Offset pagination on large tables | Linear slowdown as offset grows | Keyset / cursor pagination |
| ORM N+1 on hot paths | Hundreds of round trips | JOIN, batch `ANY()`, or eager load |

## When to use

- After `EXPLAIN` shows the plan is structurally expensive (large sorts, hash joins on huge sets)
- When ORMs generate inefficient SQL(Structured Query Language)
- When API(Application Programming Interface) latency scales with row count linearly
- When write amplification is high from many small statements

## Best practices

- Review ORM-generated SQL for hot paths
- Use **prepared statements** for repeated queries (plan caching)
- Set **`statement_timeout`** as a safety net
- Use **`EXPLAIN`** on production-shaped data, not empty dev databases