# API Design & Protection Guide

A practical reference for designing HTTP(Hypertext Transfer Protocol) APIs and protecting them in production — full request flow, load balancer vs API gateway, stack choices, auth models, rate-limit tiers, threat modeling, and OpenAPI/Swagger's role in the lifecycle.

Related: [API Rate Limiting](../api-rate-limiting/README.md) (algorithms and deployment layers in depth) · [high-throughput-systems](../high-throughput-systems/README.md) (end-to-end throughput playbook) · [tree-and-index-structures](../tree-and-index-structures/README.md) (storage engine theory)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview & full flow](includes/00-overview.md) |
| 1 | [API design best practices](includes/01-api-design.md) |
| 2 | [API protection](includes/02-api-protection.md) |
| 3 | [Load balancer, API gateway & entry architecture](includes/03-api-gateway.md) |
| 3A | [Gateway — request flows](includes/03A-api-gateway-request-flows.md) |
| 3B | [Gateway — stacks and product selection](includes/03B-api-gateway-stacks-and-selection.md) |
| 4 | [Auth model](includes/04-auth-model.md) |
| 5 | [Rate-limit tiers](includes/05-rate-limit-tiers.md) |
| 6 | [Threat model](includes/06-threat-model.md) |
| 7 | [OpenAPI / Swagger](includes/07-openapi-swagger.md) |
| 7A | [Developer portal](includes/07A-developer-portal.md) |
| 8 | [Lifecycle & reference architecture](includes/08-lifecycle-and-architecture.md) |
| 9 | [Checklist & best practices](includes/09-checklist-and-practices.md) |
| 10 | [Async patterns](includes/10-async-patterns.md) |
| 10A | [Async — jobs and polling](includes/10A-async-jobs-polling.md) |
| 10B | [Async — webhooks](includes/10B-async-webhooks.md) |
| 10C | [Async — streaming and long poll](includes/10C-async-streaming.md) |
| 10D | [Async — notification delivery](includes/10D-notification-delivery.md) |
| 10E | [Async — notification provider operations](includes/10E-notification-provider-operations.md) |
| 11 | [Stateless architecture](includes/11-stateless-architecture.md) |
| 11A | [Stateless — auth and operations](includes/11A-stateless-auth-operations.md) |
| 12 | [Identity: RBAC, IAM & Active Directory](includes/12-identity-rbac-iam-ad.md) |
| 12A | [Identity — Active Directory](includes/12A-identity-active-directory.md) |
| 12B | [Identity — API access](includes/12B-identity-enterprise-api.md) |
| 12C | [Identity — SCIM and JML provisioning](includes/12C-scim-and-jml-provisioning.md) |
| 12D | [Identity — Fine-grained AuthZ](includes/12D-fine-grained-authz.md) |
| 13 | [Idempotency](includes/13-idempotency.md) |
| 13A | [Idempotency — client and server flow](includes/13A-idempotency-client-and-server-flow.md) |
| 13B | [Idempotency — storage](includes/13B-idempotency-storage.md) |
| 13C | [Idempotency — async, webhooks, and OpenAPI](includes/13C-idempotency-integrations.md) |
| 14 | [API versioning & deprecation](includes/14-api-versioning-and-deprecation.md) |
| 15 | [Contract & schema testing](includes/15-contract-and-schema-testing.md) |
| 16 | [Multi-tenant APIs](includes/16-multi-tenant-apis.md) |
| 17 | [GraphQL and gRPC](includes/17-graphql-and-grpc.md) |
| 17A | [GraphQL in production](includes/17A-graphql-production.md) |
| 17B | [gRPC and Protobuf CI](includes/17B-grpc-and-protobuf-ci.md) |
| 18 | [Object storage and uploads](includes/18-object-storage-and-uploads.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **New to API infra** | Overview → [§3 LB vs gateway](includes/03-api-gateway.md) → [3A request flows](includes/03A-api-gateway-request-flows.md) → §11 (stateless) → §8 (reference arch) |
| **Designing the API contract** | §1 → §7 (OpenAPI) → §15 (contract CI(Continuous Integration)) → §14 (versioning) → [§13 idempotency](includes/13-idempotency.md) + [13A client flow](includes/13A-idempotency-client-and-server-flow.md) → [§10 async](includes/10-async-patterns.md) + [10A jobs](includes/10A-async-jobs-polling.md) · non-REST(Representational State Transfer) → [§17 GraphQL/gRPC](includes/17-graphql-and-grpc.md) |
| **Hardening for production** | §2 → §3 → §5 → §6 → [§13](includes/13-idempotency.md) + [13A](includes/13A-idempotency-client-and-server-flow.md) → §9 |
| **B2B(Business-to-Business) / SaaS(Software as a Service) partner API** | §4 auth → §5 tiers → [§16 multi-tenant](includes/16-multi-tenant-apis.md) → [§12 identity](includes/12-identity-rbac-iam-ad.md) + [§12C SCIM/JML](includes/12C-scim-and-jml-provisioning.md) + [api-rate-limiting §6 scope](../api-rate-limiting/includes/06-scope-identity.md) |
| **Enterprise provisioning / offboarding** | [§12C SCIM and JML](includes/12C-scim-and-jml-provisioning.md) → [§12A AD/IdP](includes/12A-identity-active-directory.md) → [auth §3b revoke](../auth-oauth-oidc-and-login-security/includes/03B-revoke-logout-denylist.md) → [auth §2d multi-tenant OIDC](../auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md) |
| **OAuth(Open Authorization) / OIDC(OpenID Connect) / login depth** | [auth-oauth-oidc-and-login-security](../auth-oauth-oidc-and-login-security/README.md) after §4 |
| **GraphQL or gRPC(Google Remote Procedure Call) API** | [§17](includes/17-graphql-and-grpc.md) → [§17A GraphQL production](includes/17A-graphql-production.md) / [§17B gRPC + protobuf CI](includes/17B-grpc-and-protobuf-ci.md) → §1 (REST baseline) → §15 (contract CI) |
| **Picking rate limits** | [api-rate-limiting](../api-rate-limiting/README.md) + §5 here |
| **Long-running or heavy endpoints** | [§10 async](includes/10-async-patterns.md) + [10A jobs + polling](includes/10A-async-jobs-polling.md) + §5 (async escape hatch) |
| **Email / push / SMS notifications** | [§10D notification delivery](includes/10D-notification-delivery.md) → [§10E provider ops](includes/10E-notification-provider-operations.md) → [§10A](includes/10A-async-jobs-polling.md) → [system-design §7](../system-design-walkthroughs/includes/07-notification-pipeline.md) |
| **Partner / public API portal** | [§7 OpenAPI](includes/07-openapi-swagger.md) → [§7A developer portal](includes/07A-developer-portal.md) → [§5 tiers](includes/05-rate-limit-tiers.md) → [§3 gateway](includes/03-api-gateway.md) |
| **Object-level / sharing AuthZ(Authorization)** | [§12D fine-grained AuthZ](includes/12D-fine-grained-authz.md) → [§12B](includes/12B-identity-enterprise-api.md) → [§4](includes/04-auth-model.md) → [§6 BOLA](includes/06-threat-model.md) |
| **File uploads / media** | [§18 Object storage and uploads](includes/18-object-storage-and-uploads.md) → §4 (auth) → §6 (SSRF/threat model) → [finops §4](../finops-and-cost/includes/04-storage-and-retention-cost.md) (cost) |
| **Audit trail / event-sourced writes** | [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) + §1 (write safety) + §8 (CQRS(Command Query Responsibility Segregation) diagram) |

---

## See also

| Guide | Topics |
|-------|--------|
| [api-rate-limiting](../api-rate-limiting/README.md) | Algorithms, deployment layers, common mistakes |
| [auth-oauth-oidc-and-login-security](../auth-oauth-oidc-and-login-security/README.md) | OAuth(Open Authorization) grants, OIDC(OpenID Connect), token lifecycle, cookie/session, login hardening |
| [apache-kafka](../apache-kafka/README.md) | Schema choice, multi-tenant topics, consumer idempotency with Kafka |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Event store, CQRS(Command Query Responsibility Segregation), outbox, audit APIs |
| [architecture-decisions](../architecture-decisions/README.md) | Tenancy models, cells/residency, boundaries, ADRs |
| [resilience-patterns](../resilience-patterns/README.md) | Timeouts, retries, breakers, load shedding, checkout example |
| [fullstack-bff-and-clients](../fullstack-bff-and-clients/README.md) | BFF(Backend for Frontend) contracts, auth UX, realtime client seam |
| [database-connection-and-security](../database-connection-and-security/README.md) | DB credentials, IAM(Identity and Access Management), vault patterns |
| [deployment-strategies](../deployment-strategies/README.md) | Safe rollout of API changes |
| [high-throughput-systems](../high-throughput-systems/README.md) | End-to-end throughput: measure, cache, async, backpressure |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | B+ vs LSM(Log-Structured Merge) storage engines for write-heavy workloads |
| [postgresql-performance](../postgresql-performance/README.md) | Read replicas, consistency, connection pooling |
| [deployment-strategies §12](../deployment-strategies/includes/12-schema-migrations-and-deploy.md) | Version routing + schema expand/contract |
| [finops-and-cost](../finops-and-cost/README.md) | Storage tiering and retention cost for uploaded objects |