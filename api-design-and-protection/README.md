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
| 4 | [Auth model](includes/04-auth-model.md) |
| 5 | [Rate-limit tiers](includes/05-rate-limit-tiers.md) |
| 6 | [Threat model](includes/06-threat-model.md) |
| 7 | [OpenAPI / Swagger](includes/07-openapi-swagger.md) |
| 8 | [Lifecycle & reference architecture](includes/08-lifecycle-and-architecture.md) |
| 9 | [Checklist & best practices](includes/09-checklist-and-practices.md) |
| 10 | [Async patterns](includes/10-async-patterns.md) |
| 10a | [Async — jobs and polling](includes/10-async-jobs-polling.md) |
| 10b | [Async — webhooks](includes/10-async-webhooks.md) |
| 10c | [Async — streaming and long poll](includes/10-async-streaming.md) |
| 11 | [Stateless architecture](includes/11-stateless-architecture.md) |
| 11a | [Stateless — auth and operations](includes/11-stateless-auth-operations.md) |
| 12 | [Identity: RBAC, IAM & Active Directory](includes/12-identity-rbac-iam-ad.md) |
| 12a | [Identity — Active Directory](includes/12-identity-active-directory.md) |
| 12b | [Identity — API access](includes/12-identity-enterprise-api.md) |
| 13 | [Idempotency](includes/13-idempotency.md) |
| 14 | [API versioning & deprecation](includes/14-api-versioning-and-deprecation.md) |
| 15 | [Contract & schema testing](includes/15-contract-and-schema-testing.md) |
| 16 | [Multi-tenant APIs](includes/16-multi-tenant-apis.md) |
| 17 | [GraphQL and gRPC](includes/17-graphql-and-grpc.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **New to API infra** | Overview → §3 (LB vs gateway) → §11 (stateless) → §8 (reference arch) |
| **Designing the API contract** | §1 → §7 (OpenAPI) → §15 (contract CI) → §14 (versioning) → §13 (idempotency) → §10 (async) |
| **Hardening for production** | §2 → §3 → §5 → §6 → §13 → §9 |
| **Picking rate limits** | [api-rate-limiting](../api-rate-limiting/README.md) + §5 here |
| **Long-running or heavy endpoints** | §10 (async patterns) + §5 (async escape hatch) |
| **Audit trail / event-sourced writes** | [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) + §1 (write safety) + §8 (CQRS(Command Query Responsibility Segregation) diagram) |

---

## See also

| Guide | Topics |
|-------|--------|
| [api-rate-limiting](../api-rate-limiting/README.md) | Algorithms, deployment layers, common mistakes |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Event store, CQRS(Command Query Responsibility Segregation), outbox, audit APIs |
| [database-connection-and-security](../database-connection-and-security/README.md) | DB credentials, IAM(Identity and Access Management), vault patterns |
| [deployment-strategies](../deployment-strategies/README.md) | Safe rollout of API changes |
| [high-throughput-systems](../high-throughput-systems/README.md) | End-to-end throughput: measure, cache, async, backpressure |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | B+ vs LSM(Log-Structured Merge) storage engines for write-heavy workloads |
| [postgresql-performance](../postgresql-performance/README.md) | Read replicas, consistency, connection pooling |
| [deployment-strategies §12](../deployment-strategies/includes/12-schema-migrations-and-deploy.md) | Version routing + schema expand/contract |