# Engineering Guides

Practical reference docs for building and operating production APIs and data systems. Each guide has a **README** (table of contents linking to sections) and **`includes/*.md`** (full articles).

> **Reading on GitHub:** Start from [learning paths](#learning-paths) or a guide README — **click a topic in the table** to open the full section file. Acronym expansions appear on first use in each file (`CDC(Change Data Capture)`).

---

## Guides at a glance

| Guide | What it covers |
|-------|----------------|
| [api-design-and-protection](api-design-and-protection/README.md) | REST(Representational State Transfer) design, protection, gateway, auth, identity, async, idempotency, stateless architecture |
| [api-rate-limiting](api-rate-limiting/README.md) | Limiter algorithms, scope, deployment layers, response strategies |
| [database-connection-and-security](database-connection-and-security/README.md) | DB credentials, TLS(Transport Layer Security), Vault, cloud IAM(Identity and Access Management), PgBouncer, production connection patterns |
| [deployment-strategies](deployment-strategies/README.md) | Rolling, blue/green, canary, feature flags, GitOps(Git Operations), progressive delivery |
| [event-sourcing-and-cqrs](event-sourcing-and-cqrs/README.md) | Event store, aggregates, CQRS(Command Query Responsibility Segregation), projections, outbox, sagas, API(Application Programming Interface) implications |
| [high-throughput-systems](high-throughput-systems/README.md) | End-to-end throughput: measure, cache, async, streaming, backpressure, scale |
| [postgresql-performance](postgresql-performance/README.md) | Measurement, indexing, queries, vacuum, pooling, replicas, bulk ops, consistency |
| [tree-and-index-structures](tree-and-index-structures/README.md) | B+, LSM(Log-Structured Merge), in-memory trees, specialized structures, decision guides |

---

## How the guides relate

```mermaid
flowchart LR
    subgraph api [Public API]
        A[api-design-and-protection]
        R[api-rate-limiting]
        D[deployment-strategies]
    end
    subgraph perf [Performance]
        H[high-throughput-systems]
        P[postgresql-performance]
        T[tree-and-index-structures]
    end
    subgraph advanced [Advanced patterns]
        E[event-sourcing-and-cqrs]
    end
    subgraph ops [Data layer security]
        S[database-connection-and-security]
    end
    A --> R
    A --> H
    H --> P
    P --> T
    A --> E
    P --> S
    A --> S
    H --> D
    A --> D
```

---

## Learning paths

### Ship a public API

Design the contract, protect the edge, connect to the database safely, and deploy without downtime.

1. [api-design-and-protection](api-design-and-protection/README.md) — design, gateway ([§3 hub](api-design-and-protection/includes/03-api-gateway.md), [3A request flows](api-design-and-protection/includes/03A-api-gateway-request-flows.md)), auth, checklist
2. [api-rate-limiting](api-rate-limiting/README.md) — algorithms and where to enforce limits; multi-instance → [§12 distributed](api-rate-limiting/includes/12-distributed-rate-limiting.md)
3. [database-connection-and-security](database-connection-and-security/README.md) — production credentials and IAM
4. [deployment-strategies](deployment-strategies/README.md) — rolling, canary, blue/green

### Make it fast

Optimize in order: measure, reduce work, fix the database hot path, then cache and scale.

1. [high-throughput-systems](high-throughput-systems/README.md) — system-wide throughput order and layers
   - Async brokers and queues → [HTS §14 message brokers](high-throughput-systems/includes/14-message-brokers-and-queues.md)
   - CDC(Change Data Capture) and search indexing → [HTS §15 CDC](high-throughput-systems/includes/15-cdc-and-search-indexing.md)
2. [postgresql-performance](postgresql-performance/README.md) — indexes, queries, pooling, replicas
   - Read [§9 scale-out terminology](postgresql-performance/includes/09-views-functions-and-scale-out-terminology.md) first if partitioning vs replication vs sharding is unclear
3. [tree-and-index-structures](tree-and-index-structures/README.md) — B+ vs LSM when writes dominate
4. Global users → [HTS §13 multi-region](high-throughput-systems/includes/13-multi-region-read-routing.md) + [PG §14 consistency](postgresql-performance/includes/14-consistency-promises-and-costs.md)

### Global scale and consistency

Multi-region reads, consistency promises, and DR before expanding globally.

1. [high-throughput-systems §13 multi-region](high-throughput-systems/includes/13-multi-region-read-routing.md) — active-passive, read-local, geo routing
2. [postgresql-performance §14 consistency](postgresql-performance/includes/14-consistency-promises-and-costs.md) — read-your-writes, staleness, costs
3. [database-connection-and-security §12 DR](database-connection-and-security/includes/12-credential-rotation-and-dr.md) — RPO(Recovery Point Objective)/RTO(Recovery Time Objective), failover drills
4. [deployment-strategies](deployment-strategies/README.md) — safe deploy during regional failover

### Event-sourced domain

Append-only writes, read projections, and reliable async integration.

1. [event-sourcing-and-cqrs](event-sourcing-and-cqrs/README.md) — core concepts and decision guide
2. [event-sourcing-and-cqrs §5 async](event-sourcing-and-cqrs/includes/05-async-integration.md) — outbox, reliable publish
3. [event-sourcing-and-cqrs §7 sagas](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) — cross-service workflows, compensation, ops
4. [event-sourcing-and-cqrs §8 schema evolution](event-sourcing-and-cqrs/includes/08-event-schema-evolution.md) — upcasting, projector compatibility
5. [event-sourcing-and-cqrs §9 testing](event-sourcing-and-cqrs/includes/09-testing-and-verification.md) — aggregate, projector, and saga tests
6. [api-design-and-protection §10 async](api-design-and-protection/includes/10-async-patterns.md) — hub; [10A jobs + polling](api-design-and-protection/includes/10A-async-jobs-polling.md), [10B webhooks](api-design-and-protection/includes/10B-async-webhooks.md)
7. [api-design-and-protection §13 idempotency](api-design-and-protection/includes/13-idempotency.md) — hub; [13A client and server flow](api-design-and-protection/includes/13A-idempotency-client-and-server-flow.md)
8. [postgresql-performance §2 indexing](postgresql-performance/includes/02-indexing.md) — event table performance

### Production hardening

Security review, overload protection, and operational safety nets.

1. [api-design-and-protection §2 protection](api-design-and-protection/includes/02-api-protection.md) + [§6 threat model](api-design-and-protection/includes/06-threat-model.md)
2. [api-design-and-protection §12 identity](api-design-and-protection/includes/12-identity-rbac-iam-ad.md)
3. [database-connection-and-security](database-connection-and-security/README.md) — network, TLS, secrets, cloud identity
4. [high-throughput-systems §9 backpressure](high-throughput-systems/includes/09-backpressure-and-limits.md) + [api-rate-limiting §12 distributed limiting](api-rate-limiting/includes/12-distributed-rate-limiting.md) (Redis topology, regional quotas, fail-open) + [api-rate-limiting](api-rate-limiting/README.md)

### DBA / platform engineer

Operate PostgreSQL safely: connections, migrations, backups, and deploy coupling.

1. [postgresql-performance](postgresql-performance/README.md) — measure, index, pool, maintain
2. [postgresql-performance §15 migrations](postgresql-performance/includes/15-schema-migration-checklist.md) — expand/contract, concurrent indexes
3. [postgresql-performance §16 backup/PITR](postgresql-performance/includes/16-backup-restore-and-pitr.md) — restore drills and WAL(Write-Ahead Log)
4. [database-connection-and-security](database-connection-and-security/README.md) — credentials, IAM, rotation, DR drills
5. [deployment-strategies §12–13](deployment-strategies/includes/12-schema-migrations-and-deploy.md) — schema + deploy order, SLO(Service Level Objective) rollback

### On-call / incident response

Triage saturation-first, rollback, and DR when alerts fire.

1. [RUNBOOK-TEMPLATE.md](RUNBOOK-TEMPLATE.md) or [example orders-api runbook](RUNBOOK-EXAMPLE-orders-api.md)
2. [high-throughput-systems §11 observability](high-throughput-systems/includes/11-observability.md) — triage order, RED(Rate, Errors, Duration)/USE(Utilization, Saturation, Errors), tracing
3. [deployment-strategies §13 SLO rollback](deployment-strategies/includes/13-slo-rollback-triggers.md)
4. [postgresql-performance §16 backup/PITR](postgresql-performance/includes/16-backup-restore-and-pitr.md) + [database-connection §12 DR](database-connection-and-security/includes/12-credential-rotation-and-dr.md)

### B2B / partner API

Partner auth, quotas, and abuse caps.

1. [api-design-and-protection §4 auth](api-design-and-protection/includes/04-auth-model.md) + [§12 identity](api-design-and-protection/includes/12-identity-rbac-iam-ad.md)
2. [api-design-and-protection §5 tiers](api-design-and-protection/includes/05-rate-limit-tiers.md)
3. [api-rate-limiting §6 scope](api-rate-limiting/includes/06-scope-identity.md)
4. [api-design-and-protection §16 multi-tenant](api-design-and-protection/includes/16-multi-tenant-apis.md) — if SaaS with org isolation

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for layout, link conventions, and validation.

| Resource | Purpose |
|----------|---------|
| [GLOSSARY.md](GLOSSARY.md) | Shared terms across guides |
| [CHANGELOG.md](CHANGELOG.md) | Section additions and renames |
| [RUNBOOK-TEMPLATE.md](RUNBOOK-TEMPLATE.md) | Copy per service for incidents |
| [RUNBOOK-EXAMPLE-orders-api.md](RUNBOOK-EXAMPLE-orders-api.md) | Filled example runbook |

Validate:

```bash
cd documents && make validate
```

`make validate` checks file links, cross-file `#anchors`, and README ↔ includes sync. Optional: `make validate-external` for https URLs (see CONTRIBUTING).

---

## Scope

These guides cover **backend API, data, throughput, and deploy** patterns. They intentionally omit deep dives on frontend, mobile, Kubernetes networking, and generic Terraform — link out to official docs when you adopt those stacks.

---

## File layout (every guide)

```
documents/
├── README.md              ← start here
├── CONTRIBUTING.md
├── GLOSSARY.md
├── CHANGELOG.md
├── RUNBOOK-TEMPLATE.md
├── acronyms.json          ← acronym registry for expand-acronyms.py
├── Makefile
├── scripts/
│   ├── expand-acronyms.py
│   ├── github-format.py
│   ├── validate-doc-links.py
│   ├── validate-doc-readme.py
│   └── validate-doc-prose.py
└── guide-name/
    ├── README.md
    └── includes/
```

---

## Cross-link convention

| Source | Path to sibling guide |
|--------|------------------------|
| `guide/includes/*.md` | `../../other-guide/...` |
| `guide/README.md` | `../other-guide/...` |

Every guide ends with a **## See also** table (sibling guides). Section-level cross-links inside chapters may use **## See also** or **## Other guides in this repo** where context-specific.