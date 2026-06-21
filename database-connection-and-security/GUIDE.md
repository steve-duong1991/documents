# Database Connection & Security (Full)

> Combined view of all sections. Modular sources live in `includes/`.

---

# Overview — Database Connection & Security

Production database access is **layered**: network isolation and TLS first, then authentication, secrets, pooling, and audit. Pick a connection pattern based on cloud, scale, and compliance — not on what is easiest in dev.

> **Related:** Pool sizing and `max_connections` → [postgresql-performance §7](../postgresql-performance/includes/07-connection-management.md) · Service identity → [api-design §12 Identity](../api-design-and-protection/includes/12-identity-rbac-iam-ad.md) · Pattern picker → [§13 Decision guide](13-decision-guide.md)

## Security layers at a glance

| Layer | Focus | Sections |
|-------|-------|----------|
| **Network** | Private subnet, no public IP, firewall | [§2 Production security](02-prod-db-security.md) |
| **TLS** | Encrypt in transit; verify server cert | [§2](02-prod-db-security.md), [§10 mTLS](10-mtls-client-certs.md) |
| **Authentication** | One DB user per service; least privilege | [§2](02-prod-db-security.md), cloud patterns §3–§11 |
| **Secrets** | No credentials in git or images | [§3 Vault](03-hcv-vault.md), [§5 Secret manager](05-secret-manager-password.md) |
| **Pooling** | Avoid connection storms | [§4 RDS Proxy](04-aws-iam-rds-proxy.md), [§9 PgBouncer](09-pgbouncer-proxy-password.md) |
| **Identity** | IAM / workload identity instead of passwords | [§4](04-aws-iam-rds-proxy.md), [§6](06-direct-rds-iam.md), [§7](07-gcp-cloud-sql-identity.md), [§8](08-azure-database-identity.md) |
| **Rotation & DR** | Rotate creds; test restores | [§12 Credential rotation and DR](12-credential-rotation-and-dr.md) |

## Connection patterns at a glance

| Pattern | Short-lived creds? | Typical complexity | Best when |
|---------|-------------------|-------------------|-----------|
| [§11 PaaS](11-paas-managed-db.md) | Usually no | Very low | MVP, small teams |
| [§5 Secret manager + password](05-secret-manager-password.md) | No (rotated password) | Low | Default production baseline |
| [§4 AWS IAM + RDS Proxy](04-aws-iam-rds-proxy.md) | Yes (IAM token) | Medium | AWS at scale, Lambda/K8s |
| [§6 Direct RDS IAM](06-direct-rds-iam.md) | Yes | Medium | AWS, low connection count |
| [§7 GCP Cloud SQL](07-gcp-cloud-sql-identity.md) / [§8 Azure](08-azure-database-identity.md) | Yes | Medium | All-in on GCP or Azure |
| [§3 Vault dynamic](03-hcv-vault.md) | Yes (temp DB user) | High | Multi-cloud, strict audit |
| [§9 PgBouncer + secret](09-pgbouncer-proxy-password.md) | No | Low–medium | Self-hosted Postgres at scale |
| [§10 mTLS](10-mtls-client-certs.md) | Cert expiry | High | Zero-trust, mature PKI |

Full decision flow → **[§13 Decision guide](13-decision-guide.md)**.

## Default recommendation

For most production services on a major cloud:

1. Database in a **private subnet** with **TLS required** (`verify-full`)
2. **One DB user per service** with least-privilege grants
3. Credentials from a **secret manager** ([§5](05-secret-manager-password.md)) or **cloud IAM auth** (§4, §6, §7, §8)
4. **Connection proxy or pooler** when replica count or serverless concurrency grows ([§4](04-aws-iam-rds-proxy.md), [§9](09-pgbouncer-proxy-password.md))
5. **Rotation runbook** and quarterly restore drill ([§12](12-credential-rotation-and-dr.md))

Local dev uses [§1 Local credentials](01-local-db-credentials.md) — never copy `trust` auth or dashboard connection strings into production.

## Document map

| # | Topic | File |
|---|-------|------|
| 1 | Local credentials *(dev template)* | [01-local-db-credentials.md](01-local-db-credentials.md) |
| 2 | Production security | [02-prod-db-security.md](02-prod-db-security.md) |
| 3–11 | Connection patterns (Vault, IAM, cloud, PaaS, mTLS) | See [§13](13-decision-guide.md) flow |
| 12 | Credential rotation and DR | [12-credential-rotation-and-dr.md](12-credential-rotation-and-dr.md) |
| 13 | Decision guide | [13-decision-guide.md](13-decision-guide.md) |

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Production `trust` auth from local dev | TLS + secret manager or IAM in prod |
| One DB credential shared by all services | One role (or secret) per service |
| Skip rotation runbook | Dual-active creds → [§12](12-credential-rotation-and-dr.md) |
| Vault on day one for one small app | Start [§5](05-secret-manager-password.md) |
| Public database endpoint for convenience | Private subnet; no public IP |

---

# Local Database Credentials

> **Note:** This section is a **local dev template** — host, username, and paths are machine-specific. Replace them for your environment. Production connection patterns start in [§2 Production security](02-prod-db-security.md).

> **Related:** Production baseline → [§2 Production security](02-prod-db-security.md) · Pattern picker → [§13 Decision guide](13-decision-guide.md) · Never use local auth in prod → [§00 Overview](00-overview.md)

> **Environment:** macOS · Homebrew · PostgreSQL 17  
> **Last updated:** June 2026

## Connection details

| Setting | Value |
|---------|-------|
| **Host** | `localhost` (or `127.0.0.1`) |
| **Port** | `5432` |
| **Database** | `postgres` |
| **Username** | `steveduong` |
| **Password** | *(none — not required for local connections)* |
| **SSL** | Not required locally |

## Connection strings

**URI format:**

```
postgresql://steveduong@localhost:5432/postgres
```

**JDBC (Java / Spring Boot):**

```
jdbc:postgresql://localhost:5432/postgres
```

**Environment variables:**

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=postgres
export PGUSER=steveduong
# PGPASSWORD is not set — local auth uses trust
```

## Quick connect

```bash
pg-start          # start PostgreSQL (manual, on-demand)
psql postgres     # connect to default database
pg-stop           # stop when done
```

## Shell aliases

Defined in `~/.zshrc`:

| Alias | Command |
|-------|---------|
| `pg-start` | `pg_ctl -D /opt/homebrew/var/postgresql@17 start` |
| `pg-stop` | `pg_ctl -D /opt/homebrew/var/postgresql@17 stop` |
| `pg-status` | `pg_ctl -D /opt/homebrew/var/postgresql@17 status` |

## Install paths

| Item | Path |
|------|------|
| Binaries | `/opt/homebrew/opt/postgresql@17/bin` |
| Data directory | `/opt/homebrew/var/postgresql@17` |
| Config | `/opt/homebrew/var/postgresql@17/pg_hba.conf` |

## Authentication (local only)

Local connections use **`trust`** authentication — no password is required:

```
local   all   all                 trust
host    all   all   127.0.0.1/32    trust
host    all   all   ::1/128         trust
```

> **Note:** This setup is for **local development only**. Do not use `trust` auth in production.

## Optional: set a password

If a GUI tool requires a password field:

```bash
psql postgres -c "ALTER USER steveduong PASSWORD 'your_password';"
```

## Start behaviour

PostgreSQL is **not** set to auto-start on macOS boot.

- Do **not** use `brew services start postgresql@17` (runs in background + auto-start on login).
- Use `pg-start` / `pg-stop` manually when needed.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Copy local connection string to production | Use [§5](05-secret-manager-password.md) or cloud IAM patterns |
| Commit `.env` with `DATABASE_URL` | Platform secrets / CI variables only |
| Use `brew services` when manual start is intended | `pg-start` / `pg-stop` per project convention |
| Expose Postgres on `0.0.0.0` for convenience | Localhost only in dev |

---

# Production Database Security

> How to protect **service → database** connections in production.

> **Related:** Pattern picker (canonical flow) → [§13 Decision guide](13-decision-guide.md) · Pool sizing → [postgresql-performance §7](../postgresql-performance/includes/07-connection-management.md) · Rotation runbook → [§12 Credential rotation and DR](12-credential-rotation-and-dr.md)

Production database security is **layered** — no single control is enough. Secret managers such as HashiCorp Vault or AWS IAM + RDS Proxy address authentication and secrets, but they sit alongside network, TLS, and monitoring controls.

---

## Security layers at a glance

| Layer | Focus |
|-------|--------|
| 1. Network isolation | Keep the DB off the public internet |
| 2. TLS/SSL | Encrypt traffic in transit |
| 3. Authentication | One DB user per service, least privilege |
| 4. Secrets management | No credentials in code or git |
| 5. Connection proxy | Pooling and credential brokering |
| 6. Workload identity | IAM / K8s service accounts |
| 7. Application protections | SQL injection, RLS, read replicas |
| 8. Encryption at rest | Disk and backup encryption |
| 9. Monitoring & audit | Log and alert on connections |
| 10. Admin vs app access | Separate human and service access |

---

## 1. Network isolation

Keep the database off the public internet and reachable only from trusted hosts.

| Approach | What it does |
|----------|--------------|
| Private subnet / VPC | DB has only a private IP inside your cloud network |
| Security groups / firewall | Allow inbound DB port (e.g. 5432) only from app servers |
| No public IP | Disable public accessibility on managed DB (RDS, Cloud SQL) |
| PrivateLink / VPC peering | Private connectivity without exposing DB to the internet |
| Separate DB subnet | App tier and DB tier in different subnets |

**Goal:** Even if credentials leak, the DB is not reachable from the outside.

---

## 2. Encryption in transit (TLS/SSL)

| Approach | What it does |
|----------|--------------|
| Require SSL/TLS | `sslmode=require` or `verify-full` (PostgreSQL) |
| Verify server certificate | Prevent man-in-the-middle attacks |
| Mutual TLS (mTLS) | Client presents a cert; DB verifies client identity |
| TLS 1.2+ only | Disable old protocols and weak ciphers |

Example connection string:

```
postgresql://user:pass@db-host:5432/mydb?sslmode=verify-full
```

---

## 3. Authentication

| Approach | What it does |
|----------|--------------|
| Dedicated DB user per service | Never use `postgres` / admin for apps |
| Least privilege | Grant only needed tables and operations |
| Strong passwords | Long, random; stored in a secret manager |
| IAM / identity-based auth | AWS RDS IAM, Azure AD, GCP Cloud SQL IAM |
| Certificate-based client auth | Client cert required to connect |
| Credential rotation | Rotate passwords and keys on a schedule |
| Short-lived credentials | Tokens that expire (Vault dynamic secrets, IAM auth tokens) |

**Principle:** One service = one DB role, with minimal permissions.

---

## 4. Secrets management

| Approach | What it does |
|----------|--------------|
| Secret manager | AWS Secrets Manager, HashiCorp Vault, Azure Key Vault |
| Runtime injection | Env vars injected at deploy time, not baked into images |
| No secrets in git | Never commit `.env` or connection strings |
| Automatic rotation | Secret manager rotates DB password and updates the app |
| Dynamic secrets | Vault creates a new DB user/password per request |

Instead of hardcoded credentials:

```
Hardcoded password in .env → Database
```

A secret manager gives you:

```
Service identity → secret manager → short-lived credentials → Database
```

See the dedicated guides for each production connection approach:

| # | Approach | Guide |
|---|----------|-------|
| 3 | HashiCorp Vault (dynamic creds) | [03-hcv-vault.md](03-hcv-vault.md) |
| 4 | AWS IAM + RDS Proxy | [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) |
| 5 | Secret manager + static password | [05-secret-manager-password.md](05-secret-manager-password.md) |
| 6 | Direct RDS IAM (no Proxy) | [06-direct-rds-iam.md](06-direct-rds-iam.md) |
| 7 | GCP Cloud SQL identity | [07-gcp-cloud-sql-identity.md](07-gcp-cloud-sql-identity.md) |
| 8 | Azure Database identity | [08-azure-database-identity.md](08-azure-database-identity.md) |
| 9 | PgBouncer + secret | [09-pgbouncer-proxy-password.md](09-pgbouncer-proxy-password.md) |
| 10 | mTLS (client certificates) | [10-mtls-client-certs.md](10-mtls-client-certs.md) |
| 11 | PaaS / platform-managed DB | [11-paas-managed-db.md](11-paas-managed-db.md) |

**Quick comparison:**

| Approach | Short-lived creds? | Typical complexity | Best when |
|----------|-------------------|-------------------|-----------|
| Secret manager + password | No (rotated password) | Low | Default starting point |
| Vault dynamic creds | Yes (temp DB user) | High | Multi-cloud, strict audit |
| AWS IAM + RDS Proxy | Yes (IAM token) | Medium | All-in on AWS, high concurrency |
| Direct RDS IAM | Yes (IAM token) | Medium | AWS, smaller connection count |
| GCP / Azure identity | Yes (cloud token) | Medium | All-in on GCP or Azure |
| PgBouncer + secret | No | Low–medium | Self-hosted Postgres at scale |
| mTLS | Cert expiry | High | Zero-trust, PKI in place |
| PaaS connection string | Usually no | Very low | MVP / small apps |

---

## Choosing a connection approach

Full decision flowchart, scenario table, migration path, and pattern comparison → **[§13 Decision guide](13-decision-guide.md)**.

Quick picks:

| Situation | Start with |
|-----------|------------|
| MVP / prototype | [§11 PaaS](11-paas-managed-db.md) |
| First cloud production | [§5 Secret manager + password](05-secret-manager-password.md) |
| AWS scale / Lambda bursts | [§4 IAM + RDS Proxy](04-aws-iam-rds-proxy.md) |
| Self-hosted at high connection count | [§9 PgBouncer + secret](09-pgbouncer-proxy-password.md) |
| Multi-cloud / strict audit | [§3 Vault](03-hcv-vault.md) |

---

## 5. Connection proxy / pooler

| Tool | What it does |
|------|--------------|
| PgBouncer | Connection pooling between app and DB |
| RDS Proxy / Cloud SQL Auth Proxy | Managed proxy with TLS and auth handling |
| Credential brokering | App authenticates to proxy; proxy uses DB credentials |

---

## 6. Workload / cloud identity

| Approach | What it does |
|----------|--------------|
| K8s service account → IAM role | Pod assumes cloud role, gets DB token |
| AWS RDS IAM authentication | App uses AWS SDK for a short-lived auth token |
| GCP Workload Identity | GKE pod → GCP SA → Cloud SQL |
| Azure Managed Identity | App Service / AKS pod gets token for Azure Database |

**Benefit:** No long-lived DB password stored in the application.

---

## 7. Application-level protections

| Approach | What it does |
|----------|--------------|
| Parameterized queries / ORM | Prevent SQL injection |
| Read-only DB user | Read paths use a read-only role |
| Read replicas | Writes to primary; reads from replica |
| Row-Level Security (RLS) | Postgres policies restrict rows per tenant |
| Connection timeouts and limits | Avoid connection exhaustion |

---

## 8. Encryption at rest

| Approach | What it does |
|----------|--------------|
| Volume/disk encryption | EBS, managed DB encryption |
| Encrypted backups | Backups encrypted with KMS-managed keys |
| Customer-managed keys (CMK) | You control encryption keys |

---

## 9. Monitoring and audit

| Approach | What it does |
|----------|--------------|
| Connection logging | Log who connected, when, and from where |
| Audit extensions | `pg_audit`, cloud audit logs |
| Failed login alerts | Alert on brute-force or auth failures |
| SIEM integration | CloudWatch, Datadog, Splunk |

---

## 10. Admin vs app access

| Approach | What it does |
|----------|--------------|
| App connects from private network | TLS + least-privilege user |
| Humans use bastion / VPN | Admins never expose DB publicly |
| Break-glass accounts | Emergency admin access, heavily audited |

Apps and humans should **not** share the same DB credentials.

---

## Recommended production baseline

1. DB in a **private subnet**, no public IP
2. **Security group** allows only app servers on the DB port
3. **TLS required** (`verify-full`)
4. **One DB user per service**, least privilege
5. Credentials in a **secret manager**, rotated regularly
6. **Connection proxy** at scale (optional but recommended)
7. **Audit logs + alerts** on failed connections
8. **Encryption at rest** enabled

Minimum stack:

```
Private subnet → TLS required → Least-privilege user → Secret manager → Audit logs
```

With Vault:

```
Private subnet → TLS → Vault dynamic creds → Postgres → Vault revokes after TTL
```

With AWS IAM + RDS Proxy:

```
Private subnet → TLS → IAM token → RDS Proxy → RDS
```

---

## Quick reference

| Method | Protects against |
|--------|------------------|
| Private network | Internet attackers |
| Firewall / security group | Unauthorized hosts |
| TLS | Eavesdropping / MITM |
| mTLS | Stolen credentials from wrong host |
| Least-privilege DB user | Over-permissioned compromise |
| Secret manager | Leaked code or config |
| Vault dynamic secrets | Long-lived password theft |
| IAM auth | Long-lived password theft |
| Proxy | Credential sprawl, connection storms |
| Audit logs | Undetected breach |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Public RDS endpoint for convenience | Private subnet; no public IP |
| `sslmode=prefer` or disabled SSL | `require` or `verify-full` in production |
| Shared `postgres` superuser for apps | One least-privilege role per service |
| Password in git, Docker layer, or `.env` | Secret manager or IAM auth |
| Skip proxy at high replica count | [§4 RDS Proxy](04-aws-iam-rds-proxy.md) or [§9 PgBouncer](09-pgbouncer-proxy-password.md) |
| No failed-login or connection alerts | CloudWatch / SIEM on auth failures |

---

## Local dev vs production

| | Local (Homebrew Postgres) | Production |
|--|---------------------------|------------|
| Auth | `trust` — no password | TLS + short-lived credentials |
| Credentials | macOS username, no password | Vault, IAM token, or secret manager |
| Auto-start | Manual (`pg-start`) | Managed by orchestrator |
| Secret storage | Not needed locally | Vault, Secrets Manager, or IAM |

---

# HashiCorp Vault (HCV)

> **HCV** = **H**ashi**C**orp **V**ault — a secrets management platform for securing service-to-database connections in production.

> **Related:** AWS-native alternative → [§4 AWS IAM + RDS Proxy](04-aws-iam-rds-proxy.md) · Pooling at scale → [§9 PgBouncer + secret](09-pgbouncer-proxy-password.md) · Decision guide → [§13 Decision guide](13-decision-guide.md)

Vault helps you:

1. **Store** DB credentials securely
2. **Issue short-lived credentials** on demand
3. **Rotate** credentials automatically
4. **Control which services** can access the database

---

## Vault patterns for databases

### 1. Static secrets (KV engine)

Store a fixed connection string or password in Vault.

```
App → authenticates to Vault → reads secret → connects to DB
```

| | |
|---|---|
| **Good for** | Simple setups, legacy apps |
| **Limitation** | Still a long-lived password (just not in source code) |

---

### 2. Dynamic database credentials ⭐ (best Vault feature)

Vault's **Database Secrets Engine** creates a **temporary DB user** for each request.

```
1. App starts
2. App authenticates to Vault (K8s SA / IAM / AppRole)
3. Vault creates DB user: v-token-abc123  (TTL: 1 hour)
4. App connects with that user
5. After TTL expires, Vault revokes the user automatically
```

Example:

```bash
vault read database/creds/my-app-role
```

Response:

```json
{
  "username": "v-root-my-app-xYz9",
  "password": "Abc123-random",
  "lease_duration": 3600
}
```

| Benefit | Description |
|---------|-------------|
| No long-lived password | Credentials expire automatically |
| Per-service creds | Each service/instance gets its own user |
| Auto-revocation | Vault deletes the DB user after TTL |
| Audit trail | Every secret access is logged |

---

### 3. Credential rotation

Vault can rotate the **master/admin DB password** (used only by Vault to create dynamic users) without redeploying applications.

---

## How apps authenticate to Vault

Before Vault gives DB credentials, the service must prove its identity:

| Auth method | Typical use |
|-------------|-------------|
| **Kubernetes auth** | Pods use service account JWT |
| **AWS IAM auth** | EC2 / ECS / Lambda uses IAM role |
| **AppRole** | VMs and custom apps with `role_id` + `secret_id` |
| **JWT / OIDC** | Cloud-native workloads |

---

## Common Vault deployment patterns

### Sidecar / Vault Agent

```
[App container]  +  [Vault Agent sidecar]
```

Vault Agent authenticates to Vault, fetches/renews DB credentials, and writes them to a shared file for the app.

### Init container (Kubernetes)

An init container fetches credentials before the main app container starts.

### Direct SDK / API

The app calls the Vault API at startup and again before credentials expire.

---

## What Vault protects against

| Threat | How Vault helps |
|--------|-----------------|
| Password in git or `.env` | Credentials come from Vault at runtime |
| Stolen long-lived password | Dynamic credentials expire quickly |
| Over-shared DB user | One Vault role per service |
| No audit trail | Vault logs every secret access |
| Manual rotation pain | Automated rotation |

---

## Vault vs cloud secret managers

| | HashiCorp Vault | AWS Secrets Manager / similar |
|--|-----------------|-------------------------------|
| Dynamic DB users | ✅ Native DB engine | ⚠️ Limited / varies |
| Multi-cloud | ✅ Yes | ❌ Cloud-specific |
| Complexity | Higher | Lower |
| Identity-based access | Very flexible | Tied to cloud IAM |
| Best for | Multi-service, multi-cloud, strict security | AWS-native, simpler apps |

---

## Example production setup with Vault

```
┌─────────────┐   K8s/IAM auth   ┌──────────────────┐
│  App Service │ ──────────────► │ HashiCorp Vault  │
└──────┬──────┘                  └────────┬─────────┘
       │                                  │ CREATE USER (temp, 1h TTL)
       │ TLS + temp credentials           ▼
       └────────────────────────► ┌──────────────────┐
                                  │   PostgreSQL     │
                                  └──────────────────┘
                                           ▲
                                           │ REVOKE after TTL
                                  ┌────────┴─────────┐
                                  │ HashiCorp Vault  │
                                  └──────────────────┘
```

Steps:

1. Postgres in a **private subnet**
2. **TLS required** for all DB connections
3. Vault holds a **DB admin role** (used only by Vault, never by apps)
4. Each app gets its own **Vault role** (`api-service`, `worker-service`, etc.)
5. App pod uses **Kubernetes auth** to reach Vault
6. Vault issues **1-hour dynamic credentials**
7. App connects to Postgres with those credentials
8. Vault **revokes** the DB user after TTL expires

---

## When to use Vault

### ✅ Use Vault if

- Many services connect to the same database
- You want short-lived, auto-revoked DB credentials
- You need strong audit trails and compliance
- You run multi-cloud or hybrid infrastructure

### ⏭️ Skip Vault (for now) if

- Small app with one service and one database
- Fully on AWS and **IAM auth + RDS Proxy** is sufficient — see [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md)
- Your team cannot operate Vault reliably (it requires ongoing care)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Vault on day one for one small service | Start [§5 Secret manager](05-secret-manager-password.md) |
| Dynamic creds without connection pooling | Pair with [§9 PgBouncer](09-pgbouncer-proxy-password.md) or [§4 RDS Proxy](04-aws-iam-rds-proxy.md) |
| Vault Agent sidecar without renewal testing | Test credential expiry and app reconnect paths |
| Single Vault role shared by all services | One Vault role per service |
| No audit review of secret access | Enable and monitor Vault audit logs |

---

# AWS IAM auth + RDS Proxy

> AWS-native path for the same goals as Vault — no DB password in code, short-lived credentials, least privilege — without running HashiCorp Vault.

> **Related:** Direct RDS without Proxy → [§6 Direct RDS IAM](06-direct-rds-iam.md) · Vault comparison → [§3 HashiCorp Vault](03-hcv-vault.md) · Pool tuning → [postgresql-performance §7](../postgresql-performance/includes/07-connection-management.md)

## What it solves

- No DB password in `.env`, git, or container images
- Short-lived credentials (IAM auth tokens expire in ~15 minutes)
- Least privilege via IAM policies (`rds-db:connect` scoped to specific DB users)
- Connection pooling and fewer open connections to RDS (via RDS Proxy)

It is **AWS-managed** — no Vault cluster to run — but **AWS-specific** and less flexible than Vault for multi-cloud or per-request dynamic DB users.

---

## Architecture

```
App (EC2 / ECS / Lambda / EKS)
  │
  │ 1. Assume IAM role (instance profile, task role, IRSA)
  │ 2. aws rds generate-db-auth-token
  │ 3. TLS connect — token used as password
  ▼
RDS Proxy  ── pool + authenticate ──►  RDS (PostgreSQL / MySQL / Aurora)
         ▲
         └── private subnet; app connects to proxy endpoint, not RDS directly
```

**Minimum production stack:**

```
Private subnet → TLS → RDS Proxy → RDS
                    ↑
              IAM auth token (no static password)
```

---

## Two IAM + Proxy patterns

### Pattern A: Standard IAM auth (most common)

| Hop | Who authenticates | How |
|-----|-------------------|-----|
| App → RDS Proxy | App via **IAM** | App calls `aws rds generate-db-auth-token`; token is used as the DB **password** |
| RDS Proxy → RDS | Proxy via **Secrets Manager** | Proxy reads stored username/password for the DB user |

Setup:

1. Enable IAM auth on the RDS instance/cluster (`--enable-iam-database-authentication`).
2. Create a **database user** mapped for IAM auth (PostgreSQL: `GRANT rds_iam TO app_user`).
3. Attach an IAM policy to the app's role allowing `rds-db:connect` for that DB user ARN.
4. Configure RDS Proxy with **Secrets Manager** credentials for the backend DB login.
5. Apps connect **through the proxy endpoint**, not directly to RDS.

**Flow:**

1. App runs with an IAM role (EC2 instance profile, ECS task role, Lambda execution role, or EKS IRSA).
2. App generates a token:

```bash
aws rds generate-db-auth-token \
  --hostname my-proxy.proxy-abc123.us-east-1.rds.amazonaws.com \
  --port 5432 \
  --username app_user \
  --region us-east-1
```

3. App opens a TLS connection to the **proxy endpoint** — username = DB user, password = token.
4. Proxy validates IAM auth, pools the connection, and connects to RDS using Secrets Manager credentials.

---

### Pattern B: End-to-end IAM auth

| Hop | Who authenticates | How |
|-----|-------------------|-----|
| App → RDS Proxy | App via **IAM** | Same token generation |
| RDS Proxy → RDS | Proxy via **IAM** | Proxy's IAM role has `rds-db:connect`; no Secrets Manager DB password needed |

- Proxy is configured with IAM as the default auth scheme.
- Proxy's IAM role gets `rds-db:connect` for target DB users.
- Eliminates storing DB passwords in Secrets Manager for proxy-to-DB hops.
- Stronger, but more IAM wiring; both app role and proxy role need correct `rds-db:connect` grants.

---

## Key components

1. **RDS** — PostgreSQL or MySQL/Aurora; IAM auth enabled; private subnet; no public IP; TLS required.
2. **Database user** — Dedicated per service; granted `rds_iam` (Postgres) or equivalent; least-privilege on schemas/tables.
3. **IAM policy on app role** — Allow `rds-db:connect` only for that user's ARN:

```json
{
  "Effect": "Allow",
  "Action": "rds-db:connect",
  "Resource": "arn:aws:rds-db:us-east-1:ACCOUNT_ID:dbuser:DB_RESOURCE_ID/app_user"
}
```

4. **RDS Proxy** — Same VPC/subnets as app; security group allows app tier → proxy only; proxy target = RDS cluster/instance.
5. **Secrets Manager** (Pattern A) — Stores DB credentials the proxy uses to reach RDS; proxy IAM role can read that secret.
6. **App code** — Generate token before connect (or refresh before ~15 min expiry); use proxy hostname, not RDS hostname.

Example connect:

```bash
export PGPASSWORD=$(aws rds generate-db-auth-token \
  --hostname my-proxy.proxy-abc123.us-east-1.rds.amazonaws.com \
  --port 5432 \
  --username app_user \
  --region us-east-1)

psql "host=my-proxy.proxy-abc123.us-east-1.rds.amazonaws.com port=5432 dbname=mydb user=app_user sslmode=require"
```

---

## How this maps to security layers

| Layer | IAM + RDS Proxy coverage |
|-------|--------------------------|
| 1. Network isolation | RDS + Proxy in private subnets; SG: app → proxy → RDS only |
| 2. TLS | Required for IAM auth connections |
| 3. Authentication | IAM token + dedicated DB user per service |
| 4. Secrets management | No app-side password; Pattern A still uses Secrets Manager for proxy→RDS |
| 5. Connection proxy | RDS Proxy handles pooling and multiplexing |
| 6. Workload identity | EC2/ECS/Lambda/EKS IAM roles — native AWS identity |
| 9. Monitoring | CloudWatch, RDS logs, IAM CloudTrail for `rds-db:connect` |

---

## IAM + RDS Proxy vs HashiCorp Vault

| | IAM + RDS Proxy | Vault dynamic DB creds |
|--|-----------------|------------------------|
| Credential type | IAM auth **token** (password field); DB user is **fixed** | New **DB user/password** per lease |
| Scope | AWS only | Multi-cloud |
| Ops burden | Low (managed AWS) | High (run/maintain Vault) |
| Per-instance users | Same DB user; identity is IAM role | Unique temp DB user per request |
| Proxy/pooling | Built into RDS Proxy | You add PgBouncer or connect direct |

See [03-hcv-vault.md](03-hcv-vault.md) for the Vault approach.

---

## When IAM + RDS Proxy is sufficient

Use this instead of Vault when:

- Everything runs on AWS (EC2, ECS, Lambda, EKS with IRSA)
- One or a few services share RDS
- You want short-lived auth without operating Vault
- RDS Proxy connection pooling is enough for your scale
- AWS IAM + CloudTrail audit meets compliance needs

Consider Vault (or Pattern B + stricter IAM) when:

- Multi-cloud or on-prem workloads also need DB access
- You need **unique temporary DB users** per session/instance
- You want centralized secrets across non-AWS systems
- You need Vault-style dynamic user revocation independent of IAM token TTL

## Common mistakes

| Mistake | Fix |
|---------|-----|
| IAM auth but connect directly to RDS at scale | Use Proxy endpoint; see connection count limits |
| Token generated for RDS hostname, connect to Proxy | `generate-db-auth-token` hostname must match connect target |
| Missing `GRANT rds_iam` on DB user | Enable IAM auth on PostgreSQL role |
| Over-broad `rds-db:connect` IAM policy | Scope to specific DB user ARN per service |
| Token not refreshed before ~15 min expiry | Refresh on connect or background renewal loop |

---

# Secret manager + static password

> The most common production baseline — store a DB username/password in a cloud secret manager and inject it at runtime. No credentials in git or container images.

> **Related:** Upgrade path → [§4 IAM + RDS Proxy](04-aws-iam-rds-proxy.md) · Self-hosted pooling → [§9 PgBouncer + secret](09-pgbouncer-proxy-password.md) · Rotation runbook → [§12 Credential rotation and DR](12-credential-rotation-and-dr.md)

## What it solves

- Removes passwords from source code, `.env` files committed to git, and Docker image layers
- Central place to rotate and audit database credentials
- Works with **any** database engine and **any** cloud or on-prem deployment
- Simple for teams starting production without Vault or IAM auth

## What it does not solve

- Credentials are still **long-lived** (until rotated) — not per-request dynamic users
- If a secret leaks, it works until rotation
- App must handle rotation events (restart, reload, or polling)

---

## Architecture

```
App (EC2 / ECS / Lambda / K8s / VM)
  │
  │ 1. Assume IAM role / managed identity / K8s SA (to read secret)
  │ 2. Fetch secret at startup (or on interval)
  │ 3. TLS connect with username + password
  ▼
Database (RDS / Cloud SQL / self-hosted Postgres)
```

**Minimum stack:**

```
Private subnet → TLS → least-privilege DB user → password from secret manager
```

---

## Cloud secret managers

| Platform | Service | Typical fetch |
|----------|---------|---------------|
| AWS | Secrets Manager | SDK / env from ECS task definition / Lambda extension |
| GCP | Secret Manager | SDK / Workload Identity |
| Azure | Key Vault | SDK / Managed Identity |
| HashiCorp | Vault KV engine | Vault Agent or API — see [03-hcv-vault.md](03-hcv-vault.md) |

---

## Setup steps

1. **RDS / managed DB** in a private subnet; TLS required; no public IP.
2. **Dedicated DB user** per service with least privilege (not `postgres` admin).
3. **Store credentials** in the secret manager as JSON or connection string:

```json
{
  "username": "api_service",
  "password": "long-random-password",
  "host": "mydb.abc123.us-east-1.rds.amazonaws.com",
  "port": 5432,
  "dbname": "myapp"
}
```

4. **Grant app identity** read access to that secret only (IAM policy, Key Vault access policy, etc.).
5. **Inject at runtime** — env vars, mounted file, or SDK fetch on startup.
6. **Enable automatic rotation** (optional) — secret manager rotates password and updates the secret; app must reconnect or restart.

---

## Deployment patterns

### ECS / Lambda (AWS)

Task definition or Lambda env references Secrets Manager ARN; AWS injects at launch.

### Kubernetes (External Secrets Operator)

```
External Secrets Operator → syncs from AWS/GCP/Azure → K8s Secret → pod env
```

Pod never embeds the password in the Deployment YAML — only references the K8s Secret name.

### VM / bare metal

App calls secret manager API at startup using instance profile or service account.

---

## Example: fetch and connect (AWS)

```bash
# CLI example — apps use SDK in production
aws secretsmanager get-secret-value \
  --secret-id prod/myapp/db \
  --query SecretString --output text
```

```bash
# Connect after parsing username/password
psql "host=$DB_HOST port=5432 dbname=myapp user=$DB_USER sslmode=verify-full"
# PGPASSWORD set from secret, never hardcoded
```

---

## How this maps to security layers

| Layer | Coverage |
|-------|----------|
| 1. Network isolation | DB in private subnet; SG allows app tier only |
| 2. TLS | Required (`sslmode=verify-full`) |
| 3. Authentication | Dedicated DB user, least privilege |
| 4. Secrets management | Password in secret manager, not in code |
| 9. Monitoring | Secret access logged in CloudTrail / audit logs |

---

## Comparison with other approaches

| | Secret manager + password | Vault dynamic | AWS IAM + RDS Proxy |
|--|---------------------------|---------------|---------------------|
| Short-lived creds | No (rotated password) | Yes (temp DB user) | Yes (IAM token) |
| Complexity | Low | High | Medium |
| Works everywhere | Yes | Yes | AWS only |

---

## When to use

**Use when:**

- Starting production and need a secure, simple path
- Any cloud or self-hosted Postgres/MySQL
- Team does not want to operate Vault or IAM auth yet

**Upgrade when:**

- You need short-lived credentials → [03-hcv-vault.md](03-hcv-vault.md) or [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md)
- Connection storms at scale → add [09-pgbouncer-proxy-password.md](09-pgbouncer-proxy-password.md)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| One secret shared by all microservices | One secret (and DB user) per service |
| Rotate password without dual-active window | Issue new cred alongside old → [§12](12-credential-rotation-and-dr.md) |
| Fetch secret once at startup, never reload | Poll or restart on rotation event |
| Secret in container image env at build time | Runtime injection via task role / sidecar |
| No TLS despite secret manager | Private subnet + `sslmode=verify-full` |

---

# Direct RDS IAM auth (no RDS Proxy)

> App connects to RDS using an IAM auth token as the password — same token model as [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md), but **without** RDS Proxy in the path.

> **Related:** When to add Proxy → [§4 AWS IAM + RDS Proxy](04-aws-iam-rds-proxy.md) · App-side pooling → [§9 PgBouncer + secret](09-pgbouncer-proxy-password.md) · `max_connections` → [postgresql-performance §7](../postgresql-performance/includes/07-connection-management.md)

## What it solves

- No long-lived DB password in the application
- Short-lived IAM auth tokens (~15 minute expiry)
- Least privilege via `rds-db:connect` IAM policies
- Fewer components than Proxy — good for smaller AWS workloads

## What it does not solve

- **No managed connection pooling** — you handle pool limits (app pool, PgBouncer, or accept RDS connection limits)
- AWS-only
- Fixed DB user per service (not unique temp users like Vault dynamic creds)

---

## Architecture

```
App (EC2 / ECS / Lambda / EKS)
  │
  │ 1. Assume IAM role
  │ 2. aws rds generate-db-auth-token (hostname = RDS endpoint)
  │ 3. TLS connect — token as password
  ▼
RDS (PostgreSQL / MySQL / Aurora)   ← direct, no proxy
```

**Stack:**

```
Private subnet → TLS → IAM token → RDS
```

Compare with Proxy:

```
Private subnet → TLS → IAM token → RDS Proxy → RDS   (see 04-aws-iam-rds-proxy.md)
```

---

## Setup steps

1. **Enable IAM auth** on the RDS instance or Aurora cluster:

```bash
aws rds modify-db-instance \
  --db-instance-identifier mydb \
  --enable-iam-database-authentication \
  --apply-immediately
```

2. **Create DB user** and grant IAM auth (PostgreSQL):

```sql
CREATE USER app_user;
GRANT rds_iam TO app_user;
GRANT CONNECT ON DATABASE myapp TO app_user;
-- least-privilege grants on schemas/tables
```

3. **IAM policy** on the app's role:

```json
{
  "Effect": "Allow",
  "Action": "rds-db:connect",
  "Resource": "arn:aws:rds-db:us-east-1:ACCOUNT_ID:dbuser:DB_RESOURCE_ID/app_user"
}
```

4. **App generates token** using the **RDS endpoint** (not a proxy hostname):

```bash
export PGPASSWORD=$(aws rds generate-db-auth-token \
  --hostname mydb.abc123.us-east-1.rds.amazonaws.com \
  --port 5432 \
  --username app_user \
  --region us-east-1)

psql "host=mydb.abc123.us-east-1.rds.amazonaws.com port=5432 dbname=myapp user=app_user sslmode=require"
```

5. **Refresh token** before expiry on long-lived connections or reconnect per request.

---

## Direct IAM vs RDS Proxy

| | Direct RDS IAM | IAM + RDS Proxy |
|--|----------------|-----------------|
| Components | App + RDS | App + Proxy + RDS |
| Connection pooling | App or PgBouncer | Built into Proxy |
| Failover handling | App reconnect logic | Proxy handles some failover |
| Best for | Low–medium connection count | Many Lambdas, high concurrency |
| Token hostname | RDS endpoint | Proxy endpoint |

---

## How this maps to security layers

| Layer | Coverage |
|-------|----------|
| 1. Network isolation | RDS in private subnet |
| 2. TLS | Required for IAM auth |
| 3. Authentication | IAM token + dedicated DB user |
| 4. Secrets management | No static app password |
| 6. Workload identity | EC2/ECS/Lambda/EKS IAM roles |

---

## When to use

**Use direct IAM when:**

- All-in on AWS
- Connection count is manageable without Proxy
- You want IAM tokens without Proxy cost/complexity

**Add RDS Proxy when:**

- Lambda bursts open many connections
- You hit RDS `max_connections` limits
- See [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md)

**Consider Vault when:**

- Multi-cloud or unique temp DB users per lease — see [03-hcv-vault.md](03-hcv-vault.md)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Lambda/K8s burst without Proxy | [§4 RDS Proxy](04-aws-iam-rds-proxy.md) |
| App pool size × replicas > `max_connections` | PgBouncer or RDS Proxy |
| Stale IAM token after 15 minutes | Regenerate before connect |
| Same DB user for every service | Separate users + scoped IAM policies |
| Skip TLS because IAM replaces password | TLS still required for IAM auth |

---

# GCP Cloud SQL identity

> Connect to Cloud SQL (PostgreSQL / MySQL) using GCP-native identity, proxies, and Secret Manager — the GCP equivalent of AWS IAM + RDS patterns.

> **Related:** AWS equivalents → [§4 IAM + RDS Proxy](04-aws-iam-rds-proxy.md), [§6 Direct RDS IAM](06-direct-rds-iam.md) · Static secret baseline → [§5 Secret manager](05-secret-manager-password.md) · Decision guide → [§13 Decision guide](13-decision-guide.md)

## What it solves

- No DB password in application code (when using IAM / Workload Identity)
- Encrypted connections via Cloud SQL Auth Proxy or connector libraries
- Integration with GKE Workload Identity and GCP service accounts
- Private connectivity without exposing the DB to the public internet

---

## Three main patterns

### Pattern A: Cloud SQL Auth Proxy (sidecar or daemon)

```
App → localhost:5432 → Auth Proxy → Cloud SQL instance
              ↑
        Proxy handles TLS + authentication to Cloud SQL
```

The **Cloud SQL Auth Proxy** (or **Cloud SQL Connector** in app code) runs as:

- Sidecar container in GKE / Cloud Run
- Local daemon on a VM
- Embedded via language connectors (Go, Java, Python)

App connects to `127.0.0.1:5432`; the proxy authenticates to Cloud SQL using the pod/VM's GCP credentials.

**Setup:**

1. Cloud SQL instance with **private IP** (VPC) or authorized networks restricted.
2. Enable **Cloud SQL Admin API**.
3. Grant the app's service account `roles/cloudsql.client`.
4. Run proxy with instance connection name: `project:region:instance`.

```bash
cloud-sql-proxy project:region:my-instance --port 5432
```

5. App connects with DB user/password **or** IAM database auth (see Pattern B).

---

### Pattern B: IAM database authentication

Cloud SQL supports **IAM users** as database principals (PostgreSQL and MySQL).

```
GKE pod → Workload Identity → GCP SA → IAM token → Cloud SQL
```

**Setup:**

1. Enable IAM DB auth on the Cloud SQL instance.
2. Add IAM user in Cloud SQL (e.g. `service-account@project.iam`).
3. Bind GKE **Workload Identity**: K8s SA → GCP SA.
4. Grant GCP SA `roles/cloudsql.instanceUser` and `roles/cloudsql.client`.
5. App uses Cloud SQL Connector with automatic IAM auth — no password in env.

**Benefit:** Same philosophy as AWS RDS IAM — identity-based, no long-lived password.

---

### Pattern C: Secret Manager + static password

Same as [05-secret-manager-password.md](05-secret-manager-password.md), using **GCP Secret Manager**:

```
App → fetch secret (Workload Identity) → TLS → Cloud SQL
```

Common when IAM DB auth is not enabled or for legacy apps.

---

## Architecture comparison

| Pattern | Short-lived creds | Pooling | Complexity |
|---------|-------------------|---------|------------|
| Auth Proxy + password | No | Via app / PgBouncer | Low |
| Auth Proxy + IAM auth | Yes (IAM token) | Via app / PgBouncer | Medium |
| Secret Manager + password | No (rotated) | Via app | Low |

---

## How this maps to security layers

| Layer | Coverage |
|-------|----------|
| 1. Network isolation | Private IP / VPC peering; no public IP |
| 2. TLS | Proxy or connector enforces encryption |
| 3. Authentication | IAM DB user or dedicated SQL user |
| 4. Secrets management | Secret Manager or IAM (no app password) |
| 6. Workload identity | GKE Workload Identity → GCP SA |

---

## GCP vs AWS equivalents

| GCP | AWS equivalent |
|-----|----------------|
| Cloud SQL Auth Proxy | RDS Proxy / direct connect |
| IAM DB auth on Cloud SQL | RDS IAM auth |
| Secret Manager | Secrets Manager |
| Workload Identity | EKS IRSA |

See [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) and [06-direct-rds-iam.md](06-direct-rds-iam.md) for AWS detail.

---

## When to use

**Use Cloud SQL Auth Proxy when:**

- Running on GKE, Cloud Run, or GCE
- You want Google-managed TLS and auth to Cloud SQL

**Use IAM DB auth when:**

- No static passwords; GKE Workload Identity is in place

**Use Secret Manager + password when:**

- Simplest migration path from dev — see [05-secret-manager-password.md](05-secret-manager-password.md)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Public IP on Cloud SQL for app convenience | Private IP + Auth Proxy |
| Missing `roles/cloudsql.client` on service account | Grant before deploy |
| Auth Proxy not colocated with app | Sidecar on GKE / daemon on VM |
| Workload Identity not wired on GKE | Bind K8s SA → GCP SA |
| IAM DB auth without testing token refresh | Same ~hourly token expiry patterns as AWS |

---

# Azure Database identity

> Connect to Azure Database for PostgreSQL / MySQL using Managed Identity and Azure AD — no DB password stored in the application.

> **Related:** Static secrets via Key Vault → [§5 Secret manager + password](05-secret-manager-password.md) · AWS comparison → [§4](04-aws-iam-rds-proxy.md), [§6](06-direct-rds-iam.md) · Decision guide → [§13 Decision guide](13-decision-guide.md)

## What it solves

- Passwordless or centrally managed authentication for Azure-hosted apps
- Integration with **Azure App Service**, **AKS**, **Azure Functions**, and VMs
- Azure Key Vault for static secrets when IAM-style auth is not used
- TLS to Azure Database endpoints

---

## Three main patterns

### Pattern A: Azure AD authentication (Microsoft Entra ID)

Azure Database for PostgreSQL (Flexible Server) supports **Azure AD authentication** — the database accepts tokens from Azure AD principals.

```
App Service / AKS pod → Managed Identity → Azure AD token → Azure PostgreSQL
```

**Setup:**

1. Enable Azure AD auth on the PostgreSQL flexible server.
2. Create an **Azure AD admin** on the server.
3. Assign the app's **Managed Identity** as an Azure AD user in PostgreSQL.
4. App acquires token via `DefaultAzureCredential` (or MSI endpoint).
5. Connect using token as password (similar model to AWS IAM auth tokens).

**Benefit:** No long-lived SQL password in config; identity is the Azure AD principal.

---

### Pattern B: Managed Identity + Key Vault (static secret)

```
App → Managed Identity → Key Vault → username/password → TLS → Azure Database
```

Same model as [05-secret-manager-password.md](05-secret-manager-password.md):

1. Store DB credentials in **Key Vault**.
2. Grant app's Managed Identity `get` on secrets.
3. Fetch at startup; connect with TLS.

**Use when:** Azure AD DB auth is not configured or app/driver lacks token support.

---

### Pattern C: AKS + workload identity

For Kubernetes on Azure (**AKS**):

```
Pod → Workload Identity → Azure AD / Key Vault → Database
```

- **Workload Identity** federates K8s service account to Azure Managed Identity.
- Same patterns as A or B, but credentials flow through the pod's federated identity.

---

## Architecture

```
┌─────────────────┐     token or secret     ┌──────────────────┐
│  App Service    │ ─────────────────────► │ Azure PostgreSQL │
│  or AKS pod     │      over TLS          │ (Flexible Server)│
└────────┬────────┘                        └──────────────────┘
         │
         ▼
  Managed Identity / Azure AD
```

**Minimum stack:**

```
Private VNet → TLS → Azure AD auth or Key Vault secret → Azure Database
```

---

## How this maps to security layers

| Layer | Coverage |
|-------|----------|
| 1. Network isolation | VNet integration; private access; firewall rules |
| 2. TLS | Required (`sslmode=require`) |
| 3. Authentication | Azure AD principal or dedicated SQL user |
| 4. Secrets management | Key Vault or token-based (no app password) |
| 6. Workload identity | Managed Identity on App Service / AKS |

---

## Azure vs AWS equivalents

| Azure | AWS equivalent |
|-------|----------------|
| Managed Identity | IAM role on EC2/ECS/Lambda |
| Azure AD DB auth | RDS IAM auth |
| Key Vault | Secrets Manager |
| Private VNet access | RDS in private subnet |

See [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) and [06-direct-rds-iam.md](06-direct-rds-iam.md).

---

## When to use

**Use Azure AD authentication when:**

- App runs on App Service, Functions, or AKS with Managed Identity
- You want passwordless DB auth aligned with Entra ID

**Use Key Vault + password when:**

- Drivers or legacy apps need traditional username/password — see [05-secret-manager-password.md](05-secret-manager-password.md)

**Consider Vault when:**

- Multi-cloud secrets and dynamic DB users — see [03-hcv-vault.md](03-hcv-vault.md)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Azure AD auth without creating DB principal | Map Managed Identity to PostgreSQL user |
| Key Vault secret never rotated | Schedule rotation → [§12](12-credential-rotation-and-dr.md) |
| Driver without Azure AD token support | Use supported driver or Pattern B (Key Vault) |
| Public firewall rule `0.0.0.0` | Private VNet / private endpoint |
| Same connection string in dev and prod | Separate secrets per environment |

---

# PgBouncer + secret (proxy + password)

> Connection pooling in front of the database using **PgBouncer** (or similar), with credentials from a secret manager — no IAM or Vault required.

> **Related:** Secret source → [§5 Secret manager + password](05-secret-manager-password.md) · AWS managed proxy → [§4 RDS Proxy](04-aws-iam-rds-proxy.md) · Pool modes and sizing → [postgresql-performance §7](../postgresql-performance/includes/07-connection-management.md)

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

1. **Postgres** in private subnet; TLS; dedicated app users with least privilege.
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

---

# mTLS (client certificate auth)

> The database verifies a **client TLS certificate** instead of (or in addition to) a password — strong binding between identity and connection.

> **Related:** TLS baseline → [§2 Production security](02-prod-db-security.md) · Cert lifecycle in Vault → [§3 HashiCorp Vault](03-hcv-vault.md) · Simpler baseline → [§5 Secret manager](05-secret-manager-password.md)

## What it solves

- No password in the application — the **certificate private key** is the credential
- **Mutual TLS (mTLS)** — both client and server present certs; prevents MITM and stolen-password reuse from wrong hosts
- Useful in zero-trust networks and service-mesh environments
- Works with self-hosted Postgres and cloud DBs that support client cert auth

## What it does not solve

- **Certificate lifecycle** — issue, rotate, revoke, and store private keys securely
- Operational complexity higher than secret manager + password
- Not all managed DB offerings support client cert auth equally

---

## Architecture

```
App                          PostgreSQL
  │                              │
  │──── TLS handshake ──────────►│  server cert (verify server)
  │◄─── server cert ─────────────│
  │                              │
  │──── client cert + key ──────►│  pg_hba: cert authentication
  │                              │
  │──── SQL over encrypted channel│
```

**Stack:**

```
Private subnet → mTLS (client + server certs) → Postgres
                      ↑
               client cert from cert manager / Vault PKI
```

---

## PostgreSQL setup

### 1. Server TLS

Configure Postgres with server certificate (`ssl = on`, `ssl_cert_file`, `ssl_key_file`).

### 2. pg_hba.conf — cert auth

```
hostssl  all  app_user  10.0.0.0/8  cert
```

Or `cert` with `map=` to map certificate CN to database user.

### 3. Client certificate

Issue a client cert (CN or SAN maps to DB role):

```bash
# Connect with client cert — no password
psql "host=db.internal port=5432 dbname=myapp user=app_user \
  sslmode=verify-full \
  sslcert=/path/to/client.crt \
  sslkey=/path/to/client.key \
  sslrootcert=/path/to/ca.crt"
```

### 4. Store private key securely

- K8s Secret (encrypted at rest)
- Vault PKI / cert manager (cert-manager, AWS ACM PCA)
- Never commit `.key` files to git

---

## Certificate management options

| Tool | Role |
|------|------|
| **cert-manager** (K8s) | Auto-issue and renew certs for pods |
| **HashiCorp Vault PKI** | Issue short-lived client certs |
| **AWS ACM Private CA** | Enterprise CA on AWS |
| **Manual OpenSSL** | Dev/small setups only |

Short-lived client certs (hours/days) reduce impact of key compromise — similar benefit to IAM tokens.

---

## mTLS vs password vs IAM

| | mTLS | Password + secret manager | IAM auth |
|--|------|---------------------------|----------|
| Credential | Client cert + key | Password | IAM token |
| Expiry | Cert NotAfter | Rotation schedule | ~15 min token |
| Host binding | Strong (cert required) | Weak (password works anywhere) | Medium (IAM + network) |
| Complexity | High | Low | Medium (AWS) |

---

## How this maps to security layers

| Layer | Coverage |
|-------|----------|
| 1. Network isolation | Still required — cert alone does not hide DB from internet |
| 2. TLS / mTLS | **Core** — client and server certificates |
| 3. Authentication | Certificate CN mapped to DB user |
| 4. Secrets management | Private key in cert store, not in code |

---

## When to use

**Use mTLS when:**

- Zero-trust or service mesh (Istio, Linkerd) already issues workload certs
- Compliance requires certificate-based DB access
- You want to eliminate passwords entirely and control cert TTL

**Avoid as first choice when:**

- Team lacks PKI operations experience
- Managed DB does not support client cert auth well
- [05-secret-manager-password.md](05-secret-manager-password.md) or [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) meets requirements with less ops burden

## Common mistakes

| Mistake | Fix |
|---------|-----|
| mTLS without network isolation | Private subnet first — cert ≠ firewall |
| No cert rotation runbook | Automate issue/revoke; test before expiry |
| Private key in application repo | HSM, cert manager, or Vault PKI |
| `pg_hba.conf` `cert` without CN mapping | Map certificate CN to DB role explicitly |
| mTLS as first prod choice without PKI team | Start [§5](05-secret-manager-password.md) or cloud IAM |

---

# PaaS / platform-managed database

> The platform (Supabase, Neon, Railway, Heroku, PlanetScale, etc.) hosts the database and gives you a **connection string** — credentials managed in the provider dashboard or CI, not in application source code.

> **Related:** Production hardening path → [§5 Secret manager](05-secret-manager-password.md) · When to leave PaaS → [§13 Decision guide](13-decision-guide.md) · Security layers gap → [§2 Production security](02-prod-db-security.md)

## What it solves

- Fastest path from dev to production — no RDS/Vault/proxy setup
- Provider handles backups, patches, scaling, and often TLS
- Connection strings rotatable from the provider UI or API
- Good for MVPs, side projects, and small teams

## What it does not solve

- Less control over network isolation (often public endpoint + IP allowlist or SSL only)
- Shared connection string per environment is common — not per-service IAM
- Vendor lock-in and limited auth models vs self-managed Postgres
- May not meet strict compliance (private subnet, customer-managed keys, etc.)

---

## Architecture

```
App (Vercel / Railway / Fly / local)
  │
  │ connection string from env (set in platform dashboard / CI)
  │ TLS (required by most providers)
  ▼
Provider-managed Postgres (multi-tenant or dedicated)
```

**Typical flow:**

```
Platform dashboard → copy DATABASE_URL → set in deployment env → app connects
```

**Never** commit `DATABASE_URL` to git — use platform secrets / CI variables.

---

## Common providers

| Provider | Notes |
|----------|-------|
| **Supabase** | Postgres + pooler (Supavisor); connection string in project settings |
| **Neon** | Serverless Postgres; pooled and direct connection strings |
| **Railway / Render / Fly** | Managed Postgres add-on; env var injection |
| **Heroku Postgres** | `DATABASE_URL` automatically injected |
| **PlanetScale** | MySQL-compatible; branch-based workflows |
| **Amazon RDS** | Not PaaS-style by default — use [05-secret-manager-password.md](05-secret-manager-password.md) or [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) |

---

## Security practices (still required)

Even with PaaS, follow production basics from [02-prod-db-security.md](02-prod-db-security.md):

1. **TLS** — use `sslmode=require` (Postgres); providers usually enforce SSL.
2. **Secrets in env only** — Vercel/Railway/Render secret stores, not repo.
3. **IP allowlisting** — if provider supports it, restrict to app egress IPs.
4. **Separate databases** per environment (dev/staging/prod) — never share prod URL.
5. **Rotate** connection string after team member offboarding or suspected leak.
6. **Least privilege** — use read-only connection string for read-only services if provider supports multiple roles.

---

## Example

```bash
# Set in platform secrets (not .env committed to git)
export DATABASE_URL="postgresql://user:pass@ep-xxx.region.provider.co:5432/dbname?sslmode=require"
```

```javascript
// Node — pg / Prisma / Drizzle read from process.env
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
```

---

## PaaS vs self-managed production

| | PaaS connection string | Self-managed + secret manager |
|--|------------------------|-------------------------------|
| Setup time | Minutes | Days–weeks |
| Network control | Limited | Full VPC/private subnet |
| IAM / dynamic creds | Rare | Vault, RDS IAM, etc. |
| Compliance | Varies by provider | You own the stack |
| Cost at scale | Can grow quickly | Often cheaper at large scale |

---

## How this maps to security layers

| Layer | PaaS typical coverage |
|-------|------------------------|
| 1. Network isolation | Partial — SSL + allowlist; rarely private VPC |
| 2. TLS | Usually enforced by provider |
| 3. Authentication | Single DB user per connection string |
| 4. Secrets management | Platform env / dashboard — not in git |
| 8. Encryption at rest | Provider-managed |
| 9. Monitoring | Provider dashboards; limited audit |

---

## When to use

**Use PaaS when:**

- MVP, prototype, or small app
- Team lacks infra to run RDS + Vault + Proxy
- Provider SLAs and features are enough

**Migrate to self-managed when:**

- Need private subnet, IAM auth, or compliance controls
- Connection pooling and identity per service matter at scale
- Start with [05-secret-manager-password.md](05-secret-manager-password.md), then [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) or [03-hcv-vault.md](03-hcv-vault.md)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `DATABASE_URL` committed to git | Platform env / CI secrets only |
| Same connection string for all services | Split users when moving to RDS/VPC |
| Rely on IP allowlist only | TLS + least-privilege user still required |
| No backup/restore test because PaaS "handles it" | Verify PITR and export on your tier |
| Stay on PaaS past compliance requirements | Migrate to [§5](05-secret-manager-password.md) + private network |

---

# Credential Rotation and Disaster Recovery

Production database security does not end at **first connection** — credentials rotate, backups fail silently, and restores are untested until you need them.

> **Related:** Secret patterns → [05-secret-manager-password.md](05-secret-manager-password.md) · Deploy rollout → [deployment-strategies/includes/12-schema-migrations-and-deploy.md](../deployment-strategies/includes/12-schema-migrations-and-deploy.md) · Connection pooling → [postgresql-performance/includes/07-connection-management.md](../postgresql-performance/includes/07-connection-management.md)

---

## At a glance

| Practice | Frequency | Owner |
|----------|-----------|-------|
| **Password / token rotation** | 30–90 days or on incident | Platform + app teams |
| **Backup verification** | Daily automated; monthly restore test | DBA / platform |
| **PITR drill** | Quarterly on staging clone | DBA |
| **Runbook review** | After every production incident | On-call |

**Rule of thumb:** A backup you have **never restored** is a hypothesis, not a recovery plan.

---

## Credential rotation runbook

```mermaid
flowchart TD
    Start[Rotation due] --> Dual[Issue new credential alongside old]
    Dual --> Deploy[Deploy apps with new secret reference]
    Deploy --> Verify[Verify connections and metrics]
    Verify --> Revoke[Revoke old credential]
    Revoke --> Audit[Audit log + ticket closed]
```

| Step | Detail |
|------|--------|
| **1. Dual-active window** | Vault/Secrets Manager holds `current` + `pending`; RDS supports two passwords briefly on some setups |
| **2. Rolling app restart** | Stateless pods pick up new secret via sidecar or env reload |
| **3. Pooler refresh** | PgBouncer/RDS Proxy may cache — plan reconnect or pool reload |
| **4. Revoke old** | Only after error rate and connection count stable |
| **5. Document** | Rotation date in CMDB; alert before next due |

Coordinate with [deployment-strategies](../deployment-strategies/README.md) — rotate during low traffic; avoid same window as schema contract migrations.

---

## Rotation by pattern

| Pattern | Rotation approach |
|---------|-------------------|
| **Static password in Secrets Manager** | Generate new password → update secret → rolling restart → DB user password change |
| **Vault dynamic credentials** | TTL handles expiry; ensure app renews leases |
| **RDS IAM auth token** | Short-lived tokens; no manual password rotation |
| **mTLS client certs** | CA + cert expiry alerts; renew before 30-day window |
| **PaaS connection string** | Provider dashboard rotation; update platform env |

---

## Backup and PITR fundamentals

| Term | Meaning |
|------|---------|
| **Full backup** | Snapshot of data at a point in time |
| **WAL / transaction log** | Continuous archive for point-in-time recovery |
| **PITR** | Restore to arbitrary second between backups |
| **RPO** | Max acceptable data loss (backup interval) |
| **RTO** | Max acceptable downtime to restore |

Typical managed PostgreSQL (RDS, Cloud SQL, Azure): enable automated backups + WAL; set retention to meet compliance.

---

## DR drill flow

```mermaid
flowchart LR
    Prod[(Production)] --> Snap[Snapshot / backup]
    Snap --> Restore[Restore to isolated instance]
    Restore --> Test[Smoke tests + row counts]
    Test --> Doc[Update runbook timings]
```

| Drill step | Verify |
|------------|--------|
| Restore latest snapshot | Instance starts; extensions present |
| PITR to specific timestamp | Data matches expected transaction boundary |
| App connectivity | TLS, security group, credentials from secret |
| Replication re-establish | If promoting replica — lag and cutover steps |

Record **actual RTO** from drill — update on-call runbook.

---

## What to backup beyond the database

| Asset | Why |
|-------|-----|
| **Schema migrations history** | Rebuild empty DB correctly |
| **Vault policies / IAM bindings** | Restore access paths |
| **PgBouncer / proxy config** | Pool rules match app |
| **Encryption keys** | KMS keys and rotation state |

---

## Checklist

- [ ] Automated daily backups enabled with retention ≥ compliance requirement
- [ ] PITR window documented (e.g. 7–35 days)
- [ ] Restore tested to non-production in last 90 days
- [ ] Credential rotation runbook with dual-active window
- [ ] Alerts on backup failure and cert expiry
- [ ] Secrets not in git; rotation does not require code deploy (env/secret reference only)
- [ ] On-call runbook includes RDS/Cloud SQL restore commands

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Rotate password without rolling apps | Connection storm and auth errors |
| Backup enabled but never restored | Schedule quarterly drill |
| Single shared DB user for all services | Per-service identity; rotate independently |
| Revoke old credential immediately | Dual-active verification period |
| DR instance in same region only | Cross-region snapshot for regional outage |

---

## Pros and cons

### Regular rotation + tested restore

**Pros:** Limits blast radius of leaked creds; proven RTO/RPO; audit-friendly.

**Cons:** Operational overhead; coordination with deploys; brief dual-credential complexity.

---

# Decision Guide — Connection Patterns

Eleven connection patterns exist in this guide. Use this flow to pick a starting point, then read the linked section for implementation detail.

> **Related:** Production layers → [02-prod-db-security.md](02-prod-db-security.md) · Pooling → [postgresql-performance/includes/07-connection-management.md](../postgresql-performance/includes/07-connection-management.md) · Rotation → [12-credential-rotation-and-dr.md](12-credential-rotation-and-dr.md)

---

## Master decision flow

```mermaid
flowchart TD
    Start[Service needs DB] --> Q1{Environment?}
    Q1 -->|Local dev| Local[01 Local credentials template]
    Q1 -->|Production| Q2{Stage / scale?}
    Q2 -->|MVP / PaaS| PaaS[11 PaaS managed DB]
    Q2 -->|Cloud prod| Q3{Dynamic creds required?}
    Q3 -->|No — start simple| SM[05 Secret manager + password]
    Q3 -->|Yes — rotate often| Q4{Cloud?}
    Q4 -->|AWS| Q5{RDS Proxy?}
    Q5 -->|Yes| AWSProxy[04 AWS IAM + RDS Proxy]
    Q5 -->|No| AWSIAM[06 Direct RDS IAM]
    Q4 -->|GCP| GCP[07 GCP Cloud SQL identity]
    Q4 -->|Azure| AZ[08 Azure Database identity]
    Q4 -->|Multi-cloud / on-prem| Vault[03 HashiCorp Vault]
    SM --> Q6{High connection count?}
    Q6 -->|Yes| PGB[09 PgBouncer + secret]
    Q6 -->|No| Done[Deploy with TLS + least privilege]
    Vault --> Done
    AWSProxy --> Done
```

---

## Quick pick table

| Situation | Section | Pattern |
|-----------|---------|---------|
| Laptop Postgres | [01](01-local-db-credentials.md) | Trust / local user *(template)* |
| Supabase, Neon, Railway | [11](11-paas-managed-db.md) | Platform connection string |
| First AWS prod app | [05](05-secret-manager-password.md) | Secrets Manager + DB user |
| Many microservices on RDS | [04](04-aws-iam-rds-proxy.md) | IAM auth + RDS Proxy |
| Compliance / dynamic secrets | [03](03-hcv-vault.md) | Vault database secrets engine |
| Connection storm | [09](09-pgbouncer-proxy-password.md) + [PG §7](../postgresql-performance/includes/07-connection-management.md) | PgBouncer |
| mTLS instead of password | [10](10-mtls-client-certs.md) | Client certificates |
| Regulated rotation + DR | [12](12-credential-rotation-and-dr.md) | Dual-active creds + restore drills |

---

## Security layers (every pattern)

| # | Layer | All patterns must |
|---|-------|-------------------|
| 1 | Network | Private subnet or allowlist; no public PG port |
| 2 | TLS | `sslmode=require` or equivalent in prod |
| 3 | Auth | One DB role per service; least privilege |
| 4 | Secrets | Not in git; rotate on schedule |
| 9 | Monitoring | Failed auth, connection count, slow queries |

Full table → [02-prod-db-security.md](02-prod-db-security.md).

---

## Migration path (typical)

| Stage | Pattern |
|-------|---------|
| **1. MVP** | PaaS connection string ([11](11-paas-managed-db.md)) |
| **2. First cloud prod** | Secret manager + password ([05](05-secret-manager-password.md)) |
| **3. Scale services** | PgBouncer ([09](09-pgbouncer-proxy-password.md)) |
| **4. Zero long-lived passwords** | Vault or cloud IAM ([03](03-hcv-vault.md), [04](04-aws-iam-rds-proxy.md)) |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Shared DB superuser for all apps | One role per service |
| IAM auth but no Proxy at high scale | RDS Proxy + pool |
| Vault everywhere on day one | Start [05] → evolve |
| Rotation without rolling restart plan | Dual-active window → [12](12-credential-rotation-and-dr.md) |

---

## See also

- [deployment-strategies §12](../deployment-strategies/includes/12-schema-migrations-and-deploy.md) — deploy during credential rotation
- [api-design §12 identity](../api-design-and-protection/includes/12-identity-rbac-iam-ad.md) — map service identity to DB role

---


---

## See also

| Guide | Topics |
|-------|--------|
| [postgresql-performance](../postgresql-performance/README.md) | Connection management, pooling, read replicas |
| [postgresql-performance §7](../postgresql-performance/includes/07-connection-management.md) | PgBouncer, pool sizing, `max_connections` |
| [api-design-and-protection](../api-design-and-protection/README.md) | JWT, IAM, RBAC — identity that maps to DB users |
| [high-throughput-systems](../high-throughput-systems/README.md) | App-tier scaling with pooled DB connections |
| [deployment-strategies](../deployment-strategies/README.md) | Coordinate credential rotation with deploys |
| [api-rate-limiting](../api-rate-limiting/README.md) | Rate limits unrelated to DB auth but share Redis |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Event store credentials and archival |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | Storage engine vs connection choice |
