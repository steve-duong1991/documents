# Specialized Data Systems Guide

A practical reference for the data systems that live **beyond general-purpose OLTP(Online Transaction Processing) and the warehouse** — time-series stores, graph databases, vector/RAG(Retrieval-Augmented Generation) infrastructure, and workflow engines — and when each earns its operational cost over PostgreSQL or a hand-rolled alternative.

Related: [data-platforms](../data-platforms/README.md) (OLTP/OLAP(Online Analytical Processing) split, search, Redis roles) · [postgresql-performance](../postgresql-performance/README.md) (what PostgreSQL already covers) · [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) (sagas as the hand-rolled workflow baseline)

> **Scope:** This guide is **architecture and decision criteria** for adopting a specialized store — not a product tutorial. It answers "does this workload need a dedicated system, and which shape," and links to [sre-and-incidents](../sre-and-incidents/README.md), [postgresql-performance](../postgresql-performance/README.md), and [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) for the operational depth each already owns.

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Time-series databases](includes/01-time-series.md) |
| 2 | [Graph databases](includes/02-graph-databases.md) |
| 3 | [Vector stores and RAG](includes/03-vector-and-rag.md) |
| 3A | [Feature stores and ML serving](includes/03A-feature-stores-and-ml-serving.md) |
| 3B | [LLM gateway and inference edge](includes/03B-llm-gateway-and-inference-edge.md) |
| 4 | [Workflow engines](includes/04-workflow-engines.md) |
| 5 | [Decision guide](includes/05-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Metrics/IoT/telemetry at scale** | Overview → §1 Time-series → [sre-and-incidents §4](../sre-and-incidents/includes/04-observability-practice.md) |
| **Modeling deeply connected data** | §2 Graph databases → [postgresql-performance §2](../postgresql-performance/includes/02-indexing.md) (recursive CTE(Common Table Expression) baseline) |
| **Building retrieval for an LLM(Large Language Model) feature** | §3 Vector stores and RAG → §5 Decision guide |
| **Online features / model serving** | §3A Feature stores → §3 if retrieval-heavy → [data-platforms](../data-platforms/README.md) |
| **Shipping LLM/AI behind a gateway** | [§3B LLM gateway](includes/03B-llm-gateway-and-inference-edge.md) → §3 if retrieval → §3A if features |
| **Replacing a hand-rolled saga or cron pipeline** | [event-sourcing-and-cqrs §7](../event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) → §4 Workflow engines |
| **Deciding if you need any of this at all** | §5 Decision guide first, then the relevant section |

---

## See also

| Guide | Topics |
|-------|--------|
| [data-platforms](../data-platforms/README.md) | OLTP/OLAP split, search systems, Redis roles, migration coordination |
| [postgresql-performance](../postgresql-performance/README.md) | Indexing, partitioning, recursive queries, when PostgreSQL is still enough |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Sagas, outbox, event log as the baseline workflow engines replace |
| [high-throughput-systems](../high-throughput-systems/README.md) | Streaming ingestion feeding time-series and vector pipelines |
| [apache-kafka](../apache-kafka/README.md) | Event bus feeding CDC(Change Data Capture) into specialized stores |
| [sre-and-incidents](../sre-and-incidents/README.md) | Observability practice; time-series as the metrics backend |
| [resilience-patterns](../resilience-patterns/README.md) | Idempotency and retries for workflow engine activities |
| [enterprise-security-compliance](../enterprise-security-compliance/README.md) | PII(Personally Identifiable Information) handling in embeddings and audit trails |
| [finops-and-cost](../finops-and-cost/README.md) | Managed vs self-hosted TCO(Total Cost of Ownership) for specialized stores |