# Testing and Verification

Event-sourced systems need tests at three layers: command handling, projection correctness, and integration paths (outbox, sagas).

> **Related:** Sagas → [07-sagas-and-distributed-workflows.md](07-sagas-and-distributed-workflows.md) · Schema evolution → [08-event-schema-evolution.md](08-event-schema-evolution.md) · Contract CI → [api-design §15](../../api-design-and-protection/includes/15-contract-and-schema-testing.md)

---

## At a glance

| Layer | What to prove | Technique |
|-------|---------------|-----------|
| **Aggregate** | Given events → state; command → events | In-memory event store |
| **Projector** | Event sequence → read model rows | Table-driven fixtures |
| **Outbox relay** | Row published after commit | Integration test + test broker |
| **Saga** | Happy path + compensation order | Orchestrator test harness |
| **Replay** | Upcasters + rebuild = expected state | Golden event files |

**Rule of thumb:** Test **behavior from events**, not hidden mutable fields. Use the same upcasters in tests and production loaders.

---

## Aggregate tests

```mermaid
flowchart LR
    Events[Fixture event list] --> Replay[Replay aggregate]
    Replay --> State[Assert state]
    Cmd[Command] --> Handler[Handle]
    Handler --> NewEvents[Assert emitted events]
```

| Check | Example |
|-------|---------|
| Replay from empty | `OrderCreated` → status `open` |
| Optimistic concurrency | Stale version → conflict |
| Invalid command | No events appended |

---

## Projector tests

| Pattern | Detail |
|---------|--------|
| **Given / when / then** | Given events in file → run projector → assert DB rows |
| **Idempotent replay** | Run projector twice → same rows |
| **Version jump** | Include v1 and v2 events after upcast |

Rebuild test: wipe read table → replay full stream → compare to snapshot CSV.

---

## Saga and integration tests

| Test type | Setup |
|-----------|--------|
| **Orchestrator unit** | Mock participant APIs; assert command order and compensation LIFO |
| **In-memory bus** | Choreography with synchronous handlers |
| **Outbox integration** | Real PG + test Kafka/SQS; assert message after TX commit |
| **Failure injection** | Fail step 3 → assert compensate 2, 1 |

Propagate `saga_id` in test traces — same as production — [§7 Observability](07-sagas-and-distributed-workflows.md#observability-and-operations).

---

## CI checklist

- [ ] Golden event fixtures per `schema_version`
- [ ] Projector tests on every PR touching projection logic
- [ ] Contract test for published integration events (JSON Schema / Avro)
- [ ] Saga compensation order test for each new workflow
- [ ] Load test projector catch-up after deploy (optional nightly)

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Test only happy path | Compensation + duplicate delivery |
| Mock event store that differs from prod | Same loader/upcaster code path |
| Skip rebuild test after schema change | Automated rebuild in CI |
| Saga tests without idempotency | Replay same command twice |

---

## Pros and cons

### Fixture-driven event tests

**Pros:** Deterministic; catches regression in rules and projections.

**Cons:** Fixture maintenance as schemas evolve — pair with [§8](08-event-schema-evolution.md).