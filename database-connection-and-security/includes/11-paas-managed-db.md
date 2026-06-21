# PaaS / platform-managed database

> The platform (Supabase, Neon, Railway, Heroku, PlanetScale, etc.) hosts the database and gives you a **connection string** — credentials managed in the provider dashboard or CI, not in application source code.

> **Related:** Production hardening path → [§5 Secret manager](05-secret-manager-password.md) · When to leave PaaS → [§13 Decision guide](13-decision-guide.md) · Security layers gap → [§2 Production security](02-prod-db-security.md)

## What it solves

- Fastest path from dev to production — no RDS/Vault/proxy setup
- Provider handles backups, patches, scaling, and often TLS(Transport Layer Security)
- Connection strings rotatable from the provider UI or API(Application Programming Interface)
- Good for MVPs, side projects, and small teams

## What it does not solve

- Less control over network isolation (often public endpoint + IP allowlist or SSL only)
- Shared connection string per environment is common — not per-service IAM(Identity and Access Management)
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
| No backup/restore test because PaaS "handles it" | Verify PITR(Point-in-Time Recovery) and export on your tier |
| Stay on PaaS past compliance requirements | Migrate to [§5](05-secret-manager-password.md) + private network |
