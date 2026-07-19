# Implementation Map

Where the patterns in this guide usually show up in real stacks — without turning the guide into a library tutorial.

> **Related:** Policy placement → [§11](11-policy-placement.md) · HTTP(Hypertext Transfer Protocol) clients / APIs → [api-design-and-protection](../../api-design-and-protection/README.md) · Mesh discovery → [distributed-systems-primitives §5](../../distributed-systems-primitives/includes/05-service-discovery.md)

---

## At a glance

| Pattern | Typical knobs |
|---------|----------------|
| **Timeouts** | HTTP client connect/request; gRPC(Google Remote Procedure Call) deadlines; context/cancellation |
| **Retries + jitter** | Client middleware; queue visibility + max receive count |
| **Circuit breakers** | App libraries; mesh outlier ejection |
| **Bulkheads** | Semaphores, bounded executors, per-host pools |
| **Shed / degrade** | Gateway rate limits; app admission; feature flags |
| **Idempotency** | `Idempotency-Key` store; consumer dedup keys |
| **Drain** | SIGTERM handlers; K8s grace; LB deregister |

**Rule of thumb:** Prefer **one** well-configured client wrapper per dependency over copy-pasted timeouts in every call site.

---

## Library / platform pointers (illustrative)

| Ecosystem | Common building blocks |
|-----------|------------------------|
| **Java** | Resilience4j (retry/breaker/bulkhead); Micrometer; Spring `RestClient`/`WebClient` timeouts |
| **.NET** | `Polly` / Microsoft resilience pipelines; `HttpClient` timeout + `CancellationToken` |
| **Go** | `context.WithTimeout`; `golang.org/x/time/rate`; semaphores / bounded worker pools |
| **Node** | `AbortController` deadlines; `p-retry` / `cockatiel`; undici/connect timeouts |
| **Python** | `httpx`/`aiohttp` timeouts; `tenacity`; asyncio semaphores |
| **Envoy / Istio / Linkerd** | Route timeouts, retry budgets, outlier detection — keep aligned with [§11](11-policy-placement.md) |
| **API(Application Programming Interface) gateways** | Coarse timeout, rate limit, 429 — [api-rate-limiting](../../api-rate-limiting/README.md) |
| **Kubernetes** | readiness/liveness, `terminationGracePeriodSeconds`, PodDisruptionBudget — [cicd §7](../../cicd-and-environments/includes/07-containers-and-health.md) |
| **Queues** | SQS(Simple Queue Service) visibility + DLQ(Dead Letter Queue); Kafka max.poll + retry topics — [§8](08-delivery-semantics.md) |

Names change; the **controls** (deadline, budget, isolation, owner layer) do not.

---

## Minimal client wrapper checklist

For each outbound dependency:

- [ ] Connect timeout + request/deadline timeout
- [ ] Cancellation hooked to parent context
- [ ] Retry policy explicit (`none` is valid) + jitter
- [ ] Idempotency mode documented
- [ ] Concurrency cap (bulkhead)
- [ ] Breaker or mesh outlier (not both fighting)
- [ ] Metrics from [§13](13-observability-for-resilience.md)
- [ ] Fallback/degrade path if tier ≥ T1

---

## What not to expect from this map

| Out of scope here | See instead |
|-------------------|-------------|
| Full library tutorials | Upstream docs for your stack |
| Mesh install / CRDs | Platform / cicd guides |
| Payment-specific charge classes | [payments-and-fintech](../../payments-and-fintech/README.md) |
| Exact timeout numbers | Measure p99 — [HTS §1](../../high-throughput-systems/includes/01-measurement-and-slo.md) |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Framework defaults left infinite | Set timeouts in the shared client |
| Two retry middlewares registered | One owner — [§2](02-retries-backoff-jitter.md), [§11](11-policy-placement.md) |
| Breaker library without metrics | Export state — [§13](13-observability-for-resilience.md) |
| Per-call ad hoc policies | Shared named policies per dependency |

## Pros and cons

| | Shared client policies | Ad hoc per call site |
|--|------------------------|----------------------|
| **Pros** | Consistent; reviewable | Flexible |
| **Cons** | Needs platform ownership | Drift and missed deadlines |