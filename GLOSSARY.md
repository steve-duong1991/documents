# Glossary

Terms reused across guides. For guide-specific terms, see each guide's includes.

| Term | Meaning | See also |
|------|---------|----------|
| **Aggregate (ES)** | Consistency boundary; state rebuilt by replaying its event stream | event-sourcing-and-cqrs §1 |
| **At-least-once delivery** | Message may arrive more than once; consumer must be idempotent | HTS §6, api-design §13 |
| **Autovacuum** | PostgreSQL background process reclaiming dead tuples and updating stats | PG §6 |
| **Backpressure** | Reject or queue load when downstream is saturated | HTS §9 |
| **Blue/green** | Two full environments; switch traffic between them | deployment-strategies §3 |
| **B+ tree** | Disk-oriented index; ordered keys; default in PostgreSQL | tree-and-index-structures |
| **Cache stampede** | Many concurrent cache misses hammering origin after expiry or cold start | HTS §4 |
| **Cache-aside** | App reads cache, on miss loads DB and populates cache | HTS §4 |
| **Canary** | Route small % of traffic to new version first | deployment-strategies §4 |
| **Circuit breaker** | Stop calling a failing dependency after a threshold; fail fast or fallback | HTS §9 |
| **Compensating transaction** | Local undo step in a saga; semantically reverses a completed forward step | ES §7 |
| **Concurrent index** | `CREATE INDEX CONCURRENTLY` — builds index without blocking writes | PG §15 |
| **Connection pool** | Reuse DB connections (PgBouncer, RDS Proxy) instead of one session per request | PG §7, database-connection |
| **CQRS** | Separate write model and read models | event-sourcing-and-cqrs |
| **Dead letter queue (DLQ)** | Queue for messages that failed max retries | HTS §6, §7 |
| **Error budget** | Allowed unreliability below SLO (100% − SLO) | HTS §11 |
| **Event sourcing** | State from append-only domain events | event-sourcing-and-cqrs |
| **Eventual consistency** | Reads may lag writes; acceptable when business tolerates staleness | PG §14, ES §2 |
| **Expand / contract** | Safe migration: add schema → deploy → remove old | deployment §12, PG §15 |
| **Fail closed (rate limit)** | Block traffic when the limit store (Redis) is unavailable | api-rate-limiting §11 |
| **Fail open (rate limit)** | Allow traffic when the limit store is down, often with a local emergency cap | api-rate-limiting §11 |
| **Feature flag** | Runtime toggle to enable/disable behavior without redeploy | deployment-strategies §7 |
| **GitOps** | Declarative infra/app state in git; cluster reconciles to desired state | deployment-strategies §9 |
| **Hot key** | Cache or DB key receiving disproportionate traffic; throughput bottleneck | HTS §4 |
| **Idempotency key** | Client header for safe retry of writes | api-design §13 |
| **Inbox pattern** | Consumer dedup table — same TX as side effect; pairs with outbox | ES §7, ES §5 |
| **LSM tree** | Log-structured merge; write-optimized storage | tree-and-index-structures §4 |
| **Optimistic concurrency** | Detect conflicting writes via version/check; retry on conflict | ES §1, PG §12 |
| **Outbox pattern** | DB table + relay for reliable event publish | ES §5, api-design §10 |
| **Partitioning** | Split one logical table across child tables on a single PostgreSQL server | PG §10 |
| **PITR** | Point-in-time recovery from WAL + backup | database-connection §12 |
| **Projector** | Process that builds read models from events | event-sourcing-and-cqrs §2 |
| **Process manager** | Central saga orchestrator that sends commands and tracks workflow state | ES §7 |
| **Projector rebuild** | Recompute read models from full event history; runbook for schema changes | ES §3, deployment §12 |
| **Rate limit tier** | Product quota (free/paid/enterprise) | api-design §5 |
| **Read replica** | Standby replaying WAL; offloads SELECT, adds replication lag | PG §11 |
| **Read-your-writes** | User sees own write immediately after POST | PG §14, api-design §11 |
| **Replication** | Full copy of database on another node for HA or read scale | PG §9, §11 |
| **Rolling deploy** | Replace instances incrementally; mixed versions during rollout | deployment-strategies §2 |
| **RPO** | Recovery point objective — max data loss | database-connection §12 |
| **RTO** | Recovery time objective — max downtime to restore | database-connection §12 |
| **Saga** | Sequence of local transactions across services; failure undone via compensating actions | ES §7 |
| **Sharding** | Horizontal split of data across multiple independent database nodes | PG §9 |
| **Singleflight** | Coalesce concurrent cache misses into one origin fetch | HTS §4 |
| **SLO** | Service level objective (target reliability/latency) | HTS §1, §11 |
| **Snapshot (ES)** | Cached aggregate state at version N; not source of truth | ES §3 |
| **Stateless app tier** | No session in process memory; horizontal scale | api-design §11 |
| **Thundering herd** | Same as cache stampede — synchronized miss storm on hot keys | HTS §4 |
| **Token bucket** | Rate limit algorithm allowing controlled bursts | api-rate-limiting §4 |
| **Transactional outbox** | Same transaction: business write + outbox row | ES §5 |
| **Two-phase commit (2PC)** | Distributed commit protocol across nodes; avoided for microservice sagas | ES §7 |
| **Write-through cache** | Update cache and DB together on write | HTS §4 |
