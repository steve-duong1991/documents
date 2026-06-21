# Overview — Quick Comparison

> **Scope:** **Strategy comparison** — downtime, rollback speed, risk, and fit at a glance. Per-strategy mechanics → §1–§8; choosing and practices → [§11 Choosing a strategy](11-choosing-and-practices.md).
>
> **Related:** Stateless apps → [api-design §11 Stateless architecture](../../api-design-and-protection/includes/11-stateless-architecture.md) · Schema + deploy → [§12 Schema migrations](12-schema-migrations-and-deploy.md) · Decision guide → [§11 Choosing a strategy](11-choosing-and-practices.md)

| Strategy | Downtime | Rollback speed | Risk | Complexity | Best for |
|----------|----------|----------------|------|------------|----------|
| **Recreate (Big Bang)** | Yes | Slow | High | Low | Dev/staging, small apps |
| **Rolling** | Minimal/none | Medium | Medium | Medium | Most production services |
| **Blue-Green** | None (if done right) | Very fast | Low–Medium | Medium–High | Critical uptime, fast rollback |
| **Canary** | None | Fast | Low | High | Risk-sensitive releases |
| **A/B Testing** | None | N/A (experiment) | Low | High | Product/experimentation |
| **Shadow / Mirror** | None | N/A | Low (infra cost) | High | Validation before cutover |
| **Feature flags** | None | Instant (toggle) | Low | Medium | Decouple deploy from release |

## At a glance

- **Recreate** — simplest, accepts downtime
- **Rolling** — default for most services
- **Blue-green** — fast rollback, needs double capacity
- **Canary / progressive** — limit blast radius with real traffic
- **Feature flags** — separate *deploying code* from *releasing features*
- **Shadow** — validate rewrites safely before cutover
- **GitOps(Git Operations)** — declarative, auditable delivery (common on Kubernetes)

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Breaking schema + code in one deploy | Expand → deploy → contract |
| Recreate in production for convenience | Rolling or canary with health checks |
| Rollback app after non-reversible migration | Forward-fix or expand/contract only |
| No build ID on metrics during canary | Tag version on traces and dashboards |
| Feature flags left on forever | Delete flag after 100% rollout |

## See also

| Guide | Topics |
|-------|--------|
| [api-design-and-protection](../../api-design-and-protection/includes/11-stateless-architecture.md) | Stateless app tier — prerequisite for rolling and blue/green |
| [high-throughput-systems §10](../../high-throughput-systems/includes/10-scale-and-deploy.md) | Autoscaling and deploy during high load |
| [event-sourcing-and-cqrs](../../event-sourcing-and-cqrs/README.md) | Projector compatibility during rolling deploys |