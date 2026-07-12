# EPIC / FEATURE / USER_STORY Templates

> **Related:** Solution design → [§1](01-solution-design.md) · Architecture → [§2](02-solution-architecture.md) · Overview → [§0](00-overview.md)

Copy-paste templates for backlog work. Use one layer at a time: **EPIC → FEATURE → USER_STORY**.

## Layer rules

| Level | Owns | Does not own |
|-------|------|--------------|
| **EPIC** | Outcome, value, success metrics, broad non-goals, dependencies, risks | Implementation tasks, Given/When/Then AC |
| **FEATURE** | Shippable capability, in scope / out of scope for the slice, demo definition | Persona story wording (that belongs on USER_STORY) |
| **USER_STORY** | As / I want / So that, Given/When/Then AC(Acceptance Criteria), story-level out-of-scope notes | Feature-wide non-goals (keep those on FEATURE / EPIC) |

**Scope rule of thumb**

- **EPIC / FEATURE:** explicit **non-goals** (and FEATURE **in scope** when useful)
- **USER_STORY:** short **out of scope** in Notes only — do not duplicate a long in-scope list; AC already define what “done” means

---

## EPIC template

Outcome + value. Not implementation.

```markdown
## EPIC: [Name]

**Outcome:** What becomes true when this epic is done
**Value:** Why it matters (user / business impact)
**Success metrics:** How we know it worked (numeric or binary)
**Non-goals:** What this epic will not include
**Dependencies:** Other epics, teams, systems
**Risks:** What could block or derail it
```

---

## FEATURE template

Independently demonstrable slice under one EPIC.

```markdown
## FEATURE: [Name]
**Parent EPIC:** …

**Description:** What capability this delivers (1–3 sentences)

**In scope:**
- …

**Out of scope / non-goals:**
- …

**Demo / done when:** …
**Dependencies:** …
```

---

## USER_STORY template

One small, shippable slice of a FEATURE. Stories should be INVEST(Independent, Negotiable, Valuable, Estimable, Small, Testable)-sized. AC define done.

```markdown
## USER_STORY: [Short title]
**Parent FEATURE:** …

**As a** [persona]
**I want** [capability]
**So that** [benefit]

**Acceptance criteria**
- Given … When … Then …
- Given … When … Then …   # include at least one negative / edge path

**Notes**
- Out of scope: …          # only assumptions people might wrongly include
- Dependencies: …
```

### Given / When / Then (reminder)

| Part | Meaning |
|------|---------|
| **Given** | Starting context / preconditions |
| **When** | Action or event |
| **Then** | Expected outcome |

---

## Worked example: one EPIC → many FEATUREs → many USER_STORIES

Shows how one EPIC breaks into multiple FEATUREs, and each FEATURE into multiple USER_STORIES.

### Tree

```text
EPIC: Payout reconciliation
├── FEATURE 1: Import payout batches
│   ├── US 1.1 Upload payout CSV
│   └── US 1.2 Review import errors
├── FEATURE 2: Match payouts to ledger entries
│   ├── US 2.1 Auto-match by payout ID
│   ├── US 2.2 Manually match an exception
│   └── US 2.3 View match summary
└── FEATURE 3: Export reconciliation report
    ├── US 3.1 Export CSV for date range
    └── US 3.2 Include exception status in export
```

### EPIC: Payout reconciliation

**Outcome:** Finance can close regional payouts without manual spreadsheet assembly  
**Value:** Faster monthly close, fewer reconciliation errors  
**Success metrics:** Close time &lt; 1h; error rate &lt; 1%  
**Non-goals:** Real-time ledger rewrite; new mobile app  
**Dependencies:** Existing payout status API(Application Programming Interface)  
**Risks:** Incomplete historical payout data in one region  

---

### FEATURE 1: Import payout batches

**Parent EPIC:** Payout reconciliation  

**Description:** Ops can ingest daily payout files from the payment processor into the reconciliation workspace.

**In scope:**
- Upload CSV
- Validate required columns
- Show import summary

**Out of scope / non-goals:**
- Auto-fetch from processor API
- PDF imports

**Demo / done when:** Ops uploads a processor CSV and sees valid rows ready for matching  

#### USER_STORY 1.1 — Upload payout CSV

**As a** finance ops user  
**I want** to upload a payout CSV  
**So that** I can start reconciliation without pasting rows by hand  

**Acceptance criteria**

```text
Given I am on the reconciliation import screen
When I upload a valid payout CSV
Then the file is accepted and I see row count + total amount

Given I upload a CSV missing required columns
When the upload completes validation
Then I see which columns are missing and no rows are imported
```

**Notes**
- Out of scope: drag-and-drop from email; multi-file zip upload

#### USER_STORY 1.2 — Review import errors

**As a** finance ops user  
**I want** to see failed rows with reasons  
**So that** I can fix the source file and re-import  

**Acceptance criteria**

```text
Given an import has invalid rows
When I open the import result
Then I see each failed row with error reason
  And valid rows are still available for matching
```

---

### FEATURE 2: Match payouts to ledger entries

**Parent EPIC:** Payout reconciliation  

**Description:** Ops can auto-match imported payouts to internal ledger entries and resolve exceptions.

**In scope:**
- Auto-match by payout ID + amount
- Manual match
- Exception queue

**Out of scope / non-goals:**
- FX conversion engine redesign

**Demo / done when:** A batch shows matched pairs plus an exception queue for the rest  

#### USER_STORY 2.1 — Auto-match by payout ID

**As a** finance analyst  
**I want** imported payouts to auto-match ledger entries by payout ID  
**So that** I only review exceptions  

**Acceptance criteria**

```text
Given imported payouts and ledger entries share the same payout ID and amount
When I run auto-match
Then matched pairs move to "Matched"
  And unmatched items remain in the exception queue
```

#### USER_STORY 2.2 — Manually match an exception

**As a** finance analyst  
**I want** to manually link an unmatched payout to a ledger entry  
**So that** known edge cases can still close  

**Acceptance criteria**

```text
Given an unmatched payout in the exception queue
When I select a ledger entry and confirm match
Then both items move to "Matched"
  And the action is recorded in the audit log

Given I try to match two items with different currencies
When I confirm
Then the system blocks the match and explains why
```

#### USER_STORY 2.3 — View match summary

**As a** finance analyst  
**I want** a summary of matched vs unmatched counts  
**So that** I know when the batch is ready to export  

**Acceptance criteria**

```text
Given a batch has been partially matched
When I open the batch summary
Then I see matched count, unmatched count, and total amounts
```

---

### FEATURE 3: Export reconciliation report

**Parent EPIC:** Payout reconciliation  

**Description:** Ops can export a CSV of completed reconciliation for monthly close.

**In scope:**
- Date-range CSV export
- Totals match UI

**Out of scope / non-goals:**
- PDF export
- Scheduled email

**Demo / done when:** Ops exports last month’s CSV and totals match the UI  

#### USER_STORY 3.1 — Export CSV for date range

**As a** finance ops user  
**I want** to export a reconciliation CSV for a date range  
**So that** I can archive evidence for monthly close  

**Acceptance criteria**

```text
Given completed matches exist for the selected range
When I click "Export CSV"
Then I download a CSV within 30 seconds
  And totals match the on-screen summary

Given no matches exist for the range
When I click "Export CSV"
Then I see "No payouts found" and no file downloads
```

**Notes**
- Out of scope: email delivery, multi-merchant bulk export, custom column picker
- Dependencies: payout status API for `completed` payouts

#### USER_STORY 3.2 — Include exception status in export

**As a** finance ops user  
**I want** unmatched exceptions included with status  
**So that** auditors can see what was left open  

**Acceptance criteria**

```text
Given unmatched exceptions exist in the range
When I export CSV
Then the file includes those rows with status "Unmatched"
```

---

## Cursor prompt (reuse)

```text
Plan mode. Solution design only — no code.

Using the templates in @documents/cursor-workflows/includes/01A-epic-feature-user-story-templates.md,
break down the following into EPIC → FEATURE → USER_STORY.

Context: …
Constraints: …
Non-goals: …

Rules:
- One layer at a time if I ask for only EPICs or only stories
- FEATUREs must be independently demonstrable
- USER_STORIES: As/I want/So that + Given/When/Then AC
- Put broad non-goals on EPIC/FEATURE; story-level out of scope in Notes only
- No implementation detail in stories
```

---

## Checklist before treating backlog as final

| # | Check |
|---|--------|
| 1 | Each EPIC has outcome + value (not activity-only) |
| 2 | EPIC/FEATURE non-goals are explicit |
| 3 | FEATUREs are shippable / demo-able slices |
| 4 | USER_STORIES have Given/When/Then AC, including an edge/negative path |
| 5 | Story Notes call out out-of-scope assumptions and dependencies |
| 6 | No implementation tasks disguised as stories |