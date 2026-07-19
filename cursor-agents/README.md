# Cursor Agents Guide

Practical reference for **single-agent** vs **multi-agent** workflows in Cursor — when to use each, how to run parallel agents and subagents, and how to configure automatic subagent delegation.

Related: [Cursor Workflows](../cursor-workflows/README.md) (design → ship → operate loop) · [Cursor subagents docs](https://cursor.com/docs/agent/subagents) · [Agents Window docs](https://cursor.com/docs/agent/agents-window)

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [Single agent](includes/01-single-agent.md) |
| 2 | [Multi agent](includes/02-multi-agent.md) |
| 3 | [Subagents and auto-delegation](includes/03-subagents-and-auto-delegation.md) |
| 4 | [Decision guide](includes/04-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## See also

| Resource | Topics |
|----------|--------|
| [cursor-workflows](../cursor-workflows/README.md) | Full delivery loop using Cursor (MCP, reviews, ship, operate) |
| [Engineering Guides](../README.md) | This corpus — edit and validate per [CONTRIBUTING](../CONTRIBUTING.md) |
| [VISUAL-INDEX](../VISUAL-INDEX.md) | Request / async / release / incident spines |
| [Repo `.cursor/`](../.cursor/rules/engineering-guides.mdc) | Project rules, validate hook, doc-reviewer subagent |
| [Architecture decisions](../architecture-decisions/README.md) | ADRs and governance when agents draft design docs |
| [Testing strategy](../testing-strategy/README.md) | Quality gates agents should not skip |
| [Cursor Agent overview](https://cursor.com/docs/agent/overview) | Tools, checkpoints, queued messages |
| [Cursor subagents](https://cursor.com/docs/agent/subagents) | Built-in subagents, custom agents, cloud subagents |
| [Cursor Agents Window](https://cursor.com/docs/agent/agents-window) | Parallel agents, worktrees, cloud handoff |