# Testing Strategy Guide

A practical reference for choosing what to automate, where each test layer pays off, and how quality gates and production verification keep releases honest.

Related: [api-design §15 contract testing](../api-design-and-protection/includes/15-contract-and-schema-testing.md) · [cicd-and-environments](../cicd-and-environments/README.md) · [event-sourcing §9 testing](../event-sourcing-and-cqrs/includes/09-testing-and-verification.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Test pyramid and diamond](includes/01-test-pyramid-and-diamond.md) |
| 2 | [What not to automate](includes/02-what-not-to-automate.md) |
| 3 | [Contract testing boundaries](includes/03-contract-testing-boundaries.md) |
| 4 | [Integration and E2E](includes/04-integration-and-e2e.md) |
| 5 | [Load, soak, and resilience tests](includes/05-load-soak-resilience-tests.md) |
| 6 | [Flaky test management](includes/06-flaky-test-management.md) |
| 7 | [Quality gates](includes/07-quality-gates.md) |
| 8 | [Production verification](includes/08-production-verification.md) |
| 9 | [Decision guide](includes/09-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | OpenAPI lifecycle, Pact/Spectral CI(Continuous Integration), versioning |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Aggregate, projector, outbox, and saga tests |
| [apache-kafka](../apache-kafka/README.md) | Broker/integration testing and schema contracts |
| [cicd-and-environments](../cicd-and-environments/README.md) | Pipeline stages, promotion, quality gates wiring |
| [auth-oauth-oidc-and-login-security §5a](../auth-oauth-oidc-and-login-security/includes/05A-auth-testing-checklist.md) | Auth/OIDC(OpenID Connect)/CSRF(Cross-Site Request Forgery)/revoke negative test checklist |
| [deployment-strategies](../deployment-strategies/README.md) | Canary, progressive delivery, SLO(Service Level Objective) rollback |
| [resilience-patterns](../resilience-patterns/README.md) | Timeouts, retries, chaos — what resilience tests prove |
| [sre-and-incidents](../sre-and-incidents/README.md) | Capacity planning, synthetics, error budgets |
| [tech-lead-practice](../tech-lead-practice/README.md) | Definition of done, review standards, ownership |
| [high-throughput-systems](../high-throughput-systems/README.md) | Load shapes, backpressure, observability |