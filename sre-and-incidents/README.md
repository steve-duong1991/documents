# SRE & Incidents Guide

A practical reference for tech leads running production services — SLIs/SLOs, error budgets, observability culture, alerting, incident command, postmortems, on-call, drills, and post-release hypercare.

Related: [high-throughput-systems §11](../high-throughput-systems/includes/11-observability.md) (signals and triage) · [deployment-strategies §13](../deployment-strategies/includes/13-slo-rollback-triggers.md) (SLO rollback) · [RUNBOOK-TEMPLATE.md](../RUNBOOK-TEMPLATE.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [SRE for Tech Leads](includes/00-overview.md) |
| 1 | [SLI, SLO, and SLA](includes/01-sli-slo-sla.md) |
| 2 | [Error budgets](includes/02-error-budgets.md) |
| 3 | [Capacity and load testing](includes/03-capacity-and-load-testing.md) |
| 4 | [Observability practice](includes/04-observability-practice.md) |
| 5 | [Alerting and paging](includes/05-alerting-and-paging.md) |
| 6 | [Incident command](includes/06-incident-command.md) |
| 7 | [Postmortems](includes/07-postmortems.md) |
| 8 | [On-call design](includes/08-on-call-design.md) |
| 9 | [Game days and drills](includes/09-game-days-and-drills.md) |
| 10 | [Synthetic monitoring](includes/10-synthetic-monitoring.md) |
| 10A | [Hypercare checklist (first 72h)](includes/10A-hypercare-checklist.md) |
| 11 | [Decision guide](includes/11-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Guide | Topics |
|-------|--------|
| [high-throughput-systems](../high-throughput-systems/README.md) | Measurement, saturation signals, observability layers |
| [deployment-strategies](../deployment-strategies/README.md) | Canary, progressive delivery, SLO(Service Level Objective)-based rollback |
| [cicd-and-environments](../cicd-and-environments/README.md) | Promotion, rollback vs forward-fix, health checks |
| [testing-strategy](../testing-strategy/README.md) | Load/soak/resilience tests, quality gates, prod verification |
| [resilience-patterns](../resilience-patterns/README.md) | Timeouts, retries, circuit breakers, failure domains |
| [database-connection-and-security](../database-connection-and-security/README.md) | Credential rotation, DR vocabulary, restore drills |
| [postgresql-performance](../postgresql-performance/README.md) | Backup/PITR(Point-in-Time Recovery), connection saturation |
| [api-design-and-protection](../api-design-and-protection/README.md) | Protection, threat model, checklist observability |
| [enterprise-security-compliance](../enterprise-security-compliance/README.md) | Secure SDLC(Software Development Life Cycle), audit logging, compliance evidence |
| [architecture-decisions](../architecture-decisions/README.md) | Failure domains, service boundaries |
| [api-rate-limiting](../api-rate-limiting/README.md) | Overload protection at the edge |
| [apache-kafka](../apache-kafka/README.md) | Consumer lag, ops and DR when streams are in path |
| [RUNBOOK-TEMPLATE.md](../RUNBOOK-TEMPLATE.md) | Per-service incident runbook skeleton |