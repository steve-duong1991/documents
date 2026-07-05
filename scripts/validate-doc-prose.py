#!/usr/bin/env python3
"""Flag likely corrupted prose in markdown (e.g. stripped links after expand-acronyms)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Corpus files at documents/ root (not per-guide README/GUIDE).
ROOT_MARKDOWN = {
    "README.md",
    "GLOSSARY.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "RUNBOOK-TEMPLATE.md",
    "RUNBOOK-EXAMPLE-orders-api.md",
}

# (compiled regex, human-readable label)
PROSE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"—\s+\.\s*$"), "em dash then '.' (missing link)"),
    (re.compile(r"→\s+\.\s*$"), "arrow then '.' (missing link)"),
    (re.compile(r"\bSee\s{2,}for\b"), "See  for (missing link)"),
    (re.compile(r"\bPair with\s+\."), "Pair with . (missing link)"),
    (re.compile(r"\bPair with\s{2,}for\b"), "Pair with  for (missing link)"),
    (re.compile(r"\(\s+\+"), "( + (missing word before +)"),
    (re.compile(r"\(e\.g\.\s*\)"), "(e.g. ) (missing inline example)"),
    (re.compile(r"\bAlert\s+:"), "Alert : (missing alert name)"),
    (re.compile(r"\|\s*,\s*\|"), "table cell with only comma (stripped inline code?)"),
]


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for name in sorted(ROOT_MARKDOWN):
        path = ROOT / name
        if path.is_file():
            files.append(path)
    for guide in sorted(ROOT.iterdir()):
        if not guide.is_dir() or guide.name.startswith("."):
            continue
        readme = guide / "README.md"
        if readme.is_file():
            files.append(readme)
        includes = guide / "includes"
        if includes.is_dir():
            files.extend(sorted(includes.glob("*.md")))
    return files


def strip_fenced_code(text: str) -> str:
    """Remove fenced code blocks so patterns don't match examples inside them."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def check_file(path: Path) -> list[tuple[int, str, str]]:
    raw = path.read_text(encoding="utf-8")
    body = strip_fenced_code(raw)
    issues: list[tuple[int, str, str]] = []
    for line_no, line in enumerate(body.splitlines(), start=1):
        for pattern, label in PROSE_PATTERNS:
            if pattern.search(line):
                issues.append((line_no, label, line.strip()))
    return issues


def main() -> int:
    all_issues: list[tuple[Path, int, str, str]] = []
    for path in iter_markdown_files():
        for line_no, label, snippet in check_file(path):
            all_issues.append((path, line_no, label, snippet))

    if not all_issues:
        print("validate-doc-prose: OK")
        return 0

    print("validate-doc-prose: suspicious prose patterns found:\n")
    for path, line_no, label, snippet in all_issues:
        rel = path.relative_to(ROOT)
        print(f"  {rel}:{line_no} — {label}")
        print(f"    {snippet[:120]}{'…' if len(snippet) > 120 else ''}")
    print(f"\n{len(all_issues)} issue(s). Fix stripped links/text or adjust patterns.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
