# Bugbot rules — Engineering Guides (`documents/`)

This repo is **markdown documentation**, not application code. Review for **navigation integrity**, **convention drift**, and **incomplete content** — not runtime bugs.

## Flag as blocking

- `make validate` or `make check` would fail (run mentally against changed files):
  - Broken relative links or missing `#heading` anchors
  - Guide README TOC missing a new `includes/*.md` or referencing a deleted file
  - TOC table not two columns (`| # | Topic |`)
  - Cross-link paths wrong (`../` from README, `../../` from includes)
- New `TODO`, `FIXME`, or placeholder sections shipped as content
- New top-level guide added without root [README.md](../README.md) index update
- Acronym format wrong on first use: must be `ACRONYM(Full Text)` with no space before `(`
- Acronym expansions inside `#` headings
- Include file naming violates `NN-kebab-case.md` or sub-article `NNA-` pattern

## Flag as should-fix (non-blocking)

- Missing `## See also` on a new or heavily edited guide README
- Capstone/overview section missing `> **Related:**` links when sibling guides exist
- Overlapping sibling topic without `> **Scope:**` clarification
- Duplicate full sibling guide table mid-document (should use `## Other guides in this repo`)
- CHANGELOG not updated for notable section additions or renames

## Do not flag

- Prose style preferences (tone, paragraph length) when conventions are met
- Missing mermaid diagrams unless the section claims a flow without any structure
- Suggesting code changes in other repos — these guides link out by design
- Nitpicks on acronym choice when [acronyms.json](../acronyms.json) and inline format are correct

## Validation reference

CI runs the same checks as:

```bash
make check
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full conventions.
