# Overview — Database Connection & Security

Production database access is **layered**: network isolation and TLS(Transport Layer Security) first, then authentication, secrets, pooling, and audit. Pick a connection pattern based on cloud, scale, and compliance — not on what is easiest in dev.

> **Related:** Pool sizing and `max_connections` → [postgresql-performance §7](../../postgresql-performance/includes/07-connection-management.md) · Service identity → [api-design §12 Identity](../../api-design-and-protection/includes/12-identity-rbac-iam-ad.md) · Pattern picker → [§13 Decision guide](13-decision-guide.md)

## Security layers at a glance

| Layer | Focus | Sections |
|-------|-------|----------|
| **Network** | Private subnet, no public IP, firewall | [§2 Production security](02-prod-db-security.md) |
| **TLS** | Encrypt in transit; verify server cert | [§2](02-prod-db-security.md), [§10 mTLS](10-mtls-client-certs.md) |
| **Authentication** | One DB user per service; least privilege | [§2](02-prod-db-security.md), cloud patterns §3–§11 |
| **Secrets** | No credentials in git or images | [§3 Vault](03-hcv-vault.md), [§5 Secret manager](05-secret-manager-password.md) |
| **Pooling** | Avoid connection storms | [§4 RDS Proxy](04-aws-iam-rds-proxy.md), [§9 PgBouncer](09-pgbouncer-proxy-password.md) |
| **Identity** | IAM(Identity and Access Management) / workload identity instead of passwords | [§4](04-aws-iam-rds-proxy.md), [§6](06-direct-rds-iam.md), [§7](07-gcp-cloud-sql-identity.md), [§8](08-azure-database-identity.md) |
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
| 3–11 | Connection patterns (Vault, IAM, cloud, PaaS, mTLS(Mutual Transport Layer Security)) | See [§13](13-decision-guide.md) flow |
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
