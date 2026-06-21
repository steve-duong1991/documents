# Identity: RBAC, IAM & Active Directory

Enterprise identity foundations for APIs: how IAM governs access, how RBAC assigns permissions through roles, and how Active Directory (and cloud IdPs) feed tokens and policies your gateway and services enforce.

> **Related:** Auth protocols (OAuth(Open Authorization), JWT(JSON Web Token), mTLS(Mutual Transport Layer Security)) → [Auth model](04-auth-model.md) · Gateway enforcement → [Load Balancer & API Gateway](03-api-gateway.md) · Multi-tenant claims → [16-multi-tenant-apis.md](16-multi-tenant-apis.md) · DB connection identity → [database-connection-and-security](../../database-connection-and-security/README.md)


## Articles in this section

| Article | Topics |
|---------|--------|
| [Active Directory and enterprise IdP](12-identity-active-directory.md) | AD(Active Directory) structure, Kerberos, Entra hybrid, group → role mapping |
| [API access decisions](12-identity-enterprise-api.md) | Decision flow, takeaways, common mistakes |

## At a glance

| Concept | What it is | Primary question |
|---------|------------|------------------|
| **IAM** | Discipline + systems for identity and access lifecycle | Who are you, and are you allowed to do this? |
| **RBAC** | Access **model**: permissions via **roles** | What role do you have, and what does that role allow? |
| **Active Directory (AD(Active Directory))** | Microsoft **directory service** (identity store + auth) | Where do users, groups, and computers live in the org? |

**Relationship:** AD (or another IdP) holds identities → IAM is the overall framework that uses them → RBAC is one common way IAM assigns permissions at apps, APIs, and cloud layers.

For **how clients authenticate** (OAuth, API(Application Programming Interface) keys, JWT validation), see [Auth model](04-auth-model.md). This section covers **organizational identity** and **authorization structure**.

---

## What IAM is

**Identity and Access Management (IAM)** is the end-to-end lifecycle and enforcement of access across people, services, and resources.

| Area | Examples |
|------|----------|
| **Authentication (AuthN)** | Password, MFA, SSO, certificates, API keys |
| **Authorization (AuthZ)** | RBAC, ABAC, resource policies |
| **Provisioning** | SCIM, LDAP sync, just-in-time (JIT) access |
| **Governance** | Access reviews, least privilege, audit logs |
| **Federation** | SAML, OIDC(OpenID Connect) — trust external IdPs |
| **Secrets & keys** | Service principals, workload identity |

Cloud **IAM** (AWS IAM, Azure RBAC, GCP IAM) applies the same ideas to cloud control planes: principals + policies + enforcement at the API layer.

### IAM components

```mermaid
flowchart TB
    subgraph Identity["Identity layer"]
        U[Users / humans]
        S[Service accounts / workloads]
        IdP[Identity Provider<br/>AD, Entra ID, Okta, Cognito]
    end

    subgraph AuthN["Authentication — Who are you?"]
        Login[Login / SSO / MFA]
        Token[Tokens: session, JWT, SAML assertion]
    end

    subgraph AuthZ["Authorization — What can you do?"]
        RBAC[RBAC — roles]
        ABAC[ABAC — attributes]
        PBAC[Policy-based — IAM policies]
    end

    subgraph Enforcement["Enforcement points"]
        App[Applications]
        GW[API Gateway]
        Cloud[Cloud IAM — AWS / Azure / GCP]
    end

    U --> IdP
    S --> IdP
    IdP --> Login --> Token
    Token --> AuthZ
    AuthZ --> App
    AuthZ --> GW
    AuthZ --> Cloud
```

### IAM lifecycle (joiner-mover-leaver)

```mermaid
sequenceDiagram
    participant HR as HR / JML process
    participant IdP as Identity Provider (e.g. AD)
    participant IAM as IAM / Provisioning
    participant App as App / API / Cloud

    HR->>IdP: New hire → create user
    IdP->>IAM: User + group membership
    IAM->>App: Provision account / assign roles
    Note over App: User can authenticate

    HR->>IdP: Role change / transfer
    IdP->>IAM: Update groups
    IAM->>App: Update roles / permissions

    HR->>IdP: Termination
    IdP->>IAM: Disable account
    IAM->>App: Revoke access immediately
```

### Pros of a formal IAM program

- Single source of truth for who has access and why
- Faster onboarding/offboarding with fewer orphaned accounts
- Audit trail for compliance (SOC2, ISO 27001)
- Consistent mapping from org structure → app permissions

### Cons

- Tooling sprawl (AD, IdP, SCIM, cloud IAM, app-local roles)
- Group-to-role mapping drift if not governed
- Over-permissioning when teams copy "admin" roles for convenience

---

## What RBAC is

**Role-Based Access Control (RBAC)** assigns permissions to **roles**, not directly to every user. Users get roles; roles get permissions.

### RBAC model

```mermaid
flowchart LR
    subgraph Users
        Alice[Alice]
        Bob[Bob]
    end

    subgraph Roles
        Dev[Developer]
        Ops[Ops Engineer]
        Admin[Admin]
    end

    subgraph Permissions
        R1[read:api/users]
        W1[write:api/orders]
        D1[delete:database]
        A1[manage:all]
    end

    Alice --> Dev
    Bob --> Ops
    Bob --> Admin

    Dev --> R1
    Dev --> W1
    Ops --> R1
    Ops --> W1
    Admin --> A1
    Ops -.-> D1
```

### RBAC hierarchy (NIST-style)

```mermaid
flowchart TB
    U[Users] -->|assigned| R[Roles]
    R -->|grants| P[Permissions / Privileges]
    P -->|on| O[Objects / Resources<br/>APIs, files, DB tables]

    R --> RH[Role hierarchy<br/>Senior Dev inherits Dev]
    R --> SoD[Separation of Duties<br/>e.g. approver ≠ requester]
    R --> C[Constraints<br/>time, location, MFA]
```

### RBAC vs other access models

| Model | Basis of access | Good for |
|-------|-----------------|----------|
| **RBAC** | Job function (role) | Orgs with stable job titles |
| **ABAC** | Attributes (dept, clearance, resource tags) | Fine-grained, dynamic rules |
| **ACL** | Per-resource list of who can access | Small sets, file shares |
| **PBAC / Policy** | Declarative policies (Rego, IAM JSON) | Cloud, APIs, zero-trust |

### RBAC at the API layer

Map roles to **scopes** or **route policies** at the gateway and re-check in the app for object-level AuthZ ([Auth model — layered flow](04-auth-model.md#layered-auth-flow)).

```mermaid
sequenceDiagram
    participant Client
    participant GW as API Gateway
    participant IdP as IdP / AD + OIDC
    participant API as Backend API

    Client->>GW: GET /orders + Bearer JWT
    GW->>GW: Validate JWT signature & expiry
    GW->>GW: Extract roles/scopes from token
    alt role contains "order-reader"
        GW->>API: Forward request
        API-->>Client: 200 + data
    else missing role
        GW-->>Client: 403 Forbidden
    end
```

| RBAC artifact | API example |
|---------------|-------------|
| **Role** | `order-reader`, `order-admin` |
| **Permission** | `GET /orders`, `POST /orders`, `DELETE /orders/{id}` |
| **Assignment** | Alice → `order-reader` (via AD group → app role mapping) |

Gateway checks **coarse** role/scope; the app still enforces **object ownership** (BOLA(Broken Object-Level Authorization)) — see [Auth model](04-auth-model.md).

---

---
