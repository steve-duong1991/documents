# Contributing to Engineering Guides

How to add or change content in `documents/` without breaking navigation or links.

---

## Layout

```
guide-name/
├── README.md       ← TOC (links to includes), section summaries, ## See also
└── includes/
    └── NN-topic.md ← one major section per file (full article)

documents/
├── README.md           ← master index + learning paths
├── CONTRIBUTING.md     ← this file
├── .cursor/            ← agent rules, hooks, subagents (see cursor-agents guide)
└── scripts/
    ├── expand-acronyms.py
    ├── github-format.py
    ├── validate-doc-links.py
    ├── validate-doc-readme.py
    └── validate-doc-prose.py
```

Start from each guide **README** table of contents — topics link directly to `includes/NN-topic.md` on GitHub.

### GitHub navigation

Readers on GitHub should use **guide README tables** — each topic links directly to `includes/NN-topic.md`. The TOC is the navigation surface; do not duplicate full section summaries in the README body.

- **README TOC:** one column, topic → include path (run `python3 scripts/github-format.py` after bulk TOC edits). Skim summaries below the TOC are optional — the table is the primary GitHub navigation.
- **Headings:** no acronym expansions in `#` titles — body text keeps first-use `ACRONYM(Full Text)`.
- **GLOSSARY:** `See also` column uses markdown links to guides or sections.

---

## When to add a new guide vs a new include

| Situation | Action |
|-----------|--------|
| New topic fits an existing guide's scope | Add `includes/NN-name.md` + README TOC row |
| Cross-cutting topic with 3+ existing guides referencing it | Consider a new top-level guide |
| Small cross-link only | Link from existing section; don't create a guide |

Prefer **expanding existing includes** over new top-level folders.

---

## Naming

| Item | Convention | Example |
|------|------------|---------|
| Folder | `kebab-case` | `database-connection-and-security` |
| Include files | `NN-kebab-case.md` (zero-padded) | `15-schema-migration-checklist.md` |
| Sub-articles (split section) | `NNA-` prefix + topic slug (`A`/`B`/`C` uppercase) | `10A-async-jobs-polling.md`, `07C-sagas-operations.md`, `03A-api-gateway-request-flows.md`, `13B-idempotency-storage.md` |
| Title | Plain English with `&` where needed | Database Connection & Security |

Folder name and display title should tell the same story.

---

## Cross-link paths

| Source | Path to sibling guide |
|--------|------------------------|
| `guide/includes/*.md` | `../../other-guide/...` |
| `guide/README.md` | `../other-guide/...` |

After editing links, run:

```bash
cd documents && make validate
```

`make validate` runs:

- `validate-doc-links.py` — file paths and `#heading` anchors
- `validate-doc-readme.py` — every `includes/*.md` appears in the guide README TOC
- `validate-doc-prose.py` — suspicious empty links or stripped inline text (regression guard for acronym runs)

Optional external URL check (slow):

```bash
make validate-external   # HEAD/GET on https:// links
```

---

## See also vs Other guides

| Location | Heading | Purpose |
|----------|---------|---------|
| End of every `README.md` | `## See also` | Repo-wide sibling guide table |
| Mid-chapter (e.g. checklist) | `## Other guides in this repo` | Contextual links inside a section |

Do not duplicate the full sibling table mid-document under `## See also`.

---

## CI

GitHub Actions: `.github/workflows/documents.yml` — link/anchor validation, README TOC sync, acronym check. Same as `make check` (without optional external URL validation).

---

## Content style

- Open with **At a glance** table or **Rule of thumb** where helpful
- Capstone, overview, and decision-guide sections: open with **`> **Related:**`** links to sibling guides
- Sections that overlap a sibling guide (same topic, different lens): add **`> **Scope:**`** before **Related** — state what this file owns and link to the sibling (e.g. HTS §1 system SLOs vs PG §1 `EXPLAIN`; api-design §5 product tiers vs api-rate-limiting §7 layers)
- Algorithm/strategy card sections: add **Related** (where to enforce) + **Common mistakes** when depth warrants it
- Use mermaid for flows and architecture
- End sections with **Common mistakes** and **Pros and cons** when depth warrants it
- Link to sibling guides instead of duplicating full algorithms
- No `TODO` / placeholder sections — ship complete sections or don't add the file

### Acronym expansions

- On **first use per file**, expand registered acronyms inline: `ACRONYM(Full Text)` — no space before `(` (e.g. `CDC(Change Data Capture)`).
- **Headings** stay short — no `(Full Text)` in `#` titles; acronyms in headings are marked seen without expansion.
- Registry: [acronyms.json](acronyms.json). Refresh expansions after adding terms: `python3 scripts/expand-acronyms.py`.
- After bulk edits, run `python3 scripts/github-format.py` to normalize README TOC links and GLOSSARY.
- CI runs `python3 scripts/expand-acronyms.py --check` to catch drift.

---

## Editing with Cursor agents

The repo ships [`.cursor/`](.cursor/) (rules, hooks, doc-reviewer subagent) aligned with the [cursor-agents](cursor-agents/README.md) guide. After agent-assisted edits, run `make check` — the `afterFileEdit` hook runs `make validate` on markdown changes automatically.

---

## Checklist before finishing

- [ ] README TOC updated with new section (sub-articles use labels like `10a` under parent `10`)
- [ ] Cross-links use correct `../` vs `../../`
- [ ] `make validate` passes (or equivalent scripts)
- [ ] Root [README.md](README.md) updated if adding a new top-level guide or learning path
