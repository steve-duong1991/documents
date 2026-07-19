# Load Shedding and Degradation

Protect core user journeys when the system is overloaded — reject or simplify work deliberately.

> **Related:** Backpressure → [HTS §9](../../high-throughput-systems/includes/09-backpressure-and-limits.md) · Rate limits → [api-rate-limiting](../../api-rate-limiting/README.md) · Dependency tiers → [architecture §11](../../architecture-decisions/includes/11-failure-domains.md) · Checkout example → [§12](12-worked-example-checkout.md) · Metrics → [§13](13-observability-for-resilience.md)

---

## At a glance

| Mode | Meaning |
|------|---------|
| **Load shedding** | Refuse some work (429/503) to save the rest |
| **Degradation** | Serve partial/simpler responses |
| **Admission control** | Bound concurrency before queues explode |

**Rule of thumb:** Shed **non-critical** and **expensive** work first. Never “try harder” with unbounded queues when CPU, pools, or dependencies are saturated.

---

## Shedding order

```mermaid
flowchart TD
    Sat[Saturation signal] --> DropAnon[Shed anonymous / abusive]
    DropAnon --> DropT2[Disable T2 features]
    DropT2 --> DegradeT1[Degrade T1: cache/stale/skip]
    DegradeT1 --> ProtectT0[Protect T0 with strict caps]
    ProtectT0 --> Reject[Reject excess with 503]
```

| Signal | Action |
|--------|--------|
| Queue depth high | Stop accepting heavy jobs |
| Pool wait spiking | Shed reads that hit DB |
| p99 past SLO(Service Level Objective) | Enable degrade flags |
| Dependency breaker open | Cached or empty optional sections |

---

## Degradation patterns

| Pattern | Example |
|---------|---------|
| **Stale cache** | Show last known profile |
| **Feature flag off** | Hide recommendations |
| **Approximate answers** | Count estimates |
| **Async fallback** | Accept write, process later |
| **Static fallback page** | Maintenance-lite for T2 sites |

Product must agree what “degraded” means before the incident.

---

## Fallback contracts (what the client gets)

Degradation is a **contract**, not an accident. For each T1/T2 dependency, pick one primary fallback and document it for UI, BFF(Backend for Frontend), and API(Application Programming Interface) consumers.

| Fallback | Client sees | When acceptable | Risk |
|----------|-------------|-----------------|------|
| **Stale cache** | Last good payload + optional `stale: true` / age header | Browse, profiles, catalogs | Wrong price/stock if TTL too long |
| **Empty / omit section** | Field absent or `[]`; rest of page OK | Recs, ads, “customers also bought” | Layout shift if UI assumes presence |
| **Approximate / default** | Estimate, generic copy, offline defaults | Counts, badges, non-binding ETA | Users treat estimate as truth |
| **Hard error (fail closed)** | 4xx/5xx for that resource | T0 money, authZ, inventory reserve | Better than silent wrong write |
| **Async accept** | `202` + job id; poll or notify later | Non-critical writes under overload | Backlog; need DLQ(Dead Letter Queue) |

| Tier | Default fallback |
|------|------------------|
| **T0** | No silent degrade — fail closed or bounded async with clear UX |
| **T1** | Stale or omit; never block T0 on T1 latency |
| **T2** | Omit or best-effort queue; never on the request critical path |

**Contract checklist**

- [ ] Status/body shape when degraded (same schema vs explicit degrade flag)
- [ ] Max staleness for cache fallbacks
- [ ] Whether clients should retry (usually **no** on intentional shed)
- [ ] Product copy for partial UX (“Recommendations unavailable”)
- [ ] Metric: `degrade_mode` / fallback hit rate — [§13](13-observability-for-resilience.md)

Worked example → [§12 checkout](12-worked-example-checkout.md).

---

## Relation to rate limiting

| Layer | Role |
|-------|------|
| Edge / gateway limits | Fairness and abuse — [api-rate-limiting](../../api-rate-limiting/README.md) |
| App admission | Protect local resources |
| Dependency bulkhead | Protect outbound |

Use `Retry-After` and clear errors so well-behaved clients back off — [api-rate-limiting §9](../../api-rate-limiting/includes/09-response-strategies.md).

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Unbounded in-memory queue | Cap + shed |
| Shedding randomly including checkout | Priority by tier |
| Degrade without metrics | Track degrade mode rate — [§13](13-observability-for-resilience.md) |
| Stale fallback with no TTL bound | Cap age; fall to omit/error when too old |
| UI assumes T1 fields always present | Contract for omit/empty |
| Only shedding at edge | Also shed in workers |
| Fail-open on expensive writes | Fail closed under uncertainty |

## Pros and cons

| | Controlled shed/degrade | No admission control |
|--|-------------------------|----------------------|
| **Pros** | Survives overload with core UX | — |
| **Cons** | Needs product design | Meltdown for everyone |