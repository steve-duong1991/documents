# Incident Runbook — orders-api (example)

Filled example for [RUNBOOK-TEMPLATE.md](RUNBOOK-TEMPLATE.md). Copy structure, replace values for your service.

> **Related:** SLO(Service Level Objective) rollback → [deployment-strategies/includes/13-slo-rollback-triggers.md](deployment-strategies/includes/13-slo-rollback-triggers.md) · Observability → [high-throughput-systems/includes/11-observability.md](high-throughput-systems/includes/11-observability.md) · DR(Disaster Recovery) restore → [postgresql-performance/includes/16-backup-restore-and-pitr.md](postgresql-performance/includes/16-backup-restore-and-pitr.md)

---

## Metadata

| Field | Value |
|-------|-------|
| **Service** | orders-api |
| **Owner** | platform-commerce / `#oncall-commerce` |
| **Last tested** | 2026-05-15 (rollback drill) |
| **Severity** | SEV1 if checkout p99 > 2s or 5xx > 1% for 5 min |

---

## Symptoms

- Alert `orders-api-p99-high`: p99 > 2s on `GET /v1/orders`, `POST /v1/orders`
- Alert `orders-api-5xx-rate`: 5xx > 1% on checkout routes
- Alert `orders-worker-lag`: SQS(Simple Queue Service) `orders-export` depth > 10k for 15 min

**Dashboards:** Grafana `commerce/orders-api` · Datadog `orders-api-production`

---

## Triage (first 5 minutes)

```mermaid
flowchart TD
    A[Alert fired] --> B{Deploy in last 2h?}
    B -->|Yes| C[Compare error by build_id]
    C --> D{SLO breach?}
    D -->|Yes| Rollback[Roll back canary / rolling]
    B -->|No| E{Pool wait or queue lag?}
    E -->|Yes| F[Scale workers / throttle export tier]
    E -->|No| G[Trace slow span — DB or payments-api]
```

| Check | Command / dashboard |
|-------|---------------------|
| Last deploy | Argo CD(Continuous Delivery) `orders-api` · `build_id` metric |
| Error by route | Grafana `orders-api` by `route` |
| DB pool wait | `pg_stat_activity` · pool metric `wait_count` |
| Consumer lag | SQS `orders-export` approximate age |
| Replication lag | `pg_stat_replication` · lag < 5s SLO |

---

## Mitigation options

| Option | When | Steps |
|--------|------|-------|
| **Rollback deploy** | Error spike matches new `build_id` | Argo rollback to previous revision; verify p99 < 500ms |
| **Disable flag** | `new-checkout-flow` correlated | LaunchDarkly disable `checkout-v2` |
| **Scale workers** | Queue lag, low 5xx | HPA `orders-worker` max 20 → manual 30 if needed |
| **Rate limit export** | Abuse or partner bulk export | Gateway tier cap; 429 on `POST /v1/exports` |
| **Failover read** | Primary DB CPU saturated | Route session reads to primary only; pause replica reads for dashboards |
| **DB failover** | Primary unavailable | Runbook: `database-connection` §12 + PG §16 PITR(Point-in-Time Recovery) |

---

## Escalation

| Condition | Escalate to |
|-----------|-------------|
| Payment double-capture suspected | payments team + SEV1 incident commander |
| Data corruption in `orders` table | DBA + engineering lead |
| > 30 min SEV1 unresolved | commerce EM |

---

## Post-incident

- [ ] Timeline in `#incidents` doc
- [ ] Root cause (5 whys)
- [ ] Action items with owners
- [ ] Update this runbook if steps were wrong
- [ ] Add regression test or alert if gap found

---

## Related guides

| Topic | Link |
|-------|------|
| Rollback triggers | [deployment-strategies §13](deployment-strategies/includes/13-slo-rollback-triggers.md) |
| DR / PITR | [PG §16 backup restore](postgresql-performance/includes/16-backup-restore-and-pitr.md) |
| On-call triage | [HTS §11 observability](high-throughput-systems/includes/11-observability.md) |
| Saga stuck orders | [ES §7 sagas](event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |