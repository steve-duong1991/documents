# Anonymous and Guest Sessions

Many products need a **guest session** before login: cart, multi-step signup, “continue as guest,” or a wizard that later becomes an account. Treat guests as a **real session type** with narrow AuthZ — not “no auth, trust the browser.”

> **Scope:** Issue guest `sid`, store workflow state server-side, promote on register/login, TTL/abuse controls. Authenticated cookie/CSRF(Cross-Site Request Forgery) mechanics → [§4](04-cookie-session-and-csrf.md). Integrity → [§3a](03A-token-cookie-integrity.md). Signup / magic link → [§5b](05B-signup-verify-and-magic-links.md). Lifetimes → [§3d](03D-lifetimes-and-sliding-sessions.md). Concurrent devices → [§3e](03E-concurrent-sessions-and-devices.md).

> **Related:** Session fixation / rotate `sid` on login → [§4](04-cookie-session-and-csrf.md) · Rate limits for anonymous → [api-rate-limiting](../../api-rate-limiting/README.md)

---

## At a glance

| Concern | Practice |
|---------|----------|
| **Guest credential** | Opaque `sid` in `HttpOnly` `Secure` cookie (prefer `__Host-`) |
| **Authority** | Server session row with `principal_type=guest` + narrow capabilities |
| **Workflow data** | Cart / draft / step progress keyed by guest id — not only `localStorage` |
| **Promote** | On register or login: bind data → `user_id`, **rotate `sid`**, revoke old guest |
| **TTL** | Short idle + absolute (hours–days), stricter than authenticated SSO(Single Sign-On) |
| **Abuse** | Per-IP / fingerprint rate limits; cap create-guest and mutations |

**Rule of thumb:** Anonymous is still authenticated *as guest*. Fail closed for anything that needs a real user.

---

## When you need a guest session

| Use case | Guest session? |
|----------|----------------|
| Browse public catalog (read-only) | Optional — cookie-less + CDN(Content Delivery Network) is fine |
| Cart / wishlist before login | **Yes** |
| Multi-step registration wizard | **Yes** (or signed continuation tokens per step) |
| “Try the product” sandbox | **Yes** with hard quotas |
| Call privileged APIs(Application Programming Interfaces) | **No** — require real AuthN |

---

## Step-by-step: anonymous → register → authenticated

```mermaid
sequenceDiagram
    participant U as Browser
    participant B as BFF / app
    participant S as Session store
    participant D as Domain DB

    U->>B: First mutating / workflow request (no cookie)
    B->>S: CREATE guest sid (ttl, caps, csrf)
    B->>U: Set-Cookie __Host-sid=guest_…
    U->>B: Step N (cookie + CSRF)
    B->>S: Load guest; AuthZ guest caps
    B->>D: Upsert draft/cart by guest_id
    U->>B: Register or login (email/OIDC)
    B->>B: Create/verify user; AuthN OK
    B->>D: Promote guest_id → user_id (merge)
    B->>S: DEL old guest; CREATE auth sid
    B->>U: Set-Cookie new sid (rotated)
```

### 1. Create guest on first need

Issue when the user starts a **stateful** flow (add to cart, start signup), not on every anonymous GET if you can avoid it.

```text
session:{sid} = {
  principal_type: "guest",
  guest_id: "g_…",          # stable id for domain rows
  created_at, idle_exp, absolute_exp,
  csrf_secret,
  caps: ["cart:write", "signup:draft"],
  meta: { ip_hash, ua_hash }  # optional abuse signals
}
```

Cookie flags match authenticated sessions — [§4](04-cookie-session-and-csrf.md). Same CSRF rules once the cookie exists.

### 2. Authorize as guest

| Allow | Deny |
|-------|------|
| Create/update **own** cart/draft by `guest_id` | Anything needing `user_id` / roles / PII(Personally Identifiable Information) of others |
| Read public + own draft | Admin, payments capture, cross-tenant |
| Start signup / request verify email | Refresh tokens, long-lived OAuth(Open Authorization) grants |

Never copy guest caps into an authenticated session without an explicit promote.

### 3. Persist workflow state

Prefer **server (or DB) rows** keyed by `guest_id`:

| Store | Example keys |
|-------|----------------|
| Cart | `cart:guest:{guest_id}` |
| Signup draft | `signup_draft:{guest_id}` (email unverified, steps done) |
| Wizard cursor | `flow:{guest_id}:{flow_name}` |

Browser storage alone is lost across devices and easy to tamper with — treat it as UX cache only.

### 4. Promote on register or login

1. Complete AuthN (password signup, magic link, or OIDC(OpenID Connect) — [§5b](05B-signup-verify-and-magic-links.md), [§2b](02B-sso-integration-playbook.md))
2. **Merge** domain data: `UPDATE … SET user_id=? WHERE guest_id=?` (define conflict policy: keep user cart, merge lines, or ask)
3. **Rotate session:** delete guest `sid`; issue new authenticated `sid` (session fixation defense)
4. Clear/reissue CSRF secret with the new session
5. Audit: `guest_promoted` with old `guest_id` → `user_id` (no raw cookies)

### 5. Expire and garbage-collect

| Clock | Guest default (tune per product) |
|-------|----------------------------------|
| Idle | 30 min – 24 h |
| Absolute | 24 h – 7 d |
| Domain draft GC | Align with absolute; soft-delete then purge |

Authenticated lifetimes stay in [§3d](03D-lifetimes-and-sliding-sessions.md) — do not give guests IdP-length SSO.

---

## Continuation without a long-lived cookie

For email-driven steps (verify link, resume on another device):

| Pattern | Use |
|---------|-----|
| **Signed one-time continuation token** | Short TTL; bind `guest_id` + step; single-use |
| **Magic link** that lands mid-flow | After verify, promote or attach to guest — [§5b](05B-signup-verify-and-magic-links.md) |
| **Do not** put `guest_id` alone in a guessable URL | Attacker enumerates carts/drafts |

---

## Security checklist

- [ ] Guest cookie: `HttpOnly` + `Secure` + `SameSite` (+ `__Host-` when possible)  
- [ ] CSRF on guest mutations  
- [ ] Caps enforced server-side every request  
- [ ] `sid` rotated on promote / login  
- [ ] Merge policy documented (cart / draft conflicts)  
- [ ] Rate limit: create-guest, signup start, cart write (IP + optional device)  
- [ ] Guest cannot obtain refresh tokens or broad scopes  
- [ ] Logs omit raw `sid`; include `guest_id` / `user_id` only as needed  
- [ ] Tests: stolen guest sid after promote → 401; fixation: pre-login sid rejected after login  

---

## Common mistakes

| Mistake | Why it hurts | Fix |
|---------|---------------|-----|
| “Anonymous = no session” + trust client cart | Tamper / replay / lossy UX | Server guest session + caps |
| Reuse same `sid` after login | Session fixation | Rotate on promote |
| Guest and user share one long-lived refresh | Guest theft → account | Guests: session only; refresh after AuthN |
| Guessable `guest_id` in URLs | Enumeration | Opaque ids; authz on every read |
| Infinite guest TTL | Storage + abuse | Short idle/absolute + GC |
| Promote without merge policy | Lost carts / duplicate orders | Explicit merge + audit |

---

## Pros and cons

| Pros | Cons |
|------|------|
| Smooth funnel before AuthN | Extra session type to secure and GC |
| Server-side draft survives refresh | CSRF + rate limits still required |
| Clean promote path to real account | Merge conflicts need product rules |

**Bottom line:** create a **narrow guest session**, keep workflow state **server-side**, and on register/login **promote + rotate `sid`** — never treat anonymous as “unauthenticated and unbounded.”