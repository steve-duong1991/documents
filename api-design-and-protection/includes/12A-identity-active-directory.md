# Identity — Active Directory and enterprise IdP

> **Related:** IAM(Identity and Access Management) and RBAC(Role-Based Access Control) → [12-identity-rbac-iam-ad.md](12-identity-rbac-iam-ad.md) · API(Application Programming Interface) decisions → [12B-identity-enterprise-api.md](12B-identity-enterprise-api.md) · SCIM(System for Cross-domain Identity Management) / JML(Joiner-Mover-Leaver) playbook → [12C-scim-and-jml-provisioning.md](12C-scim-and-jml-provisioning.md) · Auth protocols → [04-auth-model.md](04-auth-model.md)

## What Active Directory is

**Active Directory (AD)** is Microsoft's directory service for Windows-centric enterprises. It is primarily an **identity store and authentication system**, not a full IAM product by itself — though **Microsoft Entra ID** (Azure AD(Active Directory)) extends it for cloud and modern protocols.

### AD logical structure

```mermaid
flowchart TB
    Forest[Forest — security boundary]
    Forest --> Domain1[Domain: corp.example.com]
    Forest --> Domain2[Domain: dev.example.com]

    Domain1 --> DC1[Domain Controllers<br/>auth + replication]
    Domain1 --> OU1[OU: Engineering]
    Domain1 --> OU2[OU: Finance]

    OU1 --> User1[User: alice@corp]
    OU1 --> Group1[Group: DevTeam]
    OU2 --> User2[User: bob@corp]

    Group1 --> User1
    DC1 --> LDAP[LDAP / Kerberos]
```

### Key AD concepts

| Term | Meaning |
|------|---------|
| **Domain** | Administrative + authentication boundary (e.g. `corp.example.com`) |
| **Forest** | Collection of domains with shared schema |
| **Domain Controller (DC)** | Server that authenticates users and holds directory data |
| **OU (Organizational Unit)** | Container for users/groups/computers; delegation and GPO |
| **Security Group** | Collection of principals; permissions and RBAC mapping |
| **GPO (Group Policy)** | Central config for machines/users (password policy, software) |
| **Kerberos** | Default AD auth protocol (tickets, mutual auth) |
| **LDAP(Lightweight Directory Access Protocol)** | Directory query protocol (read users, groups, attributes) |

### AD authentication flow (Kerberos — simplified)

```mermaid
sequenceDiagram
    participant User as User / Client
    participant DC as Domain Controller
    participant Svc as Service / App / File Server

    User->>DC: 1. Login (username + password)
    DC->>DC: Verify credentials
    DC-->>User: 2. TGT (Ticket-Granting Ticket)

    User->>DC: 3. Request service ticket (TGT + service name)
    DC-->>User: 4. Service ticket for Svc

    User->>Svc: 5. Present service ticket
    Svc->>Svc: Validate ticket with DC trust
    Svc-->>User: 6. Access granted
```

Modern APIs rarely terminate Kerberos at the gateway directly. Typical pattern: AD → Entra ID / IdP → **OIDC(OpenID Connect)/SAML(Security Assertion Markup Language)** → JWT(JSON Web Token) with groups/roles → gateway + app.

SAML protocol depth (assertions, bindings, SP(Savings Plan) checklist, SAML→OIDC bridge) → [auth §2c](../../auth-oauth-oidc-and-login-security/includes/02C-saml-protocol.md). SSO(Single Sign-On) integration playbook → [auth §2b](../../auth-oauth-oidc-and-login-security/includes/02B-sso-integration-playbook.md).

### AD vs Microsoft Entra ID

| | **On-prem AD** | **Microsoft Entra ID** |
|--|----------------|------------------------|
| **Primary use** | Windows domain, LAN, legacy apps | Cloud, SaaS(Software as a Service), modern auth (OIDC/SAML) |
| **Protocol** | Kerberos, NTLM, LDAP | OAuth(Open Authorization) 2.0, OIDC, SAML |
| **Structure** | Domains, OUs, GPO | Tenants, users, groups, conditional access |
| **Hybrid** | — | AD Connect syncs on-prem AD ↔ cloud |

---

## How RBAC, IAM, and AD work together

End-to-end enterprise picture for API access:

```mermaid
flowchart TB
    subgraph Source["Identity source"]
        AD[Active Directory<br/>users, groups, OUs]
    end

    subgraph IAMPlatform["IAM platform"]
        Sync[Sync / Federation<br/>AD Connect, SCIM]
        Entra[Entra ID / IdP]
        RBACEngine[RBAC mapping<br/>AD group → App role]
        Policy[Policies + MFA + Conditional Access]
    end

    subgraph Apps["Applications & APIs"]
        SaaS[SaaS apps]
        GW[API Gateway]
        Cloud[Cloud resources]
    end

    AD --> Sync --> Entra
    Entra --> RBACEngine
    RBACEngine --> Policy
    Policy --> SaaS
    Policy --> GW
    Policy --> Cloud

    User([Employee]) -->|login SSO| Entra
    Entra -->|JWT with roles/groups| GW
```

### Concrete example

1. **AD:** Alice is in security group `Finance-Analysts`
2. **IAM provisioning:** Sync maps `Finance-Analysts` → app role `finance-reader`
3. **RBAC:** Role `finance-reader` allows `GET /reports`, `GET /invoices`
4. **Enforcement:** API gateway reads JWT `roles: ["finance-reader"]`; app verifies resource ownership

```mermaid
flowchart LR
    ADG[AD Group:<br/>Finance-Analysts] --> Map[Group-to-Role mapping]
    Map --> Role[App Role:<br/>finance-reader]
    Role --> Perm[Permissions:<br/>read reports, read invoices]
    Perm --> GW[API Gateway enforces]
    Perm --> App[App enforces object-level AuthZ]
```

---

## Decision flow: can this user access this API?

Unified authorization check (IAM + RBAC + token from AD-backed IdP):

```mermaid
flowchart TD
    Start([Request with credentials]) --> AuthN{Authenticated?<br/>valid token / MFA}
    AuthN -->|No| Deny1[401 Unauthorized]
    AuthN -->|Yes| Identity[Resolve identity<br/>user ID, groups, roles]

    Identity --> RBAC{User has required role<br/>or scope?}
    RBAC -->|No| Deny2[403 Forbidden]
    RBAC -->|Yes| Policy{Other IAM policies?<br/>IP, time, resource, ABAC}
    Policy -->|Fail| Deny3[403 Forbidden]
    Policy -->|Pass| Object{Object-level AuthZ<br/>user owns resource?}
    Object -->|Fail| Deny4[403 Forbidden]
    Object -->|Pass| Allow[Allow → execute business logic]

    Allow --> Audit[Log access decision]
```

Aligns with the [layered auth flow](04-auth-model.md#layered-auth-flow): gateway handles AuthN(Authentication) and coarse AuthZ(Authorization); the app must still run the object check.

---

## Comparison summary

| | **IAM** | **RBAC** | **Active Directory** |
|--|---------|----------|----------------------|
| **Type** | Framework + tooling | Access **model** | Directory + auth **product** |
| **Answers** | Full identity lifecycle | "What can this role do?" | "Who is this user in the org?" |
| **Scope** | People, apps, cloud, APIs | Permissions via roles | Typically enterprise Windows / hybrid |
| **Typical artifacts** | Policies, MFA(Multi-Factor Authentication), audit, provisioning | Roles, bindings, permissions | Users, groups, OUs, GPO, DCs |
| **In API context** | Gateway auth, OAuth, lifecycle | JWT roles/scopes, usage plans | SSO(Single Sign-On) source; groups → API roles |

Hub comparison → [12 — IAM, RBAC, and AD](12-identity-rbac-iam-ad.md#iam-rbac-and-ad--comparison).

---

## IAM lifecycle (joiner-mover-leaver)

Provisioning and offboarding must revoke API and app access when HR disables an account — not only when a JWT expires. App-side SCIM contract, JIT(Just-In-Time) vs pre-provision, and deactivate→revoke races → [12C SCIM and JML](12C-scim-and-jml-provisioning.md).

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

API access checklist and mistakes → [12B — API design takeaways](12B-identity-enterprise-api.md#api-design-takeaways).

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Terminate **Kerberos** at the public API gateway | AD/Entra → OIDC/SAML → JWT at the edge ([Auth model](04-auth-model.md)) |
| Expose **LDAP** to the internet for app auth | Federation via Entra ID / IdP; LDAP stays internal |
| Stale **hybrid sync** (AD Connect / SCIM(System for Cross-domain Identity Management)) | Monitor sync lag; on disable revoke sessions — [12C lag/races](12C-scim-and-jml-provisioning.md#lag-races-and-revoke); otherwise revoked users remain valid in JWTs until TTL(Time To Live) expires |
| Treat AD **groups** as app permissions in code | Map groups → roles centrally — see [12B API access mistakes](12B-identity-enterprise-api.md#common-mistakes) |
| Skip **object-level AuthZ** because RBAC passed | App still checks resource ownership ([Auth model — layered flow](04-auth-model.md#layered-auth-flow)) |

General API identity pitfalls (JWT TTL, offboarding, service accounts) → [12B — Common mistakes](12B-identity-enterprise-api.md#common-mistakes).