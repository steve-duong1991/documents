# WebAuthn and Passkeys

**WebAuthn** (W3C) + **FIDO(Fast IDentity Online)2** authenticators give **phishing-resistant** AuthN(Authentication): the browser/OS proves possession of a private key bound to your **origin**. **Passkeys** are the product name for syncable or device-bound WebAuthn credentials. Prefer them for privileged users and as primary login when you can.

> **Scope:** Registration/assertion ceremony, discoverable credentials, attestation (when to use), recovery, step-up. Login playbook MFA(Multi-Factor Authentication) overview → [§5](05-login-security-playbook.md). OIDC(OpenID Connect) `acr` / step-up → [§2a](02A-oidc-logout-and-step-up.md). Session after login → [§4](04-cookie-session-and-csrf.md).

> **Related:** Magic link is not a passkey replacement → [§5b](05B-signup-verify-and-magic-links.md) · Auth tests → [§5a](05A-auth-testing-checklist.md)

---

## At a glance

| Term | Meaning |
|------|---------|
| **WebAuthn** | Browser API(Application Programming Interface) for public-key AuthN ceremonies |
| **Passkey** | User-friendly WebAuthn credential (platform or synced) |
| **RP (Relying Party)** | Your site (`rp.id` = registrable domain) |
| **Authenticator** | Platform (Touch ID, Windows Hello) or roaming (security key) |
| **Ceremony** | `create` (register) or `get` (assert / login) |

**Rule of thumb:** Passkeys beat passwords + SMS for phishing. Still design **recovery** and **lost-device** paths — [§5](05-login-security-playbook.md).

---

## Register (create credential)

```mermaid
sequenceDiagram
    participant U as User / authenticator
    participant B as Browser
    participant RP as Your server (RP)

    RP->>B: PublicKeyCredentialCreationOptions (challenge, rp, user, pubKeyCredParams)
    B->>U: Biometric / PIN / key gesture
    U->>B: Attestation Object + clientDataJSON
    B->>RP: credentialId, publicKey, transports…
    RP->>RP: Verify challenge; store credentialId + pubkey + user_id
```

| Server must | Detail |
|-------------|--------|
| Issue fresh **challenge** | Store server-side; single-use; short TTL(Time To Live) |
| Bind **rpId** / origin | Match your site; no confusing lookalikes |
| Store **credential id + public key** | Per user; support multiple passkeys |
| Check **signCount** (if present) | Clone detection signal |
| Decide **attestation** | Usually `none` for consumer; enterprise may require |

---

## Assert (login / step-up)

```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant RP as Server

    RP->>B: PublicKeyCredentialRequestOptions (challenge, rpId, allowCredentials?)
    B->>U: Gesture
    U->>B: authenticatorData + signature
    B->>RP: assertion
    RP->>RP: Verify sig with stored pubkey; challenge; origin; rpId
    RP->>B: Establish session (rotate sid)
```

| Mode | Use |
|------|-----|
| **Discoverable** (resident) empty `allowCredentials` | Usenameless passkey login |
| **Allow list** | Known credential ids after email entered |
| **Step-up** | Re-assert for sensitive action; bind to existing session |

After success: create/rotate session like any login — [§4](04-cookie-session-and-csrf.md); set `acr`/`amr` accordingly for OIDC-style policy — [§2a](02A-oidc-logout-and-step-up.md).

---

## Passkeys vs passwords vs TOTP

| Factor | Phishing resistance | UX |
|--------|---------------------|-----|
| **Passkey / WebAuthn** | High (origin-bound) | Excellent on supported devices |
| **TOTP(Time-based One-Time Password)** | Medium (prompted codes can be relayed) | Good fallback |
| **SMS OTP(One-Time Password)** | Low (SIM swap / prompt) | Convenient only |
| **Magic link** | Low–medium (inbox / link phishing) | Low friction — [§5b](05B-signup-verify-and-magic-links.md) |
| **Password only** | Low | Legacy |

Mandate passkeys (or WebAuthn security keys) for **admin** roles when feasible.

---

## Recovery and device loss

| Strategy | Notes |
|----------|-------|
| **Multiple passkeys** | Enroll laptop + phone + backup key |
| **Bootstrap with MFA** | Add passkey while TOTP still valid |
| **Recovery codes** | Single-use; hashed; show once |
| **IdP(Identity Provider) / SSO(Single Sign-On)** | Enterprise: re-issue via IdP — [§2b](02B-sso-integration-playbook.md) |
| **Support break-glass** | Dual control — [§5d](05D-impersonation-and-support-access.md) |

Never “email me a permanent bypass link” as the only recovery for high-value accounts.

---

## Implementation checklist

- [ ] Challenges single-use, short TTL, bound to session/flow  
- [ ] Verify origin, rpId, signature, challenge on every assertion  
- [ ] Support multiple credentials per user  
- [ ] Usenameless and/or identifier-first UX tested on iOS/Android/desktop  
- [ ] Step-up path for money/admin without full logout  
- [ ] Recovery documented; codes hashed  
- [ ] Audit register / assert fail / remove credential  
- [ ] Fallback factors enrolled before removing last password (if any)  

---

## Common mistakes

| Mistake | Why it hurts | Fix |
|---------|---------------|-----|
| Skipping challenge verify | Replay | Server-side challenge store |
| Wrong `rp.id` across envs | Breaks prod vs staging | Per-env RP config; no shared credentials across sites |
| Attestation required for consumers | Blocks legitimate devices | Default `none`; attest only if policy needs |
| One passkey only | Brick on phone loss | Encourage 2+ + recovery |
| Equating SMS OTP with passkey | Account takeover | Reserve SMS for backup |
| No step-up ceremony | Long session = lasting privilege | WebAuthn get for sensitive ops |

---

## Pros and cons

| Pros | Cons |
|------|------|
| Phishing-resistant; fast UX | Platform quirks; support matrix |
| Replaces SMS for many users | Recovery UX is the hard part |
| Strong step-up signal | Not all enterprise IdPs expose WebAuthn the same way |

**Bottom line:** implement WebAuthn **register + assert** with real cryptographic verification, prefer **passkeys for privileged users**, and invest as much design in **recovery** as in the happy path.