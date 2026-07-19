# Decision Guide — Payments and Fintech

When to apply which payment-specific control, and the mistakes that turn a payments feature into a compliance finding or a chargeback spiral.

> **Related:** Overview map → [00-overview.md](00-overview.md) · Generic idempotency → [resilience-patterns §6](../../resilience-patterns/includes/06-idempotency-systemwide.md), [api-design-and-protection §13](../../api-design-and-protection/includes/13-idempotency.md) · Sagas → [event-sourcing-and-cqrs §7](../../event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md)

---

## Master decision flow

```mermaid
flowchart TD
    Start[Payments feature] --> Card{Does your backend ever\nsee raw card data?}
    Card -->|Yes| Reduce[Redesign with hosted fields /\ntokenization — §1]
    Card -->|No| Charge[Design the charge write path]
    Reduce --> Charge
    Charge --> Idem[Layer three idempotency keys —\nclient, processor, ledger §2]
    Idem --> Ledger[Post to immutable\ndouble-entry ledger §3]
    Ledger --> Multi{Multi-step\n(reserve, charge, notify)?}
    Multi -->|Yes| Saga[Model as a saga with\ncompensation]
    Multi -->|No| Fraud[Add pre-auth fraud scoring §4]
    Saga --> Fraud
    Fraud --> Recon[Automate reconciliation\nagainst settlement files §4]
    Recon --> Dispute[Retain evidence for the\nfull dispute window §4]
```

---

## Scenario recommendations

| Scenario | Recommended approach |
|----------|----------------------|
| New checkout flow, first time accepting cards | Hosted fields/SDK tokenization ([§1](01-pci-scope-reduction.md)); never touch raw PAN(Primary Account Number) server-side |
| Mobile client with unreliable networks retrying charges | Client `Idempotency-Key` + processor-side key derived from order ID + verify-before-retry — [§2](02-idempotency-and-double-charge.md) |
| Multi-currency ledger with processor fees | Post fee/FX(Foreign Exchange) entries as their own journal lines — [§3](03-ledger-and-double-entry.md) |
| Refund spanning ledger + processor + notification | Saga with ledger-first posting and compensation — [event-sourcing §7](../../event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| Sudden spike in card-testing attempts | Velocity-based fraud scoring; step-up authentication for medium risk — [§4](04-fraud-and-reconciliation.md) |
| Settlement file shows amounts your ledger doesn't have | Automated daily reconciliation with an exception queue — [§4](04-fraud-and-reconciliation.md) |
| Delayed fulfillment (ship-in-N-days) order | Authorize at checkout, capture at fulfillment — [§2](02-idempotency-and-double-charge.md) |
| High-risk merchant category or new-to-platform seller | Reserve hold against anticipated chargeback liability — [§4](04-fraud-and-reconciliation.md) |
| Regulatory threshold crossed on transaction size/volume | KYC(Know Your Customer)/AML(Anti-Money Laundering) checks — [§4](04-fraud-and-reconciliation.md), [enterprise-security-compliance §10](../../enterprise-security-compliance/includes/10-compliance-evidence.md) |

---

## Priority checklist

- [ ] No raw PAN or CVV(Card Verification Value) ever reaches your application servers or logs
- [ ] Three-layer idempotency in place: client key, processor key, ledger unique constraint
- [ ] Every charge/refund path verifies before retrying on ambiguous failure
- [ ] Ledger is append-only double-entry; balances derived, not mutated in place
- [ ] Multi-step money movement modeled as a saga with compensation, not a single distributed transaction
- [ ] Pre-authorization fraud scoring in place, tiered by risk, not a single hard rule
- [ ] Reconciliation runs automated and daily, with alerting on unmatched-entry rate
- [ ] Evidence retention covers the full dispute/chargeback window, not generic app retention
- [ ] Encryption, secrets, and audit logging reviewed against [enterprise-security-compliance](../../enterprise-security-compliance/README.md)

---

## Common mistakes

| Mistake | Why it hurts | Fix |
|---------|---------------|-----|
| Raw PAN touching your servers or logs | Pulls your whole environment into full PCI audit scope | Hosted fields/tokenization — [§1](01-pci-scope-reduction.md) |
| Trusting `Idempotency-Key` alone to prevent double charges | Client retries, ambiguous timeouts, and webhook redelivery all bypass a single key | Three-layer defense — [§2](02-idempotency-and-double-charge.md) |
| Mutable balance column as source of truth | Silent drift, lost updates, no auditability | Immutable double-entry ledger — [§3](03-ledger-and-double-entry.md) |
| Reconciliation as an afterthought or manual spreadsheet | Drift goes undetected until a customer or auditor finds it | Automated daily reconciliation — [§4](04-fraud-and-reconciliation.md) |
| Evidence for disputes collected only after a chargeback arrives | Missed representment window, lost disputes | Retain evidence proactively for the full dispute window |
| Treating fraud, ledger, and compliance as separate, uncoordinated workstreams | Gaps at the seams (e.g. a fraud hold with no corresponding ledger entry) | Design them together, cross-linked as in this guide |

---

## Quick decision summary

| Question | Default answer |
|----------|-----------------|
| Should our servers ever see a raw card number? | No — hosted fields/tokenization always |
| Is one `Idempotency-Key` enough? | No — layer client, processor, and ledger-level dedup |
| Should balances be mutable fields? | No — derive from an immutable double-entry journal |
| How to handle multi-step money movement? | Saga with compensation, ledger-first |
| How often to reconcile? | Daily, automated, with an exception queue |
| How long to retain dispute evidence? | The full network dispute window, not generic app retention |

---

## See also

| Guide | Topics |
|-------|--------|
| [resilience-patterns](../../resilience-patterns/README.md) | Systemwide idempotency, delivery semantics |
| [api-design-and-protection](../../api-design-and-protection/README.md) | `Idempotency-Key` contract, webhook replay protection |
| [event-sourcing-and-cqrs](../../event-sourcing-and-cqrs/README.md) | Sagas, compensation, outbox |
| [enterprise-security-compliance](../../enterprise-security-compliance/README.md) | Encryption, secrets, audit, compliance evidence |
| [postgresql-performance](../../postgresql-performance/README.md) | ACID(Atomicity, Consistency, Isolation, Durability) transactions, consistency costs |