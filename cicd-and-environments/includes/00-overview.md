# Overview — CI/CD for Tech Leads

CI/CD(Continuous Integration / Continuous Delivery) is how change becomes production risk you can **measure and reverse**. This guide covers pipeline design and environment policy; traffic-shifting patterns live in deployment-strategies.

> **Related:** Deploy strategies → [deployment-strategies](../../deployment-strategies/README.md) · Secrets → [database-connection-and-security](../../database-connection-and-security/README.md) · Reliability gates → [sre-and-incidents](../../sre-and-incidents/README.md) · Decision guide → [§9](09-decision-guide.md)

---

## At a glance

| Layer | Owns | Guide section |
|-------|------|---------------|
| **CI** | Build, test, lint, scan, artifact | [§1](01-ci-pipeline-design.md) |
| **CD / promote** | Same artifact across envs | [§2](02-cd-and-promotion.md) |
| **Config / secrets** | 12-factor parity | [§3](03-config-vs-secrets.md) |
| **Flags** | Decouple ship from expose | [§4](04-feature-flags-as-control.md) |
| **Branching** | How code flows to main | [§5](05-branching-and-release-trains.md) |
| **Undo** | Rollback vs forward-fix | [§6](06-rollback-vs-forward-fix.md) |
| **Runtime contract** | Images, health, resources | [§7](07-containers-and-health.md) |
| **Ownership** | TL vs platform | [§8](08-platform-boundaries.md) |

**Rule of thumb:** Build **once**, promote the **same immutable artifact**, change only **config/secrets/flags** per environment.

---

## How the pieces connect

```mermaid
flowchart LR
    PR[PR] --> CI[CI: test lint scan]
    CI --> Art[Artifact + SBOM]
    Art --> Dev[Dev / ephemeral]
    Dev --> Stage[Staging promote]
    Stage --> Prod[Prod promote]
    Prod --> Traffic[Deploy strategy]
    Traffic --> Flags[Feature flags]
```

| Concern | This guide | Sibling |
|---------|------------|---------|
| Artifact correctness | §1–§2 | — |
| How traffic shifts | links out | [deployment-strategies](../../deployment-strategies/README.md) |
| SLO(Service Level Objective) rollback triggers | §6 + links | [deployment §13](../../deployment-strategies/includes/13-slo-rollback-triggers.md) |
| Who gets paged | links out | [sre-and-incidents](../../sre-and-incidents/README.md) |

---

## Environment model (typical)

| Env | Purpose | Data | Promote gate |
|-----|---------|------|--------------|
| **PR / ephemeral** | Preview | Synthetic | CI green |
| **Dev** | Integration | Shared fake | CI + smoke |
| **Staging** | Prod-like | Anonymized / subset | Tests + synthetics |
| **Prod** | Users | Real | Manual or progressive + SLO |

Exact names vary; the invariant is **increasing fidelity** and **stricter gates**, not reinventing the binary each time.

---

## Tech lead outcomes

| Outcome | Evidence |
|---------|----------|
| Reproducible builds | Artifact digest pinned in promote |
| Fast feedback | CI < ~15–20 min for default path |
| Safe secrets | No secrets in git ([§3](03-config-vs-secrets.md)) |
| Known undo path | Documented rollback/forward-fix ([§6](06-rollback-vs-forward-fix.md)) |
| Clear ownership | Platform vs app chart ([§8](08-platform-boundaries.md)) |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Rebuild per environment | Promote digests |
| “Works on staging” different flags/config | Parity ([§3](03-config-vs-secrets.md)) |
| CD without health checks | [§7](07-containers-and-health.md) |
| Flags as permanent architecture | Short-lived release flags ([§4](04-feature-flags-as-control.md)) |
| No link to runbooks | [RUNBOOK-TEMPLATE.md](../../RUNBOOK-TEMPLATE.md) |