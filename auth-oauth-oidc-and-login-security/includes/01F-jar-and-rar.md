# JAR and RAR

Two OAuth(Open Authorization) / OIDC(OpenID Connect) extensions that harden or enrich the **authorization request**: **JAR(JWT-secured Authorization Request)** (RFC 9101) packages authorize parameters as a signed (and optionally encrypted) JWT(JSON Web Token); **RAR(Rich Authorization Requests)** (RFC 9396) carries fine-grained `authorization_details` beyond flat scopes.

> **Scope:** When to use JAR vs PAR(Pushed Authorization Requests), request object shape, RAR `authorization_details`, relation to scopes and resource indicators. PAR deep dive → [§1c](01C-pushed-authorization-requests.md). Scopes/consent → [§1b](01B-scopes-and-consent.md). Resource/`aud` → [§1d](01D-resource-indicators.md).

> **Related:** Client auth / keys → [§1a](01A-client-auth-and-token-exchange.md) · Access token validation → [§3](03-token-lifecycle-and-validation.md)

---

## At a glance

| Extension | Problem it solves | Typical combo |
|-----------|-------------------|---------------|
| **PAR** | Fat / sensitive authorize **query string** | Auth Code + PKCE(Proof Key for Code Exchange) |
| **JAR** | Integrity (and confidentiality) of authorize **parameters** | Often JAR inside PAR, or `request` / `request_uri` |
| **RAR** | Permissions too rich for space-delimited **scopes** | `authorization_details` + optional PAR/JAR |

**Rule of thumb:** Start with Auth Code + PKCE. Add **PAR** for large/sensitive authorize URLs. Add **JAR** when the AS requires signed request objects. Add **RAR** when scopes cannot express the action (payments, open banking, fine-grained ops).

---

## JAR — JWT-secured Authorization Request

### Idea

Instead of (or in addition to) query parameters, the client sends a **request object** JWT whose claims are the authorize parameters (`response_type`, `client_id`, `redirect_uri`, `scope`, `state`, `nonce`, …).

| Delivery | How |
|----------|-----|
| **`request`** | Compact JWT by value on authorize (or inside PAR body) |
| **`request_uri`** | AS fetches or already holds the object (PAR often issues this) |

```mermaid
flowchart LR
    C[Client] -->|1. Build + sign request JWT| JWT[Request object]
    JWT -->|2a. PAR POST or authorize| AS[Authorization Server]
    AS -->|3. Validate sig / claims| AuthN[AuthN + consent]
    AuthN --> Code[Auth code → tokens]
```

### Security properties

| Property | Practice |
|----------|----------|
| **Signed request** | AS verifies with client JWKS(JSON Web Key Set) / registered key |
| **`client_id` match** | Claim inside JWT must match authenticated / registered client |
| **One-time / short exp** | `exp` / `jti` as AS policy requires |
| **Optional encryption (JWE)** | When authorize params are confidential to intermediaries |
| **PKCE still applies** | Put `code_challenge` inside the request object for public clients |

JAR does **not** replace PKCE or exact `redirect_uri` allowlisting.

### JAR vs PAR

| Need | Prefer |
|------|--------|
| Hide fat query from browser history / proxies | **PAR** (or PAR+JAR) |
| Cryptographic integrity of params from client keys | **JAR** |
| AS mandates `require_signed_request_object` | **JAR** (often with PAR) |
| Simple first-party BFF(Backend for Frontend) | Neither until required |

Some IdPs: push with PAR, and the pushed body is (or contains) a JAR.

---

## RAR — Rich Authorization Requests

### Idea

Scopes are coarse (`payments`, `accounts`). RAR sends structured **`authorization_details`** (JSON array) describing *what* is authorized: type, actions, datatypes, locations, amounts, etc.

```json
"authorization_details": [
  {
    "type": "payment_initiation",
    "actions": ["initiate"],
    "locations": ["https://api.bank.example/payments"],
    "instructedAmount": { "currency": "EUR", "amount": "123.50" },
    "creditorName": "MerchantX"
  }
]
```

AS shows a consent UI from these details; access token (or introspection) carries the granted details for the resource server to enforce.

### RAR vs scopes vs resource indicators

| Mechanism | Expresses |
|-----------|-----------|
| **scope** | Coarse client capabilities |
| **resource / aud** ([§1d](01D-resource-indicators.md)) | Which API(Application Programming Interface) may accept the token |
| **authorization_details (RAR)** | Fine-grained, often transactional, authorization |

Use together: `resource` names the API; RAR describes the operation; scopes may still gate “can this client use payment_initiation at all.”

### When to adopt RAR

| Adopt | Skip |
|-------|------|
| Open banking / payments / high-value ops | CRUD app with a few scopes |
| Consent must show amount, payee, account | “Read profile” style OIDC |
| RS must enforce structured details | Flat RBAC(Role-Based Access Control) enough — [api-design §12](../../api-design-and-protection/includes/12-identity-rbac-iam-ad.md) |

Large RAR payloads → send via **PAR** (and optionally JAR), not a giant GET query — [§1c](01C-pushed-authorization-requests.md).

---

## Combined stack (high assurance)

```text
PAR (transport) + JAR (integrity) + RAR (fine authz) + PKCE + resource indicators
→ Auth Code → short access token with aud + authorization_details
```

Most SaaS products never need the full stack. Add layers when the IdP or regulated API requires them.

---

## Implementation checklist

### JAR

- [ ] Register client signing keys / JWKS with AS  
- [ ] Include mandatory authorize claims inside the request object  
- [ ] Verify AS rejects tampered / expired / wrong `client_id`  
- [ ] Keep PKCE + `state` / `nonce`  

### RAR

- [ ] Agree `authorization_details` **types** with AS and RS  
- [ ] Consent UI renders human-readable details  
- [ ] RS enforces details (not only scopes)  
- [ ] Prefer PAR when details are large or sensitive  

---

## Common mistakes

| Mistake | Why it hurts | Fix |
|---------|---------------|-----|
| JAR without verifying signature at AS | Forged authorize params | Enforce signed request object policy |
| Putting secrets only in unsigned query next to JAR | Dual source of truth | AS ignores plain params when JAR present (per policy) |
| Encoding RAR only in scopes | Lossy / unreadable consent | Real `authorization_details` |
| Giant RAR on GET `/authorize` | Truncation / leaks | PAR (+ JAR) |
| RS ignores RAR in token | Over-wide access | Enforce details server-side |

---

## Pros and cons

| Extension | Pros | Cons |
|-----------|------|------|
| JAR | Integrity / optional confidentiality of authorize params | Key management; IdP variance |
| RAR | Precise consent and RS enforcement | Schema design + consent UX cost |
| PAR alone | Simpler hardening for fat URLs | No client-key integrity by itself |

**Bottom line:** **PAR** moves params off the URL; **JAR** signs them; **RAR** expresses rich permissions — compose only what your AS and threat model require.