# Database Connection & Security

A reference for local PostgreSQL credentials (dev template), production security, and production database connection patterns.

Related: [postgresql-performance](../postgresql-performance/README.md) (connection pooling, PgBouncer tuning) · [api-design-and-protection](../api-design-and-protection/README.md) (service identity and IAM(Identity and Access Management) to databases)

---

## Table of contents

| # | Section |
|---|---------|--------------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Local credentials](#1-local-credentials) *(dev template)* | [includes/01-local-db-credentials.md](includes/01-local-db-credentials.md) |
| 2 | [Production security](includes/02-prod-db-security.md) |
| 3 | [HashiCorp Vault (HCV)](includes/03-hcv-vault.md) |
| 4 | [AWS IAM + RDS Proxy](includes/04-aws-iam-rds-proxy.md) |
| 5 | [Secret manager + password](includes/05-secret-manager-password.md) |
| 6 | [Direct RDS IAM](includes/06-direct-rds-iam.md) |
| 7 | [GCP Cloud SQL identity](includes/07-gcp-cloud-sql-identity.md) |
| 8 | [Azure Database identity](includes/08-azure-database-identity.md) |
| 9 | [PgBouncer + secret](includes/09-pgbouncer-proxy-password.md) |
| 10 | [mTLS client certificates](includes/10-mtls-client-certs.md) |
| 11 | [PaaS / platform-managed DB](includes/11-paas-managed-db.md) |
| 12 | [Credential rotation and DR](includes/12-credential-rotation-and-dr.md) |
| 13 | [Decision guide — connection patterns](includes/13-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section. [GUIDE.md](GUIDE.md) combines all sections in one file.

---

## Overview

Security layers, connection pattern comparison, and default production baseline.

See full details → [includes/00-overview.md](includes/00-overview.md)

---

## 1. Local credentials *(dev template)*

Machine-specific dev template — replace host, user, and paths for your environment.

See full details → [includes/01-local-db-credentials.md](includes/01-local-db-credentials.md)

---

## 2. Production security

Layered security for service → database connections and a comparison of connection approaches (sections 3–11).

See full details → [includes/02-prod-db-security.md](includes/02-prod-db-security.md)

---

## 3. HashiCorp Vault (HCV)

Dynamic DB users with auto-revocation — multi-cloud, high security.

See full details → [includes/03-hcv-vault.md](includes/03-hcv-vault.md)

---

## 4. AWS IAM + RDS Proxy

IAM auth tokens + managed connection pooling on AWS.

See full details → [includes/04-aws-iam-rds-proxy.md](includes/04-aws-iam-rds-proxy.md)

---

## 5. Secret manager + password

Most common baseline — static password in AWS Secrets Manager, GCP Secret Manager, or Azure Key Vault.

See full details → [includes/05-secret-manager-password.md](includes/05-secret-manager-password.md)

---

## 6. Direct RDS IAM

IAM auth tokens straight to RDS — no RDS Proxy.

See full details → [includes/06-direct-rds-iam.md](includes/06-direct-rds-iam.md)

---

## 7. GCP Cloud SQL identity

Cloud SQL Auth Proxy, IAM DB auth, and Workload Identity on GCP.

See full details → [includes/07-gcp-cloud-sql-identity.md](includes/07-gcp-cloud-sql-identity.md)

---

## 8. Azure Database identity

Managed Identity, Azure AD(Active Directory) auth, and Key Vault on Azure.

See full details → [includes/08-azure-database-identity.md](includes/08-azure-database-identity.md)

---

## 9. PgBouncer + secret

Self-hosted connection pooling with credentials from a secret manager.

See full details → [includes/09-pgbouncer-proxy-password.md](includes/09-pgbouncer-proxy-password.md)

---

## 10. mTLS client certificates

Certificate-based client authentication — no password in the app.

See full details → [includes/10-mtls-client-certs.md](includes/10-mtls-client-certs.md)

---

## 11. PaaS / platform-managed DB

Supabase, Neon, Railway, Heroku — connection string from the platform dashboard.

See full details → [includes/11-paas-managed-db.md](includes/11-paas-managed-db.md)

---

## 12. Credential rotation and DR

Rotation runbook with dual-active credentials, backup/PITR(Point-in-Time Recovery) fundamentals, and restore drill checklist.

See full details → [includes/12-credential-rotation-and-dr.md](includes/12-credential-rotation-and-dr.md)

---

## 13. Decision guide — connection patterns

Master flow to pick PaaS, secret manager, Vault, IAM, PgBouncer, or mTLS.

See full details → [includes/13-decision-guide.md](includes/13-decision-guide.md)

---

## See also

| Guide | Topics |
|-------|--------|
| [postgresql-performance](../postgresql-performance/README.md) | Connection management, pooling, read replicas |
| [postgresql-performance §7](../postgresql-performance/includes/07-connection-management.md) | PgBouncer, pool sizing, `max_connections` |
| [api-design-and-protection](../api-design-and-protection/README.md) | JWT(JSON Web Token), IAM, RBAC(Role-Based Access Control) — identity that maps to DB users |
| [high-throughput-systems](../high-throughput-systems/README.md) | App-tier scaling with pooled DB connections |
| [deployment-strategies](../deployment-strategies/README.md) | Coordinate credential rotation with deploys |
| [api-rate-limiting](../api-rate-limiting/README.md) | Rate limits unrelated to DB auth but share Redis |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Event store credentials and archival |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | Storage engine vs connection choice |