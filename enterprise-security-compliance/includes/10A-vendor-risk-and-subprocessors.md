# Vendor Risk and Subprocessors

Enterprise customers ask **who touches their data** — vendor intake, DPAs(Data Processing Agreements), periodic review, and subprocessor registers are engineering-adjacent compliance work, not only legal paperwork.

> **Scope:** Third-party and subprocessor lifecycle — intake, contract, technical review, continuous monitoring. Evidence collection → [§10](10-compliance-evidence.md). Program tradeoffs → [§11](11-decision-guide.md). PII(Personally Identifiable Information) classification → [§7](07-pii-and-data-classification.md). Supply chain → [§4](04-supply-chain-security.md).
>
> **Related:** Secrets in vendor integrations → [§5](05-secrets-beyond-database.md) · Encryption requirements → [§8](08-encryption-policy.md) · DSAR(Data Subject Access Request) vendor roles → [§7A](07A-erasure-and-dsar.md) · Audit retention → [§6](06-audit-logging-and-retention.md)

---

## At a glance

| Stage | Output |
|-------|--------|
| **Intake** | Risk tier, data classes, owner |
| **Contract** | DPA(Data Processing Agreement) + SCCs if cross-border |
| **Technical review** | Security questionnaire + evidence |
| **Approve** | Register entry + renewal date |
| **Monitor** | Breach news, cert expiry, usage drift |

**Rule of thumb:** If a vendor stores or processes **customer PII**, it belongs in the **subprocessor list** before prod traffic — not after the first enterprise audit.

---

## Lifecycle

```mermaid
flowchart LR
    Req[New vendor request] --> Tier[Risk tier]
    Tier --> Legal[DPA / order form]
    Legal --> Tech[Security review]
    Tech --> Approve[Approved register]
    Approve --> Prod[Prod integration]
    Prod --> Monitor[Continuous monitor]
    Monitor --> Renew[Annual re-review]
```

| Risk tier | Examples | Review depth |
|-----------|----------|--------------|
| **Critical** | IdP(Identity Provider), primary DB host, payment PSP(Payment Service Provider) | Full SOC 2 + pen test |
| **High** | Email, analytics with PII | DPA + cert review |
| **Medium** | Internal tooling, no customer data | Lightweight checklist |
| **Low** | No data processing | Register only |

---

## Intake checklist (engineering)

| Question | Why |
|----------|-----|
| **Data classes** | Maps to [§7](07-pii-and-data-classification.md) |
| **Subprocessor?** | Customer notification obligation |
| **Regions** | Residency — [architecture §10A](../../architecture-decisions/includes/10A-regional-cells-and-residency.md) |
| **Retention / delete** | DSAR support — [§7A](07A-erasure-and-dsar.md) |
| **Auth model** | SSO(Single Sign-On), API(Application Programming Interface) keys, IP allowlist |
| **Incident notify SLA(Service Level Agreement)** | 24–72 h typical |

Block prod keys until security + legal sign-off for Critical/High.

---

## DPA and subprocessors

| Artifact | Engineering input |
|----------|-------------------|
| **Subprocessor register** | Name, purpose, region, link to DPA |
| **Customer notification** | 30-day add/change process |
| **Flow-down terms** | Your obligations match vendor capability |
| **Audit rights** | Prefer SOC 2 Type II over one-off questionnaires |

Evidence samples live in the compliance pack — [§10](10-compliance-evidence.md).

---

## Continuous monitoring

| Signal | Action |
|--------|--------|
| **Cert / SOC report expiry** | Ticket 90 days before |
| **Security incident news** | Assess customer impact; comms if needed |
| **Scope creep** | New API fields sent to vendor → re-tier |
| **Usage anomaly** | Unexpected export volume |
| **Offboarding** | Key revoke + data return cert |

Align with [§11](11-decision-guide.md) for build-vs-buy when vendor risk exceeds appetite.

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Shadow IT SaaS(Software as a Service) with customer data | Central intake |
| Stale subprocessor PDF | Live register + change log |
| "They don't store data" without review | Data flow diagram required |
| No offboarding runbook | Keys, exports, deletion cert |
| Critical vendor without backup IdP | DR(Disaster Recovery) test — [sre §12](../../sre-and-incidents/includes/12-disaster-recovery.md) |
| Engineering skips questionnaire | Named technical owner per vendor |

---

## Pros and cons

| Model | Pros | Cons |
|-------|------|------|
| **Central vendor management (VM) tool** | Workflow + renewals | Cost; still need eng review |
| **Spreadsheet register** | Simple early stage | Drifts; no alerts |
| **Block all third parties** | Lowest vendor risk | Slow product velocity |
