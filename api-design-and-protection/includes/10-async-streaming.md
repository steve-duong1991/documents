# Async patterns — streaming and long poll

> **Related:** Overview → [Async patterns](10-async-patterns.md) · Jobs and polling → [10-async-jobs-polling.md](10-async-jobs-polling.md) · Webhooks → [10-async-webhooks.md](10-async-webhooks.md)

## Pattern 3 — Long polling

For **near-real-time** status without webhooks (mobile, firewalled clients):

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API

    C->>A: GET /v1/jobs/job_123?wait=30
    Note over A: Hold request up to 30s until status changes
    A-->>C: 200 { status: "completed" }

    Note over C: On timeout with no change, reconnect immediately
```

| Pros | Cons |
|------|------|
| Fewer requests than short polling | Holds a server connection |
| Simple client logic | Gateway timeout must exceed `wait` |
| Works through most firewalls | Less scalable than webhooks at high volume |

---

## Pattern 4 — Server-Sent Events (SSE)

**One-way server → client stream** over HTTP(Hypertext Transfer Protocol). Good for progress logs, live feeds, LLM token streaming.

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API

    C->>A: GET /v1/jobs/job_123/events<br/>Accept: text/event-stream
    A-->>C: event: progress\ndata: {"percent":10}\n\n
    A-->>C: event: progress\ndata: {"percent":50}\n\n
    A-->>C: event: completed\ndata: {"download_url":"…"}\n\n
    Note over A: Close stream
```

```http
GET /v1/jobs/job_123/events
Accept: text/event-stream
Authorization: Bearer …
```

Response (chunked):

```
event: progress
data: {"percent": 10}

event: completed
data: {"download_url": "https://…"}
```

| Good for | Not good for |
|----------|--------------|
| Progress UI, log tailing | Client → server messages |
| Browser `EventSource` API(Application Programming Interface) | Binary payloads (use WebSockets) |
| AI/LLM token streams | High concurrency without connection planning |

---

## Pattern 5 — Chunked streaming (NDJSON)

**Incremental results in a single request** — search results, large CSV rows, LLM output:

```mermaid
flowchart LR
    C[Client] -->|POST /v1/search/stream| A[API]
    A -->|chunk 1| C
    A -->|chunk 2| C
    A -->|chunk N| C
    A -->|close stream| C
```

```http
HTTP/1.1 200 OK
Content-Type: application/x-ndjson
Transfer-Encoding: chunked

{"id":"res_1","title":"…"}
{"id":"res_2","title":"…"}
```

One JSON object per line. Client must stay connected; mid-stream retry is harder than job + poll.

---

## Pattern 6 — Sync timeout fallback (avoid if possible)

Gateway timeout can force a hybrid — prefer **always `202`** for known-slow endpoints:

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant A as API

    C->>G: POST /v1/process
    G->>A: Forward sync attempt

    alt Completes in under gateway timeout
        A-->>C: 200 { result }
    else Still running at timeout
        G-->>C: 504 Gateway Timeout
        Note over C: GET /jobs by correlation or Idempotency-Key
    end
```

---
