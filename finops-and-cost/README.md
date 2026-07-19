# FinOps & Cost Guide

Treat **cloud cost as a design constraint** for Tech Leads — unit economics, drivers, right-sizing, retention, build vs managed, budgets, and architecture tradeoffs.

Related: [high-throughput-systems](../high-throughput-systems/README.md) · [architecture-decisions](../architecture-decisions/README.md) · [data-platforms](../data-platforms/README.md) (store sprawl cost)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Unit economics](includes/01-unit-economics.md) |
| 2 | [Cloud cost drivers](includes/02-cloud-cost-drivers.md) |
| 3 | [Right-sizing and autoscaling](includes/03-right-sizing-and-autoscaling.md) |
| 3A | [Commitments and discount strategy](includes/03A-commitments-and-discount-strategy.md) |
| 4 | [Storage and retention cost](includes/04-storage-and-retention-cost.md) |
| 5 | [Build vs managed cost](includes/05-build-vs-managed-cost.md) |
| 6 | [Cost visibility and budgets](includes/06-cost-visibility-and-budgets.md) |
| 6A | [Platform showback and unit cost](includes/06A-platform-showback-and-unit-cost.md) |
| 7 | [Architecture cost tradeoffs](includes/07-architecture-cost-tradeoffs.md) |
| 8 | [Decision guide](includes/08-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **New to FinOps as a tech lead** | Overview → [§1 Unit economics](includes/01-unit-economics.md) → [§2 Cloud cost drivers](includes/02-cloud-cost-drivers.md) → [§8 Decision guide](includes/08-decision-guide.md) |
| **Cost visibility / chargeback** | [§6 Cost visibility](includes/06-cost-visibility-and-budgets.md) → [§6A Showback](includes/06A-platform-showback-and-unit-cost.md) → [§1 Unit economics](includes/01-unit-economics.md) |
| **Right-sizing before scale-out** | [§3 Right-sizing](includes/03-right-sizing-and-autoscaling.md) → [§3A Commitments and discounts](includes/03A-commitments-and-discount-strategy.md) → [PG performance](../postgresql-performance/README.md) → [§7 Architecture tradeoffs](includes/07-architecture-cost-tradeoffs.md) |
| **Storage / retention spend** | [§4 Storage and retention](includes/04-storage-and-retention-cost.md) → [data-platforms §5](../data-platforms/includes/05-data-ownership-lineage-retention.md) → [§5 Build vs managed](includes/05-build-vs-managed-cost.md) |

## See also

| Guide | Topics |
|-------|--------|
| [high-throughput-systems](../high-throughput-systems/README.md) | Scale order, caching, streaming — cost follows waste |
| [architecture-decisions](../architecture-decisions/README.md) | ADRs, tradeoff frameworks, service boundaries — cost as a decision input |
| [data-platforms](../data-platforms/README.md) | Warehouse/search/Redis sprawl, retention ownership |
| [apache-kafka](../apache-kafka/README.md) | Retention, storage, managed vs self-hosted |
| [postgresql-performance](../postgresql-performance/README.md) | Right-size DB before horizontal sprawl |
| [deployment-strategies](../deployment-strategies/README.md) | Progressive delivery vs always-on dual environments |
| [api-rate-limiting](../api-rate-limiting/README.md) | Abuse caps that also cap cost |
| [database-connection-and-security](../database-connection-and-security/README.md) | Idle connections and proxy cost |