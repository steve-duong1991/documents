# Payments and Fintech Guide

A practical reference for the parts of payment systems that are unlike ordinary CRUD APIs — PCI DSS(Payment Card Industry Data Security Standard) scope reduction, double-charge prevention beyond generic idempotency, double-entry ledgers, and fraud/reconciliation.

Related: [resilience-patterns](../resilience-patterns/README.md) (idempotency, delivery semantics) · [api-design-and-protection](../api-design-and-protection/README.md) (`Idempotency-Key` contract) · [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) (sagas for multi-step money movement) · [enterprise-security-compliance](../enterprise-security-compliance/README.md) (encryption, audit, compliance evidence) · [postgresql-performance](../postgresql-performance/README.md) (transactional guarantees the ledger depends on)

> **Scope:** This guide covers **payment-specific hardening** that generic API(Application Programming Interface) and resilience patterns don't fully address — cardholder data scope, money-specific double-charge classes, ledger correctness, and fraud/reconciliation operations. It assumes you've already read [resilience-patterns §6](../resilience-patterns/includes/06-idempotency-systemwide.md) and [api-design-and-protection §13](../api-design-and-protection/includes/13-idempotency.md) for the generic idempotency baseline.

---

## Table of contents

| # | Topic |
|---|-------|
| — | [Overview](includes/00-overview.md) |
| 1 | [PCI scope reduction](includes/01-pci-scope-reduction.md) |
| 2 | [Idempotency and double-charge prevention](includes/02-idempotency-and-double-charge.md) |
| 3 | [Ledger and double-entry accounting](includes/03-ledger-and-double-entry.md) |
| 3A | [Refunds, payouts, and settlement](includes/03A-refunds-payouts-settlement.md) |
| 4 | [Fraud and reconciliation](includes/04-fraud-and-reconciliation.md) |
| 5 | [Decision guide](includes/05-decision-guide.md) |

> **On GitHub:** Click a topic in the table above for the full section.

## Reading paths

| If you are… | Read in order |
|-------------|---------------|
| **Accepting card payments for the first time** | Overview → §1 PCI scope reduction → §2 Double-charge prevention |
| **Designing the money-movement write path** | §2 Double-charge prevention → §3 Ledger and double-entry → [event-sourcing §7](../event-sourcing-and-cqrs/includes/07-sagas-and-distributed-workflows.md) |
| **Refunds / payouts / settlement** | §3 Ledger → [§3A Refunds and payouts](includes/03A-refunds-payouts-settlement.md) → §4 Fraud and reconciliation |
| **Building chargeback/reconciliation operations** | §4 Fraud and reconciliation → [§3A](includes/03A-refunds-payouts-settlement.md) → §5 Decision guide |
| **Security/compliance review before launch** | §1 PCI scope → [enterprise-security-compliance §8](../enterprise-security-compliance/includes/08-encryption-policy.md) → [§10 compliance evidence](../enterprise-security-compliance/includes/10-compliance-evidence.md) |

---

## See also

| Guide | Topics |
|-------|--------|
| [resilience-patterns](../resilience-patterns/README.md) | Systemwide idempotency, delivery semantics, retries |
| [api-design-and-protection](../api-design-and-protection/README.md) | `Idempotency-Key` HTTP(Hypertext Transfer Protocol) contract, webhook replay protection |
| [event-sourcing-and-cqrs](../event-sourcing-and-cqrs/README.md) | Sagas, compensation, outbox for multi-step money movement |
| [enterprise-security-compliance](../enterprise-security-compliance/README.md) | Encryption, secrets, audit logging, compliance evidence |
| [postgresql-performance](../postgresql-performance/README.md) | ACID(Atomicity, Consistency, Isolation, Durability) transactions, row-level security, consistency costs behind the ledger |
| [database-connection-and-security](../database-connection-and-security/README.md) | Credentials and network security around the payments datastore |
| [apache-kafka](../apache-kafka/README.md) | Event streaming for fraud signals and reconciliation pipelines |
| [high-throughput-systems](../high-throughput-systems/README.md) | Throughput and observability for payment write paths |
| [sre-and-incidents](../sre-and-incidents/README.md) | Incident response when a payment path degrades |
| [finops-and-cost](../finops-and-cost/README.md) | Processor fees and reconciliation infrastructure cost |