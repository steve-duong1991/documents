# ADRs and Design Docs

When to write an ADR(Architecture Decision Record), when to use an RFC(Request for Comments), and templates that stay useful after the meeting ends.

> **Related:** Overview process → [00-overview.md](00-overview.md) · Tradeoffs → [06-tradeoff-frameworks.md](06-tradeoff-frameworks.md) · Tech lead culture → [tech-lead-practice](../../tech-lead-practice/README.md)

---

## At a glance

| Artifact | Audience | Lifetime | Use for |
|----------|----------|----------|---------|
| **ADR** | Future you + on-call | Years | Lasting choice and consequences |
| **RFC / design doc** | Broad review | Months | Options debate before ADR |
| **Ticket comment** | Sprint | Days | Implementation detail |
| **Slack thread** | Ephemeral | Hours | Discovery only — promote if decided |

**Rule of thumb:** If reversing the decision would take more than a week of engineering, write an ADR. If many teams must buy in first, write an RFC that ends in an ADR.

---

## When to write

| Write an ADR when… | Skip when… |
|--------------------|------------|
| Choosing sync vs async between services | Picking a JSON library |
| Adopting a multi-tenant isolation model | Renaming a private method |
| Introducing a shared DB anti-pattern exception | Routine bugfix |
| Committing to Kafka vs queue for a domain | Temporary spike code behind a flag |

---

## ADR template

```markdown
# ADR-NNNN: Title

Date: YYYY-MM-DD
Status: Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
Deciders: names

## Context
What forces the decision? Constraints, incidents, scale, org.

## Decision
What we will do — one clear paragraph.

## Alternatives considered
- Option A — why rejected
- Option B — why rejected

## Consequences
Positive, negative, follow-ups (tickets, SLOs, runbooks).

## Related
Links to RFCs, diagrams, sibling ADRs.
```

Keep ADRs **immutable** once Accepted; supersede with a new ADR instead of editing history silently.

---

## RFC / design doc shape

| Section | Purpose |
|---------|---------|
| Problem | User or ops pain |
| Goals / non-goals | Scope control |
| Options | 2–3 with cost |
| Recommendation | Tentative until review |
| Rollout | Flags, strangler, metrics |
| Open questions | Force decisions |

After approval, extract the **Decision** into an ADR so the long RFC can age out of the critical path.

---

## Lightweight review flow

```mermaid
flowchart LR
    D[Draft RFC] --> R[Review window]
    R --> A[Accept ADR]
    A --> I[Implement]
    I --> V[Validate metrics]
    V --> S[Supersede if needed]
```

| Tip | Why |
|-----|-----|
| Time-box review (e.g. 5 business days) | Avoid endless bike-shed |
| Require a “do nothing” option | Anchors cost |
| Link from README/architecture index | Discoverability |
| Status in filename or front matter | On-call finds truth fast |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| ADR after the code shipped | Draft before irreversible merges |
| 20-page ADR | Move debate to RFC; ADR stays short |
| No status / supersede trail | Explicit lifecycle |
| Private Google Doc only | Store in repo next to code |
| Every ticket becomes an ADR | Threshold on irreversibility |

## Pros and cons

| | Written ADRs | Tribal memory |
|--|--------------|---------------|
| **Pros** | Onboarding, audit, fewer re-litigations | Fast for tiny teams |
| **Cons** | Process overhead | Knowledge loss, thrash |