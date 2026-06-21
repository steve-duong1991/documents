# API(Application Programming Interface) Design & Protection Guide

A practical reference for designing HTTP(Hypertext Transfer Protocol) APIs and protecting them in production — full request flow, load balancer vs API gateway, stack choices, auth models, rate-limit tiers, threat modeling, and OpenAPI/Swagger's role in the lifecycle.

Related: [API Rate Limiting](../api-rate-limiting/README.md) (algorithms and deployment layers in depth) · [high-throughput-systems](../high-throughput-systems/README.md) (end-to-end throughput playbook) · [tree-and-index-structures](../tree-and-index-structures/README.md) (storage engine theory)

---

## Table of contents

| # | Topic | Include file |
|---|-------|--------------|
| — | [Overview & full flow](#overview--full-flow) | [includes/00-overview.md](includes/00-overview.md) |
| 1 | [API design best practices](#1-api-design-best-practices) | [includes/01-api-design.md](includes/01-api-design.md) |
| 2 | [API protection](#2-api-protection) | [includes/02-api-protection.md](includes/02-api-protection.md) |
| 3 | [Load balancer, API gateway & entry architecture](#3-load-balancer-api-gateway--entry-architecture) | [includes/03-api-gateway.md](includes/03-api-gateway.md) |
| 4 | [Auth model](#4-auth-model) | [includes/04-auth-model.md](includes/04-auth-model.md) |
| 5 | [Rate-limit tiers](#5-rate-limit-tiers) | [includes/05-rate-limit-tiers.md](includes/05-rate-limit-tiers.md) |
| 6 | [Threat model](#6-threat-model) | [includes/06-threat-model.md](includes/06-threat-model.md) |
| 7 | [OpenAPI / Swagger](#7-openapi--swagger) | [includes/07-openapi-swagger.md](includes/07-openapi-swagger.md) |
| 8 | [Lifecycle & reference architecture](#8-lifecycle--reference-architecture) | [includes/08-lifecycle-and-architecture.md](includes/08-lifecycle-and-architecture.md) |
| 9 | [Checklist & best practices](#9-checklist--best-practices) | [includes/09-checklist-and-practices.md](includes/09-checklist-and-practices.md) |
| 10 | [Async patterns](#10-async-patterns) | [includes/10-async-patterns.md](includes/10-async-patterns.md) |
| 11 | [Stateless architecture](#11-stateless-architecture) | [includes/11-stateless-architecture.md](includes/11-stateless-architecture.md) |
| 12 | [Identity: RBAC, IAM & Active Directory](#12-identity-rbac-iam--active-directory) | [includes/12-identity-rbac-iam-ad.md](includes/12-identity-rbac-iam-ad.md) |
| 13 | [Idempotency](#13-idempotency) | [includes/13-idempotency.md](includes/13-idempotency.md) |
| 14 | [API versioning & deprecation](#14-api-versioning--deprecation) | [includes/14-api-versioning-and-deprecation.md](includes/14-api-versioning-and-deprecation.md) |
| 15 | [Contract & schema testing](#15-contract--schema-testing) | [includes/15-contract-and-schema-testing.md](includes/15-contract-and-schema-testing.md) |
| 16 | [Multi-tenant APIs](#16-multi-tenant-apis) | [includes/16-multi-tenant-apis.md](includes/16-multi-tenant-apis.md) |
| 17 | [GraphQL and gRPC](#17-graphql-and-grpc) | [includes/17-graphql-and-grpc.md](includes/17-graphql-and-grpc.md) |

> **Tip:** Open [GUIDE.md](GUIDE.md) for the full combined document in one file.

---

## Overview & full flow

End-to-end flow from client → edge (WAF(Web Application Firewall)/DDoS) → gateway (auth, rate limits) → load balancer (health checks) → application (AuthZ, business logic) → data and observability.

See full details → [includes/00-overview.md](includes/00-overview.md)

---

## 1. API design best practices

Resource-oriented URLs, HTTP semantics, versioning, pagination, idempotency, and standard error shapes — with pros/cons of REST(Representational State Transfer) vs GraphQL vs gRPC.

See full details → [includes/01-api-design.md](includes/01-api-design.md)

---

## 2. API protection

Layered defense: TLS(Transport Layer Security), AuthN/AuthZ, validation, rate limiting, logging, fail-open vs fail-closed.

See full details → [includes/02-api-protection.md](includes/02-api-protection.md)

---

## 3. Load balancer, API gateway & entry architecture

**Start here if you're choosing infrastructure.**

| Section | What you'll learn |
|---------|-------------------|
| [At a glance](includes/03-api-gateway.md#at-a-glance) | LB vs gateway in one table |
| [Comparison & when to use](includes/03-api-gateway.md#load-balancer-vs-api-gateway) | Roles, overlap, service mesh |
| [Request flows](includes/03-api-gateway.md#request-flows) | LB only, gateway only, both, sequence diagram |
| [Tech stacks](includes/03-api-gateway.md#tech-stacks-by-scenario) | AWS, K8s, B2B, MVP, self-hosted |
| [Gateway products](includes/03-api-gateway.md#choosing-an-api-gateway-product) | Kong, AWS, APIM, Cloudflare matrix |

See full details → [includes/03-api-gateway.md](includes/03-api-gateway.md)

---

## 4. Auth model

OAuth(Open Authorization) + PKCE(Proof Key for Code Exchange), API keys, JWT(JSON Web Token), mTLS(Mutual Transport Layer Security), webhook HMAC(Hash-based Message Authentication Code) — mapped by client type with layered AuthN/AuthZ flow. Enterprise identity (RBAC(Role-Based Access Control), IAM(Identity and Access Management), AD(Active Directory)) → [§12](includes/12-identity-rbac-iam-ad.md).

See full details → [includes/04-auth-model.md](includes/04-auth-model.md)

---

## 5. Rate-limit tiers

Free → Enterprise quotas, per-endpoint multipliers, response headers, and async escape hatch for heavy work.

See full details → [includes/05-rate-limit-tiers.md](includes/05-rate-limit-tiers.md)

---

## 6. Threat model

STRIDE(Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) + OWASP(Open Worldwide Application Security Project) API Security Top 10 mapped to controls; trust zones and threat modeling workshop steps.

See full details → [includes/06-threat-model.md](includes/06-threat-model.md)

---

## 7. OpenAPI / Swagger

Where Swagger fits in design, build, deploy, and operate — and what it does **not** enforce at runtime.

See full details → [includes/07-openapi-swagger.md](includes/07-openapi-swagger.md)

---

## 8. Lifecycle & reference architecture

Design → build → deploy → operate loop; public SaaS reference stack (edge → gateway → LB → services); MVP evolution path.

See full details → [includes/08-lifecycle-and-architecture.md](includes/08-lifecycle-and-architecture.md)

---

## 9. Checklist & best practices

Pre-launch checklist, common mistakes, observability, and links to related guides in this repo.

See full details → [includes/09-checklist-and-practices.md](includes/09-checklist-and-practices.md)

---

## 10. Async patterns

Job resources, polling, webhooks, SSE(Server-Sent Events), and streaming — with flows, HTTP contracts, rate-limit strategy, idempotency, and OpenAPI modeling for long-running work.

See full details → [includes/10-async-patterns.md](includes/10-async-patterns.md)

---

## 11. Stateless architecture

Why stateless app tiers enable horizontal scaling, safe deploys, and load-balancer freedom — with flows, externalized state patterns, JWT auth, pros/cons, and migration steps.

See full details → [includes/11-stateless-architecture.md](includes/11-stateless-architecture.md)

---

## 12. Identity: RBAC(Role-Based Access Control), IAM & Active Directory

Enterprise identity foundations: IAM lifecycle, RBAC role mapping, Active Directory structure, AD/Entra → JWT → gateway enforcement, and decision flows for API access.

See full details → [includes/12-identity-rbac-iam-ad.md](includes/12-identity-rbac-iam-ad.md)

---

## 13. Idempotency

Safe retries on writes: HTTP semantics, `Idempotency-Key`, Redis/DB storage, concurrent duplicates, async job dedup, webhooks, and OpenAPI modeling.

See full details → [includes/13-idempotency.md](includes/13-idempotency.md)

---

## 14. API versioning & deprecation

URL vs header versioning, breaking vs non-breaking changes, `Sunset` headers, and gateway routing.

See full details → [includes/14-api-versioning-and-deprecation.md](includes/14-api-versioning-and-deprecation.md)

---

## 15. Contract & schema testing

Spectral lint, OpenAPI breaking diff in CI, and consumer-driven contracts (Pact).

See full details → [includes/15-contract-and-schema-testing.md](includes/15-contract-and-schema-testing.md)

---

## 16. Multi-tenant APIs

Tenant isolation in tokens, data, cache keys, rate limits, and residency.

See full details → [includes/16-multi-tenant-apis.md](includes/16-multi-tenant-apis.md)

---

## 17. GraphQL and gRPC

When to use alternative API styles vs REST; BFF(Backend for Frontend) GraphQL and internal gRPC patterns.

See full details → [includes/17-graphql-and-grpc.md](includes/17-graphql-and-grpc.md)

---

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
| [database-connection-and-security](../database-connection-and-security/README.md) | DB credentials, IAM, vault patterns |
| [deployment-strategies](../deployment-strategies/README.md) | Safe rollout of API changes |
| [high-throughput-systems](../high-throughput-systems/README.md) | End-to-end throughput: measure, cache, async, backpressure |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | B+ vs LSM(Log-Structured Merge) storage engines for write-heavy workloads |
| [postgresql-performance](../postgresql-performance/README.md) | Read replicas, consistency, connection pooling |
| [deployment-strategies §12](../deployment-strategies/includes/12-schema-migrations-and-deploy.md) | Version routing + schema expand/contract |
