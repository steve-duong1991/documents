# Changelog — Engineering Guides

Format: guide name, brief summary. Update when adding or materially expanding sections.

---

## 2026-07-12

### System design curriculum gaps closed (6 new guides + 3 extensions)
- **system-design-walkthroughs:** 11 sections — how to approach, URL shortener, news feed, chat/presence, ride-sharing geo, distributed rate limiter (system design), notification pipeline, search autocomplete, video streaming basics, decision guide
- **nosql-and-key-value-stores:** 7 sections — when to choose DynamoDB/Cassandra/Mongo vs PostgreSQL, access-pattern modeling (GSI/LSI, hot partitions), Dynamo-style multi-tenant SaaS, Cassandra, MongoDB, decision guide
- **distributed-systems-primitives:** 9 sections — CAP/PACELC mechanisms, consistent hashing, unique IDs, consensus/leader election, service discovery, Bloom/HLL/Count-Min, clocks/ordering, decision guide
- **realtime-at-scale:** 6 sections — WebSocket fan-out, pub/sub backplanes, presence/typing, CRDT/OT, decision guide (complements fullstack §5 UX and api-design §10C contracts)
- **specialized-data-systems:** 6 sections — time-series, graph DBs, vector/RAG, workflow engines vs sagas, decision guide
- **payments-and-fintech:** 6 sections — PCI scope reduction, double-charge prevention, double-entry ledger, fraud/reconciliation, decision guide
- **api-design-and-protection §18:** Object storage and large-file uploads (presigned URLs, multipart, virus scan, CDN delivery, SSRF)
- **high-throughput-systems §16:** Networking fundamentals (DNS, HTTP/2/3, TLS placement, anycast, connection draining)
- **architecture-decisions §13:** Capacity estimation workbook (DAU→RPS, Little's Law, DB/Redis/Kafka sizing checklist)
- **Corpus:** root README index + relation diagram + learning paths (system design practice, NoSQL, realtime, specialized data, payments, media/networking); Scope expanded; acronyms for NFR, CRDT, OT, TSDB, ANN, RAG, PCI DSS, PAN, DNS, QUIC, …

---

## 2026-07-11

### Tech Lead Fullstack curriculum (10 new guides)
- **architecture-decisions:** 13 sections — monolith/modular/microservices, boundaries, DDD, strangler, ADRs, tradeoffs, integration, data ownership, BFF composition, multi-tenant models, failure domains, decision guide
- **resilience-patterns:** 12 sections — timeouts, retries/backoff/jitter, circuit breakers, bulkheads, load shedding, systemwide idempotency, locks, delivery semantics, cascading failure, chaos, decision guide
- **sre-and-incidents:** 12 sections — SLI/SLO/SLA, error budgets, capacity/load, observability practice, alerting, incident command, postmortems, on-call, drills, synthetics, decision guide
- **cicd-and-environments:** 10 sections — CI pipeline, CD/promotion, config vs secrets, flags as control, branching, rollback vs forward-fix, containers/health, platform boundaries, decision guide
- **enterprise-security-compliance:** 12 sections — secure SDLC, threat-modeling process (vs api-design §6), OWASP, supply chain/SBOM, secrets beyond DB, audit/retention, PII, encryption, zero trust, compliance evidence, decision guide
- **fullstack-bff-and-clients:** 11 sections — frontend architecture, SSR/CSR/SSG, BFF contracts, Web Vitals, realtime UX, a11y, auth UX, offline/flaky network, design-system boundaries, decision guide
- **testing-strategy:** 10 sections — pyramid/diamond, what not to automate, contracts, integration/E2E, load/soak/resilience, flakes, quality gates, production verification, decision guide
- **tech-lead-practice:** 12 sections — vision/roadmap, design & code reviews, mentoring, debt, estimation, stakeholders, cross-team API ownership, build vs buy, escalation, decision guide
- **data-platforms:** 9 sections — OLTP vs OLAP, search, Redis roles, caching coherence, ownership/lineage/retention, migration coordination, analytics isolation, decision guide
- **finops-and-cost:** 9 sections — unit economics, cost drivers, right-sizing, retention cost, build vs managed TCO, budgets, architecture cost tradeoffs, decision guide
- **Corpus:** root README index + relation diagram + Tech Lead Fullstack / architecture / testing / practice learning paths; Scope expanded; acronyms CI/CD, SRE, SBOM, FinOps, SSR/SSG, …

---

## 2026-07-05

### Navigation and discoverability polish
- **Corpus:** root README Scope note for cursor-agents (meta/tooling) + `.cursor/` in file layout; mermaid tooling subgraph
- **See also:** apache-kafka rows in postgresql-performance, deployment-strategies, database-connection-and-security, api-rate-limiting, tree-and-index-structures READMEs
- **cursor-agents:** See also links to Engineering Guides repo and `.cursor/` rules
- **CI:** `.cursor/**` in documents workflow path filters
- **api-rate-limiting §6:** Redis key patterns by scope, layered keys, cardinality and hot-key notes
- **deployment-strategies §5:** A/B vs canary vs feature-flag boundary, decision table, workflow sequence
- **Corpus polish:** aligned Redis key convention (§6 + §12); GLOSSARY A/B test, experiment flag, subagent; CONTRIBUTING `.cursor/` note; validate-doc-prose scans guide READMEs; expanded api-rate-limiting §1–§5 and §9 algorithm cards
- **Final nits:** global Redis key documented as 5-segment special case (§6); expanded deployment §00, §3, §6, §9, §10 strategy cards

### cursor-agents (new guide)
- **New guide:** 5 sections — single vs multi agent overview, single agent usage, parallel Agents Window + subagents, auto-delegation setup, decision guide
- **Corpus:** root README guide row + learning path

### apache-kafka §6 schema polish
- **§6:** Avro/Protobuf/JSON naming tables; event envelope vs raw payload; field rules (money, timestamps, IDs); CloudEvents; HTTP OpenAPI vs bus vs event store diagram
- **GLOSSARY:** CloudEvents row
- **Corpus:** acronym expansions applied across `apache-kafka/` includes

---

## 2026-06-22

### apache-kafka (new guide)
- **New guide:** 12 sections — commit log internals, topics/replication/multi-tenant, producers/consumers, retention, Avro/Protobuf/JSON schema choice, Connect/Streams, integration patterns, cluster setup, ops/DR/security, decision guide, testing
- **Corpus:** root README guide row + learning path; GLOSSARY Kafka terms; deep-dive links from HTS §7/§14/§15, ES §5/§8/§9/§7C, api §15/§16

---

## 2026-06-21

### api-design §12 hub trim + §7/§15 dedupe
- **§12:** trimmed identity hub to overview + comparison; moved IAM lifecycle (JML) to `12A`, RBAC at API layer to `12B`
- **§7 / §15:** Scope blocks; removed duplicate contract-testing CI block from §7; §15 owns Spectral, diff, Pact pipeline

### api-design-and-protection reading paths
- README: B2B/SaaS partner path (§4, §5, §16, §12, rate-limiting §6); GraphQL/gRPC path (§17)
- Contract design path links to §17 for non-REST APIs
- §12A Active Directory: AD-specific common mistakes + pointer to §12B

### Materialized view discoverability
- **postgresql-performance:** README TOC §11 label mentions materialized views; §3/§9/§13 deep-links to `#materialized-views`
- **GLOSSARY:** Materialized view row → PG §11

### Deferred polish
- **Corpus:** consolidated same-day CHANGELOG entries under one `## 2026-06-21` header
- **HTS §11:** merged duplicate distributed tracing sections into OpenTelemetry block
- **PG §9:** trimmed materialized view subsection; defers refresh patterns to §11

### Minor navigation polish
- **Corpus:** root README learning paths deep-link to `NNA` sub-articles (`10A`, `13A`, `3A`); api-design README reading paths updated
- **api-design-and-protection:** trimmed `10-async-patterns` hub (OpenAPI → `10A`, idempotency diagram → `13C`); fixed duplicate `---` separators
- **CHANGELOG:** historical split entries updated to current `NNA-topic.md` filenames

### Sub-article letter suffixes
- **Corpus:** renamed 14 hub-split sub-articles to `NNA-topic.md`; README TOC labels uppercase (`3A`, `10A`, `7C`); ~32-file link sweep
- **Scripts:** `validate-doc-readme.py` accepts `\d{2}[A-Z]?-` includes; `github-format.py` section map hub-only

### Optional corpus polish
- **Corpus:** GLOSSARY **Compaction (LSM)** row; root README explicit §12 distributed limiting in learning paths
- **api-design-and-protection:** split §3 Gateway → `03A`, `03B`; split §13 Idempotency → `13A`–`13C`; cross-link anchor updates
- **CONTRIBUTING:** sub-article examples for §3 and §13 hub splits

### GitHub navigation — slim READMEs, article splits
- **Corpus:** README Option A (TOC-primary); TOC table fix; GLOSSARY memtable/SSTable rows
- **api-rate-limiting:** §12 Distributed rate limiting
- **postgresql-performance:** §7 Scope block (pool vs credentials/IAM)
- **event-sourcing-and-cqrs:** §9 golden event fixture example
- **deployment-strategies:** §1, §6, §8 production signals tables
- **api-design-and-protection:** split §10 → `10A`–`10C`; §11 → `11A`; §12 → `12A`, `12B`
- **event-sourcing-and-cqrs:** split §7 → `07A`–`07C`
- **Removed:** `GUIDE.md`, `mkdocs.yml`, `build-guide.py`, pre-commit, external-link CI workflow

### Acronym expansions
- **Corpus:** `acronyms.json` + `expand-acronyms.py`; GLOSSARY SLI, RED, SSRF rows; `make check` acronym drift

### Coverage expansion
- **high-throughput-systems:** §14 message brokers; §15 CDC/search indexing; §1 capacity planning; §4 Redis ops; §11 OpenTelemetry
- **event-sourcing-and-cqrs:** §8 schema evolution; §9 testing and verification
- **postgresql-performance:** §16 backup/PITR; §11 Scope vs HTS §4
- **api-design-and-protection:** §16 multi-tenant; §17 GraphQL/gRPC; §4/§12 Scope blocks
- **Corpus:** GLOSSARY BOLA, BRIN, GIN, CDC, choreography, RED/USE, upcasting; on-call and B2B learning paths; RUNBOOK example

### Polish — nav, scope, HTS §13
- **high-throughput-systems:** §14 multi-region → §13; §6/§10 Scope blocks
- **event-sourcing-and-cqrs:** §4 Scope block
- **api-design-and-protection:** §1, §10 Scope blocks
- **tree-and-index-structures:** §3 production signals table
- **Corpus:** Global scale learning path; CI/pre-commit in repo root

### Saga ops gaps
- **event-sourcing-and-cqrs:** §7 when-not-to-use, retry vs compensate, inbox, deploy versioning, testing
- **Corpus:** GLOSSARY Inbox pattern, 2PC; event-sourced learning path §5 + §7

### Saga transactions
- **event-sourcing-and-cqrs:** §7 transactions and distributed databases (local ACID vs cross-service)

### Saga style decision
- **event-sourcing-and-cqrs:** §7 choreography vs orchestration decision flow

### Sagas
- **event-sourcing-and-cqrs:** new §7 Sagas and distributed workflows
- **Corpus:** GLOSSARY Saga, compensating transaction, process manager

### Scope blocks
- **high-throughput-systems:** §1, §3, §5, §12 Scope blocks
- **postgresql-performance:** §1 Scope block
- **api-design-and-protection:** §3, §5, §11 Scope blocks
- **api-rate-limiting:** §7, §9 Scope blocks
- **CONTRIBUTING:** Scope + Related pattern documented

### Dedup + scope clarity
- **api-rate-limiting:** §9 deduped `429` example → api-design §5
- **HTS §2 / api-design §3:** Scope blocks and cross-links
- **Corpus:** GLOSSARY fail open / fail closed

### Filename consistency + overlap dedup
- **Corpus:** `*-anti-patterns*` → `*-common-mistakes*`; api-design §5, api-rate-limiting §7, HTS §3/§5 dedup pointers

### Consistency pass 3
- **Corpus:** 100/100 includes with `Related` + `Common mistakes` across all guides

### Consistency pass 2
- **postgresql-performance:** §1, §2, §7, §10, §11 Common mistakes
- **database-connection-and-security:** §2 deduped decision flow → §13
- **event-sourcing-and-cqrs:** §0–§6 Related + Common mistakes

### Consistency
- **postgresql-performance / database-connection-and-security:** Related + Common mistakes on remaining sections; §00 overview for db-connection
- **Corpus:** pre-commit GUIDE.md drift; MkDocs CI step

### Editorial
- **postgresql-performance:** §00/§13 decision flow dedup; §9 in priority order
- **high-throughput-systems:** §12 scenario table scoped
- **api-design-and-protection:** §13 deduped async diagram
- **api-rate-limiting / deployment-strategies:** Related + Common mistakes on §1–§10
- **Corpus:** root README scripts list; CONTRIBUTING style note

### Maintenance
- **postgresql-performance:** scale-out terminology → §9; renumbered §10–§15; §11 deduped read path
- **Corpus:** `validate-doc-readme.py`; `#anchor` checks; GLOSSARY expansion

### Initial section additions
- **api-design-and-protection:** §14 versioning; §15 contract testing
- **high-throughput-systems:** §14 multi-region (later §13); §1/§4/§6/§7/§11 expansions
- **deployment-strategies:** §12 schema migrations; §13 SLO rollback; §2/§4/§7 expansions
- **postgresql-performance:** schema migration checklist (§15)
- **database-connection-and-security:** renamed from `database-securities`; §12 DR; §13 decision guide
- **event-sourcing-and-cqrs:** §3 snapshots/archival/GDPR
- **api-rate-limiting:** §11 war stories
- **Corpus:** root README, CONTRIBUTING, GLOSSARY, RUNBOOK-TEMPLATE, Makefile, link validation
