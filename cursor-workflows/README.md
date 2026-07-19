# Cursor Workflows Guide

Practical playbook for using Cursor across the software delivery loop: **solution design**, **solution architecture**, **coding**, **code review**, **ship to PROD**, and **operate and learn** — including what to input at each stage, where to store stack-specific best practices, which MCP(Model Context Protocol) servers help, and how to use review subagents.

Related: [Cursor Agents guide](../cursor-agents/README.md) · [Feature to PROD playbook](../deployment-strategies/includes/14-feature-to-prod-playbook.md) · [Architecture decisions](../architecture-decisions/README.md) · [Testing strategy](../testing-strategy/README.md) · [SRE and incidents](../sre-and-incidents/README.md)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Solution design](includes/01-solution-design.md) |
| 1A | [EPIC / FEATURE / USER_STORY templates](includes/01A-epic-feature-user-story-templates.md) |
| 2 | [Solution architecture](includes/02-solution-architecture.md) |
| 3 | [Coding](includes/03-coding.md) |
| 4 | [Code reviews](includes/04-code-reviews.md) |
| 5 | [Ship to PROD](includes/05-ship-to-prod.md) |
| 6 | [Operate and learn](includes/06-operate-and-learn.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Resource | Topics |
|----------|--------|
| [Engineering Guides](../README.md) | Full corpus — validate per [CONTRIBUTING](../CONTRIBUTING.md) |
| [Cursor Agents](../cursor-agents/README.md) | Single vs multi agent, subagents, Agents Window |
| [Architecture decisions](../architecture-decisions/README.md) | ADRs, boundaries, tradeoffs, capacity, Team Topologies, ARB |
| [tech-lead §1A Product discovery](../tech-lead-practice/includes/01A-product-discovery.md) | Problem evidence before solution design |
| [Fullstack BFF and clients](../fullstack-bff-and-clients/README.md) | React, BFF(Backend for Frontend), client architecture |
| [API design and protection](../api-design-and-protection/README.md) | OpenAPI, contracts, mocks |
| [Testing strategy](../testing-strategy/README.md) | Pyramid, contracts, E2E |
| [Deployment §14 feature to PROD](../deployment-strategies/includes/14-feature-to-prod-playbook.md) | Ordered release gates (design → canary → drill) |
| [SRE and incidents](../sre-and-incidents/README.md) | SLOs, rollback culture, game days |
| [Tech lead practice](../tech-lead-practice/README.md) | Debt portfolio, prioritization after ship |
| [Repo `.cursor/`](../.cursor/rules/engineering-guides.mdc) | Project rules, hooks, doc-reviewer subagent |