# Backpressure and Limits

High throughput systems must **reject, queue, or shed load** when at capacity — not queue unbounded work until they collapse.

> **Related:** Rate limit deployment layers → [api-rate-limiting/includes/07-deployment-layers.md](../../api-rate-limiting/includes/07-deployment-layers.md) · Algorithm choice → [api-rate-limiting/includes/10-decision-guide.md](../../api-rate-limiting/includes/10-decision-guide.md) · Rate tiers → [api-design-and-protection/includes/05-rate-limit-tiers.md](../../api-design-and-protection/includes/05-rate-limit-tiers.md) · Load shedding / degrade → [resilience §5](../../resilience-patterns/includes/05-load-shedding-and-degradation.md) · Timeouts / retries / breakers → [resilience-patterns](../../resilience-patterns/README.md)

---

## At a glance

| Mechanism | What it limits | Typical layer |
|-----------|----------------|---------------|
| **Rate limit (RPS)** | Requests per time window | Edge, gateway, app |
| **Concurrency semaphore** | Simultaneous expensive ops | App, worker pool |
| **Queue depth cap** | Backlog size | Queue consumer |
| **Circuit breaker** | Calls to failing downstream | App outbound client |
| **Timeout** | Max wait per hop | Gateway, app, DB client |

**Rule of thumb:** Shed load **as early as possible** — edge and gateway — but enforce **business-aware limits** (plan tier, expensive endpoints) in the app.

---

## Layered limits

```mermaid
flowchart LR
    Client --> Edge[Edge_CDN_coarse_RL]
    Edge --> GW[Gateway_per_API_key]
    GW --> App[App_per_endpoint_and_tier]
    App --> DB[DB_concurrency_semaphore]
```

| Concern | Best layer |
|---------|------------|
| Block garbage / DDoS(Distributed Denial of Service) | Edge / CDN(Content Delivery Network) |
| Enforce API(Application Programming Interface) key validity + global quota | API Gateway |
| Per-plan business quotas | App middleware |
| Protect database writes | App semaphore or leaky bucket near DB |

Full layer comparison → [api-rate-limiting/includes/07-deployment-layers.md](../../api-rate-limiting/includes/07-deployment-layers.md).

---

## HTTP 429 and Retry-After

When limiting, return proper semantics so clients backoff:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1718380800
```

| Header | Purpose |
|--------|---------|
| **`429`** | Client should retry later — not generic error |
| **`Retry-After`** | Seconds or HTTP-date until retry |
| **Rate limit headers** | Client-side throttling and UX |

---

## Concurrency semaphores

Rate limits cap **requests per second**; semaphores cap **in-flight expensive work**.

| Operation | Why semaphore |
|-----------|---------------|
| Full-text export | Long DB hold |
| Complex search | CPU + IO heavy |
| Bulk write endpoint | WAL(Write-Ahead Log) and lock pressure |
| External API fan-out | Partner rate limits |

```text
max_concurrent_exports = 10   // global across app cluster via Redis or DB
acquire_slot() → process → release_slot()
else → 429 or 503 with Retry-After
```

---

## Circuit breakers

When downstream (payment API, search cluster) fails or slows:

| State | Behavior |
|-------|----------|
| **Closed** | Normal calls |
| **Open** | Fail fast — no call for cooldown period |
| **Half-open** | Trial request; close on success |

**Throughput benefit:** Failing fast frees threads and connection pool slots for healthy paths.

---

## Fail-open vs fail-closed

If the rate-limit store (Redis) is unavailable:

| Route type | Default |
|------------|---------|
| **Public read (low cost)** | Fail-open with alert — availability bias |
| **Expensive writes, exports** | Fail-closed — abuse risk |
| **Auth validation** | Fail-closed |
| **Login / password reset** | Fail-closed |

See [api-rate-limiting/includes/07-deployment-layers.md](../../api-rate-limiting/includes/07-deployment-layers.md#fail-open-vs-fail-closed).

---

## Distributed rate limiting

| Type | Pros | Cons | When |
|------|------|------|------|
| **In-memory per instance** | Fastest | Wrong global count with N replicas | Dev, soft limits |
| **Centralized Redis** | Accurate global view | Dependency, latency | Production multi-instance |
| **Local + sync gossip** | No single bottleneck | Eventually consistent | Very large edge |

**Production pattern:** Redis with atomic `INCR` or Lua scripts; optional local shadow cache to cut round trips.

---

## Algorithm quick pick

| Scenario | Algorithm |
|----------|-----------|
| Strict fairness | Sliding window counter |
| Burst-friendly mobile | Token bucket |
| Protect slow downstream | Leaky bucket or concurrency limit |
| Simple monthly quota | Fixed window |

Full decision flow → [api-rate-limiting/includes/10-decision-guide.md](../../api-rate-limiting/includes/10-decision-guide.md).

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| IP-only limits on public API | Identity-based: API key, user ID |
| Per-instance counters | Shared Redis store |
| 200 OK with "rate limited" body | Use `429` + headers |
| No limit on async enqueue | Limit job creation rate too |
| Fail-open on paid write APIs | Fail closed + alert |

---

## Pros and cons

### Aggressive backpressure

**Pros:** Stable p99 under spike; protects DB and workers; predictable capacity.

**Cons:** Some requests rejected; client retry storms if `Retry-After` omitted.

### No backpressure

**Pros:** Accepts all traffic until collapse.

**Cons:** Cascading failure; 5xx instead of 429; long recovery.