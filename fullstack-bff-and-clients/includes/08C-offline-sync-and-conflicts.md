# Offline Sync and Conflicts

Offline-capable clients need **durable local queues, versioned merges, and honest conflict UX** — beyond the CRDT(Conflict-free Replicated Data Type) overview in [realtime §4](../../realtime-at-scale/includes/04-crdt-and-ot.md). Foundation patterns live in [§8](08-offline-and-flaky-network.md); this section covers sync protocol and conflict resolution at scale.

> **Scope:** Outbox sync, server versioning, conflict detection, and merge policies for mobile and web. Network UX baseline → [§8](08-offline-and-flaky-network.md). CRDT/OT(Operational Transformation) depth → [realtime §4](../../realtime-at-scale/includes/04-crdt-and-ot.md).
>
> **Related:** [§8 Offline and flaky network](08-offline-and-flaky-network.md) · [realtime §4 CRDT and OT](../../realtime-at-scale/includes/04-crdt-and-ot.md) · Idempotency → [api-design §13](../../api-design-and-protection/includes/13-idempotency.md) · Realtime reconnect → [§5](05-realtime-ux.md)

---

## At a glance

| Concern | Default |
|---------|---------|
| **Local writes** | Outbox + idempotency keys — [§8](08-offline-and-flaky-network.md) |
| **Server truth** | Version vector, `ETag`, or monotonic `revision` |
| **Conflicts** | Detect; don’t silently LWW(Last-Write-Wins) user content |
| **Merge policy** | Field-level rules per domain type |
| **Realtime** | Push invalidations after server wins — [§5](05-realtime-ux.md) |
| **CRDTs** | For collaborative text/presence — [realtime §4](../../realtime-at-scale/includes/04-crdt-and-ot.md) |

**Rule of thumb:** Optimistic UI without a **durable outbox** is a data-loss bug; conflict UI without **detectable versions** is a trust bug.

---

## Sync loop

```mermaid
sequenceDiagram
    participant C as Client outbox
    participant B as BFF
    participant A as API

    C->>B: Mutation + Idempotency-Key + base revision
    B->>A: Forward with AuthZ(Authorization)
    alt Success
        A-->>B: 200 + new revision
        B-->>C: ACK; update local state
    else Conflict
        A-->>B: 409 + server copy + revision
        B-->>C: Conflict payload
        C->>C: User merge or accept server
    end
```

| Component | Responsibility |
|-----------|----------------|
| **Outbox** | Persist pending ops; exponential backoff — [§8](08-offline-and-flaky-network.md) |
| **API(Application Programming Interface)** | Compare `If-Match` / revision; return structured 409 |
| **BFF(Backend for Frontend)** | Stable error shape; optional server-side merge for simple fields |
| **Client** | Show conflict; never drop user edits silently |

---

## Conflict strategies by domain

| Data type | Strategy |
|-----------|----------|
| User profile scalar | Server wins with notice, or field-level merge |
| Notes / docs | CRDT or OT — [realtime §4](../../realtime-at-scale/includes/04-crdt-and-ot.md) |
| Inventory / money | Server wins; no client merge |
| Lists / ordering | Reconcile with explicit reorder op |
| Deletes | Tombstone + sync; propagate deletes before edits |

Document **which fields are mergeable** in the API contract — [api-design §1](../../api-design-and-protection/includes/01-api-design.md).

---

## Beyond CRDT overview

CRDTs excel at concurrent editing; most product APIs still need **operation logs**:

| When CRDT | When revision + 409 |
|-----------|---------------------|
| Live cursors, rich text | Form saves, settings, commerce |
| Always-online collaboration | Mobile offline queues |
| Commutative edits | Strong invariants (balance, stock) |

Hybrid: CRDT for document body; REST(Representational State Transfer) mutation for publish/finalize with revision check.

---

## Operational checklist

- [ ] Every mutating endpoint supports idempotency — [api-design §13](../../api-design-and-protection/includes/13-idempotency.md)
- [ ] 409 responses include server entity + revision
- [ ] Outbox survives app kill; flush on connectivity — [§8](08-offline-and-flaky-network.md)
- [ ] Metrics: conflict rate, outbox depth, time-to-sync
- [ ] Realtime channel notifies when server overrides client — [§5](05-realtime-ux.md)

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Blind LWW on user content | Detect conflict; prompt or field merge |
| No idempotency on outbox replay | `Idempotency-Key` per op |
| Client revision from local clock | Server-issued revision / ETag |
| CRDT everywhere | Use only where commutative edits are product-safe |
| Conflict only logged server-side | User-visible resolution UI |
| Sync ignores delete tombstones | Delete ops in outbox with higher precedence |
