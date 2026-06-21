# Idempotency — storage patterns

> **Related:** Overview → [Idempotency](13-idempotency.md) · Client and server flow → [13A-idempotency-client-and-server-flow.md](13A-idempotency-client-and-server-flow.md) · Integrations → [13C-idempotency-integrations.md](13C-idempotency-integrations.md)

---

## Where to store idempotency keys

Enforcement lives in the **application**; storage must be **shared** across all app instances ([Stateless architecture](11-stateless-architecture.md)).

| Store | Best for | Pros | Cons |
|-------|----------|------|------|
| **Redis** | Default for API(Application Programming Interface) idempotency | Fast `SET NX`, TTL, response cache; often colocated with rate limits | Another failure domain; define fail-closed vs fail-open |
| **PostgreSQL** | Writes already in same DB transaction | Strong consistency; unique constraint is authoritative | Slower than Redis; couples to DB availability |
| **Domain table** | Payments, orders with `client_reference_id` | No separate idempotency table; business key is the dedup key | Requires modeling upfront |

**Not here:** gateway, load balancer, or app instance memory.

### Pattern A — Redis

```text
Key:   idem:{tenant}:{endpoint}:{idempotency_key}
Value: { status, headers, body, request_hash, created_at }
TTL:   86400 (24h) for completed; 300 (5m) for "processing"
```

```text
SET key "processing" NX EX 300     → if fail, GET and return cached or 409
... do work ...
SET key {response_json} XX EX 86400
```

### Pattern B — PostgreSQL

```sql
CREATE TABLE idempotency_records (
  tenant_id       UUID NOT NULL,
  idempotency_key TEXT NOT NULL,
  request_hash    TEXT NOT NULL,
  response_status INT,
  response_body   JSONB,
  created_at      TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (tenant_id, idempotency_key)
);
```

```text
BEGIN;
INSERT ... ON CONFLICT DO NOTHING RETURNING *;
-- no row → SELECT existing and return cached response
-- row inserted → process, UPDATE with response, COMMIT
```

Combine with the business write in one transaction when possible.

### Pattern C — Natural domain key

```json
{
  "amount": 5000,
  "currency": "usd",
  "client_reference_id": "checkout-session-abc"
}
```

Unique constraint on `(merchant_id, client_reference_id)`. Duplicate insert fails; return the existing payment. No separate idempotency table when the domain model already deduplicates.

### TTL and cleanup

| Setting | Typical value |
|---------|---------------|
| Completed response cache | **24 hours** to **7 days** |
| Processing lock | **5–15 minutes** |
| After TTL expires | Treat as new key, or return `409` if strict forever-dedup is required |

Expire with Redis TTL or a background job on DB rows.
