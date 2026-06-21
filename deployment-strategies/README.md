# Deployment Strategies Guide

A practical reference for common deployment patterns — how they work, pros and cons, when to use each, and best practices.

Related: [api-design-and-protection](../api-design-and-protection/README.md) (stateless architecture enables safe rollouts) · [high-throughput-systems](../high-throughput-systems/README.md) (scale and deploy layer)

---

## Table of contents

| # | Strategy | Include file |
|---|----------|--------------|
| — | [Quick comparison](#quick-comparison) | [includes/00-overview.md](includes/00-overview.md) |
| 1 | [Recreate (Big Bang)](#1-recreate-big-bang) | [includes/01-recreate.md](includes/01-recreate.md) |
| 2 | [Rolling deployment](#2-rolling-deployment) | [includes/02-rolling.md](includes/02-rolling.md) |
| 3 | [Blue-Green deployment](#3-blue-green-deployment) | [includes/03-blue-green.md](includes/03-blue-green.md) |
| 4 | [Canary deployment](#4-canary-deployment) | [includes/04-canary.md](includes/04-canary.md) |
| 5 | [A/B testing](#5-ab-testing) | [includes/05-ab-testing.md](includes/05-ab-testing.md) |
| 6 | [Shadow / mirror / dark launch](#6-shadow--mirror--dark-launch) | [includes/06-shadow.md](includes/06-shadow.md) |
| 7 | [Feature flags](#7-feature-flags) | [includes/07-feature-flags.md](includes/07-feature-flags.md) |
| 8 | [Immutable deployment](#8-immutable-deployment) | [includes/08-immutable.md](includes/08-immutable.md) |
| 9 | [GitOps](#9-gitops) | [includes/09-gitops.md](includes/09-gitops.md) |
| 10 | [Progressive delivery](#10-progressive-delivery) | [includes/10-progressive-delivery.md](includes/10-progressive-delivery.md) |
| 11 | [Choosing a strategy & best practices](#11-choosing-a-strategy--best-practices) | [includes/11-choosing-and-practices.md](includes/11-choosing-and-practices.md) |
| 12 | [Schema migrations and deploy coupling](#12-schema-migrations-and-deploy-coupling) | [includes/12-schema-migrations-and-deploy.md](includes/12-schema-migrations-and-deploy.md) |
| 13 | [SLO-based rollback triggers](#13-slo-based-rollback-triggers) | [includes/13-slo-rollback-triggers.md](includes/13-slo-rollback-triggers.md) |

> **Tip:** Open [GUIDE.md](GUIDE.md) for the full combined document in one file.

---

## Quick comparison

See full details → [includes/00-overview.md](includes/00-overview.md)

---

## 1. Recreate (Big Bang)

Stop the old version, deploy the new one, start fresh. Simple but causes downtime.

See full details → [includes/01-recreate.md](includes/01-recreate.md)

---

## 2. Rolling deployment

Replace instances gradually while traffic keeps flowing. The default for most production services.

See full details → [includes/02-rolling.md](includes/02-rolling.md)

---

## 3. Blue-Green deployment

Two full environments — deploy to idle, switch traffic, keep old env for instant rollback.

See full details → [includes/03-blue-green.md](includes/03-blue-green.md)

---

## 4. Canary deployment

Route a small percentage of traffic to the new version; expand if metrics look good.

See full details → [includes/04-canary.md](includes/04-canary.md)

---

## 5. A/B testing

Split traffic to compare product behavior — an experiment pattern, not primarily a safety net.

See full details → [includes/05-ab-testing.md](includes/05-ab-testing.md)

---

## 6. Shadow / mirror / dark launch

Copy production traffic to the new system without serving responses to users.

See full details → [includes/06-shadow.md](includes/06-shadow.md)

---

## 7. Feature flags

Deploy code with features disabled; enable for users when ready. Decouples deploy from release.

See full details → [includes/07-feature-flags.md](includes/07-feature-flags.md)

---

## 8. Immutable deployment

Never patch running servers — replace entire artifacts (images, AMIs, containers).

See full details → [includes/08-immutable.md](includes/08-immutable.md)

---

## 9. GitOps(Git Operations)

Git is the source of truth; a controller reconciles live state to match the repo.

See full details → [includes/09-gitops.md](includes/09-gitops.md)

---

## 10. Progressive delivery

Combines rolling, canary, feature flags, and automated analysis for high-stakes releases.

See full details → [includes/10-progressive-delivery.md](includes/10-progressive-delivery.md)

---

## 11. Choosing a strategy & best practices

Decision flow, cross-cutting practices, and common stack combinations.

See full details → [includes/11-choosing-and-practices.md](includes/11-choosing-and-practices.md)

---

## 12. Schema migrations and deploy coupling

Expand / deploy / contract, online DDL with rolling and canary, and CQRS(Command Query Responsibility Segregation) projector ordering.

See full details → [includes/12-schema-migrations-and-deploy.md](includes/12-schema-migrations-and-deploy.md)

---

## 13. SLO(Service Level Objective)-based rollback triggers

Error-budget burn, version-tagged metrics, and automated halt/rollback by deploy strategy.

See full details → [includes/13-slo-rollback-triggers.md](includes/13-slo-rollback-triggers.md)

---

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
