# Decision Guide — Choosing a Limiter

> **Related:** Algorithm sections §1–§5 · Deployment layers → [§7](07-deployment-layers.md) · Distributed store → [§12](12-distributed-rate-limiting.md) · Common mistakes → [§11](11-common-mistakes-and-architecture.md) · Product tiers → [api-design §5](../../api-design-and-protection/includes/05-rate-limit-tiers.md)

## Algorithm decision flow

```mermaid
flowchart TD
    Start[Need rate limiting?] --> Q1{Strict fairness required?}
    Q1 -->|Yes| SW[Sliding Window Counter or Log]
    Q1 -->|No| Q2{Burst traffic expected?}
    Q2 -->|Yes| TB[Token Bucket]
    Q2 -->|No| Q3{Protect slow downstream?}
    Q3 -->|Yes| LB[Leaky Bucket or Concurrency Limit]
    Q3 -->|No| FW[Fixed Window — simple quotas]

    SW --> Q4{Multi-instance deployment?}
    TB --> Q4
    LB --> Q4
    FW --> Q4
    Q4 -->|Yes| Redis[Redis / distributed store]
    Q4 -->|No| Mem[In-memory OK for dev/single node]
```

## Scenario recommendations

| Scenario | Recommended stack |
|----------|-------------------|
| Public REST(Representational State Transfer) API (SaaS) | Sliding window + per API key + per-endpoint on heavy routes |
| Mobile app backend | Token bucket (burst-friendly) + per user |
| Login / auth endpoints | Sliding window log, strict per-IP + per-username |
| Internal microservices | Gateway global limit + per-service concurrency |
| GraphQL | Cost-based limiting + query depth/complexity analysis |
| File upload API | Per-user quota + concurrent upload limit + bandwidth cap |
| LLM(Large Language Model) / inference API | Token bucket on tokens/min + per-user daily quota |
| DDoS(Distributed Denial of Service) / volumetric attack | Edge/CDN(Content Delivery Network) rate limit + WAF(Web Application Firewall) before app logic |
| Paid API with tiers | Quota system + per API key + graduated response |

## Common stack combinations

### Starter (single service)

```text
Nginx limit_req (per-IP) → App middleware (per user) → Handler
```

### Production SaaS

```text
Cloudflare (edge) → Kong (per API key, sliding window) → App (per-endpoint weights) → Redis
```

### High-stakes / attack-prone

```text
CDN + WAF → API Gateway → Adaptive limits → Redis → App concurrency semaphore
```

## Common mistakes

| Mistake | Fix |
|---------|-----|
| One algorithm for all endpoints | Match algorithm to fairness and burst needs |
| In-memory limiter on multi-node app | Redis or gateway-enforced distributed store |
| Login endpoint same limit as read API | Stricter per-IP + per-username on auth routes |
| GraphQL with only request count | Cost-based limits + depth/complexity caps |
| No fail-open/closed policy documented | Define behavior when Redis is unavailable |