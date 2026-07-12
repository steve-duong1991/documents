# Stateless architecture — auth, consistency, and operations

> **Related:** Core concepts → [Stateless architecture](11-stateless-architecture.md) · Auth model → [04-auth-model.md](04-auth-model.md) · Async workers → [10-async-patterns.md](10-async-patterns.md)

## Stateless auth flow

Typical token-based flow for public APIs:

```mermaid
sequenceDiagram
    autonumber
    participant U as User / Client
    participant Auth as Auth service
    participant API as API (any instance)
    participant DB as Database

    U->>Auth: POST /oauth/token (credentials or code)
    Auth->>DB: Verify user
    Auth-->>U: access_token (JWT) + refresh_token

    U->>API: GET /v1/profile<br/>Authorization: Bearer access_token
    Note over API: Validate signature + expiry<br/>Optional: check revocation list
    API->>DB: Fetch profile by user_id from claims
    API-->>U: 200 Profile JSON

    U->>Auth: POST /oauth/token (refresh_token)
    Auth-->>U: New access_token
```

| Approach | Stateless? | Tradeoff |
|----------|------------|----------|
| JWT(JSON Web Token) access token (short TTL) | Yes — local validation | Revocation needs denylist or very short TTL |
| Opaque token + Redis lookup | Hybrid | DB/cache hit per request; easier revocation |
| Server-side session cookie | No | Requires sticky sessions or shared session store |
| API(Application Programming Interface) key in header | Yes | Key rotation and scoping discipline required |

---

## Reference architecture (stateless app tier)

How stateless services fit the [reference stack](08-lifecycle-and-architecture.md#reference-architecture--public-saas-api):

```mermaid
flowchart TB
    Client[Client] --> Edge[Edge: WAF / DDoS]
    Edge --> GW[API Gateway<br/>auth, rate limits]
    GW --> LB[Load Balancer<br/>no sticky sessions]
    LB --> App1[App instance 1]
    LB --> App2[App instance 2]
    LB --> App3[App instance 3]

    App1 --> Redis[(Redis — cache, rate limits, ephemeral data)]
    App2 --> Redis
    App3 --> Redis

    App1 --> DB[(PostgreSQL — source of truth)]
    App2 --> DB
    App3 --> DB

    App1 --> Queue[(Queue — async jobs)]
    App2 --> Queue
    App3 --> Queue
```

| Pattern | Role in stateless design |
|---------|--------------------------|
| **JWT access tokens** | Identity travels with every request |
| **Redis** | Shared cache and counters — not per-app memory |
| **PostgreSQL** | Durable transactional state |
| **Message queue** | Decouple work; workers are interchangeable |
| **Object storage** | Files and exports — not local disk |
| **Idempotency keys** | Safe retries without duplicate side effects |

---

## Benefits

| Benefit | Why it matters for APIs |
|---------|-------------------------|
| **Horizontal scaling** | Scale on CPU, latency, or queue depth — not session count |
| **High availability** | Failed instance does not strand a cohort of users |
| **Simple deployments** | Blue/green, rolling, canary — new instances serve traffic immediately |
| **Cloud-native fit** | Containers, Kubernetes, serverless, auto-scaling |
| **Load balancer freedom** | Any routing algorithm; no session drain on scale-down |
| **Easier testing** | Each request is self-contained; no hidden server state |
| **Multi-region** | Requests can land in any region if data is shared or replicated |
| **Rate-limit fairness** | Shared Redis counters; identity-based tiers work across nodes |

---

## Use cases

| Use case | Why stateless fits |
|----------|-------------------|
| **REST(Representational State Transfer) / GraphQL public APIs** | Each call is independent; JWT/API keys carry identity |
| **Microservices** | Services scale and fail independently |
| **Third-party partner APIs** | Unknown client count; elastic scale required |
| **Serverless / FaaS** | Functions are ephemeral by design |
| **Mobile & SPA backends** | Clients hold tokens; no cookie-based server sessions |
| **CDN(Content Delivery Network)-backed read APIs** | Cacheable responses; no per-server session |
| **Queue workers** | Workers pull jobs; no affinity to a specific machine |
| **Blue/green & canary deploys** | New version instances accept traffic without session migration |

---

## Pros and cons

### Pros

- Elastic scaling — add replicas under load, remove them off-peak
- Resilience — blast radius of a bad instance is one request, not many users
- Operational simplicity — identical instances, no session replication cluster
- Aligns with [12-factor app](https://12factor.net/processes) — processes are disposable; state is external
- Pairs naturally with API gateway + load balancer entry architecture
- Enables safe [deployment strategies](../../deployment-strategies/README.md) (rolling, blue/green)

### Cons

- **Token management complexity** — expiry, refresh tokens, revocation lists, key rotation
- **More network I/O** — context often fetched from DB/cache every request (mitigate with caching)
- **JWT payload size** — embedding too many claims bloats headers
- **Revocation is harder** — stateless JWTs cannot be "deleted" without extra infra (denylist, short TTL)
- **Not ideal for all workloads** — WebSockets, long-lived connections, in-memory game rooms
- **Consistency tradeoffs** — distributed caches and read replicas introduce eventual consistency

See [Strong consistency — promises and costs](../../postgresql-performance/includes/14-consistency-promises-and-costs.md) for definitions, costs, and when to require primary reads.

---

## Consistency and read routing

Stateless APIs often fetch context from a DB or cache on every request. That makes **read routing** a consistency decision, not just a performance one.

| Read type | Route to | Example endpoints |
|-----------|----------|-------------------|
| **Strong / session-critical** | Primary DB | `GET /me`, post-checkout order status, balance after transfer |
| **Eventual / stale OK** | Read replica or cache | Product lists, dashboards, search suggestions |
| **Read-your-writes** | Primary for N seconds after user's write, or poll until visible | Create resource → immediate GET by ID |

**API practices:**

- Document consistency per endpoint in OpenAPI (e.g. "Read model may lag up to 30s")
- Return **`409 Conflict`** with `ETag` / version on stale updates — aligns with optimistic concurrency on the write side
- After **`202` async jobs**, treat result reads like projections — poll until complete; don't assume immediate consistency on a replica

> **Related:** Layered read path and replication lag → [Read scaling and caching](../../postgresql-performance/includes/11-read-scaling-and-caching.md) · CQRS(Command Query Responsibility Segregation) projector lag → [Eventual consistency in read models](../../event-sourcing-and-cqrs/includes/02-cqrs-and-read-models.md#eventual-consistency)
- **Security discipline** — never trust client-sent identity without cryptographic validation

---

## When stateless is the wrong default

| Scenario | Better approach |
|----------|-----------------|
| **WebSocket / SSE(Server-Sent Events) connection state** | Stateful connection gateway + stateless business logic behind it |
| **In-memory chat/game room** | Dedicated stateful service or CRDT(Conflict-free Replicated Data Type)/sync layer |
| **Heavy model loaded once per GPU** | Stateful worker pool with routing to warm instances |
| **Legacy apps with server sessions** | Sticky sessions temporarily → migrate to external session store (Redis) |
| **Strong immediate revocation required** | Short-lived tokens + introspection endpoint or session store lookup |

**Hybrid is common:** stateless HTTP(Hypertext Transfer Protocol) API + stateful connection layer (WebSocket server forwarding to stateless services).

```mermaid
flowchart LR
    Client[Client] --> WS[WebSocket gateway<br/>holds connection]
    WS --> API1[Stateless API]
    WS --> API2[Stateless API]
    API1 --> DB[(Shared DB)]
    API2 --> DB
```

---

## Migrating from stateful to stateless

```mermaid
flowchart TD
    S1[Server-side sessions in memory] --> S2[External session store<br/>Redis keyed by session_id]
    S2 --> S3[JWT access tokens<br/>no session store for reads]
    S3 --> S4[Remove sticky sessions<br/>from load balancer]
```

| Step | Action |
|------|--------|
| 1 | Move session data from app memory to Redis or DB |
| 2 | Issue JWT or opaque tokens; stop growing in-memory session maps |
| 3 | Remove sticky sessions from load balancer |
| 4 | Verify any instance can serve any authenticated request |
| 5 | Externalize uploads, temp files, and local caches |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Sticky sessions enabled "just in case" | Remove affinity once auth is token-based |
| User ID from request body without token validation | Derive identity only from validated JWT/API key |
| Rate limits stored per instance | Shared Redis counters at gateway or app |
| Shopping cart in server memory | Redis or DB keyed by `user_id` |
| File uploads to local disk | Stream to object storage (S3) |
| Assuming "no session" means "no state anywhere" | State belongs in external stores, not nowhere |
| Long-lived JWT with no revocation plan | Short TTL + refresh token + optional denylist |

---

## Checklist: is your app tier stateless?

| Check | Pass? |
|-------|-------|
| Any instance can handle any request without sticky sessions | |
| User identity comes from validated token/key, not server memory | |
| Durable data is in DB/cache/storage, not local disk or RAM | |
| You can kill an instance mid-traffic without corrupting user state | |
| You can add a new instance and immediately send it traffic | |
| Uploads, temp files, and job state are externalized | |
| Rate limits and idempotency use shared stores | |
| Config and secrets come from env/vault, not local files | |

---

## Decision summary

| Question | Default for public APIs |
|----------|-------------------------|
| Store sessions in app memory? | No — use JWT or external session store |
| Sticky sessions on load balancer? | No — unless legacy migration in progress |
| Where does durable state live? | PostgreSQL + Redis + object storage + queue |
| Where is AuthZ enforced? | Application code on every instance ([Auth model](04-auth-model.md)) |
| Can workers share a queue? | Yes — design workers as stateless consumers |
| Stateless at the gateway too? | Gateway holds policy state (rate limits in Redis), not user sessions |