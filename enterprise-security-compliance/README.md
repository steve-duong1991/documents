# Enterprise Security & Compliance Guide

A practical reference for engineering teams who own secure delivery, threat modeling beyond the API(Application Programming Interface) edge, supply-chain controls, secrets outside the database path, audit/PII(Personally Identifiable Information) handling, encryption policy, zero trust, and SOC 2–style evidence.

Related: [api-design-and-protection](../api-design-and-protection/README.md) (threat model, identity) · [database-connection-and-security](../database-connection-and-security/README.md) (DB credentials, TLS(Transport Layer Security), vault patterns)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Secure SDLC](includes/01-secure-sdlc.md) |
| 2 | [Threat modeling process](includes/02-threat-modeling-process.md) |
| 3 | [OWASP and common vulns](includes/03-owasp-and-common-vulns.md) |
| 4 | [Supply-chain security](includes/04-supply-chain-security.md) |
| 5 | [Secrets beyond the database](includes/05-secrets-beyond-database.md) |
| 6 | [Audit logging and retention](includes/06-audit-logging-and-retention.md) |
| 7 | [PII and data classification](includes/07-pii-and-data-classification.md) |
| 7A | [Erasure and DSAR playbook](includes/07A-erasure-and-dsar.md) |
| 7B | [Consent and purpose limitation](includes/07B-consent-and-purpose-limitation.md) |
| 8 | [Encryption policy](includes/08-encryption-policy.md) |
| 8A | [Application encryption and KMS operations](includes/08A-application-encryption-and-kms.md) |
| 9 | [Zero trust and least privilege](includes/09-zero-trust-least-privilege.md) |
| 9A | [Workload identity and mTLS](includes/09A-workload-identity-and-mtls.md) |
| 10 | [Compliance evidence](includes/10-compliance-evidence.md) |
| 11 | [Decision guide](includes/11-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **New to org security expectations** | Overview → §1 Secure SDLC(Software Development Life Cycle) → §10 Compliance evidence → §11 |
| **Hardening a product before launch** | §2 Threat modeling → §3 OWASP(Open Worldwide Application Security Project) → §5 Secrets → §9 Zero trust |
| **Preparing for SOC 2 / customer questionnaires** | §6 Audit → §7 PII → [§7A erasure/DSAR](includes/07A-erasure-and-dsar.md) → §8 Encryption → §10 Evidence |
| **Fulfilling access / erasure requests** | [§7A Erasure and DSAR](includes/07A-erasure-and-dsar.md) → §7 classification → [api-design §12C](../api-design-and-protection/includes/12C-scim-and-jml-provisioning.md) |
| **Owning CI(Continuous Integration)/CD(Continuous Delivery) and dependencies** | §1 Secure SDLC → §4 Supply chain → §5 Secrets |

---

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | Edge protection, auth, STRIDE(Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) for APIs, identity |
| [api-design §12C SCIM/JML](../api-design-and-protection/includes/12C-scim-and-jml-provisioning.md) | Provisioning / offboarding automation |
| [auth-oauth-oidc-and-login-security](../auth-oauth-oidc-and-login-security/README.md) | OAuth(Open Authorization)/OIDC(OpenID Connect), cookies/sessions, password login hardening |
| [auth §2d multi-tenant OIDC](../auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md) | B2B(Business-to-Business) IdP(Identity Provider) routing / multi-issuer |
| [api-design §6 Threat model](../api-design-and-protection/includes/06-threat-model.md) | API-focused STRIDE + OWASP(Open Worldwide Application Security Project) API Top 10 |
| [database-connection-and-security](../database-connection-and-security/README.md) | DB credentials, IAM(Identity and Access Management), vault, rotation |
| [deployment-strategies](../deployment-strategies/README.md) | Safe rollout; gate security checks with deploys |
| [high-throughput-systems §11](../high-throughput-systems/includes/11-observability.md) | Logs, metrics, traces for security signals |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Append-only audit when domain history is the control |
| [apache-kafka](../apache-kafka/README.md) | Bus retention, tiered storage, ACLs/quotas, event catalog classification for PII topics |
| [fullstack-bff-and-clients](../fullstack-bff-and-clients/README.md) | Browser CSRF(Cross-Site Request Forgery), auth UX, client secrets pitfalls |