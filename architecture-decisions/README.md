# Architecture Decisions Guide

A practical reference for Tech Leads making lasting system-shape choices — monolith vs microservices, boundaries, DDD(Domain-Driven Design), strangler modernization, ADRs, tradeoff frameworks, integration styles, data ownership, BFF(Backend for Frontend), multi-tenancy, failure domains, and fit by org/stage/pricing.

Related: [API Design & Protection](../api-design-and-protection/README.md) · [Event Sourcing & CQRS](../event-sourcing-and-cqrs/README.md) · [High Throughput Systems](../high-throughput-systems/README.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Monolith, modular, microservices](includes/01-monolith-modular-microservices.md) |
| 1A | [Team Topologies](includes/01A-team-topologies.md) |
| 2 | [Service boundaries and decomposition](includes/02-service-boundaries-and-decomposition.md) |
| 3 | [Domain-driven design](includes/03-domain-driven-design.md) |
| 4 | [Strangler and modernization](includes/04-strangler-and-modernization.md) |
| 4A | [Modernization program (multi-quarter)](includes/04A-modernization-program.md) |
| 5 | [ADRs and design docs](includes/05-adrs-and-design-docs.md) |
| 5A | [Architecture governance (ARB)](includes/05A-architecture-governance.md) |
| 6 | [Tradeoff frameworks](includes/06-tradeoff-frameworks.md) |
| 7 | [Integration styles](includes/07-integration-styles.md) |
| 8 | [Data ownership](includes/08-data-ownership.md) |
| 9 | [BFF and API composition](includes/09-bff-and-api-composition.md) |
| 10 | [Multi-tenant system models](includes/10-multi-tenant-system-models.md) |
| 10A | [Regional cells and data residency](includes/10A-regional-cells-and-residency.md) |
| 11 | [Failure domains](includes/11-failure-domains.md) |
| 12 | [Decision guide](includes/12-decision-guide.md) |
| 13 | [Capacity estimation](includes/13-capacity-estimation.md) |
| 14 | [Org, stage, and pricing fit](includes/14-org-stage-and-pricing-fit.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Choosing system shape** | Overview → §1 Monolith/modular/microservices → [§14 Org/stage/pricing](includes/14-org-stage-and-pricing-fit.md) → §12 Decision guide |
| **Drawing service cuts** | §2 Boundaries → §3 DDD → §8 Data ownership |
| **Modernizing a legacy core** | §4 Strangler → [§4A program](includes/04A-modernization-program.md) → §7 Integration → [deployment-strategies](../deployment-strategies/README.md) |
| **Recording a hard call** | §5 ADRs → [§5A governance](includes/05A-architecture-governance.md) → §6 Tradeoffs → §12 Decision guide |
| **Aligning teams and architecture** | [§1A Team Topologies](includes/01A-team-topologies.md) → §1 → [§14](includes/14-org-stage-and-pricing-fit.md) |
| **Multi-tenant SaaS(Software as a Service)** | §10 Multi-tenant → [§10A cells/residency](includes/10A-regional-cells-and-residency.md) → [auth §2d](../auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md) → [PG §17 RLS](../postgresql-performance/includes/17-row-level-security-multi-tenant.md) → [PG §18 silos](../postgresql-performance/includes/18-schema-and-database-per-tenant.md) → [api-design §16](../api-design-and-protection/includes/16-multi-tenant-apis.md) |
| **Client-facing composition** | §9 BFF → [fullstack-bff-and-clients](../fullstack-bff-and-clients/README.md) |
| **Sizing a design before build** | [§13 Capacity estimation](includes/13-capacity-estimation.md) → [HTS §1 Little's Law](../high-throughput-systems/includes/01-measurement-and-slo.md#littles-law-in-practice) → §12 Decision guide |
| **Fitting shape to the company** | [§14 Org/stage/pricing](includes/14-org-stage-and-pricing-fit.md) → §1 → [finops §7](../finops-and-cost/includes/07-architecture-cost-tradeoffs.md) → ADR |

---

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | Contracts, gateway, async, idempotency, multi-tenant APIs |
| [api-rate-limiting](../api-rate-limiting/README.md) | Quotas and fairness at the edge |
| [high-throughput-systems](../high-throughput-systems/README.md) | Scale order, async, backpressure |
| [resilience-patterns](../resilience-patterns/README.md) | Timeouts, retries, breakers, bulkheads, placement, [checkout example](../resilience-patterns/includes/12-worked-example-checkout.md), observability |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Aggregates, outbox, sagas when boundaries need event history |
| [apache-kafka](../apache-kafka/README.md) | Event backbone for async integration |
| [postgresql-performance](../postgresql-performance/README.md) | Consistency costs, RLS(Row-Level Security), schema/DB-per-tenant, pooling |
| [auth-oauth-oidc-and-login-security](../auth-oauth-oidc-and-login-security/README.md) | B2B(Business-to-Business) IdP(Identity Provider) routing, multi-issuer, SSO(Single Sign-On) — [§2d](../auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md) |
| [database-connection-and-security](../database-connection-and-security/README.md) | Connection identity per service |
| [deployment-strategies](../deployment-strategies/README.md) | Safe rollout during strangler and cutovers |
| [fullstack-bff-and-clients](../fullstack-bff-and-clients/README.md) | Client BFF depth beyond composition pattern |
| [sre-and-incidents](../sre-and-incidents/README.md) | Blast radius in incident response |
| [cicd-and-environments](../cicd-and-environments/README.md) | Environment topology for multi-service delivery |
| [enterprise-security-compliance](../enterprise-security-compliance/README.md) | Isolation and compliance constraints on architecture |
| [tech-lead-practice](../tech-lead-practice/README.md) | Facilitation, ownership, ADR culture |
| [testing-strategy](../testing-strategy/README.md) | Contract and integration test strategy per boundary |
| [data-platforms](../data-platforms/README.md) | Analytics ownership vs OLTP(Online Transaction Processing) boundaries |
| [finops-and-cost](../finops-and-cost/README.md) | Cost of distribution and multi-region choices |
| [distributed-systems-primitives](../distributed-systems-primitives/README.md) | CAP(Consistency, Availability, Partition Tolerance)/PACELC mechanisms, hashing, IDs, consensus under tradeoff choices |
| [system-design-walkthroughs](../system-design-walkthroughs/README.md) | End-to-end practice problems that apply these decisions |
| [nosql-and-key-value-stores](../nosql-and-key-value-stores/README.md) | When the primary store is not PostgreSQL |