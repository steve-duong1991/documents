# Schema Design

Good schema design prevents expensive fixes later. Normalize first; denormalize only when measurement shows a real bottleneck.

> **Related:** Index choices for schema shape → [§2 Indexing](02-indexing.md) · Query patterns → [§3 Query design](03-query-design.md) · Online migrations → [§15 Schema migration checklist](15-schema-migration-checklist.md)

## Core principles

| Principle | Guidance |
|-----------|----------|
| **Normalize first** | Reduce redundancy; use FKs for integrity |
| **Denormalize deliberately** | Only when joins/aggregations are proven slow |
| **Right-size types** | `int` vs `bigint`, `text` vs `varchar(n)`, `timestamptz` over `timestamp` |
| **Use constraints** | PK, FK, `NOT NULL`, `CHECK` — help planner and data quality |
| **Avoid hot wide rows** | Split rarely accessed columns into separate tables |

## Data type choices

| Use | Instead of | Why |
|-----|------------|-----|
| `timestamptz` | `timestamp` | Timezone-aware; fewer bugs |
| `text` | `varchar(255)` | Same performance in PostgreSQL; no arbitrary limit |
| `bigint` for IDs | `int` | Avoid overflow on high-volume tables |
| `numeric` | `float` for money | Exact decimal arithmetic |
| `uuid` / `bigint` | Random string PKs | Smaller indexes; better locality with sequential IDs |

## JSONB

Good for semi-structured or evolving attributes. **Not** a replacement for columns you filter and join on constantly.

```sql
-- Queryable JSONB with GIN index
CREATE INDEX idx_events_payload ON events USING GIN (payload jsonb_path_ops);

SELECT * FROM events WHERE payload @> '{"type": "purchase"}';
```

| Use JSONB for | Use columns for |
|---------------|-----------------|
| Optional metadata | Primary filters and joins |
| Schema that changes often | Foreign keys |
| Nested documents | Sorting and range queries at scale |

## Primary keys and indexing

- Every table should have a **primary key**
- **Sequential IDs** (`bigint` identity) give better index locality than random UUIDs
- If using UUIDs, consider **`uuidv7`** or **`gen_random_uuid()`** with awareness of index bloat vs sequential inserts

## Foreign keys

Always index the **referencing column** (child side):

```sql
CREATE TABLE order_items (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id bigint NOT NULL REFERENCES orders(id),
  ...
);
CREATE INDEX idx_order_items_order_id ON order_items (order_id);
```

Without this index, deletes/updates on the parent table lock and scan the child.

## Soft deletes

If most queries filter `WHERE deleted_at IS NULL`, use a **partial index**:

```sql
CREATE INDEX idx_users_email_active ON users (email) WHERE deleted_at IS NULL;
```

## When to denormalize

- Read-heavy dashboards that aggregate across many joins
- Counters updated frequently (consider careful concurrency handling)
- Event logs where immutability makes duplication safe

Always measure join cost before denormalizing.

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| JSONB for every filter column | Slow scans, huge GIN(Generalized Inverted Index) indexes | Relational columns for hot paths |
| Random UUID primary keys | Index bloat, poor insert locality | Sequential IDs or `uuidv7` |
| Missing FK index on child table | Parent DELETE/UPDATE scans child | Index referencing columns |
| Denormalize before measuring | Extra write complexity for no gain | `EXPLAIN` join cost first |
| `varchar(255)` everywhere | Arbitrary limits, no benefit in PG | Use `text` unless length constraint needed |
| Soft delete without partial index | Index includes deleted rows | `WHERE deleted_at IS NULL` partial index |

## Best practices

- Design for **query patterns**, not just entity diagrams
- Add constraints in migrations — not only in application code
- Plan **partition keys** early for time-series tables
- Keep migration scripts **online-friendly** (`CONCURRENTLY` for indexes)
