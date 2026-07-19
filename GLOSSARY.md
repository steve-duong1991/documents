# Glossary

Terms reused across guides. For guide-specific terms, see each guide's includes.

| Term | Meaning | See also |
|------|---------|----------|
| **Aggregate (ES)** | Consistency boundary; state rebuilt by replaying its event stream | [event-sourcing-and-cqrs §1](event-sourcing-and-cqrs/includes/01-core-concepts.md) |
| **Apache Kafka** | Distributed commit log for event streaming, fan-out, and replay | [apache-kafka](apache-kafka/README.md) |
| **Avro** | Binary schema format common with Kafka Schema Registry | [apache-kafka §6](apache-kafka/includes/06-serialization-and-schema-evolution.md) |
| **At-least-once delivery** | Message may arrive more than once; consumer must be idempotent | [HTS §6](high-throughput-systems/includes/06-async-queues-workers.md), [api-design §13](api-design-and-protection/includes/13-idempotency.md) |
| **AuthN(Authentication)** | Who logged in? — primarily **OIDC(OpenID Connect)** (ID token / session), not “any JWT(JSON Web Token) to APIs” | [auth overview](auth-oauth-oidc-and-login-security/includes/00-overview.md#authn-vs-authz--and-oidc-vs-oauth-20), [auth §2](auth-oauth-oidc-and-login-security/includes/02-oidc-discovery-and-tokens.md) |
| **AuthZ(Authorization)** | What may this client/user do? — **OAuth(Open Authorization) 2.0** access tokens/scopes at the edge; object/tenant checks in the app | [auth overview](auth-oauth-oidc-and-login-security/includes/00-overview.md#authn-vs-authz--and-oidc-vs-oauth-20), [api-design §12D](api-design-and-protection/includes/12D-fine-grained-authz.md) |
| **Authorization Code + PKCE(Proof Key for Code Exchange)** | Default OAuth(Open Authorization) interactive grant; PKCE stops stolen `code` exchange | [auth §1](auth-oauth-oidc-and-login-security/includes/01-oauth2-grants-and-flows.md) |
| **A/B test** | Split users into control vs treatment variants to compare product metrics | [deployment §5](deployment-strategies/includes/05-ab-testing.md) |
| **ARB(Architecture Review Board)** | Lightweight forum for high blast-radius architecture decisions (not every ticket) | [architecture §5A](architecture-decisions/includes/05A-architecture-governance.md) |
| **Autovacuum** | PostgreSQL background process reclaiming dead tuples and updating stats | [PG §6](postgresql-performance/includes/06-vacuum-and-bloat.md) |
| **Backpressure** | Reject or queue load when downstream is saturated | [HTS §9](high-throughput-systems/includes/09-backpressure-and-limits.md) |
| **Back-channel logout** | IdP(Identity Provider) POSTs a logout_token JWT(JSON Web Token) to each RP so sessions die without browser iframes | [auth §2a](auth-oauth-oidc-and-login-security/includes/02A-oidc-logout-and-step-up.md) |
| **Blue/green** | Two full environments; switch traffic between them | [deployment-strategies §3](deployment-strategies/includes/03-blue-green.md) |
| **BOLA(Broken Object-Level Authorization)** | Broken object-level authorization — access to another user's resource | [api-design §2](api-design-and-protection/includes/02-api-protection.md), [§6](api-design-and-protection/includes/06-threat-model.md) |
| **BRIN(Block-Range Index) index** | Block-range index for very large, naturally ordered tables | [PG §2](postgresql-performance/includes/02-indexing.md) |
| **B+ tree** | Disk-oriented index; ordered keys; default PostgreSQL B-tree | [tree §1](tree-and-index-structures/includes/01-b-trees-and-b-plus.md), [PG §2](postgresql-performance/includes/02-indexing.md) |
| **CDC(Change Data Capture)** | Change data capture — stream DB changes to consumers (e.g. Debezium) | [HTS §15](high-throughput-systems/includes/15-cdc-and-search-indexing.md), [ES §5](event-sourcing-and-cqrs/includes/05-async-integration.md) |
| **Choreography** | Saga style: services react to events without central orchestrator | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **CloudEvents** | CNCF standard event envelope (`specversion`, `id`, `type`, `source`, `time`, `data`) for portable async messaging | [apache-kafka §6](apache-kafka/includes/06-serialization-and-schema-evolution.md#cloudevents) |
| **GIN(Generalized Inverted Index) index** | Inverted index for JSONB, arrays, and full-text in PostgreSQL | [PG §2](postgresql-performance/includes/02-indexing.md), [tree §6](tree-and-index-structures/includes/06-amplification-and-related-topics.md) |
| **Cache stampede** | Many concurrent cache misses hammering origin after expiry or cold start | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Cache-aside** | App reads cache, on miss loads DB and populates cache | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Canary** | Route small % of traffic to new version first | [deployment-strategies §4](deployment-strategies/includes/04-canary.md) |
| **Circuit breaker** | Stop calling a failing dependency after a threshold; fail fast or fallback | [resilience-patterns §3](resilience-patterns/includes/03-circuit-breakers.md), [HTS §9](high-throughput-systems/includes/09-backpressure-and-limits.md) |
| **Client quota (Kafka)** | Broker cap on produce/fetch byte or request rate per user/`client.id` — noisy-neighbor control | [apache-kafka §10](apache-kafka/includes/10-operations-dr-security-and-observability.md#client-quotas-and-noisy-neighbor) |
| **Compensating transaction** | Local undo step in a saga; semantically reverses a completed forward step | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Concurrent index** | `CREATE INDEX CONCURRENTLY` — builds index without blocking writes | [PG §15](postgresql-performance/includes/15-schema-migration-checklist.md) |
| **Consumer group** | Cooperating Kafka consumers sharing partition assignment and offsets | [apache-kafka §4](apache-kafka/includes/04-consumers-and-consumer-groups.md) |
| **Connection pool** | Reuse DB connections (PgBouncer, RDS Proxy) instead of one session per request | [PG §7](postgresql-performance/includes/07-connection-management.md), [database-connection](database-connection-and-security/README.md) |
| **CQRS(Command Query Responsibility Segregation)** | Separate write model and read models | [event-sourcing-and-cqrs](event-sourcing-and-cqrs/README.md) |
| **Data platform** | Set of stores beyond one OLTP DB — warehouse/lake, search, cache, bus — with ownership and sync paths | [data-platforms](data-platforms/README.md) |
| **Dead letter queue (DLQ)** | Queue for messages that failed max retries | [HTS §6](high-throughput-systems/includes/06-async-queues-workers.md), [§7](high-throughput-systems/includes/07-streaming-pipelines.md) |
| **FinOps(Cloud Financial Operations)** | Engineering practice treating cloud cost as a design and ops constraint | [finops-and-cost](finops-and-cost/README.md) |
| **Error budget** | Allowed unreliability below SLO (100% − SLO) | [HTS §11](high-throughput-systems/includes/11-observability.md) |
| **Event sourcing** | State from append-only domain events | [event-sourcing-and-cqrs](event-sourcing-and-cqrs/README.md) |
| **Eventual consistency** | Reads may lag writes; acceptable when business tolerates staleness | [PG §14](postgresql-performance/includes/14-consistency-promises-and-costs.md), [ES §2](event-sourcing-and-cqrs/includes/02-cqrs-and-read-models.md) |
| **Expand / contract** | Safe migration: add schema → deploy → remove old | [deployment §12](deployment-strategies/includes/12-schema-migrations-and-deploy.md), [PG §15](postgresql-performance/includes/15-schema-migration-checklist.md) |
| **Experiment flag** | Short-lived feature flag that assigns users to A/B variants | [deployment §5](deployment-strategies/includes/05-ab-testing.md), [§7 flag types](deployment-strategies/includes/07-feature-flags.md#flag-types) |
| **Fail closed (rate limit)** | Block traffic when the limit store (Redis) is unavailable | [api-rate-limiting §11](api-rate-limiting/includes/11-common-mistakes-and-architecture.md) |
| **Fail open (rate limit)** | Allow traffic when the limit store is down, often with a local emergency cap | [api-rate-limiting §11](api-rate-limiting/includes/11-common-mistakes-and-architecture.md) |
| **Feature flag** | Runtime toggle to enable/disable behavior without redeploy | [deployment-strategies §7](deployment-strategies/includes/07-feature-flags.md) |
| **Flag lifecycle / cleanup** | Remove release flags after 100% + bake; reclassify kill switches | [deployment §7 lifecycle](deployment-strategies/includes/07-feature-flags.md#lifecycle-and-cleanup) |
| **Feature to PROD playbook** | Ordered release gates from design through canary, rollback, and drills | [deployment §14](deployment-strategies/includes/14-feature-to-prod-playbook.md), [cursor-workflows §5](cursor-workflows/includes/05-ship-to-prod.md) |
| **Game day** | Scheduled failure drill (tabletop or live) to practice detect/mitigate/recover | [sre §9](sre-and-incidents/includes/09-game-days-and-drills.md) |
| **Operate and learn** | Post-ramp phase: watch, cleanup, incidents, drills, next backlog | [cursor-workflows §6](cursor-workflows/includes/06-operate-and-learn.md) |
| **GitOps(Git Operations)** | Declarative infra/app state in git; cluster reconciles to desired state | [deployment-strategies §9](deployment-strategies/includes/09-gitops.md) |
| **Hot key** | Cache or DB key receiving disproportionate traffic; throughput bottleneck | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Hypercare** | Structured 24–72 h watch after PROD ramp — SLOs plus business KPI and CX signals before calling a release done | [sre §10A](sre-and-incidents/includes/10A-hypercare-checklist.md) |
| **JTBD(Jobs To Be Done)** | Frame discovery around the user’s job, not a feature list | [tech-lead §1A](tech-lead-practice/includes/01A-product-discovery.md) |
| **Idempotency key** | Client header for safe retry of writes | [api-design §13](api-design-and-protection/includes/13-idempotency.md) |
| **ID token** | OIDC(OpenID Connect) JWT(JSON Web Token) proving who authenticated to the client (not for API(Application Programming Interface) Bearer) | [auth §2](auth-oauth-oidc-and-login-security/includes/02-oidc-discovery-and-tokens.md) |
| **Inbox pattern** | Consumer dedup table — same TX as side effect; pairs with outbox | [ES §5A](event-sourcing-and-cqrs/includes/05A-outbox-and-inbox.md), [ES §5](event-sourcing-and-cqrs/includes/05-async-integration.md) |
| **ISR (In-Sync Replicas)** | Kafka followers caught up with partition leader | [apache-kafka §2](apache-kafka/includes/02-topics-partitions-and-replication.md) |
| **KRaft** | Kafka Raft metadata mode (replaces ZooKeeper) | [apache-kafka §1](apache-kafka/includes/01-commit-log-and-internals.md) |
| **LSM(Log-Structured Merge) tree** | Log-structured merge; write-optimized storage | [tree-and-index-structures §4](tree-and-index-structures/includes/04-lsm-trees.md) |
| **Memtable** | In-memory sorted buffer in LSM; absorbs writes before flush to disk | [tree §4](tree-and-index-structures/includes/04-lsm-trees.md) |
| **Materialized view** | PostgreSQL snapshot of a query; fast reads until `REFRESH` | [PG §11](postgresql-performance/includes/11-read-scaling-and-caching.md#materialized-views), [§9](postgresql-performance/includes/09-views-functions-and-scale-out-terminology.md#materialized-views) |
| **Multi-tenant** | One deployment serves many customer orgs; data isolated per tenant | [arch §10](architecture-decisions/includes/10-multi-tenant-system-models.md), [api-design §16](api-design-and-protection/includes/16-multi-tenant-apis.md), [auth §2d](auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md) |
| **Regional cell / residency** | Independent stack slice + contract that tenant data stays in a pinned region | [arch §10A](architecture-decisions/includes/10A-regional-cells-and-residency.md) |
| **Team Topologies** | Four team types + three interaction modes so org design and architecture reinforce each other | [architecture §1A](architecture-decisions/includes/01A-team-topologies.md) |
| **Modernization program** | Multi-quarter strangler as waves with dual-run KPIs, cutover RACI, and an exit | [architecture §4A](architecture-decisions/includes/04A-modernization-program.md) |
| **Home-realm discovery (HRD)** | Map work email / domain (or slug) to the customer IdP before OIDC(OpenID Connect) `/authorize` | [auth §2d](auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md) |
| **Multi-issuer validation** | Accept JWTs only when `iss` is on the **active tenant’s** allowlist (per-issuer JWKS(JSON Web Key Set)) | [auth §2d](auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md), [auth §3](auth-oauth-oidc-and-login-security/includes/03-token-lifecycle-and-validation.md) |
| **Tenant membership** | User↔tenant role row; session holds `active_tenant_id` (user may belong to many orgs) | [auth §2d](auth-oauth-oidc-and-login-security/includes/02D-multi-tenant-oidc-and-b2b-sso.md) |
| **SCIM(System for Cross-domain Identity Management)** | HTTP(Hypertext Transfer Protocol) API for IdP-driven create/update/deactivate of Users/Groups in your app | [api-design §12C](api-design-and-protection/includes/12C-scim-and-jml-provisioning.md) |
| **JML(Joiner-Mover-Leaver)** | Identity lifecycle stages: hire, role change, offboard — often automated via SCIM | [api-design §12C](api-design-and-protection/includes/12C-scim-and-jml-provisioning.md), [§12A](api-design-and-protection/includes/12A-identity-active-directory.md) |
| **JIT(Just-In-Time) provisioning** | Create local user/membership on first successful SSO(Single Sign-On) instead of pre-provision | [api-design §12C](api-design-and-protection/includes/12C-scim-and-jml-provisioning.md) |
| **ReBAC(Relationship-Based Access Control)** | AuthZ(Authorization) from relation tuples (Zanzibar-style); not coarse JWT roles alone | [api-design §12D](api-design-and-protection/includes/12D-fine-grained-authz.md) |
| **DSAR(Data Subject Access Request)** | Subject requests access/export/erasure of personal data across stores | [ESC §7A](enterprise-security-compliance/includes/07A-erasure-and-dsar.md) |
| **Optimistic concurrency** | Detect conflicting writes via version/check; retry on conflict | [ES §1](event-sourcing-and-cqrs/includes/01-core-concepts.md), [PG §12](postgresql-performance/includes/12-bulk-operations-and-concurrency.md) |
| **OLAP(Online Analytical Processing)** | Analytical workloads — scans, aggregates, history; typically warehouse/lake | [data-platforms §1](data-platforms/includes/01-oltp-vs-olap.md) |
| **OLTP(Online Transaction Processing)** | Transactional workloads — short reads/writes, constraints; typically primary PostgreSQL | [data-platforms §1](data-platforms/includes/01-oltp-vs-olap.md), [postgresql-performance](postgresql-performance/README.md) |
| **Offset (Kafka)** | Position of a record in a partition log | [apache-kafka §4](apache-kafka/includes/04-consumers-and-consumer-groups.md) |
| **Outbox pattern** | DB table + relay for reliable event publish | [ES §5A](event-sourcing-and-cqrs/includes/05A-outbox-and-inbox.md), [ES §5](event-sourcing-and-cqrs/includes/05-async-integration.md), [api-design §10](api-design-and-protection/includes/10-async-patterns.md) |
| **Partition (Kafka)** | Ordered sub-stream within a topic; unit of parallelism | [apache-kafka §2](apache-kafka/includes/02-topics-partitions-and-replication.md) |
| **PAR(Pushed Authorization Requests)** | POST authorize params to AS first; redirect with short-lived `request_uri` | [auth §1c](auth-oauth-oidc-and-login-security/includes/01C-pushed-authorization-requests.md) |
| **CIBA(Client-Initiated Backchannel Authentication)** | Client starts AuthN(Authentication) out-of-band; user authenticates on a consumption device | [auth §1e](auth-oauth-oidc-and-login-security/includes/01E-device-authorization-and-ciba.md) |
| **JAR(JWT-secured Authorization Request)** | Authorize parameters as a signed (optional encrypted) JWT request object | [auth §1f](auth-oauth-oidc-and-login-security/includes/01F-jar-and-rar.md) |
| **RAR(Rich Authorization Requests)** | Structured `authorization_details` beyond flat OAuth scopes | [auth §1f](auth-oauth-oidc-and-login-security/includes/01F-jar-and-rar.md) |
| **Guest / anonymous session** | Narrow pre-login `sid` for cart/wizard; promote + rotate on register/login | [auth §4b](auth-oauth-oidc-and-login-security/includes/04B-anonymous-and-guest-sessions.md) |
| **Passkey / WebAuthn(Web Authentication)** | Origin-bound public-key AuthN (FIDO(Fast IDentity Online)2); phishing-resistant | [auth §5c](auth-oauth-oidc-and-login-security/includes/05C-webauthn-and-passkeys.md) |
| **Magic link** | One-time email link for verify or passwordless login; single-use short TTL(Time To Live) | [auth §5b](auth-oauth-oidc-and-login-security/includes/05B-signup-verify-and-magic-links.md) |
| **Impersonation (support)** | Actor acts as subject with TTL, ticket, and audit — not a silent user session | [auth §5d](auth-oauth-oidc-and-login-security/includes/05D-impersonation-and-support-access.md) |
| **Concurrent session / device revoke** | List and kill per-device `sid` / refresh families; logout-others vs everywhere | [auth §3e](auth-oauth-oidc-and-login-security/includes/03E-concurrent-sessions-and-devices.md) |
| **Partitioning** | Split one logical table across child tables on a single PostgreSQL server | [PG §10](postgresql-performance/includes/10-partitioning.md) |
| **PITR(Point-in-Time Recovery)** | Point-in-time recovery from WAL(Write-Ahead Log) + backup | [PG §16](postgresql-performance/includes/16-backup-restore-and-pitr.md), [database-connection §12](database-connection-and-security/includes/12-credential-rotation-and-dr.md) |
| **Projector** | Process that builds read models from events | [event-sourcing-and-cqrs §2](event-sourcing-and-cqrs/includes/02-cqrs-and-read-models.md) |
| **Process manager** | Central saga orchestrator that sends commands and tracks workflow state | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Projector rebuild** | Recompute read models from full event history; runbook for schema changes | [ES §3](event-sourcing-and-cqrs/includes/03-storage-and-projections.md), [deployment §12](deployment-strategies/includes/12-schema-migrations-and-deploy.md) |
| **Protobuf** | Binary schema format; common with gRPC and Kafka | [apache-kafka §6](apache-kafka/includes/06-serialization-and-schema-evolution.md) |
| **Rate limit tier** | Product quota (free/paid/enterprise) | [api-design §5](api-design-and-protection/includes/05-rate-limit-tiers.md) |
| **Read replica** | Standby replaying WAL; offloads SELECT, adds replication lag | [PG §11](postgresql-performance/includes/11-read-scaling-and-caching.md) |
| **Read-your-writes** | User sees own write immediately after POST | [PG §14](postgresql-performance/includes/14-consistency-promises-and-costs.md), [api-design §11](api-design-and-protection/includes/11-stateless-architecture.md) |
| **Refresh token rotation** | Issue new refresh on each use; reuse of old refresh revokes the family | [auth §3](auth-oauth-oidc-and-login-security/includes/03-token-lifecycle-and-validation.md) |
| **Resource indicator** | OAuth `resource` / token `aud` naming which API may accept the access token | [auth §1d](auth-oauth-oidc-and-login-security/includes/01D-resource-indicators.md) |
| **Revoke / force logout** | Invalidate sessions and refresh; optional `jti` denylist for still-valid access JWTs | [auth §3b](auth-oauth-oidc-and-login-security/includes/03B-revoke-logout-denylist.md) |
| **Denylist Redis patterns** | Key shapes and TTLs for `jti` / session / user ban / refresh family in Redis | [auth §3c](auth-oauth-oidc-and-login-security/includes/03C-denylist-redis-patterns.md) |
| **Replication** | Full copy of database on another node for HA or read scale | [PG §9](postgresql-performance/includes/09-views-functions-and-scale-out-terminology.md), [§11](postgresql-performance/includes/11-read-scaling-and-caching.md) |
| **RLS(Row-Level Security)** | PostgreSQL policy that filters rows per session (e.g. per `tenant_id`) | [PG §17](postgresql-performance/includes/17-row-level-security-multi-tenant.md), [api-design §16](api-design-and-protection/includes/16-multi-tenant-apis.md) |
| **Schema / DB per tenant** | Silo isolation — one PostgreSQL schema or database per customer org | [PG §18](postgresql-performance/includes/18-schema-and-database-per-tenant.md), [arch §10](architecture-decisions/includes/10-multi-tenant-system-models.md) |
| **Rolling deploy** | Replace instances incrementally; mixed versions during rollout | [deployment-strategies §2](deployment-strategies/includes/02-rolling.md) |
| **RPO(Recovery Point Objective)** | Recovery point objective — max data loss | [database-connection §12](database-connection-and-security/includes/12-credential-rotation-and-dr.md) |
| **RTO(Recovery Time Objective)** | Recovery time objective — max downtime to restore | [database-connection §12](database-connection-and-security/includes/12-credential-rotation-and-dr.md) |
| **Saga** | Sequence of local transactions across services; failure undone via compensating actions | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Schema Registry** | Central store for Kafka schema versions and compatibility | [apache-kafka §6](apache-kafka/includes/06-serialization-and-schema-evolution.md) |
| **Sharding** | Horizontal split of data across multiple independent database nodes | [PG §9](postgresql-performance/includes/09-views-functions-and-scale-out-terminology.md) |
| **Singleflight** | Coalesce concurrent cache misses into one origin fetch | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **RED(Rate, Errors, Duration) method** | Rate, errors, duration — monitor request-driven services | [HTS §11](high-throughput-systems/includes/11-observability.md) |
| **SLO(Service Level Objective)** | Service level objective (target reliability/latency) | [HTS §1](high-throughput-systems/includes/01-measurement-and-slo.md), [§11](high-throughput-systems/includes/11-observability.md) |
| **SLI(Service Level Indicator)** | Service level indicator — measured metric for an SLO | [HTS §1](high-throughput-systems/includes/01-measurement-and-slo.md), [§11](high-throughput-systems/includes/11-observability.md) |
| **SSTable** | Immutable on-disk sorted file in LSM; merged during compaction | [tree §4](tree-and-index-structures/includes/04-lsm-trees.md) |
| **Subagent** | Specialist agent spawned by a parent Cursor agent for isolated subtasks | [cursor-agents §3](cursor-agents/includes/03-subagents-and-auto-delegation.md) |
| **Compaction (LSM)** | Background merge of SSTables; reclaims space and limits read amplification | [tree §4](tree-and-index-structures/includes/04-lsm-trees.md), [§6 amplification](tree-and-index-structures/includes/06-amplification-and-related-topics.md) |
| **SSRF(Server-Side Request Forgery)** | Server-side request forgery — unsafe outbound fetches (e.g. webhook URL) | [api-design §10](api-design-and-protection/includes/10-async-patterns.md) |
| **Snapshot (ES)** | Cached aggregate state at version N; not source of truth | [ES §3](event-sourcing-and-cqrs/includes/03-storage-and-projections.md) |
| **Stateless app tier** | No session in process memory; horizontal scale | [api-design §11](api-design-and-protection/includes/11-stateless-architecture.md) |
| **Sliding session idle** | Extend idle timeout on activity without extending absolute cap | [auth §3d](auth-oauth-oidc-and-login-security/includes/03D-lifetimes-and-sliding-sessions.md) |
| **SAML(Security Assertion Markup Language) 2.0** | XML federation protocol (enterprise SSO(Single Sign-On)); prefer OIDC in apps, bridge when needed | [auth §2c](auth-oauth-oidc-and-login-security/includes/02C-saml-protocol.md) |
| **Tenant** | One customer org (company, workspace) on shared SaaS(Software as a Service) infrastructure | [api-design §16](api-design-and-protection/includes/16-multi-tenant-apis.md#what-is-a-tenant), [arch §10](architecture-decisions/includes/10-multi-tenant-system-models.md) |
| **TCO(Total Cost of Ownership)** | Invoice plus engineering time and risk — used in build vs managed choices | [finops §5](finops-and-cost/includes/05-build-vs-managed-cost.md) |
| **Thundering herd** | Same as cache stampede — synchronized miss storm on hot keys | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Tiered storage (Kafka)** | Hot local log segments + cold object storage for long retention | [apache-kafka §5](apache-kafka/includes/05-retention-compaction-and-storage.md#tiered-storage) |
| **Topic (Kafka)** | Named stream of partitioned logs | [apache-kafka §2](apache-kafka/includes/02-topics-partitions-and-replication.md) |
| **Token bucket** | Rate limit algorithm allowing controlled bursts | [api-rate-limiting §4](api-rate-limiting/includes/04-token-bucket.md) |
| **Token / cookie integrity** | Detect client tampering via JWT signature or opaque server lookup — not by trusting the client | [auth §3a](auth-oauth-oidc-and-login-security/includes/03A-token-cookie-integrity.md) |
| **Token exchange (OBO)** | OAuth grant that swaps a subject token for a new audience-scoped access token (BFF→API) | [auth §1a](auth-oauth-oidc-and-login-security/includes/01A-client-auth-and-token-exchange.md) |
| **Third-party cookie deprecation** | Browsers block/partition cross-site cookies — breaks iframe silent renew and front-channel logout | [auth §4a](auth-oauth-oidc-and-login-security/includes/04A-third-party-cookies-and-mobile-redirects.md) |
| **Transactional outbox** | Same transaction: business write + outbox row | [ES §5A](event-sourcing-and-cqrs/includes/05A-outbox-and-inbox.md), [ES §5](event-sourcing-and-cqrs/includes/05-async-integration.md) |
| **Two-phase commit (2PC)** | Distributed commit protocol across nodes; avoided for microservice sagas | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Unit economics (infra)** | Cost per request, tenant, or feature used to judge design margin | [finops §1](finops-and-cost/includes/01-unit-economics.md) |
| **Upcasting** | Transform historical event schema on read (v1 → v2) | [ES §8](event-sourcing-and-cqrs/includes/08-event-schema-evolution.md) |
| **USE(Utilization, Saturation, Errors) method** | Utilization, saturation, errors — monitor resources | [HTS §11](high-throughput-systems/includes/11-observability.md) |
| **Write-through cache** | Update cache and DB together on write | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Consistent hashing** | Hash ring with virtual nodes so remapping touches few keys when nodes change | [distributed-systems-primitives §2](distributed-systems-primitives/includes/02-consistent-hashing.md) |
| **CRDT(Conflict-free Replicated Data Type)** | Mergeable data type for concurrent edits without central locking | [realtime-at-scale §4](realtime-at-scale/includes/04-crdt-and-ot.md) |
| **GSI(Global Secondary Index)** | Alternate partition/sort key projection on a key-value table (DynamoDB-style) | [nosql §2](nosql-and-key-value-stores/includes/02-access-pattern-modeling.md) |
| **Hot partition** | Disproportionate traffic on one shard/key range; throughput ceiling | [nosql §2](nosql-and-key-value-stores/includes/02-access-pattern-modeling.md), [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Presigned URL** | Time-limited signed URL for direct client↔object-storage upload/download | [api-design §18](api-design-and-protection/includes/18-object-storage-and-uploads.md) |
| **Snowflake ID** | Time-sortable unique ID from timestamp + worker + sequence bits | [distributed-systems-primitives §3](distributed-systems-primitives/includes/03-unique-ids.md) |
| **Double-entry ledger** | Every money movement is balanced debit + credit journal lines | [payments §3](payments-and-fintech/includes/03-ledger-and-double-entry.md) |
| **PCI DSS(Payment Card Industry Data Security Standard)** | Cardholder-data security standard; reduce scope via tokenization/hosted fields | [payments §1](payments-and-fintech/includes/01-pci-scope-reduction.md) |
| **RAG(Retrieval-Augmented Generation)** | Retrieve relevant chunks (often via vector ANN(Approximate Nearest Neighbor)) then generate with an LLM | [specialized-data-systems §3](specialized-data-systems/includes/03-vector-and-rag.md) |
| **Capacity estimation** | Back-of-envelope QPS, storage, connections, and memory before designing | [architecture-decisions §13](architecture-decisions/includes/13-capacity-estimation.md) |