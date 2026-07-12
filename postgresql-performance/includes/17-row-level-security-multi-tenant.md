# Row-Level Security for Multi-Tenant Data

PostgreSQL **RLS(Row-Level Security)** adds a database-enforced filter on every row access. Use it as a **safety net** alongside application checks — not as the only AuthZ layer.

> **Related:** Multi-tenant API(Application Programming Interface) patterns → [api-design §16](../../api-design-and-protection/includes/16-multi-tenant-apis.md) · Security barrier views → [§9 views](09-views-functions-and-scale-out-terminology.md#security-barrier-views) · Composite indexes → [§2 indexing](02-indexing.md) · DB security checklist → [database-connection §2](../../database-connection-and-security/includes/02-prod-db-security.md)

---

## At a glance

| Step | Action |
|------|--------|
| 1 | Add `tenant_id` column + composite indexes on hot queries |
| 2 | `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` |
| 3 | Create policies comparing `tenant_id` to session variable |
| 4 | App sets `SET app.tenant_id = ...` at start of each request/transaction |
| 5 | Use non-superuser DB roles without `BYPASSRLS` in application paths |

**Rule of thumb:** RLS catches forgotten `WHERE tenant_id = ?` in ad-hoc queries and ORM bugs. It does **not** replace token validation, object ownership checks, or gateway AuthZ.

---

## Schema baseline

Every tenant-scoped table needs `tenant_id` on the row and indexes that lead with it:

```sql
CREATE TABLE orders (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id   uuid NOT NULL,
  status      text NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_orders_tenant_status_created
  ON orders (tenant_id, status, created_at DESC);
```

Child tables inherit tenant scope — either duplicate `tenant_id` on the child (simplest for RLS) or enforce via join in policy (harder to maintain).

---

## Enable RLS and create policies

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

CREATE POLICY orders_tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id', true)::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id', true)::uuid);
```

| Clause | Purpose |
|--------|---------|
| `USING` | Filters rows on `SELECT`, `UPDATE`, `DELETE` |
| `WITH CHECK` | Validates rows on `INSERT`, `UPDATE` |
| `FORCE ROW LEVEL SECURITY` | Applies policies even to table owner (except superuser) |
| `current_setting(..., true)` | Returns NULL if unset — row invisible until tenant is set |

Repeat for each tenant-scoped table, or use a shared policy pattern via migration tooling.

---

## Set tenant context from the application

Set the session variable **once per request** (or at pool checkout), inside the same transaction as queries:

```sql
-- After validating JWT / API key tenant claim
SELECT set_config('app.tenant_id', '550e8400-e29b-41d4-a716-446655440000', true);
```

```text
Request → validate token → derive tenant_id → SET app.tenant_id → queries run under RLS
```

| Language / layer | Pattern |
|------------------|---------|
| **Raw SQL(Structured Query Language)** | `SET LOCAL app.tenant_id = '...'` inside transaction |
| **Connection pool** | Reset `app.tenant_id` on connection return; never reuse stale tenant |
| **ORM** | Middleware or `before_query` hook sets session variable |
| **Migrations / admin** | Separate role with `BYPASSRLS` or superuser — never in app runtime |

**Never** take `tenant_id` from the request body alone — bind from the authenticated token ([api-design §16](../../api-design-and-protection/includes/16-multi-tenant-apis.md)).

---

## Roles and BYPASSRLS

| Role | Typical use | RLS |
|------|-------------|-----|
| **`app_api`** | Application queries | Policies enforced |
| **`app_readonly`** | Read replicas / reports | Policies enforced |
| **`app_migration`** | Schema migrations | Often `BYPASSRLS` or superuser — CI(Continuous Integration) only |
| **`postgres` superuser** | Break-glass admin | Bypasses RLS — never for app |

```sql
CREATE ROLE app_api LOGIN PASSWORD '...' NOSUPERUSER NOBYPASSRLS;
GRANT SELECT, INSERT, UPDATE, DELETE ON orders TO app_api;
```

Audit which roles have `BYPASSRLS` — see [database-connection §2](../../database-connection-and-security/includes/02-prod-db-security.md).

---

## Security barrier views (optional layer)

Views can centralize the tenant predicate for read paths:

```sql
CREATE VIEW tenant_orders
WITH (security_barrier) AS
SELECT * FROM orders
WHERE tenant_id = current_setting('app.tenant_id', true)::uuid;
```

`security_barrier` prevents the planner from pushing untrusted user filters below the tenant predicate. Full context → [§9 security barrier views](09-views-functions-and-scale-out-terminology.md#security-barrier-views).

RLS on base tables is still recommended when apps query tables directly.

---

## RLS vs application checks

| Layer | Strength | Weakness |
|-------|----------|----------|
| **Gateway / JWT(JSON Web Token)** | Stops unauthenticated cross-tenant calls | No row-level guarantee |
| **Application** | Object ownership, field-level AuthZ | Easy to miss one query |
| **RLS** | DB-wide default deny for wrong tenant | Policy drift; admin role mistakes |
| **Schema / DB per tenant** | Strongest isolation | Highest ops cost |

Use **JWT claim + app check + RLS** for shared-table B2B SaaS. Enterprise silos may drop shared RLS in favor of dedicated databases.

---

## Testing RLS

```sql
BEGIN;
SELECT set_config('app.tenant_id', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', true);
SELECT count(*) FROM orders;  -- only tenant A rows

SELECT set_config('app.tenant_id', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', true);
SELECT count(*) FROM orders;  -- only tenant B rows
ROLLBACK;
```

Add integration tests that:

1. Set tenant A, insert row, verify visible under A
2. Switch to tenant B, verify row **not** visible
3. Attempt `INSERT` with wrong `tenant_id` — should fail `WITH CHECK`

---

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| RLS enabled but no policies | All rows hidden (or none, pre-policy) | Add explicit `USING` / `WITH CHECK` policies |
| App uses superuser or `BYPASSRLS` role | RLS never applies | Dedicated `app_api` role |
| Stale `app.tenant_id` on pooled connection | Cross-tenant leak | Reset on checkout/return; use `SET LOCAL` in TX |
| `tenant_id` only in app, not on child rows | Join leaks rows | Denormalize `tenant_id` or strict join policies |
| RLS replaces AuthZ review | BOLA(Broken Object-Level Authorization) within same tenant | Object ownership checks in app |
| Missing `(tenant_id, ...)` index | Seq scans under load | Composite indexes — [§2](02-indexing.md) |
| Background job without tenant context | Worker sees no rows or wrong rows | Set `app.tenant_id` per job from message metadata |

---

## When to skip shared-table RLS

| Situation | Approach |
|-----------|----------|
| Dedicated DB per enterprise customer | DB-level isolation; RLS optional |
| Heavy cross-tenant analytics | Separate read role, warehouse, or materialized aggregates |
| Citus / sharded by tenant | Shard key replaces shared-table RLS pattern |

---

## See also

- [Multi-tenant APIs](../../api-design-and-protection/includes/16-multi-tenant-apis.md) — cache, queue, and API patterns
- [Indexing](02-indexing.md) — `(tenant_id, created_at DESC)` and partial indexes
- [Schema migration checklist](15-schema-migration-checklist.md) — `CREATE INDEX CONCURRENTLY` with tenant indexes
- [Read scaling and caching](11-read-scaling-and-caching.md) — replicas still need tenant scope in queries