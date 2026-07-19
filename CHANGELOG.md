# Changelog — Engineering Guides

Format: guide name, brief summary. Update when adding or materially expanding sections.

---

## 2026-07-19

### Visual spines, DR hub, ops depth, diagram debt closed
- **VISUAL-INDEX:** Expanded 4 → 9 spines (Identity, Data platform, DR/failover, Realtime fan-out, Money movement) + spine picker table
- **Root README:** New **Visual-first** learning path; Global scale / On-call / Data platform / Specialized / Payments / Ship API / Ship safely / Fullstack paths updated
- **sre §12A (new):** Disaster recovery playbook — swimlane, RACI, freeze→promote→validate; **§4A (new):** Observability platform product
- **HTS §13A (new):** Multi-region write and failover — sticky primary, cells vs multi-master
- **data-platforms:** §01A columnar OLAP ops · §02A search cluster ops · §05A data contracts/registries
- **specialized §03B (new):** LLM gateway and inference edge
- **cicd §08A (new):** Paved-road catalog · **deployment §07A (new):** Feature-flag operations
- **api-design:** §07A developer portal · §10E notification provider ops
- **fullstack §08A (new):** Mobile API contracts · **payments §03A (new):** Refunds/payouts/settlement
- **Diagram pack:** ~22 mermaid adds across PG, database-connection, tree; Reading paths on PG + DB-connection; tree See also dedupe
- **GLOSSARY:** Data contract, Developer portal, Disaster recovery drill, LLM gateway, Observability platform, Paved road; Schema Registry / RPO/RTO links refreshed
- **acronyms:** LLM, ILM

### Visual spines, diagram debt, and topic expands
- **VISUAL-INDEX.md (new):** Request / Async / Release / Incident spines with deep links
- **Root README:** Split guide-relation mermaid into Delivery / Data / Security views; link VISUAL-INDEX
- **P0 diagrams:** database-connection §0/§4/§9 layered access + IAM sequence; PG §11 read path + RYW sequence; §17/§18 isolation models; §6 vacuum flowchart
- **High/Med/Low topic expands (NNA):**
  - HTS §11A OpenTelemetry and cardinality
  - resilience §11A service mesh topology
  - HTS §14A queue broker operations (SQS/Rabbit/NATS)
  - api-design §17A GraphQL production · §17B gRPC and protobuf CI
  - data-platforms §3A Redis operations
  - system-design §9A CDN and media delivery
  - specialized §3A feature stores and ML serving
- **Cross-links:** cursor-agents ↔ workflows; tree/DB See also denser; learning paths updated
- **GLOSSARY / acronyms:** OTel, feature store, service mesh; SQS/gRPC/RDB/AOF/LRU/ML/…

### SA gaps: debt×CX, org fit, hypercare, learning path
- **tech-lead §5A (new):** Balancing debt, business, and CX — ship-with-degrade vs stop features vs pay debt first
- **architecture §14 (new):** Org, stage, and pricing fit — people/platform maturity, B2B vs B2C, pricing → defaults; NFR sheet
- **sre §10A (new):** Hypercare checklist (first 72h) — SLOs + business KPI + Web Vitals/support; abort/extend
- **Root README:** New **Solution Architect** learning path; TL Fullstack / Ship safely / On-call / Tech Lead / Architecture paths updated
- **Cross-links:** deploy §14 Gate 7; cursor-workflows §6; architecture §1/§12; tech-lead §5/§11; finops §7/§8; sre §10/§11; GLOSSARY Hypercare; acronyms CX/CSAT/GTM/KPI/RUM/NPS

### SA org/process depth
- **tech-lead §1A (new):** Product discovery for Tech Leads — evidence, JTBD/spikes, discovery brief → solution design
- **architecture §1A (new):** Team Topologies — stream/platform/enabling/complicated-subsystem, interaction modes, reverse Conway
- **architecture §5A (new):** Architecture governance (ARB) — decision rights by blast radius, lightweight ARB, paved-road exceptions
- **architecture §4A (new):** Modernization program — waves, dual-run KPIs, cutover RACI, program exit
- **Corpus:** SA + Tech Lead + Architecture paths updated; cursor-workflows §1 / READMEs; acronyms ARB/JTBD

### Identity depth + residency + erasure + notifications
- **api-design §12D (new):** Fine-grained AuthZ — BOLA, ReBAC/Zanzibar-style, ABAC vs RBAC, AuthZ service vs JWT, caching/tenancy
- **enterprise-security §7A (new):** Erasure and DSAR playbook — store inventory, crypto-shred, fan-out, legal hold, multi-tenant
- **architecture §10A (new):** Regional cells and data residency — topology, pins, routing, forbidden replication, cutover/drills
- **api-design §10D (new):** Notification delivery — preferences, dedup, priority queues, providers, PII in templates
- **auth overview:** AuthN vs AuthZ mapped to OIDC vs OAuth 2.0 (ID token vs access token); GLOSSARY AuthN/AuthZ; api-design §4 pointer
- **Corpus polish:** Grammar fixes; acronyms IdP/AuthN/AuthZ/TTL/RLS/B2B/SaaS/ReBAC/DSAR/LDAP/ABAC/BYO/SMB; See also HTS↔resilience, PG→arch/nosql, ESC→§12C, api §16→§12C, ES §5A→api §10; TL Fullstack + Global scale + Multi-tenant paths updated; GLOSSARY JIT/ReBAC/DSAR/cells

### Auth — multi-tenant OIDC / B2B SSO
- **auth-oauth-oidc-and-login-security §2d (new):** Multi-tenant OIDC and B2B SSO — tenant resolution (subdomain/path/email HRD), IdP topology (shared/broker/per-issuer), authorize routing, multi-issuer validation, membership + tenant switch, admin consent/SCIM pointers
- **Cross-links:** §2b pointer + checklist; §2/§2c/§3/§5a/§6; api-design §16 Scope; architecture §10; root Auth + B2B + Multi-tenant SaaS paths; GLOSSARY (HRD, multi-issuer, membership); acronyms HRD/JIT/JML/SCIM

### Identity — SCIM / JML provisioning
- **api-design-and-protection §12C (new):** SCIM and JML provisioning — joiner/mover/leaver, SCIM Users/Groups, JIT vs pre-provision, group→role, deactivate→revoke races, multi-tenant SCIM tokens, checklist
- **Cross-links:** §12 hub / §12A / §12B; auth §2b / §2d / §3b; api-design README reading paths; root B2B path; GLOSSARY SCIM/JML

### Outbox + Inbox first-class (event-sourcing)
- **event-sourcing-and-cqrs §5A (new):** Outbox ↔ inbox pair — end-to-end diagrams, relay mark-published races, retention, poison/DLQ, outbox table vs CDC-on-events, inbox schema with stored `result`, vs `saga_step_log`
- **event-sourcing-and-cqrs §5:** Pair overview + links; §7 Temporal/engine fork; §6 multi-service reading callout; §7C inbox points to §5A
- **Corpus:** ES README TOC/reading paths; root Event-sourced + Kafka learning paths; GLOSSARY Outbox/Inbox/Transactional outbox → §5A; apache-kafka §8/§13 cross-links

### Multi-tenant database design gaps closed
- **postgresql-performance §17:** Composite `(tenant_id, …)` PK/FK/unique; shared vs tenant-scoped tables; PgBouncer/`SET LOCAL`; RLS performance; expanded testing and mistakes
- **postgresql-performance §18 (new):** Schema and database per tenant — `search_path`, provisioning, migration fan-out, pool→silo cutover, tenant restore drills
- **architecture-decisions §10:** Shared platform data; pool→silo checklist; tenant restore drill; links to PG §17/§18
- **architecture-decisions §12:** SaaS silo + mid-flight migration scenarios; restore checklist item
- **api-design-and-protection §16:** Isolation matrix deduped to arch §10; API implications only; Scope block
- **Corpus:** Root learning path **Multi-tenant SaaS data**; GLOSSARY (schema/DB per tenant; multi-tenant → arch §10); PG/arch README TOC and reading paths

### Architecture ↔ resilience bridge
- **architecture-decisions §12:** Sync path = hop budget + tiers + resilience stack; BFF fan-out scenario; concrete checklist (fallback contracts, retry owner, chaos, drain); See also refreshed
- **architecture-decisions §11:** Fallback contracts + policy placement links; shared infra needs a retry/timeout owner; mistake table tightened
- **architecture-decisions §2 / README:** Hop-budget and See also point at resilience checkout example

### Resilience patterns — design + ops gaps closed
- **resilience-patterns §2:** Layer ownership (one retry owner); hedged/speculative reads with cancel
- **resilience-patterns §4:** Liveness vs readiness vs bulkheads (restart-storm trap)
- **resilience-patterns §5:** Fallback contracts (stale / omit / approximate / fail-closed / async) by tier
- **resilience-patterns §11:** Policy placement — app vs gateway vs mesh; stacked-retry anti-pattern
- **resilience-patterns §12:** Worked example — checkout journey applying the full stack
- **resilience-patterns §13:** Observability for resilience (retry ratio, breaker, pool wait, shed/degrade)
- **resilience-patterns §14:** Graceful shutdown and drain
- **resilience-patterns §15:** Implementation map (illustrative library/platform knobs; design-first)
- **resilience-patterns §16:** Decision guide renumbered from §11; checklist/scenarios updated
- **Cross-links:** architecture-decisions §12 → resilience §16; root index blurb; HTS/cicd/payments see-also via new sections

---

## 2026-07-12

### Auth / OAuth / OIDC / login security (new guide)
- **auth-oauth-oidc-and-login-security:** 27 includes / §§0–6 — OAuth 2.0 grants (Auth Code + PKCE, client credentials, device code; deprecated Implicit/ROPC), OIDC discovery + ID token claims, token lifecycle/JWKS/refresh rotation, cookie/session/CSRF, login playbook (Argon2id, lockout, MFA, device trust, recovery), decision guide; plus SSO/SAML, PAR/resource/CIBA/JAR/RAR, revoke/denylist, guest sessions, signup/magic links, WebAuthn, impersonation
- **§3a:** Token and cookie integrity (anti-tampering) — client untrusted; JWT sig vs opaque lookup vs session `sid`; HttpOnly ≠ integrity; DPoP/mTLS binding
- **§3b:** Revoke / force logout / denylist playbook — validate vs invalidate; device vs all-device logout; user/`jti`/session block stores
- **§1a:** Client authentication methods + token exchange (RFC 8693) for BFF on-behalf-of; revocation/introspection endpoint pointers
- **§2a:** OIDC RP / front / back-channel logout + step-up (`prompt` / `max_age` / `acr_values`)
- **§4a:** Third-party cookie deprecation + mobile App/Universal Links vs custom schemes
- **§3c:** Denylist Redis patterns — basic/advanced keys (`jti`, session, user disabled, family, user epoch `tv`), TTL hygiene, pipeline/cluster notes
- **§1b:** Scopes and consent design (first-party vs third-party; light resource indicators)
- **§2b:** SSO integration playbook — IdP SSO → OIDC → app session → API Bearer; enterprise vs social; account linking
- **§2c:** Full SAML 2.0 protocol guide — SP/IdP, assertions, bindings, metadata, XML risks, SAML→OIDC bridge
- **§3d:** Lifetimes and sliding sessions — matrix for access/refresh/idle/absolute/cookie/IdP SSO; silent re-auth policy
- **§5a:** Auth testing checklist for CI (OAuth/OIDC/CSRF/revoke/SAML negatives)
- **§3a:** Short DPoP advanced note (proof-of-possession)
- **§1c:** Pushed Authorization Requests (RFC 9126) — `request_uri`, when to adopt, PKCE still required
- **§1d:** Resource indicators (RFC 8707) — `resource`/`aud`, multi-API AS, exchange
- **§1e:** Device Authorization + CIBA — polling, user_code, backchannel modes
- **§1f:** JAR + RAR — signed request objects; `authorization_details`
- **§3e:** Concurrent sessions and devices — caps, revoke one/others, SSO interaction
- **§4a:** Expanded CHIPS / `Partitioned` cookie detail
- **§4b:** Anonymous / guest sessions — create, caps, promote on register/login, TTL/abuse
- **§5b:** Signup, email verification, and magic links
- **§5c:** WebAuthn and passkeys
- **§5d:** Impersonation and support access (actor≠subject)
- **Deferred (by design):** vendor Entra/Okta click-path cookbooks
- **Cross-links:** api-design §4 Scope + deep-dive pointer; fullstack §7 Scope + cookie mechanics; ESC §3 / §11; root index + Auth/login/SSO learning path; Production hardening + Fullstack + B2B paths updated
- **Corpus:** acronyms SSO, JWKS, TOTP, CHIPS, DPoP, SAML, PAR, CIBA, JAR, RAR, OTP, FIDO, WebAuthn; GLOSSARY entries for Auth Code + PKCE, ID token, refresh rotation, denylist Redis, back-channel logout, token exchange, PAR, resource indicators, guest session, CIBA, JAR, RAR, passkey, impersonation

### apache-kafka platform gaps (enterprise shared cluster)
- **apache-kafka §5:** Tiered storage — hot/cold tiers, ops checklist, when to skip, compliance boundary vs WORM/warehouse
- **apache-kafka §9:** Event catalog and ownership SLOs — manifest fields, platform vs domain ownership, freshness SLO examples
- **apache-kafka §10:** Client quotas / noisy-neighbor; active-active multi-region playbook; ESC audit/PII cross-links; quota throttle metrics
- **apache-kafka §7:** MirrorMaker 2 topologies (active-passive, active-active, fan-in) + active-active hard requirements
- **enterprise-security-compliance §6/§7:** Bidirectional links to Kafka retention, ACLs, catalog classification, PII-on-bus patterns
- **data-platforms §5:** Event catalog as topic manifest; freshness SLO ownership mistake
- **Corpus:** GLOSSARY (client quota, tiered storage); See also rows on apache-kafka, ESC, data-platforms READMEs

### Feature → PROD release playbook
- **deployment-strategies §14:** Feature to PROD playbook — ordered gates (design → contract → quality → migration → promote → canary/flag → SLO rollback → runbook/drill)
- **deployment-strategies §7:** Lifecycle and cleanup — when/how to remove release flags (1–4 weeks after 100%, not months); reclassify kill switches; quarterly inventory
- **cursor-workflows §5:** Ship to PROD — post-merge Cursor workflow (promote, progressive expose, observe/abort, close-out); overview loop extended past code review
- **cursor-workflows §6:** Operate and learn — steady-state watch, cleanup, incidents/postmortems, drills, feed next FEATURE; loop closes back to §1 design; flag cleanup points at §7 lifecycle
- **Corpus:** Ship safely + Tech Lead Fullstack / Ship a public API / Cursor agents learning paths point at §14, §5, and §6

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
