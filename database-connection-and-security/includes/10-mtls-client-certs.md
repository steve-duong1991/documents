# mTLS (client certificate auth)

> The database verifies a **client TLS(Transport Layer Security) certificate** instead of (or in addition to) a password — strong binding between identity and connection.

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

Short-lived client certs (hours/days) reduce impact of key compromise — similar benefit to IAM(Identity and Access Management) tokens.

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
- You want to eliminate passwords entirely and control cert TTL(Time To Live)

**Avoid as first choice when:**

- Team lacks PKI operations experience
- Managed DB does not support client cert auth well
- [05-secret-manager-password.md](05-secret-manager-password.md) or [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) meets requirements with less ops burden

## Common mistakes

| Mistake | Fix |
|---------|-----|
| mTLS without network isolation | Private subnet first — cert ≠ firewall |
| No cert rotation runbook | Automate issue/revoke; test before expiry |
| Private key in application repo | HSM(Hardware Security Module), cert manager, or Vault PKI |
| `pg_hba.conf` `cert` without CN mapping | Map certificate CN to DB role explicitly |
| mTLS as first prod choice without PKI team | Start [§5](05-secret-manager-password.md) or cloud IAM |