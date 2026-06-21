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
| **Kubernetes auth** | Pods use service account JWT(JSON Web Token) |
| **AWS IAM(Identity and Access Management) auth** | EC2 / ECS / Lambda uses IAM role |
| **AppRole** | VMs and custom apps with `role_id` + `secret_id` |
| **JWT / OIDC(OpenID Connect)** | Cloud-native workloads |

---

## Common Vault deployment patterns

### Sidecar / Vault Agent

```
[App container]  +  [Vault Agent sidecar]
```

Vault Agent authenticates to Vault, fetches/renews DB credentials, and writes them to a shared file for the app.

### Init container (Kubernetes)

An init container fetches credentials before the main app container starts.

### Direct SDK / API(Application Programming Interface)

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
2. **TLS(Transport Layer Security) required** for all DB connections
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
