# Pushed Authorization Requests

**PAR(Pushed Authorization Requests)** (RFC 9126) moves authorize parameters off the browser redirect URL. The client **POSTs** the request to the authorization server first, receives a short-lived `request_uri`, then redirects the user with only that handle (plus `client_id`).

> **Scope:** When and how to use PAR with Auth Code + PKCE(Proof Key for Code Exchange). Grant flow → [§1](01-oauth2-grants-and-flows.md). Client authentication at PAR/token → [§1a](01A-client-auth-and-token-exchange.md). Resource/`aud` → [§1d](01D-resource-indicators.md). OIDC(OpenID Connect) authorize params (`nonce`, `acr_values`) → [§2](02-oidc-discovery-and-tokens.md), [§2a](02A-oidc-logout-and-step-up.md).

---

## Rule of thumb

Use **Auth Code + PKCE** always. Add **PAR** when authorize query strings are large, sensitive, or must not appear in browser history, proxies, or `Referer` logs. Skip PAR for simple first-party BFF(Backend for Frontend) apps until those risks show up.

---

## Problem PAR solves

Classic authorize redirect:

```text
GET /authorize?response_type=code&client_id=…&redirect_uri=…&scope=…&state=…&code_challenge=…&nonce=…&claims=…
```

| Risk | Detail |
|------|--------|
| **URL length** | Complex `claims` / many scopes blow past browser/proxy limits |
| **Leakage** | History, server access logs, analytics, Referer to third parties |
| **Tampering** | User/malware edits query params before the IdP sees them |

PAR binds the full parameter set **server-side** under a one-time `request_uri`.

---

## Flow

```mermaid
sequenceDiagram
    participant C as Client (BFF / confidential or public+PKCE)
    participant AS as Authorization Server
    participant U as User browser

    C->>AS: POST /par (params + client auth / PKCE challenge)
    AS->>AS: Store request; mint request_uri
    AS->>C: 201 { request_uri, expires_in }
    C->>U: 302 /authorize?client_id&request_uri
    U->>AS: GET /authorize?client_id&request_uri
    AS->>AS: Load pushed request; run AuthN/consent
    AS->>U: Redirect ?code&state
    U->>C: Callback
    C->>AS: POST /token (code + code_verifier + client auth)
```

### Typical PAR request

```text
POST /par
Content-Type: application/x-www-form-urlencoded

response_type=code
&client_id=…
&redirect_uri=https://app.example.com/callback
&scope=openid orders:read
&state=…
&code_challenge=…
&code_challenge_method=S256
&nonce=…
# + client authentication (confidential) or none (public + PKCE)
```

### Typical PAR response

```json
{
  "request_uri": "urn:ietf:params:oauth:request_uri:abc123",
  "expires_in": 60
}
```

Then:

```text
GET /authorize?client_id=…&request_uri=urn:ietf:params:oauth:request_uri:abc123
```

Do **not** resend the full parameter set on `/authorize` when using `request_uri` (unless the AS explicitly allows merging — prefer pushed-only).

---

## Discovery

Look for in Authorization Server / OIDC metadata:

| Field | Meaning |
|-------|---------|
| `pushed_authorization_request_endpoint` | PAR URL |
| `require_pushed_authorization_requests` | If `true`, browser-only authorize without PAR is rejected |

Cache metadata like other discovery docs — [§2](02-oidc-discovery-and-tokens.md).

---

## Client authentication at PAR

| Client | At `POST /par` |
|--------|----------------|
| **Confidential** (BFF) | `client_secret_*`, `private_key_jwt`, or mTLS(Mutual Transport Layer Security) — [§1a](01A-client-auth-and-token-exchange.md) |
| **Public** (SPA / native) | `client_id` + PKCE fields; no secret |

PAR does **not** replace PKCE for public clients — use both.

---

## Security properties

| Property | Practice |
|----------|----------|
| **One-time `request_uri`** | Single use; short `expires_in` (often 30–90s) |
| **Client binding** | `request_uri` usable only by the pushing `client_id` |
| **PKCE** | Still required for public clients; challenge is inside the pushed body |
| **State / nonce** | Still generate and verify — [§1](01-oauth2-grants-and-flows.md), [§2](02-oidc-discovery-and-tokens.md) |
| **HTTPS** | PAR and authorize over TLS(Transport Layer Security) only |

Related: **JAR(JWT-secured Authorization Request)** and **RAR(Rich Authorization Requests)** deep dive → [§1f](01F-jar-and-rar.md). Some IdPs combine JAR + PAR. Prefer PAR alone unless the IdP requires signed request objects.

---

## When to adopt

| Adopt PAR | Skip for now |
|-----------|--------------|
| Large `scope` / `claims` / RAR payloads | Simple `openid profile` BFF login |
| Regulated / high-assurance AuthN | Authorize URL already short and first-party only |
| AS sets `require_pushed_authorization_requests` | IdP has no PAR endpoint |
| Worried about proxy/access-log leakage of authorize query | Early MVP with low sensitivity |

---

## Implementation checklist

- [ ] Discover `pushed_authorization_request_endpoint`  
- [ ] POST all authorize params to PAR (including PKCE + `state` / `nonce`)  
- [ ] Authenticate confidential clients on PAR  
- [ ] Redirect with `client_id` + `request_uri` only  
- [ ] Handle PAR `expires_in` — don’t reuse stale `request_uri`  
- [ ] Keep token-step PKCE `code_verifier` in server/session — never in the URL  
- [ ] Test: expired `request_uri`, wrong `client_id`, missing PKCE  

Add cases to [§5a](05A-auth-testing-checklist.md) when you enable PAR.

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Putting secrets in PAR body for public clients | No client secret in SPA; PKCE only |
| Replaying `request_uri` | One-shot; push again if expired |
| Duplicating params on `/authorize` and PAR | Prefer pushed request as sole source |
| Skipping PKCE because “PAR is enough” | PAR ≠ PKCE; use both for public clients |
| Logging full PAR bodies with PII(Personally Identifiable Information) | Redact; short retention |

---

## Pros and cons

| Pros | Cons |
|------|------|
| Smaller, safer redirects | Extra round-trip before authorize |
| Harder request tampering | IdP must support PAR |
| Fits complex authorize payloads | Slightly more client code |

**Bottom line:** PAR hardens the **authorize request** path; it complements Auth Code + PKCE and client auth — it does not replace them.