# Azure Database identity

> Connect to Azure Database for PostgreSQL / MySQL using Managed Identity and Azure AD(Active Directory) — no DB password stored in the application.

> **Related:** Static secrets via Key Vault → [§5 Secret manager + password](05-secret-manager-password.md) · AWS comparison → [§4](04-aws-iam-rds-proxy.md), [§6](06-direct-rds-iam.md) · Decision guide → [§13 Decision guide](13-decision-guide.md)

## What it solves

- Passwordless or centrally managed authentication for Azure-hosted apps
- Integration with **Azure App Service**, **AKS**, **Azure Functions**, and VMs
- Azure Key Vault for static secrets when IAM(Identity and Access Management)-style auth is not used
- TLS(Transport Layer Security) to Azure Database endpoints

---

## Three main patterns

### Pattern A: Azure AD authentication (Microsoft Entra ID)

Azure Database for PostgreSQL (Flexible Server) supports **Azure AD authentication** — the database accepts tokens from Azure AD principals.

```
App Service / AKS pod → Managed Identity → Azure AD token → Azure PostgreSQL
```

**Setup:**

1. Enable Azure AD auth on the PostgreSQL flexible server.
2. Create an **Azure AD admin** on the server.
3. Assign the app's **Managed Identity** as an Azure AD user in PostgreSQL.
4. App acquires token via `DefaultAzureCredential` (or MSI endpoint).
5. Connect using token as password (similar model to AWS IAM auth tokens).

**Benefit:** No long-lived SQL(Structured Query Language) password in config; identity is the Azure AD principal.

---

### Pattern B: Managed Identity + Key Vault (static secret)

```
App → Managed Identity → Key Vault → username/password → TLS → Azure Database
```

Same model as [05-secret-manager-password.md](05-secret-manager-password.md):

1. Store DB credentials in **Key Vault**.
2. Grant app's Managed Identity `get` on secrets.
3. Fetch at startup; connect with TLS.

**Use when:** Azure AD DB auth is not configured or app/driver lacks token support.

---

### Pattern C: AKS + workload identity

For Kubernetes on Azure (**AKS**):

```
Pod → Workload Identity → Azure AD / Key Vault → Database
```

- **Workload Identity** federates K8s service account to Azure Managed Identity.
- Same patterns as A or B, but credentials flow through the pod's federated identity.

---

## Architecture

```
┌─────────────────┐     token or secret     ┌──────────────────┐
│  App Service    │ ─────────────────────► │ Azure PostgreSQL │
│  or AKS pod     │      over TLS          │ (Flexible Server)│
└────────┬────────┘                        └──────────────────┘
         │
         ▼
  Managed Identity / Azure AD
```

**Minimum stack:**

```
Private VNet → TLS → Azure AD auth or Key Vault secret → Azure Database
```

---

## How this maps to security layers

| Layer | Coverage |
|-------|----------|
| 1. Network isolation | VNet integration; private access; firewall rules |
| 2. TLS | Required (`sslmode=require`) |
| 3. Authentication | Azure AD principal or dedicated SQL user |
| 4. Secrets management | Key Vault or token-based (no app password) |
| 6. Workload identity | Managed Identity on App Service / AKS |

---

## Azure vs AWS equivalents

| Azure | AWS equivalent |
|-------|----------------|
| Managed Identity | IAM role on EC2/ECS/Lambda |
| Azure AD DB auth | RDS IAM auth |
| Key Vault | Secrets Manager |
| Private VNet access | RDS in private subnet |

See [04-aws-iam-rds-proxy.md](04-aws-iam-rds-proxy.md) and [06-direct-rds-iam.md](06-direct-rds-iam.md).

---

## When to use

**Use Azure AD authentication when:**

- App runs on App Service, Functions, or AKS with Managed Identity
- You want passwordless DB auth aligned with Entra ID

**Use Key Vault + password when:**

- Drivers or legacy apps need traditional username/password — see [05-secret-manager-password.md](05-secret-manager-password.md)

**Consider Vault when:**

- Multi-cloud secrets and dynamic DB users — see [03-hcv-vault.md](03-hcv-vault.md)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Azure AD auth without creating DB principal | Map Managed Identity to PostgreSQL user |
| Key Vault secret never rotated | Schedule rotation → [§12](12-credential-rotation-and-dr.md) |
| Driver without Azure AD token support | Use supported driver or Pattern B (Key Vault) |
| Public firewall rule `0.0.0.0` | Private VNet / private endpoint |
| Same connection string in dev and prod | Separate secrets per environment |