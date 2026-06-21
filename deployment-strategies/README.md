# Deployment Strategies Guide

A practical reference for common deployment patterns — how they work, pros and cons, when to use each, and best practices.

Related: [api-design-and-protection](../api-design-and-protection/README.md) (stateless architecture enables safe rollouts) · [high-throughput-systems](../high-throughput-systems/README.md) (scale and deploy layer)

---

## Table of contents

| # | Strategy |
|---|----------|
| — | [Quick comparison](includes/00-overview.md) |
| 1 | [Recreate (Big Bang)](includes/01-recreate.md) |
| 2 | [Rolling deployment](includes/02-rolling.md) |
| 3 | [Blue-Green deployment](includes/03-blue-green.md) |
| 4 | [Canary deployment](includes/04-canary.md) |
| 5 | [A/B testing](includes/05-ab-testing.md) |
| 6 | [Shadow / mirror / dark launch](includes/06-shadow.md) |
| 7 | [Feature flags](includes/07-feature-flags.md) |
| 8 | [Immutable deployment](includes/08-immutable.md) |
| 9 | [GitOps](includes/09-gitops.md) |
| 10 | [Progressive delivery](includes/10-progressive-delivery.md) |
| 11 | [Choosing a strategy & best practices](includes/11-choosing-and-practices.md) |
| 12 | [Schema migrations and deploy coupling](includes/12-schema-migrations-and-deploy.md) |
| 13 | [SLO-based rollback triggers](includes/13-slo-rollback-triggers.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../api-design-and-protection/README.md) | Stateless app tier, lifecycle, reference architecture |
| [high-throughput-systems](../high-throughput-systems/README.md) | Autoscaling, multi-region, deploy during high load |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Projector compatibility during rolling deploys |
| [postgresql-performance](../postgresql-performance/README.md) | Schema changes and online maintenance |
| [postgresql-performance §15](../postgresql-performance/includes/15-schema-migration-checklist.md) | Online DDL and backfill patterns |
| [database-connection-and-security](../database-connection-and-security/README.md) | Secret rotation during deploys |
| [api-rate-limiting](../api-rate-limiting/README.md) | Limit rollout traffic during canary |
| [tree-and-index-structures](../tree-and-index-structures/README.md) | LSM(Log-Structured Merge) vs B+ when schema drives storage |