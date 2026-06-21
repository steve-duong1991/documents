# Production Database Security

> How to protect **service → database** connections in production.

> **Related:** Pattern picker (canonical flow) → [§13 Decision guide](13-decision-guide.md) · Pool sizing → [postgresql-performance §7](../../postgresql-performance/includes/07-connection-management.md) · Rotation runbook → [§12 Credential rotation and DR](12-credential-rotation-and-dr.md)

Production database security is **layered** — no single control is enough. Secret managers such as HashiCorp Vault or AWS IAM(Identity and Access Management) + RDS Proxy address authentication and secrets, but they sit alongside network, TLS(Transport Layer Security), and monitoring controls.

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
| 7. Application protections | SQL(Structured Query Language) injection, RLS, read replicas |
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
| Mutual TLS (mTLS(Mutual Transport Layer Security)) | Client presents a cert; DB verifies client identity |
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
| IAM / identity-based auth | AWS RDS IAM, Azure AD(Active Directory), GCP Cloud SQL IAM |
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
