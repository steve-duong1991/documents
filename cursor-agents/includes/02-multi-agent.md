# Multi Agent

**Multi agent** means several agents working at once — either as **parallel agent sessions** in the Agents Window, or as **subagents** delegated from a parent agent inside one session.

> **Related:** Single agent → [§1](01-single-agent.md) · Subagents → [§3](03-subagents-and-auto-delegation.md) · Decision guide → [§4](04-decision-guide.md)

---

## Pattern 1 — Parallel agents (Agents Window)

Multiple **independent** agent sessions, each with its own task, model, and working set.

### Good for

- Splitting unrelated work (frontend + backend + tests simultaneously)
- Research while implementation runs elsewhere
- Long-running cloud work while you keep coding locally
- PR babysitting, CI fixes, codebase exploration in the background

### How to use

1. Open **Agents Window**: `Cmd+Shift+P` → **Open Agents Window**
2. Start a new agent per task
3. Use **worktrees** so parallel agents do not overwrite each other's files
4. Switch between agents like tabs; review each agent's diffs separately

### Cloud handoff

| Command | Purpose |
|---------|---------|
| `/in-cloud` | Next task runs on a cloud VM with its own branch — good for CI fixes, long investigations |
| `/babysit` | Cloud agent iterates on a PR until merge-ready |

Switch back to the classic editor anytime: `Cmd+Shift+P` → **Open Editor Window**.

Official docs: [Agents Window](https://cursor.com/docs/agent/agents-window)

---

## Pattern 2 — Subagents (inside one session)

The **parent agent** delegates to specialists that each get their **own context window**. The parent only sees the subagent's final summary — not every intermediate search result or log line.

### Built-in subagents (automatic)

| Subagent | Purpose | When it runs |
|----------|---------|--------------|
| **Explore** | Codebase search and analysis | Large or parallel codebase exploration |
| **Bash** | Shell command series | Verbose command output |
| **Browser** | Browser automation via MCP | DOM snapshots, screenshots, UI testing |

No configuration needed — the parent agent spawns these when appropriate.

### Custom subagents

Define specialists in `.cursor/agents/` (project) or `~/.cursor/agents/` (user):

```markdown
---
name: verifier
description: Validates completed work. Use proactively after tasks are marked done.
model: inherit
readonly: true
---

You are a skeptical validator. Run tests and confirm work actually works.
```

### Explicit invocation

When you need a specific subagent:

```text
/verifier confirm the auth flow is complete
/debugger investigate this test failure
/security-auditor review the payment module
```

Or mention naturally:

```text
Use the verifier subagent to confirm the auth flow is complete
```

### Parallel subagents in one prompt

```text
Review the API changes and update the documentation in parallel
```

The parent sends multiple Task calls in one message so subagents run simultaneously.

Official docs: [Subagents](https://cursor.com/docs/agent/subagents)

---

## Common parallel-agent archetypes

Teams often run a small set of roles in the Agents Window:

| Archetype | Scope | Typical model |
|-----------|-------|---------------|
| **Research** | Read-only; writes plans to `docs/` | Long-context model |
| **Build** | Implements from a plan; Composer diffs with approval | Strong coding model |
| **Test** | Writes/runs tests in test directories | Fast loop model |
| **Review** | Read-only; comments on diffs before merge | Review-focused model |

Practical limit: avoid more than **two writing agents** at once. Use read-only agents (research, review) on cheaper models. Always use **worktrees** when multiple agents edit code concurrently.

---

## Trade-offs

| Benefit | Cost |
|---------|------|
| Faster for independent tasks | Higher token use (each agent has its own context) |
| Context isolation for noisy work | Startup overhead per subagent |
| Specialist expertise | More coordination; risk of conflicting edits without worktrees |
| Background/cloud work | Harder to track than one thread |
