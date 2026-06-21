# Contributing to Engineering Guides

How to add or change content in `documents/` without breaking navigation or links.

---

## Layout

```
guide-name/
├── README.md       ← TOC, section summaries, ## See also footer
├── GUIDE.md        ← full combined doc (rebuild with scripts/build-guide.py)
└── includes/
    └── NN-topic.md ← one major section per file

documents/
├── README.md           ← master index + learning paths
├── CONTRIBUTING.md     ← this file
└── scripts/
    ├── build-guide.py
    ├── validate-doc-links.py
    └── validate-doc-readme.py
```

Start from `README.md` for browsing. Use `GUIDE.md` for single-file reading or export.

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
| Title | Plain English with `&` where needed | Database Connection & Security |

Folder name and display title should tell the same story.

---

## Cross-link paths

| Source | Path to sibling guide |
|--------|------------------------|
| `guide/includes/*.md` | `../../other-guide/...` |
| `guide/README.md` or `guide/GUIDE.md` | `../other-guide/...` |

After editing links, run:

```bash
cd documents && make validate
```

`make validate` runs:

- `validate-doc-links.py` — file paths and `#heading` anchors
- `validate-doc-readme.py` — every `includes/*.md` appears in the guide README TOC

Optional external URL check (slow; not in pre-commit):

```bash
make validate-external   # HEAD/GET on https:// links
```

Use external checks in a **weekly scheduled CI job** or before release — not on every PR (flaky, rate limits).

---

## See also vs Other guides

| Location | Heading | Purpose |
|----------|---------|---------|
| End of every `README.md` | `## See also` | Repo-wide sibling guide table |
| End of every `GUIDE.md` | `## See also` | Same (included when rebuilding) |
| Mid-chapter (e.g. checklist) | `## Other guides in this repo` | Contextual links inside a section |

Do not duplicate the full sibling table mid-document under `## See also`.

---

## Rebuilding GUIDE.md

After changing `includes/`:

```bash
cd documents
make build-all
make build GUIDE=postgresql-performance
```

`build-guide.py` concatenates includes in sorted order, rewrites `../../` cross-links to `../` for the guide root, and appends the `## See also` block from `README.md`.

---

## CI and pre-commit

- GitHub Actions: `.github/workflows/documents.yml` — link/anchor validation, README TOC sync, `GUIDE.md` drift check, MkDocs build
- Weekly: `.github/workflows/documents-external.yml` — `make validate-external` (https links; may fail on transient outages)
- Pre-commit: `.pre-commit-config.yaml` at repo root — link validation, README sync, and `GUIDE.md` drift check; run `pre-commit install`

Both pre-commit and CI run the same checks as `make check` (without optional external URL validation).

---

## Optional MkDocs site

```bash
pip install mkdocs-material
cd documents && mkdocs serve -f mkdocs.yml
```

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

---

## Checklist before finishing

- [ ] README TOC updated with new section
- [ ] Short summary + "See full details → includes/…" in README body
- [ ] Cross-links use correct `../` vs `../../`
- [ ] `make validate` and `make build-all` pass (or equivalent scripts)
- [ ] Root [README.md](README.md) updated if adding a new top-level guide or learning path
