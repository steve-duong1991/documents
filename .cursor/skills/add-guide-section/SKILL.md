---
name: add-guide-section
description: Add or split a guide section (includes/*.md), update README TOC, cross-links, and acronyms. Use when adding a new topic, sub-article, or guide include file.
---

# Add a guide section

Use when adding `includes/NN-topic.md` or a sub-article (`NNA-...`).

## 1. Choose location

| Situation | Action |
|-----------|--------|
| Fits existing guide scope | New `includes/NN-name.md` + README TOC row |
| Cross-cutting, 3+ guides reference it | Consider new top-level guide folder |
| Small cross-link only | Link from existing section; no new file |

Prefer expanding existing includes over new top-level folders.

## 2. Create the include file

- Path: `guide-name/includes/NN-kebab-case.md`
- Sub-articles: `NNA-kebab-case.md` (uppercase letter after number)
- Complete content only — no `TODO` placeholders
- Follow [CONTRIBUTING.md](../../../CONTRIBUTING.md) style (At a glance, Related, Scope, mermaid, Common mistakes)

## 3. Update guide README

Add a row under `## Table of contents` matching existing guide READMEs — link target pattern: `includes/NN-slug.md`.

Rules:

- Two-column table only (`| # | Topic |`)
- Every file in `includes/` must have a TOC row
- Sub-articles: label like `10a` under parent `10`

## 4. Cross-links and index

- Add contextual links from related sections (correct `../` vs `../../`)
- Update root [README.md](../../../README.md) if adding a new top-level guide or learning path
- Update [CHANGELOG.md](../../../CHANGELOG.md) for notable additions

## 5. Acronyms and formatting

```bash
python3 scripts/expand-acronyms.py
python3 scripts/github-format.py   # after bulk TOC edits
make check
```

## 6. See also

- End guide README with `## See also` sibling table if new guide
- Mid-chapter links use `## Other guides in this repo`
