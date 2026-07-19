# Identity: RBAC, IAM & Active Directory

Enterprise identity foundations for APIs: how IAM governs access, how RBAC assigns permissions through roles, and how Active Directory (and cloud IdPs) feed tokens and policies your gateway and services enforce.

> **Scope:** **Organizational identity and authorization structure** — IAM, RBAC, AD(Active Directory)/IdP(Identity Provider) integration. Client auth protocols (OAuth, JWT(JSON Web Token), API(Application Programming Interface) keys) → [Auth model](04-auth-model.md). AD depth, Kerberos, hybrid sync → [12A Active Directory](12A-identity-active-directory.md). API access decisions and mistakes → [12B API access](12B-identity-enterprise-api.md). SCIM(System for Cross-domain Identity Management) / JML(Joiner-Mover-Leaver) provisioning → [12C SCIM and JML](12C-scim-and-jml-provisioning.md). Object-level / ReBAC(Relationship-Based Access Control) → [12D fine-grained AuthZ](12D-fine-grained-authz.md).
>
> **Related:** Gateway enforcement → [Load Balancer & API Gateway](03-api-gateway.md) · Multi-tenant claims → [16-multi-tenant-apis.md](16-multi-tenant-apis.md) · BYO(Bring Your Own) IdP / multi-issuer → [auth §2d](../../auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md) · DB connection identity → [database-connection-and-security](../../database-connection-and-security/README.md)

## Articles in this section

| Article | Topics |
|---------|--------|
| [Active Directory and enterprise IdP](12A-identity-active-directory.md) | AD structure, Kerberos, Entra hybrid, group → role mapping, JML overview |
| [API access decisions](12B-identity-enterprise-api.md) | RBAC at the gateway, decision flow, takeaways, common mistakes |
| [SCIM and JML provisioning](12C-scim-and-jml-provisioning.md) | SCIM Users/Groups, JIT(Just-In-Time) vs pre-provision, deactivate → revoke, multi-tenant SCIM |
| [Fine-grained AuthZ](12D-fine-grained-authz.md) | BOLA(Broken Object-Level Authorization), ReBAC/Zanzibar-style, ABAC(Attribute-Based Access Control) vs RBAC, AuthZ(Authorization) service vs JWT |

## At a glance

| Concept | What it is | Primary question |
|---------|------------|------------------|
| **IAM** | Discipline + systems for identity and access lifecycle | Who are you, and are you allowed to do this? |
| **RBAC** | Access **model**: permissions via **roles** | What role do you have, and what does that role allow? |
| **Active Directory (AD)** | Microsoft **directory service** (identity store + auth) | Where do users, groups, and computers live in the org? |

**Relationship:** AD (or another IdP) holds identities → IAM is the overall framework → RBAC is one common way IAM assigns permissions at apps, APIs, and cloud layers.

For **how clients authenticate** (OAuth, API keys, JWT validation), see [Auth model](04-auth-model.md).

---

## What IAM is

**Identity and Access Management (IAM)** covers the full lifecycle: AuthN(Authentication), AuthZ, provisioning, governance, federation, and workload identity.

| Area | Examples |
|------|----------|
| **Authentication** | Password, MFA(Multi-Factor Authentication), SSO(Single Sign-On), API keys |
| **Authorization** | RBAC, ABAC, resource policies |
| **Provisioning** | SCIM, LDAP(Lightweight Directory Access Protocol) sync, JIT(Just-In-Time) — [12C SCIM and JML](12C-scim-and-jml-provisioning.md) |
| **Governance** | Access reviews, audit logs, JML — [12C](12C-scim-and-jml-provisioning.md); AD sequence → [12A lifecycle](12A-identity-active-directory.md#iam-lifecycle-joiner-mover-leaver) |
| **Cloud control plane** | AWS IAM, Azure RBAC, GCP IAM → [database-connection-and-security](../../database-connection-and-security/README.md) |

---

## What RBAC is

**Role-Based Access Control (RBAC)** assigns permissions to **roles**, not directly to every user. Users get roles; roles get permissions.

### RBAC vs other access models

| Model | Basis of access | Good for |
|-------|-----------------|----------|
| **RBAC** | Job function (role) | Orgs with stable job titles |
| **ABAC** | Attributes (dept, clearance, resource tags) | Fine-grained, dynamic rules — depth → [12D](12D-fine-grained-authz.md) |
| **ReBAC** | Relationships (viewer of doc, member of group) | Sharing + inheritance — [12D](12D-fine-grained-authz.md) |
| **ACL(Access Control List)** | Per-resource list of who can access | Small sets, file shares |
| **PBAC / Policy** | Declarative policies (Rego, IAM JSON) | Cloud, APIs, zero-trust |

Map roles to **scopes** or route policies at the gateway; re-check **object-level AuthZ** in the app — [12B RBAC at the API layer](12B-identity-enterprise-api.md#rbac-at-the-api-layer) and [Auth model — layered flow](04-auth-model.md#layered-auth-flow).

---

## IAM, RBAC, and AD — comparison

| | **IAM** | **RBAC** | **Active Directory** |
|--|---------|----------|----------------------|
| **Type** | Framework + tooling | Access **model** | Directory + auth **product** |
| **Answers** | Full identity lifecycle | "What can this role do?" | "Who is this user in the org?" |
| **In API context** | Gateway auth, OAuth(Open Authorization), lifecycle | JWT roles/scopes, usage plans | SSO source; groups → API roles |

Enterprise AD structure, Entra hybrid, and group → role mapping → [12A Active Directory](12A-identity-active-directory.md).

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Confuse **Auth model** (OAuth/JWT) with **IAM program** (JML, audits) | Protocols in §4; org identity here + [12A](12A-identity-active-directory.md) / [12B](12B-identity-enterprise-api.md) / [12C](12C-scim-and-jml-provisioning.md) |
| RBAC at gateway only | Layered AuthZ — [12B](12B-identity-enterprise-api.md#common-mistakes); object checks → [12D](12D-fine-grained-authz.md) |
| Cloud IAM vs app RBAC conflated | Cloud IAM = AWS/Azure resources; app RBAC = business operations |
| No group → role mapping governance | Central mapping table; access reviews |

---

## Pros and cons

### Formal IAM + RBAC for APIs

**Pros:** Single audit trail; consistent org → permission mapping; supports compliance (SOC2, ISO 27001).

**Cons:** Tooling sprawl (AD, IdP, SCIM, cloud IAM); group-to-role drift; over-permissioning when teams copy admin roles.