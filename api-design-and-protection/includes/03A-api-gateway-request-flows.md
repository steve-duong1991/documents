# API Gateway — request flows

> **Related:** Overview → [Load balancer & API gateway](03-api-gateway.md) · Stacks and product selection → [03B-api-gateway-stacks-and-selection.md](03B-api-gateway-stacks-and-selection.md)

---

## Request flows

### Flow 1 — Load balancer only

Traffic spreads across identical (or similar) service instances. The client uses one hostname; the LB picks a backend.

```mermaid
flowchart LR
    C[Client] --> LB[Load Balancer]
    LB --> S1[Instance 1]
    LB --> S2[Instance 2]
    LB --> S3[Instance 3]
    S1 --> DB[(Database)]
    S2 --> DB
    S3 --> DB
```

**Steps:**

1. Client → `GET https://api.example.com/users/123`
2. LB receives request (often TLS(Transport Layer Security) termination here)
3. Health checks exclude unhealthy instances
4. LB picks instance (round-robin, least connections, etc.)
5. Same instance handles the full request/response

**Good for:** scaling one service, high availability, simple path pools (`/api` → one pool, `/static` → another).

---

### Flow 2 — API gateway only (single backend pool)

The gateway handles API concerns; one service (or small set) sits behind it.

```mermaid
flowchart LR
    C[Client] --> GW[API Gateway]
    GW -->|Auth, rate limit, route| SVC[User Service]
    SVC --> DB[(Database)]
```

**Steps:**

1. Client → `GET /v2/users/123` with `Authorization: Bearer …`
2. Gateway validates API key or JWT(JSON Web Token)
3. Applies rate limit per client or subscription tier
4. Routes `/v2/users/*` → User Service
5. May strip path prefix, add internal headers, log metrics
6. Forwards to backend; returns response (optionally transformed)

**Good for:** public APIs, versioning, monetization, central auth, OpenAPI-backed portals.

---

### Flow 3 — Both together (common at scale)

**Gateway** for API policy; **LB** for scaling each microservice.

```mermaid
flowchart TB
    C[Client] --> GW[API Gateway]
    GW -->|/users/*| LB1[LB — Users]
    GW -->|/orders/*| LB2[LB — Orders]
    GW -->|/payments/*| LB3[LB — Payments]
    LB1 --> U1[User 1]
    LB1 --> U2[User 2]
    LB2 --> O1[Order 1]
    LB2 --> O2[Order 2]
    LB3 --> P1[Payment 1]
    LB3 --> P2[Payment 2]
```

**Example — `GET /orders/456`:**

```
Client
  → API Gateway     (auth, rate limit, route to Orders)
  → Orders LB       (pick healthy Order pod)
  → Order Service   (business logic)
  → Database
  ← response back through the chain
```

---

### Flow 4 — Sequence: what each layer sees

```mermaid
sequenceDiagram
    participant Client
    participant GW as API Gateway
    participant LB as Load Balancer
    participant S1 as Backend

    Client->>GW: GET /v1/users/1 + API Key
    Note over GW: Validate key, rate limit, route
    GW->>LB: GET /users/1 (internal)
    Note over LB: Health check, pick instance
    LB->>S1: Forward request
    S1-->>LB: 200 OK
    LB-->>GW: 200 OK
    GW-->>Client: 200 OK (+ CORS, logging)
```

This sequence matches the protected call in [Overview — full flow](00-overview.md#sequence-one-protected-api-call); the overview diagram adds edge WAF(Web Application Firewall) and application AuthZ(Authorization) layers.