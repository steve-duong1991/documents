# OAuth, OIDC & Login Security Guide

A practical deep dive on **how clients authenticate and how logins stay safe**: OAuth(Open Authorization) 2.0 grant types, OIDC(OpenID Connect) discovery and ID tokens, SSO(Single Sign-On) and B2B(Business-to-Business) multi-tenant IdP(Identity Provider) routing, access/refresh lifecycle, cookie/session defenses, and the login playbook (passwords, lockout, MFA(Multi-Factor Authentication), device trust).

Related: [api-design-and-protection §4](../api-design-and-protection/includes/04-auth-model.md) (client-type auth matrix) · [§12 identity / RBAC](../api-design-and-protection/includes/12-identity-rbac-iam-ad.md) · [fullstack §7 Auth UX](../fullstack-bff-and-clients/includes/07-auth-ux.md) · [enterprise-security-compliance](../enterprise-security-compliance/README.md) (OWASP(Open Worldwide Application Security Project), secrets, audit)

> **Scope:** This guide owns **protocol depth and login hardening** — grant flows, OIDC discovery/claims, SSO/multi-tenant IdP routing, token validation/revocation, cookie CSRF(Cross-Site Request Forgery) mechanics, and credential attack defenses. Client-type selection and gateway AuthN(Authentication) stay in [api-design §4](../api-design-and-protection/includes/04-auth-model.md). Browser UX and BFF(Backend for Frontend) cookie patterns stay in [fullstack §7](../fullstack-bff-and-clients/includes/07-auth-ux.md). Org IAM(Identity and Access Management)/RBAC(Role-Based Access Control)/AD(Active Directory) stay in [api-design §12](../api-design-and-protection/includes/12-identity-rbac-iam-ad.md). API(Application Programming Interface)/data tenancy stays in [api-design §16](../api-design-and-protection/includes/16-multi-tenant-apis.md).

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [OAuth 2.0 grants and flows](includes/01-oauth2-grants-and-flows.md) |
| 1a | [Client authentication and token exchange](includes/01A-client-auth-and-token-exchange.md) |
| 1b | [Scopes and consent](includes/01B-scopes-and-consent.md) |
| 1c | [Pushed Authorization Requests](includes/01C-pushed-authorization-requests.md) |
| 1d | [Resource indicators](includes/01D-resource-indicators.md) |
| 1e | [Device authorization and CIBA](includes/01E-device-authorization-and-ciba.md) |
| 1f | [JAR and RAR](includes/01F-jar-and-rar.md) |
| 2 | [OIDC discovery and tokens](includes/02-oidc-discovery-and-tokens.md) |
| 2a | [OIDC logout and step-up](includes/02A-oidc-logout-and-step-up.md) |
| 2b | [SSO integration playbook](includes/02B-sso-integration-playbook.md) |
| 2c | [SAML protocol](includes/02C-saml-protocol.md) |
| 2d | [Multi-tenant OIDC and B2B SSO](includes/02D-multi-tenant-oidc-and-b2b-sso.md) |
| 3 | [Token lifecycle and validation](includes/03-token-lifecycle-and-validation.md) |
| 3a | [Token and cookie integrity (anti-tampering)](includes/03A-token-cookie-integrity.md) |
| 3b | [Revoke, force logout, and denylist](includes/03B-revoke-logout-denylist.md) |
| 3c | [Denylist Redis patterns](includes/03C-denylist-redis-patterns.md) |
| 3d | [Lifetimes and sliding sessions](includes/03D-lifetimes-and-sliding-sessions.md) |
| 3e | [Concurrent sessions and devices](includes/03E-concurrent-sessions-and-devices.md) |
| 4 | [Cookie, session, and CSRF](includes/04-cookie-session-and-csrf.md) |
| 4a | [Third-party cookies and mobile redirects](includes/04A-third-party-cookies-and-mobile-redirects.md) |
| 4b | [Anonymous and guest sessions](includes/04B-anonymous-and-guest-sessions.md) |
| 5 | [Login security playbook](includes/05-login-security-playbook.md) |
| 5a | [Auth testing checklist](includes/05A-auth-testing-checklist.md) |
| 5b | [Signup, email verification, and magic links](includes/05B-signup-verify-and-magic-links.md) |
| 5c | [WebAuthn and passkeys](includes/05C-webauthn-and-passkeys.md) |
| 5d | [Impersonation and support access](includes/05D-impersonation-and-support-access.md) |
| 6 | [Decision guide](includes/06-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Adding SSO(Single Sign-On) / social login** | Overview → §1 → [§2b SSO playbook](includes/02B-sso-integration-playbook.md) → §2 OIDC → [§2a logout](includes/02A-oidc-logout-and-step-up.md) → [§3d lifetimes](includes/03D-lifetimes-and-sliding-sessions.md) → §6 |
| **B2B SaaS(Software as a Service) with per-customer IdP** | [§2b SSO](includes/02B-sso-integration-playbook.md) → [§2d multi-tenant OIDC](includes/02D-multi-tenant-oidc-and-b2b-sso.md) → [api-design §12C SCIM/JML](../api-design-and-protection/includes/12C-scim-and-jml-provisioning.md) → [§16](../api-design-and-protection/includes/16-multi-tenant-apis.md) → [§12 identity](../api-design-and-protection/includes/12-identity-rbac-iam-ad.md) → §6 |
| **Enterprise SAML(Security Assertion Markup Language) customer** | [§2c SAML](includes/02C-saml-protocol.md) → [§2b bridge](includes/02B-sso-integration-playbook.md) → [§2d](includes/02D-multi-tenant-oidc-and-b2b-sso.md) if multi-tenant → §4 session |
| **First-party web app (cookie session)** | §4 → [§4a](includes/04A-third-party-cookies-and-mobile-redirects.md) → [§4b guest](includes/04B-anonymous-and-guest-sessions.md) → [§3d lifetimes](includes/03D-lifetimes-and-sliding-sessions.md) → [fullstack §7](../fullstack-bff-and-clients/includes/07-auth-ux.md) → §5 |
| **SPA or mobile with PKCE(Proof Key for Code Exchange)** | §1 → [§4a](includes/04A-third-party-cookies-and-mobile-redirects.md) → §2 → §3 → [§3a](includes/03A-token-cookie-integrity.md) → [§3d](includes/03D-lifetimes-and-sliding-sessions.md) → §6 |
| **BFF calling APIs as the user** | [§1a](includes/01A-client-auth-and-token-exchange.md) → §4 → §3 |
| **Scopes / partner consent** | [§1b](includes/01B-scopes-and-consent.md) → §1 → [api-design §4](../api-design-and-protection/includes/04-auth-model.md) |
| **Hardening authorize URLs / multi-API(Application Programming Interface) tokens** | [§1c PAR](includes/01C-pushed-authorization-requests.md) → [§1d resource indicators](includes/01D-resource-indicators.md) → [§1f JAR/RAR](includes/01F-jar-and-rar.md) → §3 |
| **TV / CLI / decoupled AuthN** | [§1e Device + CIBA](includes/01E-device-authorization-and-ciba.md) → §1 → §3 |
| **Guest cart / signup wizard** | [§4b Anonymous/guest](includes/04B-anonymous-and-guest-sessions.md) → [§5b Signup/magic link](includes/05B-signup-verify-and-magic-links.md) → §4 |
| **Passkeys / phishing-resistant MFA** | [§5c WebAuthn](includes/05C-webauthn-and-passkeys.md) → §5 → [§2a step-up](includes/02A-oidc-logout-and-step-up.md) |
| **Support “login as user”** | [§5d Impersonation](includes/05D-impersonation-and-support-access.md) → [§3e sessions](includes/03E-concurrent-sessions-and-devices.md) |
| **Logout other devices / session caps** | [§3e](includes/03E-concurrent-sessions-and-devices.md) → [§3b](includes/03B-revoke-logout-denylist.md) |
| **Multi-app SSO logout / step-up MFA** | [§2a](includes/02A-oidc-logout-and-step-up.md) → [§3b](includes/03B-revoke-logout-denylist.md) → §5 |
| **Hardening password login** | §5 → [§5b](includes/05B-signup-verify-and-magic-links.md) → [enterprise-security §3](../enterprise-security-compliance/includes/03-owasp-and-common-vulns.md) → §6 |
| **API(Application Programming Interface) gateway / B2B tokens** | [api-design §4](../api-design-and-protection/includes/04-auth-model.md) → §3 → [§3a](includes/03A-token-cookie-integrity.md) → [§12 RBAC](../api-design-and-protection/includes/12-identity-rbac-iam-ad.md) |
| **“Can the client rewrite the token?”** | [§3a](includes/03A-token-cookie-integrity.md) → §3 → §4 |
| **Force logout / ban / denylist** | [§3b](includes/03B-revoke-logout-denylist.md) → [§3c](includes/03C-denylist-redis-patterns.md) → §3 → §4 |
| **CI(Continuous Integration) auth regression suite** | [§5a testing](includes/05A-auth-testing-checklist.md) → [testing-strategy](../testing-strategy/README.md) |

---

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection §4 Auth model](../api-design-and-protection/includes/04-auth-model.md) | Which auth model per client type |
| [api-design §11A Stateless auth](../api-design-and-protection/includes/11A-stateless-auth-operations.md) | JWT(JSON Web Token) vs session store; sticky-session migration |
| [api-design §12 Identity / RBAC](../api-design-and-protection/includes/12-identity-rbac-iam-ad.md) | Roles, IAM lifecycle, AD/IdP mapping |
| [api-design §12C SCIM/JML](../api-design-and-protection/includes/12C-scim-and-jml-provisioning.md) | Provisioning / offboarding |
| [api-design §12D fine-grained AuthZ](../api-design-and-protection/includes/12D-fine-grained-authz.md) | Object-level / ReBAC(Relationship-Based Access Control) vs JWT claims |
| [api-design §16 multi-tenant](../api-design-and-protection/includes/16-multi-tenant-apis.md) | Claim binding, cache/queue tenancy |
| [architecture §10 / §10A](../architecture-decisions/includes/10-multi-tenant-system-models.md) | Pool vs silo; cells / residency |
| [fullstack-bff-and-clients §7 Auth UX](../fullstack-bff-and-clients/includes/07-auth-ux.md) | Browser storage, re-auth UX, CSRF from the UI lens |
| [enterprise-security-compliance §3](../enterprise-security-compliance/includes/03-owasp-and-common-vulns.md) | Broken AuthN/session in OWASP(Open Worldwide Application Security Project) context |
| [enterprise-security §5 Secrets](../enterprise-security-compliance/includes/05-secrets-beyond-database.md) | JWT/OIDC signing keys, rotation |
| [testing-strategy](../testing-strategy/README.md) | Where to place auth tests in the pyramid · [§5a checklist](includes/05A-auth-testing-checklist.md) |
| [database-connection-and-security](../database-connection-and-security/README.md) | Cloud IAM for workloads (not end-user login) |
| [cicd-and-environments §3](../cicd-and-environments/includes/03-config-vs-secrets.md) | OIDC federation for CI(Continuous Integration) to cloud |