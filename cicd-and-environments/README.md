# CI/CD & Environments Guide

A practical reference for tech leads designing build pipelines, environment promotion, config/secrets, flags as control, branching, rollback policy, container health, and platform boundaries.

Related: [deployment-strategies](../deployment-strategies/README.md) (how traffic moves) · [database-connection-and-security](../database-connection-and-security/README.md) (secrets, rotation) · [sre-and-incidents](../sre-and-incidents/README.md) (SLO gates, incidents)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [CI pipeline design](includes/01-ci-pipeline-design.md) |
| 2 | [CD and promotion](includes/02-cd-and-promotion.md) |
| 3 | [Config vs secrets](includes/03-config-vs-secrets.md) |
| 4 | [Feature flags as control](includes/04-feature-flags-as-control.md) |
| 5 | [Branching and release trains](includes/05-branching-and-release-trains.md) |
| 6 | [Rollback vs forward-fix](includes/06-rollback-vs-forward-fix.md) |
| 7 | [Containers and health](includes/07-containers-and-health.md) |
| 8 | [Platform boundaries](includes/08-platform-boundaries.md) |
| 9 | [Decision guide](includes/09-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Guide | Topics |
|-------|--------|
| [deployment-strategies](../deployment-strategies/README.md) | Rolling, canary, blue/green, flags, GitOps(Git Operations), SLO(Service Level Objective) rollback |
| [sre-and-incidents](../sre-and-incidents/README.md) | SLOs, error budgets, synthetics, incident response |
| [testing-strategy](../testing-strategy/README.md) | Pyramid, quality gates, flaky tests, prod verification |
| [api-design-and-protection](../api-design-and-protection/README.md) | Contract testing, stateless apps, checklist |
| [database-connection-and-security](../database-connection-and-security/README.md) | Secrets, IAM(Identity and Access Management), credential rotation |
| [enterprise-security-compliance](../enterprise-security-compliance/README.md) | Secure SDLC(Software Development Life Cycle), supply chain, secrets beyond DB |
| [high-throughput-systems](../high-throughput-systems/README.md) | Scale and deploy, observability signals |
| [architecture-decisions](../architecture-decisions/README.md) | Service boundaries, integration styles |
| [resilience-patterns](../resilience-patterns/README.md) | Timeouts, retries, bulkheads during rollout |
| [postgresql-performance](../postgresql-performance/README.md) | Schema migration coupling with deploys |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Projector compatibility during rolling deploys |
| [apache-kafka](../apache-kafka/README.md) | Safe deploy when consumers and schemas change |
| [api-rate-limiting](../api-rate-limiting/README.md) | Limit blast radius during canary |
| [RUNBOOK-TEMPLATE.md](../RUNBOOK-TEMPLATE.md) | Rollback and incident steps per service |