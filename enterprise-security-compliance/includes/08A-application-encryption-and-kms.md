# Application Encryption and KMS Operations

Platform TLS(Transport Layer Security) and disk encryption are baseline — [§8](08-encryption-policy.md). **Application-level encryption** (envelope and field-level) protects data from DB operators, backup theft, and blast-radius leaks when a row store is compromised.

> **Scope:** Envelope encryption, field encryption patterns, DEK(Data Encryption Key) lifecycle, and KMS(Key Management Service) operations. Policy and key hierarchy → [§8](08-encryption-policy.md). Secrets rotation → [§5](05-secrets-beyond-database.md).
>
> **Related:** [§8 Encryption policy](08-encryption-policy.md) · PII(Personally Identifiable Information) classes → [§7](07-pii-and-data-classification.md) · Erasure / crypto-shred → [§7A](07A-erasure-and-dsar.md) · DB TLS → [database-connection §10](../../database-connection-and-security/includes/10-mtls-client-certs.md)

---

## At a glance

| Pattern | Use when |
|---------|----------|
| **Envelope encryption** | Large blobs; per-object DEKs wrapped by CMK(Customer Master Key) |
| **Field encryption** | Restricted columns (government ID, secrets) in shared tables |
| **Searchable encryption** | Rare; prefer tokenization or blind indexes with legal review |
| **KMS envelope** | App never holds CMK; unwrap DEK via IAM(Identity and Access Management) |
| **Rotation** | Versioned DEKs; re-encrypt on schedule or CMK rotate |
| **Erasure** | Destroy DEK or CMK shard for crypto-shred — [§7A](07A-erasure-and-dsar.md) |

**Rule of thumb:** Encrypt **fields that operators must not read**; do not encrypt everything “just in case” — key management cost and query pain are real.

---

## Envelope flow

```mermaid
flowchart LR
    App[Application] --> KMS[KMS / HSM(Hardware Security Module)]
    KMS --> CMK[Customer master key]
    App --> Gen[Generate DEK]
    Gen --> Wrap[KMS wrap DEK]
    Wrap --> Store[(Ciphertext + wrapped DEK)]
    App --> Plain[Encrypt payload with DEK]
    Plain --> Store
```

| Artifact | Stored where |
|----------|--------------|
| Ciphertext + IV(Initialization Vector) | Application DB / object store |
| Wrapped DEK | Alongside ciphertext or key table |
| CMK | KMS only; IAM-controlled |

Decrypt path: IAM check → KMS unwrap DEK → decrypt in memory; zeroize buffers after use.

---

## Field encryption tactics

| Tactic | Trade-off |
|--------|-----------|
| App-layer encrypt before INSERT | Simple; breaks naive SQL(Structured Query Language) search |
| DB-native column encryption | Vendor lock-in; still need key custody story |
| Tokenization vault | Best for PAN(Primary Account Number)-class data |
| Deterministic encryption for lookup | Weaker; limit to exact-match queries |

Align field classes with [§7](07-pii-and-data-classification.md). Log **key IDs**, not plaintext or DEKs.

---

## KMS operations

| Operation | Practice |
|-----------|----------|
| **Provision CMK** | Separate keys per env; prod CMK never in dev |
| **IAM policies** | Least privilege per service account; no human decrypt in prod |
| **Audit** | CloudTrail / equivalent on every Decrypt |
| **Rotation** | Automatic CMK versioning; plan DEK re-wrap jobs |
| **Disaster recovery** | Document CMK restore vs irreversible destroy |
| **Erasure** | Crypto-shred by destroying wrapped DEKs — [§7A](07A-erasure-and-dsar.md) |

Run **re-encrypt drills** after CMK rotation — stale wrapped DEKs are a common outage.

---

## Operational checklist

- [ ] CMK per environment; IAM least privilege on `kms:Decrypt`
- [ ] DEK version stored with ciphertext; migration path documented
- [ ] No master keys in config repos — [§5](05-secrets-beyond-database.md)
- [ ] Erasure runbook includes crypto-shred steps
- [ ] Compliance evidence exports KMS audit logs — [§10](10-compliance-evidence.md)

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Same CMK for dev and prod | Environment-separated keys |
| DEK stored next to CMK in config | Envelope only; CMK in KMS |
| Encrypt then grep logs for debugging | Structured redaction; decrypt in secure tooling |
| Rotation without re-wrap plan | Job to re-wrap DEKs on new CMK version |
| Field encryption on sort/filter columns | Tokenize or accept limited query |
| Homegrown AES helpers | Use vetted SDK + KMS — [§8](08-encryption-policy.md) |
