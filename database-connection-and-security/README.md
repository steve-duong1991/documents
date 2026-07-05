# Database Connection & Security

A reference for local PostgreSQL credentials (dev template), production security, and production database connection patterns.

Related: [postgresql-performance](../postgresql-performance/README.md) (connection pooling, PgBouncer tuning) · [api-design-and-protection](../api-design-and-protection/README.md) (service identity and IAM(Identity and Access Management) to databases)

---

## Table of contents

| # | Section |
|---|---------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Local credentials *(dev template)*](includes/01-local-db-credentials.md) |
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

> **On GitHub:** Click a topic in the table above for the full section.

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
| [apache-kafka](../apache-kafka/README.md) | Connect and broker credentials, TLS(Transport Layer Security), IAM for managed Kafka |