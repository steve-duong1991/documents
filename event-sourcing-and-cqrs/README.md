# Event Sourcing & CQRS Guide

A practical reference for Event Sourcing and CQRS — append-only event stores, aggregates, read projections, storage choices, API(Application Programming Interface) design, async integration (outbox), sagas, and when to adopt vs stay with CRUD.

Related: [API Design & Protection](../api-design-and-protection/README.md) · [PostgreSQL Performance](../postgresql-performance/README.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Core concepts](includes/01-core-concepts.md) |
| 2 | [CQRS and read models](includes/02-cqrs-and-read-models.md) |
| 3 | [Storage and projections](includes/03-storage-and-projections.md) |
| 4 | [API design implications](includes/04-api-design-implications.md) |
| 5 | [Async integration](includes/05-async-integration.md) |
| 6 | [Decision guide](includes/06-decision-guide.md) |
| 7 | [Sagas and distributed workflows](includes/07-sagas-and-distributed-workflows.md) |
| 8 | [Event schema evolution](includes/08-event-schema-evolution.md) |
| 9 | [Testing and verification](includes/09-testing-and-verification.md) |

> **On GitHub:** Click a topic in the table above for the full section. [GUIDE.md](GUIDE.md) combines all sections in one file.

---

## Overview

CRUD vs Event Sourcing, core vocabulary, when teams reach for the pattern, and default storage recommendation.

See full details → [includes/00-overview.md](includes/00-overview.md)

---

## 1. Core concepts

Command handling, aggregate replay, optimistic concurrency, immutability, and Event Sourcing vs event-driven architecture.

See full details → [includes/01-core-concepts.md](includes/01-core-concepts.md)

---

## 2. CQRS and read models

Command/query split, projectors, eventual consistency, and multiple projections from one stream.

See full details → [includes/02-cqrs-and-read-models.md](includes/02-cqrs-and-read-models.md)

---

## 3. Storage and projections

PostgreSQL event tables, EventStoreDB, snapshots, retention, and where not to store authoritative events.

See full details → [includes/03-storage-and-projections.md](includes/03-storage-and-projections.md)

---

## 4. API design implications

Command vs query APIs, status codes, `If-Match` / `409`, audit/history endpoints, and gateway routing.

See full details → [includes/04-api-design-implications.md](includes/04-api-design-implications.md)

---

## 5. Async integration

Transactional outbox, message bus fan-out, webhooks, and combining domain events with job resources.

See full details → [includes/05-async-integration.md](includes/05-async-integration.md)

---

## 6. Decision guide

Use cases, pros/cons, migration path, storage and API quick picks, and reading paths.

See full details → [includes/06-decision-guide.md](includes/06-decision-guide.md)

---

## 7. Sagas and distributed workflows

Choreography vs orchestration, compensating transactions, saga state machines, idempotency across steps, and order-fulfillment examples.

See full details → [includes/07-sagas-and-distributed-workflows.md](includes/07-sagas-and-distributed-workflows.md)

---

## 8. Event schema evolution

Upcasting, version metadata, projector compatibility, and deploy order for historical events.

See full details → [includes/08-event-schema-evolution.md](includes/08-event-schema-evolution.md)

---

## 9. Testing and verification

Aggregate, projector, outbox, and saga test patterns plus CI checklist.

See full details → [includes/09-testing-and-verification.md](includes/09-testing-and-verification.md)

---

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Evaluating Event Sourcing** | Overview → §6 Decision guide |
| **Implementing write path** | §1 Core concepts → §3 Storage |
| **Building public APIs on ES** | §4 API design → [api-design-and-protection](../api-design-and-protection/README.md) §1, §10 |
| **Microservice integration** | §5 Async integration → §7 Sagas → [async patterns](../api-design-and-protection/includes/10-async-patterns.md) |

---

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | HTTP(Hypertext Transfer Protocol) contracts, async, idempotency, audit APIs |
| [high-throughput-systems](../high-throughput-systems/README.md) | Streaming, outbox at scale, read-model throughput |
| [database-connection-and-security](../database-connection-and-security/README.md) | Event store connection identity and secrets |
| [deployment-strategies](../deployment-strategies/README.md) | Rolling deploys with projector compatibility |
| [deployment-strategies §12](../deployment-strategies/includes/12-schema-migrations-and-deploy.md) | Projector order during rollout |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | Append-heavy event store storage |