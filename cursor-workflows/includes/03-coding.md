# Coding

> **Related:** Solution architecture → [§2](02-solution-architecture.md) · Fullstack clients → [../../fullstack-bff-and-clients/README.md](../../fullstack-bff-and-clients/README.md) · Testing strategy → [../../testing-strategy/README.md](../../testing-strategy/README.md)

## At a glance

| Practice | Where it lives in Cursor | When it applies |
|----------|--------------------------|-----------------|
| Universal standards | User rules | Every project |
| Repo conventions | `.cursor/rules/*.mdc` | Files matching `globs` |
| Stack playbooks | `.cursor/rules/` or `.cursor/skills/` | React, Node, Java, etc. |
| Runnable context | `AGENTS.md`, `docs/`, exemplar files | `@` mention in prompts |
| Guardrails | `.cursor/hooks.json` | Format, lint, risky commands |

**Rule of thumb:** Store **short, actionable** stack rules in `.cursor/rules/`; store **workflows and templates** in `.cursor/skills/`.

```mermaid
flowchart TD
    AC[Confirm ticket AC in prompt] --> Ctx[@ architecture doc + API spec + exemplar]
    Ctx --> Scope[State in-scope / out-of-scope files]
    Scope --> Impl[Agent implements minimal diff]
    Impl --> Test[Targeted tests + linter]
    Test --> Verify[Verifier subagent or local run]
    Verify --> PR[Open PR → code review]
```

---

## What to do in Cursor

### 1. Use Agent mode with tight scope

```text
Implement [specific behavior] in @src/orders/OrderService.ts.
Match patterns in @src/orders/PaymentService.ts.
Minimal diff — no unrelated refactors.
Add tests for the error path: duplicate order id.
```

### 2. Attach context deliberately

| Attach | Why |
|--------|-----|
| `@ticket` / MCP issue | Acceptance criteria stay visible |
| `@openapi.yaml` / `@schema.graphql` | API(Application Programming Interface) shape is authoritative |
| `@docs/adr/0042-….md` | Architectural constraints |
| Exemplar module | Naming, error handling, test style |
| `@fixtures/...` | Tests use same payloads as mocks |

### 3. Explore before large changes

For unfamiliar areas:

```text
Explore how authentication flows from middleware to the user repository.
Return: file list, sequence, extension points. Do not edit files.
```

Built-in **explore** subagent is used automatically for broad searches.

### 4. Hooks for consistency

Example project hooks (see [create-hook skill](https://cursor.com/docs)):

| Event | Behavior |
|-------|----------|
| `afterFileEdit` | Run formatter / linter on touched files |
| `beforeShellExecution` | Gate `rm -rf`, force push, prod deploy commands |
| `sessionStart` | Inject branch name + ticket ID from env |

### 5. Verify before PR

- Run tests locally (agent can execute)
- Optional custom **verifier** subagent in `.cursor/agents/`
- → [§4 Code reviews](04-code-reviews.md)

---

## Where to store best practices

### Decision matrix

| Content type | Location | Format |
|--------------|----------|--------|
| “Always do X in this repo” | `.cursor/rules/<topic>.mdc` | YAML frontmatter + `globs` |
| “How to run our design/review workflow” | `.cursor/skills/<name>/SKILL.md` | Skill with steps + templates |
| Human-readable engineering docs | `documents/<guide>/` | Markdown guides (this repo) |
| Onboarding + agent context | `AGENTS.md` (repo root) | Service map, commands, conventions |

| Scope | Path |
|-------|------|
| **Personal** (all your repos) | `~/.cursor/skills/`, User rules in Settings |
| **Team** (one repo) | `.cursor/rules/`, `.cursor/skills/`, `.cursor/agents/` |
| **Shared knowledge** | `documents/` engineering guides |

Keep each rule **under ~50 lines**, **one concern per file**.

---

## Stack-specific rules (templates)

Copy into `.cursor/rules/` and adjust `globs` for your repo layout.

### React + Apollo Client (large app)

**File:** `.cursor/rules/react-apollo-large.mdc`

```markdown
---
description: React + Apollo Client patterns for large apps
globs: "**/*.{tsx,ts}"
alwaysApply: false
---

# React + Apollo Client (large app)

## State
- Server state in Apollo cache — not Redux
- Redux only for true cross-route client state (wizard, complex UI prefs)
- Colocate queries with route/feature modules

## Apollo
- Use typed operations (codegen); no string queries in components
- Query keys: entity + id; list queries name filter variables explicitly
- Mutations: update cache or refetchQueries — document which in PR
- Error policy: handle network vs GraphQL errors separately; show correlation id

## Components
- Container/presentational split for data-heavy screens
- Suspense boundaries at route level where supported
- Avoid prop drilling >2 levels — context or composition

## Testing
- Mock Apollo with mocked responses matching @fixtures/
- Test loading/error/empty states
```

Cross-link: [frontend architecture](../../fullstack-bff-and-clients/includes/01-frontend-architecture.md)

---

### Redux (large app)

**File:** `.cursor/rules/redux-large-app.mdc`

```markdown
---
description: Redux Toolkit patterns for large apps
globs: "**/*.{tsx,ts}"
alwaysApply: false
---

# Redux (large app)

## When to use Redux
- Shared client state across many routes (session UI, feature flags client cache)
- Complex orchestration (multi-step flows with undo)
- NOT for server-fetched entities — use Apollo/React Query

## Structure
- Feature slices: `features/<name>/slice.ts`, `selectors.ts`, `thunks.ts`
- Normalized entities only for client-owned data
- RTK(Redux Toolkit) Query only if team standard — otherwise one data layer

## Patterns
- Prefer createSlice + typed hooks
- Side effects in createAsyncThunk or listener middleware — not components
- Selectors colocated; memoize expensive derivations

## Avoid
- Storing API responses duplicated from Apollo/cache
- Global store for form field state — use local state or RHF
```

---

### useState vs useReducer (small app)

**File:** `.cursor/rules/react-local-state-small.mdc`

```markdown
---
description: Local state choices for small React apps
globs: "**/*.{tsx,ts}"
alwaysApply: false
---

# useState vs useReducer (small app)

## Default: useState
- Single form, few fields, no shared transition logic
- Modal open/close, toggles, simple counters

## useReducer when
- Next state depends on previous + action type (wizard steps)
- Multiple related fields update together
- You want to test state transitions in isolation

## Rule
- <3 related state variables and no state machine → useState
- Enumerated steps or action-driven updates → useReducer
- Server data → Apollo/fetch layer, not either hook
```

---

### Node.js + Express + Apollo Server

**File:** `.cursor/rules/node-express-apollo.mdc`

```markdown
---
description: Node Express + Apollo Server API patterns
globs: "**/*.{ts,js}"
alwaysApply: false
---

# Node + Express + Apollo Server

## Layout
- `src/schema/` — typeDefs + resolvers
- `src/services/` — business logic (resolvers stay thin)
- `src/datasources/` — DB and HTTP clients
- `src/middleware/` — auth, logging, correlation id

## Resolvers
- No direct SQL in resolvers — call service layer
- DataLoader for N+1 batching
- Errors: map domain errors to GraphQL errors + extensions.code

## Express
- Health/readiness routes outside GraphQL
- Request context: user, correlationId, loaders per request
- Graceful shutdown: drain HTTP + Apollo

## Security
- Auth at context creation — fail closed
- Validate input with zod/class-validator at service boundary
```

---

### Java + Spring Boot (CRUD + transactions)

**File:** `.cursor/rules/java-spring-crud.mdc`

```markdown
---
description: Spring Boot CRUD and transaction patterns
globs: "**/*.{java,kt}"
alwaysApply: false
---

# Java Spring Boot — CRUD + transactions

## Layers
- Controller: DTO in/out, validation, HTTP codes only
- Service: @Transactional business logic
- Repository: Spring Data — no business rules

## Transactions
- @Transactional on service methods, readOnly=true for queries
- Default propagation REQUIRED; document REQUIRES_NEW for outbox/audit
- Do not call @Transactional methods via self-invocation (use self bean or separate class)

## CRUD
- PATCH: partial update DTOs — never bind entity directly from request
- Optimistic locking: @Version on contested entities
- Map Entity <-> DTO in mapper layer; never expose entities in API

## Errors
- @ControllerAdvice maps domain exceptions to Problem Details (RFC 9457)
- Idempotent creates: unique constraint + 409 response

## Tests
- @DataJpaTest for repository; @WebMvcTest for controller slice
- @SpringBootTest sparingly — prefer test slices
```

Cross-link: [database connection patterns](../../database-connection-and-security/README.md)

---

## Suggested repo layout for Cursor config

```
your-app/
├── AGENTS.md                 # How to run, test, deploy; service map
├── .cursor/
│   ├── rules/
│   │   ├── react-apollo-large.mdc
│   │   ├── redux-large-app.mdc
│   │   ├── react-local-state-small.mdc
│   │   ├── node-express-apollo.mdc
│   │   └── java-spring-crud.mdc
│   ├── skills/
│   │   └── feature-delivery/SKILL.md
│   ├── agents/
│   │   └── verifier.md
│   └── hooks.json
└── docs/
    └── adr/
```

---

## Coding session checklist

| # | Step |
|---|------|
| 1 | Confirm ticket AC in prompt |
| 2 | `@` architecture doc + API spec |
| 3 | `@` exemplar file for patterns |
| 4 | State files **in scope** and **out of scope** |
| 5 | Implement + targeted tests |
| 6 | Run linter/tests |
| 7 | Open PR → [§4](04-code-reviews.md) |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| One 500-line rule file | Split by stack and concern |
| Redux + Apollo duplicating same entities | Single server-state layer |
| @Transactional on controllers | Service layer only |
| Agent refactors unrelated files | Explicit “minimal diff” + file scope |
| No exemplar | Point at gold-standard module |