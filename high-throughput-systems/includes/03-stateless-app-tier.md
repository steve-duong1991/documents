# Stateless App Tier

Horizontal throughput requires **interchangeable app instances** — no sticky sessions, bounded concurrency, pooled connections, and minimal work per request.

> **Scope:** **Throughput lens** — per-request cost, bounded concurrency, pool sizing, when to scale replicas. Full stateless architecture (auth flows, migration, checklist) → [api-design §11 Stateless architecture](../../api-design-and-protection/includes/11-stateless-architecture.md).
>
> **Related:** Full stateless guide → [api-design §11](../../api-design-and-protection/includes/11-stateless-architecture.md) · Connection pooling → [postgresql-performance §7](../../postgresql-performance/includes/07-connection-management.md) · API(Application Programming Interface) design → [api-design §1](../../api-design-and-protection/includes/01-api-design.md)

---

## At a glance

| Requirement | Why it matters for throughput |
|-------------|-------------------------------|
| **Stateless handlers** | Any instance serves any request — LB scales freely |
| **Bounded concurrency** | Prevents connection storms and OOM(Out Of Memory) |
| **Connection pooling** | Reuse DB connections — don't open per request |
| **Cheap requests** | Higher RPS at fixed CPU |

**Rule of thumb:** Scale **replicas** only when each instance is doing minimal necessary work and pools are sized correctly.

---

## Horizontal scale prerequisites

Stateless app tier is required before horizontal scale pays off. Architecture, auth flows, migration steps, and full checklist → [api-design §11 Stateless architecture](../../api-design-and-protection/includes/11-stateless-architecture.md).

**Throughput-specific prerequisites:**

- **Bounded concurrency** — thread pools, semaphores, and DB pool limits per instance
- **Shared rate-limit counters** — Redis at gateway or app, not per instance → [api-rate-limiting §11](../../api-rate-limiting/includes/11-common-mistakes-and-architecture.md)
- **Connection pooling** — `(pool_size × instances)` must fit DB capacity → [postgresql-performance §7](../../postgresql-performance/includes/07-connection-management.md)

---

## Request cost breakdown

```mermaid
flowchart LR
    Req[Incoming_request] --> Auth[Validate_JWT]
    Auth --> Cache[Cache_lookup]
    Cache --> DB[DB_query]
    DB --> Logic[Business_logic]
    Logic --> Ser[Serialize_JSON]
    Ser --> Resp[Response]
```

| Phase | Optimization |
|-------|--------------|
| **Auth** | Local JWT(JSON Web Token) verify; cache introspection if opaque token |
| **Cache** | Redis hit avoids DB |
| **DB** | Index, eliminate N+1, pagination cap |
| **Logic** | Move heavy work to queue |
| **Serialize** | Field selection; smaller payloads |

Profile which phase dominates before adding instances.

---

## Bounded concurrency

| Resource | Limit |
|----------|-------|
| **HTTP(Hypertext Transfer Protocol) server threads / workers** | Match CPU and I/O profile |
| **DB pool per instance** | `(pool_size × instances) < DB max safe connections` |
| **Outbound HTTP clients** | Cap parallel calls to partners |
| **Expensive handlers** | Global semaphore (exports, search) |

**Unbounded concurrency** → memory growth, pool exhaustion, cascading timeouts.

### Pool sizing example

```
10 app instances × 20 pool connections = 200 DB connections
→ Use PgBouncer if PostgreSQL max_connections is ~100–300
```

See [postgresql-performance/includes/07-connection-management.md](../../postgresql-performance/includes/07-connection-management.md).

---

## I/O model

| Workload | Typical approach |
|----------|------------------|
| **I/O-bound** (DB, HTTP, cache) | Async runtime — Node, Go goroutines, Java virtual threads |
| **CPU-bound** (crypto, encoding) | Fixed worker pool; scale instances |
| **Mixed** | Async I/O + bounded pool for CPU sections |

Match model to profile — async does not help CPU-bound hot loops.

---

## Reduce per-request cost

| Technique | Throughput impact |
|-----------|-------------------|
| **Cursor pagination + max `limit`** | Bounded response size |
| **Field selection / sparse fieldsets** | Less DB and JSON work |
| **Eliminate N+1** | One query or batch load |
| **Batch endpoints** | Amortize auth and HTTP overhead |
| **Compression** (gzip/brotli) | Bandwidth — trade CPU |

API design details → [01-api-design.md](../../api-design-and-protection/includes/01-api-design.md).

---

## Workers are stateless too

Async workers follow the same rules — pull from queue, read/write shared stores, exit. Scale worker count on **queue depth**, not CPU alone.

See [06-async-queues-workers.md](06-async-queues-workers.md).

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Sticky sessions enabled | Token auth + external state |
| `pool_size = 100` per instance | Size pool × instances vs DB limit |
| Sync call to 5 microservices | Parallelize, cache, or aggregate in BFF(Backend for Frontend) |
| No pagination cap | Enforce max `limit` |
| Rate limit in app memory only | Shared Redis counters → [api-rate-limiting §11](../../api-rate-limiting/includes/11-common-mistakes-and-architecture.md) |

---

## Checklist (throughput)

| Check | Pass? |
|-------|-------|
| DB pool sized with PgBouncer if needed | |
| Expensive ops have concurrency caps | |
| Heavy work enqueued — not blocking request thread | |
| Per-request cost profiled before adding replicas | |

Full stateless checklist (identity, externalized state, deploy safety) → [api-design §11](../../api-design-and-protection/includes/11A-stateless-auth-operations.md#checklist-is-your-app-tier-stateless).