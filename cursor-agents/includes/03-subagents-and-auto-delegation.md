# Subagents and Auto-Delegation

Cursor can **automatically** delegate work to subagents — but there is no global on/off toggle. Delegation is driven by task complexity, subagent **descriptions**, and optional **Cursor rules**.

> **Related:** Multi agent patterns → [§2](02-multi-agent.md) · Decision guide → [§4](04-decision-guide.md) · [Cursor subagents docs](https://cursor.com/docs/agent/subagents)

---

## What auto-detects today (no setup)

These built-in subagents run automatically when the parent agent needs them:

| Subagent | Triggers when… |
|----------|----------------|
| **Explore** | Large codebase search or analysis |
| **Bash** | Long or noisy shell command output |
| **Browser** | Browser/MCP testing with verbose DOM output |

You do not configure these.

---

## How custom subagent auto-delegation works

The parent agent decides whether to spawn a subagent based on:

1. **Task complexity and scope** — multi-step, parallel, or context-heavy work
2. **`description` in each subagent file** — the primary detection signal
3. **Project rules** — optional guidance in `.cursor/rules/`
4. **Current context and available tools**

There is **no settings checkbox** labeled “auto-detect subagents.” Behavior is configuration-driven, not a single toggle.

---

## Step 1 — Create subagents with trigger descriptions

Put files in `.cursor/agents/` (project, share via Git) or `~/.cursor/agents/` (all projects).

```markdown
---
name: verifier
description: Validates completed work. Use proactively after any feature or bugfix is marked done. Always use for auth, payments, or API changes.
model: inherit
readonly: true
---

You are a skeptical validator. Your job is to verify that work claimed as complete actually works.

When invoked:
1. Identify what was claimed to be completed
2. Check that the implementation exists and is functional
3. Run relevant tests or verification steps
4. Look for edge cases that may have been missed

Be thorough and skeptical. Do not accept claims at face value.
```

### Description field — the main lever

The `description` is what the parent agent reads to decide when to delegate.

| Weak | Strong |
|------|--------|
| `Helps with code` | `Debugging specialist for test failures and runtime errors. Use proactively when tests fail or stack traces appear.` |
| `Reviews things` | `Expert code review specialist. Use proactively immediately after writing or modifying production code.` |

Phrases that encourage automatic delegation:

- `Use proactively`
- `Always use for …`
- `Use when …` (specific triggers)

### Optional frontmatter fields

| Field | Default | Purpose |
|-------|---------|---------|
| `name` | From filename | Identifier; use lowercase and hyphens |
| `description` | — | **When to delegate** — most important field |
| `model` | `inherit` | Same as parent, or a specific model ID |
| `readonly` | `false` | Restrict writes and state-changing shell commands |
| `is_background` | `false` | Run without blocking the parent |

---

## Step 2 — Add a Cursor rule (optional)

Reinforce delegation with a rule in `.cursor/rules/`:

```markdown
---
description: When to delegate work to subagents
alwaysApply: true
---

When completing a task:
- After implementing a feature, delegate to the verifier subagent before marking done
- On test failures, delegate to the debugger subagent
- For auth or payment changes, delegate to the security-auditor subagent
- For large codebase exploration, let the Explore subagent handle search
```

Rules tell the **parent agent** when to spawn subagents. They do not replace subagent files — both work together.

---

## Step 3 — Keep the set small

Start with **2–3 focused subagents**:

| Subagent | Typical trigger |
|----------|-----------------|
| **verifier** | After features marked done |
| **debugger** | Test failures, stack traces |
| **test-runner** | After code changes; run and fix tests |

Too many vague agents (`helps with coding`) makes auto-detection **worse**, not better.

Commit `.cursor/agents/` to version control so the team shares the same specialists.

---

## Example subagents

### Debugger

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works
```

### Test runner

```markdown
---
name: test-runner
description: Test automation expert. Use proactively to run tests and fix failures after code changes.
---

You are a test automation expert.

When you see code changes, proactively run appropriate tests.
If tests fail, analyze output, fix the root cause, and re-run to verify.
```

### Security auditor

```markdown
---
name: security-auditor
description: Security specialist. Always use for auth, payments, PII handling, or API input validation changes.
model: inherit
readonly: true
---

Check for injection, XSS, hardcoded secrets, missing input validation, and auth bypass paths.
Report findings by severity: Critical, High, Medium.
```

---

## What you cannot do (today)

| Limitation | Workaround |
|------------|------------|
| No global “always use subagents” toggle | Use rules + proactive descriptions |
| No regex/trigger config per subagent | Put trigger terms in `description` |
| No guarantee of delegation every time | Invoke explicitly: `/verifier`, `/debugger` |
| Subagents cost more tokens in parallel | Reserve for complex or isolated work |

---

## Test your setup

1. Add `.cursor/agents/verifier.md` with a specific `description`
2. Ask Agent: *“Implement X and verify it works”*
3. If it skips verification, tighten the description or add a rule
4. Confirm the subagent itself works: `/verifier check this implementation`

---

## Subagents vs skills vs slash commands

| Tool | Use when |
|------|----------|
| **Subagent** | Multi-step work needing isolated context, parallel workstreams, or independent verification |
| **Skill** | Single-purpose repeatable action (format imports, generate changelog) — no separate context window |
| **Slash command** | One-shot custom prompt; no isolation needed |

If a task completes in one shot and does not need context isolation, prefer a **skill** or slash command over a subagent.
