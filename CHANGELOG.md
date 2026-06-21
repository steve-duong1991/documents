# Changelog — Engineering Guides

Format: guide name, brief summary. Update when adding or materially expanding sections.

---

## 2026-06-21 (GitHub navigation — slim READMEs, article splits)

### Corpus
- **README Option A:** guide READMEs are TOC + `Reading paths` / `See also` only — removed duplicate skim sections
- `validate-doc-readme.py` — TOC sync only (no body link requirement per include)
- CONTRIBUTING updated for TOC-primary navigation and sub-article naming (`10a` labels, `10-async-webhooks.md` files)
- README TOC table fix — two-column separators normalized; column-count validation added

### api-rate-limiting
- §12 Distributed rate limiting — Redis cluster, hot keys, clock skew, global vs regional quotas

### postgresql-performance
- §7 Scope block — pool tuning vs database-connection credentials/IAM

### event-sourcing-and-cqrs
- §9 Golden event fixture example (JSON + test sketch)

### deployment-strategies
- §1, §6, §8 Production signals tables (stack-specific tooling)

### Corpus
- GLOSSARY: memtable, SSTable rows

### api-design-and-protection
- Split §10 Async patterns → hub + `10-async-jobs-polling`, `10-async-webhooks`, `10-async-streaming`
- Split §11 Stateless → hub + `11-stateless-auth-operations`
- Split §12 Identity → hub + `12-identity-active-directory`, `12-identity-enterprise-api`

### event-sourcing-and-cqrs
- Split §7 Sagas → hub + `07-sagas-choreography-orchestration`, `07-sagas-compensation-idempotency`, `07-sagas-operations`

### Removed (prior commit on branch)
- All `GUIDE.md` combined files, `mkdocs.yml`, `build-guide.py`, pre-commit, external-link CI workflow
- GitHub reading path: guide README TOC → `includes/*.md`

---

## 2026-06-21 (acronym expansions)

### Corpus
- `acronyms.json` registry + `scripts/expand-acronyms.py` — first-use-per-file inline expansions (`CDC(Change Data Capture)`)
- GLOSSARY Term column aligned with inline style; added SLI, RED, SSRF rows
- CONTRIBUTING: acronym convention; CI `expand-acronyms.py --check`; `make check` includes acronym drift
- Headings left unexpanded for stable `#anchors`; shorthand in parentheses `(DLQ)`, `(2PC)` not doubled

---

## 2026-06-21 (coverage expansion)

### high-throughput-systems
- §14 Message brokers and queues — queue vs stream vs outbox decision flow
- §15 CDC and search indexing — OpenSearch pipelines, reindex
- §1: capacity and cost planning
- §4: Redis operations + Scope vs PG §11
- §11: OpenTelemetry / distributed tracing
- §12: quick links to §14–§15

### event-sourcing-and-cqrs
- §8 Event schema evolution — upcasting, projector compatibility
- §9 Testing and verification — aggregates, projectors, sagas, CI
- §7: cross-link to §9 testing

### postgresql-performance
- §16 Backup, restore, and PITR — operational recovery runbook
- §11: Scope vs HTS §4 caching

### api-design-and-protection
- §16 Multi-tenant APIs — isolation, BOLA, tenant-scoped limits
- §17 GraphQL and gRPC — when to use vs REST
- §4 / §12: Scope blocks (auth protocols vs enterprise identity)

### Corpus
- GLOSSARY: BOLA, BRIN, GIN, CDC, choreography, RED/USE, SLI, SSRF, upcasting
- Root README: on-call, B2B partner learning paths; DBA path includes PG §16
- RUNBOOK-EXAMPLE-orders-api.md + RUNBOOK-TEMPLATE link
- mkdocs.yml: new sections in nav

---

## 2026-06-21 (polish — nav, scope, HTS §13)

### high-throughput-systems
- Renumbered §14 Multi-region read routing → **§13** (`13-multi-region-read-routing.md`)
- §10: cross-link to §13 multi-region
- §6: **Scope** block (throughput vs api-design §10 HTTP contract)

### event-sourcing-and-cqrs
- §4: **Scope** block (ES/CQRS API lens vs api-design §1)

### api-design-and-protection
- §1: **Scope** block (general REST vs ES §4)
- §10: **Scope** block (HTTP contract vs HTS §6 / ES §5)

### tree-and-index-structures
- §3: **Production signals** table — when specialized trees appear in real systems

### Corpus
- Root README: **Global scale and consistency** learning path; HTS §13 + PG §14 in Make it fast
- `mkdocs.yml`: per-guide TOC, full GUIDE, and individual `includes/` in nav
- CI: weekly `documents-external.yml` for `make validate-external`
- Moved CI/pre-commit into repo root (`documents/.github/`, `.pre-commit-config.yaml`); removed orphan `workflows/` folder

---

## 2026-06-21 (saga ops gaps)

### event-sourcing-and-cqrs
- §7: when not to use, scope (one ES vs cross-service), retry vs compensate, observability/DLQ, message ordering, inbox pattern, deploy versioning, testing, orchestrator security
- §5: cross-links to §7 (sagas, inbox)
- §6: when to avoid — single service / one DB → ACID not saga

### Corpus
- GLOSSARY: **Inbox pattern**, **Two-phase commit (2PC)**
- documents/README: Event-sourced domain learning path includes §5 outbox + §7 sagas

---

## 2026-06-21 (saga transactions)

### event-sourcing-and-cqrs
- §7: **Transactions and distributed databases** — local ACID vs cross-service eventual consistency, per-step commit, microservices vs distributed SQL, comparison to 2PC/TCC

---

## 2026-06-21 (saga style decision)

### event-sourcing-and-cqrs
- §7: **Which one to choose?** — choreography vs orchestration decision flow, checklist, and signals table

---

## 2026-06-21 (sagas)

### event-sourcing-and-cqrs
- New §7 **Sagas and distributed workflows** — choreography vs orchestration, compensation, state machines, idempotency, order-fulfillment example
- §1, §6: cross-links to §7; README TOC + microservice reading path

### Corpus
- GLOSSARY: **Saga**, **Compensating transaction**, **Process manager**
- HTS §6, api-design §13: cross-links to ES §7

---

## 2026-06-21 (scope blocks)

### high-throughput-systems
- §1, §3, §5, §12: added **Scope** blocks (system vs DB measurement, throughput vs architecture, scenario ownership)

### postgresql-performance
- §1: added **Scope** block (database lens vs HTS §1)

### api-design-and-protection
- §3, §5, §11: added **Scope** blocks (architecture vs throughput, product vs technical rate limits, architecture vs throughput stateless)

### api-rate-limiting
- §7, §9: added **Scope** blocks (technical vs product lens, behavior vs header contract)

### Corpus
- CONTRIBUTING: document **Scope** + **Related** pattern for overlapping sibling sections

---

## 2026-06-21 (dedup + scope clarity)

### api-rate-limiting
- §9: removed duplicate `429` HTTP example → pointer to api-design §5 (kept header purpose table)

### high-throughput-systems / api-design-and-protection
- HTS §2: added **Scope** block clarifying throughput lens vs api-design §3 architecture guide
- api-design §3: added cross-link to HTS §2 for throughput tips

### Corpus
- GLOSSARY: added **Fail open / fail closed (rate limit)** entries → api-rate-limiting §11

---

## 2026-06-21 (filename consistency + overlap dedup)

### Corpus
- Renamed legacy include files: `*-anti-patterns*` / `*-pitfalls*` → `*-common-mistakes*` / `06-amplification-and-related-topics.md`
- Standardized remaining "anti-patterns" / "pitfalls" display labels to **Common mistakes**
- **api-design §5:** deduped layered limits and async diagrams → pointers to api-rate-limiting §7/§9/§11 and §10 async
- **api-rate-limiting §7:** deduped fail-open section → pointer to §11
- **HTS §3:** deduped stateless prerequisites/checklist → pointers to api-design §11 and api-rate-limiting §11
- **HTS §5:** scenario table scoped with pointers to §12 and PG §13

---

## 2026-06-21 (consistency pass 3)

### api-design-and-protection
- §0–§2, §4–§9, §15: added `Related` and/or `Common mistakes`; §1 renamed anti-patterns → Common mistakes

### api-rate-limiting
- §0, §10, §11: added `Related`; §11 renamed pitfalls heading; §0/§10 added mistake tables

### deployment-strategies
- §0, §2–§4, §7, §11: added `Related` and `Common mistakes`

### high-throughput-systems
- §0, §1: added `Common mistakes`

### postgresql-performance / database-connection-and-security
- §00 overviews: added `Common mistakes`

### tree-and-index-structures
- §0–§5: added `Related` and/or `Common mistakes`

### high-throughput-systems
- §12: renamed Anti-patterns → Common mistakes

### Corpus
- Editorial pass 3: **100/100** includes with `Related` + `Common mistakes`

---

## 2026-06-21 (consistency pass 2)

### postgresql-performance
- §1, §2, §7, §10, §11: added Common mistakes tables
- §2: expanded Related links
- §13: added Related; renamed Anti-patterns → Common mistakes

### database-connection-and-security
- §2: deduplicated decision flow/tables → pointer to §13 (kept security layers + quick comparison)

### event-sourcing-and-cqrs
- §0–§6: standardized `Related` blockquotes; added Common mistakes to all sections

### Corpus
- CHANGELOG entry for pass 2

---

## 2026-06-21 (consistency)

### postgresql-performance
- §00, §3–§6, §8, §12: added `Related` cross-links and `Common mistakes` tables

### database-connection-and-security
- Added §00 Overview (security layers, pattern map, default baseline)
- §1–§11: added `Related` cross-links and `Common mistakes` tables
- README: aligned with other guides (Overview TOC row, no inline credential embed)

### Corpus
- Pre-commit: added `GUIDE.md` drift check (matches CI)
- CI: added MkDocs build step; fixed `site_dir` (output: `../.mkdocs-site/`)
- CONTRIBUTING / root README: document pre-commit and MkDocs CI parity

---

## 2026-06-21 (editorial)

### postgresql-performance
- §00: removed duplicate decision flowchart; links to §13; §9 in priority order
- §13: scoped to database-layer scenarios; checklist references §9

### high-throughput-systems
- §12: scenario table scoped by layer; deduped PG-overlapping rows

### api-design-and-protection
- §13: removed duplicate async/idempotency sequence diagram; links to §10

### api-rate-limiting
- §1–§9: added Related cross-links and Common mistakes tables

### deployment-strategies
- §1, §5–§6, §8–§10: added Related cross-links and Common mistakes tables

### Corpus
- Root README: scripts list, Make it fast path includes PG §9
- CONTRIBUTING: naming example, Related/Common mistakes style note

---

## 2026-06-21 (maintenance)

### postgresql-performance
- Moved scale-out terminology to §9 (before partitioning and read scaling); renumbered §9–§14 → §10–§15
- §11 read scaling: deduplicated layered-read-path diagram; defers to HTS §4

### Corpus
- Added `validate-doc-readme.py` (README TOC ↔ includes sync)
- Extended `validate-doc-links.py` with `#anchor` checks and optional `--external`
- Expanded GLOSSARY; CI now checks GUIDE.md drift

---

## 2026-06-21

### api-design-and-protection
- Added §14 API versioning and deprecation
- Added §15 Contract and schema testing

### high-throughput-systems
- Added §14 Multi-region read routing
- Expanded §1 load testing regression workflow
- Expanded §4 cache stampede; §6 DLQ; §7 Kafka patterns; §11 RED/USE

### deployment-strategies
- Added §12 Schema migrations and deploy coupling
- Added §13 SLO-based rollback triggers
- Expanded §2 rolling, §4 canary, §7 feature flags (failure modes, examples)

### postgresql-performance
- Added schema migration checklist (now §15 after later renumber)

### database-connection-and-security
- Renamed from `database-securities`; added §12 credential rotation and DR
- Added §13 Connection pattern decision guide

### event-sourcing-and-cqrs
- Expanded §3 snapshots, archival, GDPR, rebuild runbook

### api-rate-limiting
- Expanded §11 production war stories

### Corpus
- Added root README, CONTRIBUTING, GLOSSARY, RUNBOOK-TEMPLATE
- Added `scripts/build-guide.py`, `scripts/validate-doc-links.py`, Makefile
- Standardized See also footers; link validation at 0 broken
