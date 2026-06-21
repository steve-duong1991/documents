# PgBouncer + secret (proxy + password)

> Connection pooling in front of the database using **PgBouncer** (or similar), with credentials from a secret manager — no IAM(Identity and Access Management) or Vault required.

> **Related:** Secret source → [§5 Secret manager + password](05-secret-manager-password.md) · AWS managed proxy → [§4 RDS Proxy](04-aws-iam-rds-proxy.md) · Pool modes and sizing → [postgresql-performance §7](../../postgresql-performance/includes/07-connection-management.md)

## What it solves

- **Connection pooling** — many app instances share a small pool of real DB connections
- Prevents exhausting `max_connections` on Postgres under load (especially serverless/Lambda-style bursts)
- Credentials still come from a secret manager, not from code — see [05-secret-manager-password.md](05-secret-manager-password.md)
- Works on **any** cloud and **self-hosted** Postgres

## What it does not solve

- Password is still **long-lived** (unless rotated via secret manager)
- PgBouncer is **another component** to deploy, monitor, and patch
- Not a secrets platform — only pools connections

---

## Architecture

```
App 1 ──┐
App 2 ──┼──► PgBouncer (pool) ──► PostgreSQL
App N ──┘         ↑
            password from secret manager
            (PgBouncer auth or passthrough)
```

**Stack:**

```
Private subnet → TLS → PgBouncer → Postgres
                           ↑
                    DB password from secret manager
```

**With RDS Proxy (AWS):** same idea but managed — see [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) or [05-secret-manager-password.md](05-secret-manager-password.md) (Proxy + Secrets Manager, password auth).

---

## PgBouncer auth modes

| Mode | How it works |
|------|--------------|
| **Session pooling** | One server connection per client session; simplest |
| **Transaction pooling** | Server conn returned after each transaction; highest multiplexing |
| **Statement pooling** | Rare; breaks some Postgres features |

| Client auth | How |
|-------------|-----|
| **Passthrough** | App sends real DB user/password; PgBouncer forwards to Postgres |
| **auth_query** | PgBouncer validates against Postgres `pg_shadow` / custom query |
| **Static userlist** | `userlist.txt` — usually paired with secret manager reload |

---

## Setup steps

1. **Postgres** in private subnet; TLS(Transport Layer Security); dedicated app users with least privilege.
2. **Store credentials** in secret manager — [05-secret-manager-password.md](05-secret-manager-password.md).
3. **Deploy PgBouncer** in the same VPC (sidecar, dedicated VM, or K8s Deployment).
4. **Configure** `pgbouncer.ini`:

```ini
[databases]
myapp = host=postgres.internal port=5432 dbname=myapp

[pgbouncer]
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = scram-sha-256
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

5. **Apps connect to PgBouncer**, not directly to Postgres:

```
postgresql://app_user:SECRET@pgbouncer.internal:6432/myapp?sslmode=require
```

6. **Scale pool size** from app concurrency and Postgres `max_connections`.

---

## When to combine with other approaches

| Combination | Purpose |
|-------------|---------|
| PgBouncer + secret manager | Pooling + no password in git |
| PgBouncer + direct RDS IAM | IAM token to Postgres; PgBouncer in transaction mode is tricky with IAM — often connect app → RDS Proxy instead |
| PgBouncer + Vault | Vault issues creds; app → PgBouncer → DB |

For AWS IAM tokens, **RDS Proxy** is usually preferred over PgBouncer + IAM.

---

## How this maps to security layers

| Layer | Coverage |
|-------|----------|
| 1. Network isolation | PgBouncer and DB in private network; apps → PgBouncer only |
| 2. TLS | TLS to PgBouncer and/or to Postgres |
| 3. Authentication | Dedicated DB user per service |
| 4. Secrets management | Password from secret manager |
| 5. Connection proxy | **PgBouncer** — core of this approach |

---

## Comparison

| | PgBouncer + secret | RDS Proxy | Direct to DB |
|--|-------------------|-----------|--------------|
| Managed | Self-hosted | AWS managed | N/A |
| Pooling | Yes | Yes | No |
| Cloud | Any | AWS | Any |
| IAM auth | Awkward | Native | N/A |

---

## When to use

**Use when:**

- Self-hosted Postgres or RDS without RDS Proxy
- High app instance count vs low `max_connections`
- You already use static secrets from a secret manager

**Use RDS Proxy instead when:**

- On AWS and want managed pooling + IAM — [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Session pooling with prepared statements | Use transaction pooling or disable prepared statements |
| PgBouncer `max_client_conn` without DB headroom | Size pool vs Postgres `max_connections` |
| Password in PgBouncer config on disk | `auth_file` from secret manager or env injection |
| Skip TLS between app and PgBouncer | TLS end-to-end in production |
| One pool for admin and app traffic | Separate pools or roles |
