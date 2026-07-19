# Auth Testing Checklist

What to automate so OAuth(Open Authorization), OIDC(OpenID Connect), cookies, and revoke paths don’t regress. Pair with [testing-strategy](../../testing-strategy/README.md) for pyramid placement.

> **Scope:** Test cases and gates for auth. Protocols → [§1](01-oauth2-grants-and-flows.md)–[§2](02-oidc-discovery-and-tokens.md). CSRF(Cross-Site Request Forgery)/cookies → [§4](04-cookie-session-and-csrf.md). Guest → [§4b](04B-anonymous-and-guest-sessions.md). Revoke/denylist → [§3b](03B-revoke-logout-denylist.md), [§3c](03C-denylist-redis-patterns.md). Lifetimes → [§3d](03D-lifetimes-and-sliding-sessions.md). Concurrent devices → [§3e](03E-concurrent-sessions-and-devices.md). Signup/magic → [§5b](05B-signup-verify-and-magic-links.md). WebAuthn(Web Authentication) → [§5c](05C-webauthn-and-passkeys.md). Impersonation → [§5d](05D-impersonation-and-support-access.md). SAML(Security Assertion Markup Language) → [§2c](02C-saml-protocol.md).

---

## Where tests live

| Layer | Auth examples |
|-------|----------------|
| **Unit** | JWT(JSON Web Token) claim validators; RelayState allowlist; scope parser |
| **Contract** | Token introspection / JWKS(JSON Web Key Set) shapes; OpenAPI security schemes |
| **Integration** | Auth Code + PKCE(Proof Key for Code Exchange) against test IdP; session create/destroy |
| **E2E** | Login → call API(Application Programming Interface) → logout; step-up; expired session redirect |
| **Security / negative** | Tampered JWT; CSRF without token; reused refresh; open redirect |

---

## Checklist — OAuth / OIDC

- [ ] Authorization Code + PKCE happy path issues tokens  
- [ ] PAR(Pushed Authorization Requests) path (if enabled): push → authorize with `request_uri` only — [§1c](01C-pushed-authorization-requests.md)  
- [ ] Wrong `code_verifier` → token endpoint error  
- [ ] `state` mismatch → reject callback  
- [ ] Redirect URI not in allowlist → reject  
- [ ] ID token: bad sig / wrong `aud` / wrong `iss` / bad `nonce` → reject — [§2](02-oidc-discovery-and-tokens.md)  
- [ ] Access token wrong `aud` / wrong resource → API 401 — [§1d](01D-resource-indicators.md)  
- [ ] Token for API A rejected on API B  
- [ ] Implicit / password grant endpoints disabled  
- [ ] Confidential client without client auth fails `/token` — [§1a](01A-client-auth-and-token-exchange.md)  

---

## Checklist — cookies / session / CSRF

- [ ] Session cookie `HttpOnly` + `Secure` + `SameSite` set  
- [ ] Mutating request without CSRF → 403  
- [ ] CSRF valid + session → success  
- [ ] Logout clears cookie **and** server `sid` — [§3b](03B-revoke-logout-denylist.md)  
- [ ] Stolen `sid` after `DEL` session → 401  
- [ ] Session fixation: `sid` rotates on login  
- [ ] Guest promote rotates `sid`; old guest sid → 401 — [§4b](04B-anonymous-and-guest-sessions.md)  
- [ ] Guest cannot call privileged routes  

---

## Checklist — lifetimes / re-auth

- [ ] Access token past `exp` → 401  
- [ ] Idle expiry → re-auth path (interactive or top-level OIDC) — [§3d](03D-lifetimes-and-sliding-sessions.md)  
- [ ] Absolute expiry → does **not** silently re-establish a full session via SSO(Single Sign-On) without policy  
- [ ] Sliding idle extends idle but not absolute  

---

## Checklist — revoke / denylist

- [ ] `jti` on denylist → 401 within TTL — [§3c](03C-denylist-redis-patterns.md)  
- [ ] Refresh reuse → family revoke  
- [ ] User disabled → cannot refresh / new session  
- [ ] Logout-all invalidates other devices’ `sid`s  
- [ ] Logout-others keeps current `sid` only — [§3e](03E-concurrent-sessions-and-devices.md)  

---

## Checklist — signup / magic / WebAuthn / impersonation

- [ ] Verify / magic token reuse → fail — [§5b](05B-signup-verify-and-magic-links.md)  
- [ ] Magic request returns generic message (anti-enumeration)  
- [ ] WebAuthn: bad challenge / wrong origin → reject — [§5c](05C-webauthn-and-passkeys.md)  
- [ ] Impersonation without role → 403; expired grant → 401 — [§5d](05D-impersonation-and-support-access.md)  
- [ ] Impersonation cannot change subject password/MFA(Multi-Factor Authentication)  

---

## Checklist — step-up / SSO / SAML

- [ ] Sensitive route without fresh `acr`/`auth_time` → challenge — [§2a](02A-oidc-logout-and-step-up.md)  
- [ ] Account link requires verified email + confirmation — [§2b](02B-sso-integration-playbook.md)  
- [ ] SAML: unsigned assertion rejected; bad Audience rejected — [§2c](02C-saml-protocol.md)  
- [ ] SAML RelayState open redirect rejected  

---

## Checklist — multi-tenant OIDC / B2B

- [ ] Callback with wrong `iss` for resolved tenant → reject — [§2d](02D-multi-tenant-oidc-and-b2b-sso.md)  
- [ ] Token for tenant A used on tenant B URL/session → 401/403  
- [ ] Client-supplied `tenant_id` alone cannot escalate membership  
- [ ] Ambiguous email domain → org picker (not silent join)  
- [ ] Tenant switch re-binds access/refresh (old Bearer fails object AuthZ)  

---

## Checklist — mobile / browser edge

- [ ] Custom scheme alone not accepted in prod config if App Links required — [§4a](04A-third-party-cookies-and-mobile-redirects.md)  
- [ ] No dependency on hidden iframe silent renew in E2E  

---

## CI gates (suggested)

| Gate | Block merge if |
|------|----------------|
| Unit + integration auth suite | Any failure on main paths |
| Contract: security schemes | API adds route without AuthN annotation |
| Secret scan | Tokens/certs committed |
| Periodic | Dependency CVE on SAML/JWT libraries |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Only testing happy login | Negative cases find the vulns |
| Sharing one long-lived test user refresh in CI | Ephemeral users / containerized IdP |
| E2E only against prod IdP | Stub/test tenant; record/replay carefully |
| Skipping logout/deny tests | Regressions = stuck sessions |

**Bottom line:** automate **negative** auth paths (tamper, CSRF, reuse, expiry, deny) as seriously as the login happy path.