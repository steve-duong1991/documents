# Direct RDS IAM auth (no RDS Proxy)

> App connects to RDS using an IAM auth token as the password — same token model as [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md), but **without** RDS Proxy in the path.

> **Related:** When to add Proxy → [§4 AWS IAM + RDS Proxy](04-aws-iam-rds-proxy.md) · App-side pooling → [§9 PgBouncer + secret](09-pgbouncer-proxy-password.md) · `max_connections` → [postgresql-performance §7](../../postgresql-performance/includes/07-connection-management.md)

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
