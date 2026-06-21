# Glossary

Terms reused across guides. For guide-specific terms, see each guide's includes.

| Term | Meaning | See also |
|------|---------|----------|
| **Aggregate (ES)** | Consistency boundary; state rebuilt by replaying its event stream | [event-sourcing-and-cqrs §1](event-sourcing-and-cqrs/includes/01-core-concepts.md) |
| **At-least-once delivery** | Message may arrive more than once; consumer must be idempotent | [HTS §6](high-throughput-systems/includes/06-async-queues-workers.md), [api-design §13](api-design-and-protection/includes/13-idempotency.md) |
| **Autovacuum** | PostgreSQL background process reclaiming dead tuples and updating stats | [PG §6](postgresql-performance/includes/06-vacuum-and-bloat.md) |
| **Backpressure** | Reject or queue load when downstream is saturated | [HTS §9](high-throughput-systems/includes/09-backpressure-and-limits.md) |
| **Blue/green** | Two full environments; switch traffic between them | [deployment-strategies §3](deployment-strategies/includes/03-blue-green.md) |
| **BOLA(Broken Object-Level Authorization)** | Broken object-level authorization — access to another user's resource | [api-design §2](api-design-and-protection/includes/02-api-protection.md), [§6](api-design-and-protection/includes/06-threat-model.md) |
| **BRIN(Block-Range Index) index** | Block-range index for very large, naturally ordered tables | [PG §2](postgresql-performance/includes/02-indexing.md) |
| **B+ tree** | Disk-oriented index; ordered keys; default PostgreSQL B-tree | [tree §1](tree-and-index-structures/includes/01-b-trees-and-b-plus.md), [PG §2](postgresql-performance/includes/02-indexing.md) |
| **CDC(Change Data Capture)** | Change data capture — stream DB changes to consumers (e.g. Debezium) | [HTS §15](high-throughput-systems/includes/15-cdc-and-search-indexing.md), [ES §5](event-sourcing-and-cqrs/includes/05-async-integration.md) |
| **Choreography** | Saga style: services react to events without central orchestrator | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **GIN(Generalized Inverted Index) index** | Inverted index for JSONB, arrays, and full-text in PostgreSQL | [PG §2](postgresql-performance/includes/02-indexing.md), [tree §6](tree-and-index-structures/includes/06-amplification-and-related-topics.md) |
| **Cache stampede** | Many concurrent cache misses hammering origin after expiry or cold start | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Cache-aside** | App reads cache, on miss loads DB and populates cache | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Canary** | Route small % of traffic to new version first | [deployment-strategies §4](deployment-strategies/includes/04-canary.md) |
| **Circuit breaker** | Stop calling a failing dependency after a threshold; fail fast or fallback | [HTS §9](high-throughput-systems/includes/09-backpressure-and-limits.md) |
| **Compensating transaction** | Local undo step in a saga; semantically reverses a completed forward step | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Concurrent index** | `CREATE INDEX CONCURRENTLY` — builds index without blocking writes | [PG §15](postgresql-performance/includes/15-schema-migration-checklist.md) |
| **Connection pool** | Reuse DB connections (PgBouncer, RDS Proxy) instead of one session per request | [PG §7](postgresql-performance/includes/07-connection-management.md), [database-connection](database-connection-and-security/README.md) |
| **CQRS(Command Query Responsibility Segregation)** | Separate write model and read models | [event-sourcing-and-cqrs](event-sourcing-and-cqrs/README.md) |
| **Dead letter queue (DLQ)** | Queue for messages that failed max retries | [HTS §6](high-throughput-systems/includes/06-async-queues-workers.md), [§7](high-throughput-systems/includes/07-streaming-pipelines.md) |
| **Error budget** | Allowed unreliability below SLO (100% − SLO) | [HTS §11](high-throughput-systems/includes/11-observability.md) |
| **Event sourcing** | State from append-only domain events | [event-sourcing-and-cqrs](event-sourcing-and-cqrs/README.md) |
| **Eventual consistency** | Reads may lag writes; acceptable when business tolerates staleness | [PG §14](postgresql-performance/includes/14-consistency-promises-and-costs.md), [ES §2](event-sourcing-and-cqrs/includes/02-cqrs-and-read-models.md) |
| **Expand / contract** | Safe migration: add schema → deploy → remove old | [deployment §12](deployment-strategies/includes/12-schema-migrations-and-deploy.md), [PG §15](postgresql-performance/includes/15-schema-migration-checklist.md) |
| **Fail closed (rate limit)** | Block traffic when the limit store (Redis) is unavailable | [api-rate-limiting §11](api-rate-limiting/includes/11-common-mistakes-and-architecture.md) |
| **Fail open (rate limit)** | Allow traffic when the limit store is down, often with a local emergency cap | [api-rate-limiting §11](api-rate-limiting/includes/11-common-mistakes-and-architecture.md) |
| **Feature flag** | Runtime toggle to enable/disable behavior without redeploy | [deployment-strategies §7](deployment-strategies/includes/07-feature-flags.md) |
| **GitOps(Git Operations)** | Declarative infra/app state in git; cluster reconciles to desired state | [deployment-strategies §9](deployment-strategies/includes/09-gitops.md) |
| **Hot key** | Cache or DB key receiving disproportionate traffic; throughput bottleneck | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Idempotency key** | Client header for safe retry of writes | [api-design §13](api-design-and-protection/includes/13-idempotency.md) |
| **Inbox pattern** | Consumer dedup table — same TX as side effect; pairs with outbox | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md), [ES §5](event-sourcing-and-cqrs/includes/05-async-integration.md) |
| **LSM(Log-Structured Merge) tree** | Log-structured merge; write-optimized storage | [tree-and-index-structures §4](tree-and-index-structures/includes/04-lsm-trees.md) |
| **Optimistic concurrency** | Detect conflicting writes via version/check; retry on conflict | [ES §1](event-sourcing-and-cqrs/includes/01-core-concepts.md), [PG §12](postgresql-performance/includes/12-bulk-operations-and-concurrency.md) |
| **Outbox pattern** | DB table + relay for reliable event publish | [ES §5](event-sourcing-and-cqrs/includes/05-async-integration.md), [api-design §10](api-design-and-protection/includes/10-async-patterns.md) |
| **Partitioning** | Split one logical table across child tables on a single PostgreSQL server | [PG §10](postgresql-performance/includes/10-partitioning.md) |
| **PITR(Point-in-Time Recovery)** | Point-in-time recovery from WAL(Write-Ahead Log) + backup | [PG §16](postgresql-performance/includes/16-backup-restore-and-pitr.md), [database-connection §12](database-connection-and-security/includes/12-credential-rotation-and-dr.md) |
| **Projector** | Process that builds read models from events | [event-sourcing-and-cqrs §2](event-sourcing-and-cqrs/includes/02-cqrs-and-read-models.md) |
| **Process manager** | Central saga orchestrator that sends commands and tracks workflow state | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Projector rebuild** | Recompute read models from full event history; runbook for schema changes | [ES §3](event-sourcing-and-cqrs/includes/03-storage-and-projections.md), [deployment §12](deployment-strategies/includes/12-schema-migrations-and-deploy.md) |
| **Rate limit tier** | Product quota (free/paid/enterprise) | [api-design §5](api-design-and-protection/includes/05-rate-limit-tiers.md) |
| **Read replica** | Standby replaying WAL; offloads SELECT, adds replication lag | [PG §11](postgresql-performance/includes/11-read-scaling-and-caching.md) |
| **Read-your-writes** | User sees own write immediately after POST | [PG §14](postgresql-performance/includes/14-consistency-promises-and-costs.md), [api-design §11](api-design-and-protection/includes/11-stateless-architecture.md) |
| **Replication** | Full copy of database on another node for HA or read scale | [PG §9](postgresql-performance/includes/09-views-functions-and-scale-out-terminology.md), [§11](postgresql-performance/includes/11-read-scaling-and-caching.md) |
| **Rolling deploy** | Replace instances incrementally; mixed versions during rollout | [deployment-strategies §2](deployment-strategies/includes/02-rolling.md) |
| **RPO(Recovery Point Objective)** | Recovery point objective — max data loss | [database-connection §12](database-connection-and-security/includes/12-credential-rotation-and-dr.md) |
| **RTO(Recovery Time Objective)** | Recovery time objective — max downtime to restore | [database-connection §12](database-connection-and-security/includes/12-credential-rotation-and-dr.md) |
| **Saga** | Sequence of local transactions across services; failure undone via compensating actions | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Sharding** | Horizontal split of data across multiple independent database nodes | [PG §9](postgresql-performance/includes/09-views-functions-and-scale-out-terminology.md) |
| **Singleflight** | Coalesce concurrent cache misses into one origin fetch | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **RED(Rate, Errors, Duration) method** | Rate, errors, duration — monitor request-driven services | [HTS §11](high-throughput-systems/includes/11-observability.md) |
| **SLO(Service Level Objective)** | Service level objective (target reliability/latency) | [HTS §1](high-throughput-systems/includes/01-measurement-and-slo.md), [§11](high-throughput-systems/includes/11-observability.md) |
| **SLI(Service Level Indicator)** | Service level indicator — measured metric for an SLO | [HTS §1](high-throughput-systems/includes/01-measurement-and-slo.md), [§11](high-throughput-systems/includes/11-observability.md) |
| **SSRF(Server-Side Request Forgery)** | Server-side request forgery — unsafe outbound fetches (e.g. webhook URL) | [api-design §10](api-design-and-protection/includes/10-async-patterns.md) |
| **Snapshot (ES)** | Cached aggregate state at version N; not source of truth | [ES §3](event-sourcing-and-cqrs/includes/03-storage-and-projections.md) |
| **Stateless app tier** | No session in process memory; horizontal scale | [api-design §11](api-design-and-protection/includes/11-stateless-architecture.md) |
| **Thundering herd** | Same as cache stampede — synchronized miss storm on hot keys | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |
| **Token bucket** | Rate limit algorithm allowing controlled bursts | [api-rate-limiting §4](api-rate-limiting/includes/04-token-bucket.md) |
| **Transactional outbox** | Same transaction: business write + outbox row | [ES §5](event-sourcing-and-cqrs/includes/05-async-integration.md) |
| **Two-phase commit (2PC)** | Distributed commit protocol across nodes; avoided for microservice sagas | [ES §7](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Upcasting** | Transform historical event schema on read (v1 → v2) | [ES §8](event-sourcing-and-cqrs/includes/08-event-schema-evolution.md) |
| **USE(Utilization, Saturation, Errors) method** | Utilization, saturation, errors — monitor resources | [HTS §11](high-throughput-systems/includes/11-observability.md) |
| **Write-through cache** | Update cache and DB together on write | [HTS §4](high-throughput-systems/includes/04-caching-layers.md) |