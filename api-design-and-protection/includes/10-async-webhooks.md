# Async patterns — webhooks

> **Related:** Overview → [Async patterns](10-async-patterns.md) · Jobs and polling → [10-async-jobs-polling.md](10-async-jobs-polling.md) · HMAC(Hash-based Message Authentication Code) webhooks → [Auth model](04-auth-model.md#hmac-webhooks)

## Pattern 2 — Webhooks (server push)

Polling wastes requests when completion is rare or slow. **Webhooks** push terminal state to a client URL. See [HMAC webhooks](04-auth-model.md#hmac-webhooks) for inbound verification; apply the same pattern **outbound**.

### Flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant A as Your API
    participant Q as Queue
    participant W as Worker
    participant WH as Client webhook endpoint

    C->>A: POST /v1/reports/export<br/>{ callback_url: "https://client.app/hooks" }
    A->>Q: Enqueue job_123
    A-->>C: 202 + Location: /v1/jobs/job_123

    Note over C: Client can stop polling

    Q->>W: Process job_123
    W->>A: Mark completed

    A->>WH: POST + X-Signature (HMAC)<br/>{ type: "job.completed", job_id, result }
    WH-->>A: 200 OK

    alt Delivery fails
        A->>WH: Retry with exponential backoff
    end
```

### Webhook payload

```json
{
  "id": "evt_9f2a",
  "type": "job.completed",
  "created_at": "2026-06-14T18:35:00Z",
  "data": {
    "job_id": "job_123",
    "status": "completed",
    "result": { "download_url": "…" }
  }
}
```

### Security controls

```mermaid
flowchart TB
    WH[Your API sends webhook] --> Sig["Sign: HMAC-SHA256(secret, timestamp + body)"]
    Sig --> Headers["Headers: X-Signature, X-Timestamp"]
    Client[Client receiver] --> Verify["Verify signature + timestamp window"]
    Verify --> Reject["Reject replays older than ~5 min"]
```

| Control | Why |
|---------|-----|
| HMAC signature | Proves payload came from you |
| Timestamp | Prevents replay attacks |
| Event ID (`evt_…`) | Client deduplicates |
| HTTPS only | Transport security |
| **SSRF(Server-Side Request Forgery) on `callback_url`** | Block private IPs, metadata endpoints (OWASP(Open Worldwide Application Security Project) API(Application Programming Interface) #7) |

### Hybrid: webhook + poll fallback

```mermaid
flowchart TD
    Start[Job created] --> WH{Client registered webhook?}
    WH -->|Yes| Push[Push on terminal state]
    WH -->|No| Poll[Client polls GET /jobs/id]
    Push --> Fallback[If delivery fails N times]
    Fallback --> Poll
```

**Best practice:** webhook primary, `GET /jobs/{id}` always available as source of truth.

