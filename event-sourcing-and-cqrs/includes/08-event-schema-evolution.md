# Event Schema Evolution

Event logs are forever — schema changes are **read-path** transformations (upcasting), not `UPDATE` on historical rows.

> **Deep dive:** Avro vs Protobuf vs JSON on Kafka → [apache-kafka §6](../../apache-kafka/includes/06-serialization-and-schema-evolution.md) · Event envelope and naming → [apache-kafka §6 naming](../../apache-kafka/includes/06-serialization-and-schema-evolution.md#naming-conventions)
>
> **Related:** Immutability → [01-core-concepts.md#immutability-and-corrections](01-core-concepts.md#immutability-and-corrections) · Projector rebuild → [03-storage-and-projections.md](03-storage-and-projections.md) · API(Application Programming Interface) versioning → [api-design §14](../../api-design-and-protection/includes/14-api-versioning-and-deprecation.md) · Deploy coupling → [deployment §12](../../deployment-strategies/includes/12-schema-migrations-and-deploy.md)

---

## At a glance

| Strategy | What changes | Replay impact |
|----------|--------------|---------------|
| **Additive fields** | New optional JSON fields | Old events still valid |
| **Upcasting** | Transform v1 → v2 on read | Loader applies per event |
| **New event type** | `OrderCreatedV2` alongside v1 | Both types in stream |
| **Projector version** | New read model shape | Rebuild projection from scratch |

**Rule of thumb:** Never mutate stored events. Add version metadata; upcast at load time; rebuild projections when read models change structurally.

---

## Version metadata

Store on every event:

```json
{
  "event_type": "OrderCreated",
  "schema_version": 2,
  "aggregate_id": "ord-123",
  "payload": { ... }
}
```

| Field | Purpose |
|-------|---------|
| `event_type` | Routing to handler / projector |
| `schema_version` | Select upcaster chain |
| `aggregate_id` | Stream partition key |

---

## Upcasting

```mermaid
flowchart LR
    Store[(Stored v1 event)] --> Load[Event loader]
    Load --> Up1[v1 → v2 upcaster]
    Up1 --> Up2[v2 → v3 upcaster]
    Up2 --> Domain[Current domain object]
```

| Rule | Detail |
|------|--------|
| **Chain upcasters** | v1→v2, v2→v3 — not v1→v3 skip unless documented |
| **Test fixtures** | Golden files for each historical version |
| **Deploy order** | Deploy readers that understand new version **before** writers emit it |
| **Snapshots** | Re-snapshot after major schema jumps to cut replay cost |

Example: v1 `amount_cents` int → v2 `money` object `{ currency, amount }`.

---

## Projector compatibility

| Change | Safe during rolling deploy? |
|--------|----------------------------|
| Add optional column to read model | ✅ Expand |
| New projector for new view | ✅ Side-by-side |
| Rename column consumed by API | ❌ Expand/contract — [PG §15](../../postgresql-performance/includes/15-schema-migration-checklist.md) |
| Change projection logic only | Rebuild from events; may lag during deploy |

Runbook: stop projector → deploy new code → rebuild or catch-up → resume. See [Rebuild-from-scratch runbook](03-storage-and-projections.md#rebuild-from-scratch-runbook).

---

## Contract with consumers

| Consumer type | Evolution rule |
|---------------|----------------|
| **Internal projector** | Upcast + rebuild |
| **External Kafka subscriber** | Additive fields only; new topic for breaking |
| **Public event API** | Versioned envelope; deprecation window |

Pair with [api-design §15 contract testing](../../api-design-and-protection/includes/15-contract-and-schema-testing.md) for published schemas.

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `UPDATE events SET payload = ...` | Upcast on read |
| Deploy writer before reader | Two-phase deploy: readers first |
| No version field | Add `schema_version` early |
| Skip upcaster tests | Fixture per version in CI(Continuous Integration) |

---

## Pros and cons

### Upcasting on read

**Pros:** Full history preserved; gradual migration.

**Cons:** Loader complexity grows; replay slows without snapshots.