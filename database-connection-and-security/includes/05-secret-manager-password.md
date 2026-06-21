# Secret manager + static password

> The most common production baseline — store a DB username/password in a cloud secret manager and inject it at runtime. No credentials in git or container images.

> **Scope:** **Baseline pattern** — username/password in Secrets Manager (or equivalent), injected at runtime. Upgrade to short-lived IAM(Identity and Access Management) → [§4 IAM + RDS Proxy](04-aws-iam-rds-proxy.md). Enterprise dynamic creds → [§3 HCV Vault](03-hcv-vault.md).
>
> **Related:** Upgrade path → [§4 IAM + RDS Proxy](04-aws-iam-rds-proxy.md) · Self-hosted pooling → [§9 PgBouncer + secret](09-pgbouncer-proxy-password.md) · Rotation runbook → [§12 Credential rotation and DR](12-credential-rotation-and-dr.md)

## What it solves

- Removes passwords from source code, `.env` files committed to git, and Docker image layers
- Central place to rotate and audit database credentials
- Works with **any** database engine and **any** cloud or on-prem deployment
- Simple for teams starting production without Vault or IAM(Identity and Access Management) auth

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
| HashiCorp | Vault KV engine | Vault Agent or API(Application Programming Interface) — see [03-hcv-vault.md](03-hcv-vault.md) |

---

## Setup steps

1. **RDS / managed DB** in a private subnet; TLS(Transport Layer Security) required; no public IP.
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