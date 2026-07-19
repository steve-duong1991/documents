# Fullstack BFF & Clients Guide

A practical reference for fullstack Tech Leads who own the UI↔API(Application Programming Interface) boundary: frontend architecture, rendering trade-offs, BFF(Backend for Frontend) contracts, web performance, realtime UX, accessibility, browser auth, offline/flaky networks, and design-system boundaries.

Related: [api-design-and-protection](../api-design-and-protection/README.md) (contracts, auth, async) · [architecture-decisions](../architecture-decisions/README.md) (BFF composition, boundaries, ADRs)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Frontend architecture](includes/01-frontend-architecture.md) |
| 2 | [Rendering trade-offs](includes/02-rendering-tradeoffs.md) |
| 3 | [BFF ownership](includes/03-bff-ownership.md) |
| 4 | [Web performance](includes/04-web-performance.md) |
| 5 | [Realtime UX](includes/05-realtime-ux.md) |
| 6 | [Accessibility bar](includes/06-accessibility-bar.md) |
| 7 | [Auth UX](includes/07-auth-ux.md) |
| 8 | [Offline and flaky network](includes/08-offline-and-flaky-network.md) |
| 8A | [Mobile API contracts](includes/08A-mobile-api-contracts.md) |
| 9 | [Design-system boundaries](includes/09-design-system-boundaries.md) |
| 10 | [Decision guide](includes/10-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **New fullstack TL on a product** | Overview → §3 BFF → §1 Frontend architecture → §10 |
| **Choosing SSR(Server-Side Rendering) vs SPA** | §2 Rendering → §4 Performance → §10 |
| **Shipping browser auth safely** | §7 Auth UX → [auth-oauth-oidc-and-login-security](../auth-oauth-oidc-and-login-security/README.md) → [api-design §4](../api-design-and-protection/includes/04-auth-model.md) → [enterprise-security §5](../enterprise-security-compliance/includes/05-secrets-beyond-database.md) |
| **Native mobile API surface** | [§8A Mobile API contracts](includes/08A-mobile-api-contracts.md) → §8 Offline → [auth §4a](../auth-oauth-oidc-and-login-security/includes/04A-third-party-cookies-and-mobile-redirects.md) → [api-design §14](../api-design-and-protection/includes/14-api-versioning-and-deprecation.md) |
| **Realtime or live dashboards** | §5 Realtime → [api-design §10 async](../api-design-and-protection/includes/10-async-patterns.md) |
| **Design system / multi-app UI** | §9 Design-system boundaries → §1 → §6 Accessibility |

---

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | REST(Representational State Transfer) contracts, auth, async, idempotency |
| [api-design §10 Async](../api-design-and-protection/includes/10-async-patterns.md) | Jobs, polling, webhooks, SSE(Server-Sent Events), streaming |
| [api-design §4 Auth model](../api-design-and-protection/includes/04-auth-model.md) | OAuth(Open Authorization), tokens, session patterns at the API |
| [auth-oauth-oidc-and-login-security](../auth-oauth-oidc-and-login-security/README.md) | Grants, OIDC(OpenID Connect), cookie/CSRF(Cross-Site Request Forgery) mechanics, login playbook |
| [architecture-decisions](../architecture-decisions/README.md) | System shape, ADRs, BFF composition at architecture level |
| [architecture-decisions §9 BFF](../architecture-decisions/includes/09-bff-and-api-composition.md) | When a BFF exists in the system map |
| [enterprise-security-compliance](../enterprise-security-compliance/README.md) | Secrets, CSRF(Cross-Site Request Forgery)/XSS(Cross-Site Scripting) context, compliance evidence |
| [high-throughput-systems](../high-throughput-systems/README.md) | CDN(Content Delivery Network), cache layers, edge |
| [deployment-strategies](../deployment-strategies/README.md) | Feature flags and safe UI/API rollouts |
| [api-rate-limiting](../api-rate-limiting/README.md) | Client-facing 429 UX and retry storms |