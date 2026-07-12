# Secrets Beyond the Database

> **Scope:** **Application, CI(Continuous Integration), partner, and platform secrets** — API(Application Programming Interface) keys, webhook signing secrets, JWT(JSON Web Token) signing keys, cloud access keys, TLS(Transport Layer Security) material for non-DB services, and encryption keys used by apps. **Database usernames/passwords, RDS IAM(Identity and Access Management), Vault DB dynamic creds, and PgBouncer auth** → [database-connection-and-security](../../database-connection-and-security/README.md).
>
> **Related:** DB credential patterns → [database-connection README](../../database-connection-and-security/README.md) · Rotation mindset → [database-connection §12](../../database-connection-and-security/includes/12-credential-rotation-and-dr.md) · Browser token storage → [fullstack §7](../../fullstack-bff-and-clients/includes/07-auth-ux.md) · Supply-chain signing keys → [§4](04-supply-chain-security.md)

## At a glance

| Secret class | Store in | Rotate | Never |
|--------------|----------|--------|-------|
| Third-party API keys | Secret manager; inject at runtime | On hire/fire + schedule | Frontend bundles, mobile apps |
| Webhook HMAC(Hash-based Message Authentication Code) secrets | Secret manager; dual-key during rotate | Planned dual-run | Logs, tickets |
| JWT / OIDC(OpenID Connect) signing keys | KMS(Key Management Service) or HSM(Hardware Security Module)-backed | Key versioning | App config repos |
| CI deploy credentials | OIDC to cloud (prefer) or short-lived | Prefer federated over PATs | Long-lived PATs in org secrets forever |
| Service-to-service | mTLS(Mutual Transport Layer Security) or short JWT | Cert/key TTL | Shared static “cluster password” |
| DB passwords | → database-connection guide | → §12 there | Duplicated here as second source of truth |

**Rule of thumb:** One secret manager namespace per environment; **apps pull, humans rarely copy**.

## Secret lifecycle

```mermaid
sequenceDiagram
    autonumber
    participant Eng as Engineer
    participant SM as Secret manager
    participant App as Workload
    participant Aud as Audit log

    Eng->>SM: Create/rotate secret (IAM gated)
    SM->>Aud: Who changed what
    App->>SM: Fetch via workload identity
    SM-->>App: Short-lived value or reference
    Note over App: Memory only; not baked into image
    Eng->>SM: Revoke old version after soak
```

## Patterns that work

| Pattern | When |
|---------|------|
| **Workload identity → secret manager** | K8s/cloud runtimes with IAM roles |
| **Dual keys (current + next)** | Zero-downtime rotation for HMAC/API keys |
| **Reference not value in config** | Config maps hold `secret://path`; value at runtime |
| **OIDC federation for CI** | GitHub Actions / GitLab → cloud without static keys |
| **Envelope encryption** | Data keys in KMS; app secrets wrapped |

## Patterns to avoid

| Anti-pattern | Why it fails |
|--------------|--------------|
| Secrets in git “temporarily” | History retains them forever |
| Secrets in container layers | Image pull = secret leak |
| One prod key shared by 12 services | Blast radius and no attribution |
| Frontend env `NEXT_PUBLIC_*` for private keys | Anything public-prefixed is public |
| Slack/email of production keys | No audit, no rotation discipline |

## Ownership matrix

| Secret | Owner | Break-glass |
|--------|-------|-------------|
| Payment provider key | Payments TL | Security on-call |
| Email/SMS provider | Platform | Platform on-call |
| Partner webhook secret | Integrating team | Dual-key rotate |
| Org-wide signing CA | Security / platform | Documented ceremony |

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Using DB vault docs for Stripe keys | This section + secret manager; DB guide for DB only |
| Rotating without dual-key | Overlap validity windows; then revoke |
| Logging Authorization headers | Redact middleware; alert on plaintext patterns |
| Copying prod secrets into staging | Separate namespaces; synthetic providers in lower envs |
| Eternal CI PATs | OIDC federation or short-lived tokens |