# Connection Management

> **Related:** Production credentials and PgBouncer patterns → [database-connection-and-security](../../database-connection-and-security/README.md) · [§9 PgBouncer + secret](../../database-connection-and-security/includes/09-pgbouncer-proxy-password.md)

PostgreSQL creates **one process per connection**. Beyond a few hundred active connections, context switching and memory overhead hurt performance even when queries are idle.

## The problem

| Factor | Impact |
|--------|--------|
| `max_connections = 500` | 500 backend processes — each uses memory |
| Microservices × replicas | Connection count multiplies quickly |
| Idle connections | Still consume RAM and file descriptors |
| Connection storms | New connections are expensive to establish |

## Solution: connection pooling

Use a pooler between apps and PostgreSQL:

| Tool | Notes |
|------|-------|
| **PgBouncer** | Most common; transaction or session pooling |
| **RDS Proxy** | AWS managed; IAM(Identity and Access Management) auth support |
| **Supabase pooler** | Built on PgBouncer |
| **Pgpool-II** | Pooling + load balancing + replication |

## PgBouncer pooling modes

| Mode | Behavior | Best for |
|------|----------|----------|
| **Transaction** | Connection returned after each transaction | Most web apps, stateless APIs |
| **Session** | Connection held for entire client session | Prepared statements, temp tables, `SET` |
| **Statement** | Connection returned after each statement | Rare; breaks multi-statement transactions |

## Recommended settings

```text
PostgreSQL:  max_connections = 100–300 (not 1000+)
PgBouncer:   default_pool_size = 20–50 per database/user
App servers: pool size = (expected concurrent queries) not (thread count)
```

Rule of thumb: **total app pool connections < PostgreSQL max_connections**, with headroom for admin and migrations.

## Prepared statements and transaction pooling

With **transaction pooling**, prepared statements don't persist across transactions. Options:

- Disable prepared statements in the ORM for pooled connections
- Use **session pooling** if you need persistent prepared statements
- PgBouncer 1.21+ has improved prepared statement support — verify your stack

## When to use

| Situation | Action |
|-----------|--------|
| > 100 connections from apps | Add PgBouncer |
| "Too many connections" errors | Pool, don't raise `max_connections` blindly |
| Server RAM high with idle clients | Transaction pooling |
| Lambda / serverless | External pooler (RDS Proxy, PgBouncer sidecar) |

## Best practices

- Set **`idle_in_transaction_session_timeout`** to kill stuck transactions
- Set **`statement_timeout`** on application roles
- One pool per service — not one giant shared pool with no limits
- Monitor: `pg_stat_activity` connection count by `application_name`

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Raise `max_connections` instead of pooling | Memory exhaustion; thrashing | PgBouncer or RDS Proxy |
| App pool size = thread count per instance | `replicas × pool` exceeds DB limit | Size pool to concurrent queries |
| Transaction pooling + ORM prepared statements | Broken or degraded queries | Disable prepared statements or use session pooling |
| No `idle_in_transaction_session_timeout` | Idle sessions block vacuum | Set timeout on app roles |
| One shared DB user for all services | Blast radius on credential leak | One role per service |
