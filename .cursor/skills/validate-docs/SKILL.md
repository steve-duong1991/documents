---
name: validate-docs
description: Run Engineering Guides validation (links, anchors, README TOC sync, prose lint, acronyms). Use after editing markdown, before finishing doc work, or when the user asks to validate the repo.
---

# Validate Engineering Guides

Run from the `documents/` repo root (where `Makefile` lives).

## Standard validation

```bash
make validate
```

Runs:

| Script | Checks |
|--------|--------|
| `scripts/validate-doc-links.py` | File paths and `#heading` anchors |
| `scripts/validate-doc-readme.py` | Every `includes/*.md` listed in guide README TOC |
| `scripts/validate-doc-prose.py` | Corrupted prose (stripped links, empty placeholders) |

## Full check (CI-equivalent)

```bash
make check
```

Adds `python3 scripts/expand-acronyms.py --check` for acronym drift.

## Optional external URL check (slow)

```bash
make validate-external
```

## After bulk TOC or GLOSSARY edits

```bash
make github-format
make check
```

## When validation fails

1. Read stderr output — each line names file and issue
2. **README TOC mismatch**: add/remove TOC row or fix stale `includes/...` link
3. **Broken anchor**: match heading slug in target file
4. **Prose lint**: usually missing link text after acronym or formatting runs
5. **Acronym check**: run `python3 scripts/expand-acronyms.py` then re-check

Fix issues and re-run until `make check` passes.
