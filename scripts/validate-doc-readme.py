#!/usr/bin/env python3
"""Ensure each guide README.md lists every includes/*.md file (and vice versa)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE_RE = re.compile(r"\]\((includes/\d{2}[A-Z]?-[a-z0-9-]+\.md)\)")
TOC_HEADER_RE = re.compile(r"^\| # \| (?:Topic|Strategy|Section) \|$")
TOC_ROW_RE = re.compile(r"^\| (?:—|\d+) \| .+ \|$")


def table_column_count(line: str) -> int:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return 0
    return stripped.count("|") - 1


def validate_toc_table(readme_text: str, guide_name: str) -> list[str]:
    errors: list[str] = []
    in_toc = False
    expected_cols: int | None = None

    for lineno, line in enumerate(readme_text.splitlines(), start=1):
        if line.strip() == "## Table of contents":
            in_toc = True
            expected_cols = None
            continue
        if not in_toc:
            continue
        if not line.strip():
            continue
        if line.startswith(">") or line.startswith("---"):
            in_toc = False
            expected_cols = None
            continue
        if not line.strip().startswith("|"):
            in_toc = False
            expected_cols = None
            continue

        cols = table_column_count(line)
        if TOC_HEADER_RE.match(line):
            expected_cols = cols
            if cols != 2:
                errors.append(
                    f"{guide_name}/README.md:{lineno}: TOC header must be 2 columns, got {cols}"
                )
            continue
        if expected_cols is None:
            continue
        if cols != expected_cols:
            errors.append(
                f"{guide_name}/README.md:{lineno}: TOC row has {cols} columns, expected {expected_cols}"
            )

    return errors


def guide_dirs() -> list[Path]:
    return sorted(
        p for p in ROOT.iterdir() if p.is_dir() and (p / "includes").is_dir()
    )


def includes_on_disk(guide: Path) -> set[str]:
    return {f.name for f in sorted((guide / "includes").glob("*.md"))}


def includes_in_readme(readme: Path) -> set[str]:
    return {Path(m).name for m in INCLUDE_RE.findall(readme.read_text(encoding="utf-8"))}


def main() -> int:
    errors: list[str] = []

    for guide in guide_dirs():
        readme = guide / "README.md"
        if not readme.exists():
            errors.append(f"{guide.name}: missing README.md")
            continue

        disk = includes_on_disk(guide)
        listed = includes_in_readme(readme)
        missing_from_readme = sorted(disk - listed)
        stale_in_readme = sorted(listed - disk)

        for name in missing_from_readme:
            errors.append(
                f"{guide.name}/README.md: include not in TOC — includes/{name}"
            )
        for name in stale_in_readme:
            errors.append(
                f"{guide.name}/README.md: TOC references missing file — includes/{name}"
            )

        readme_text = readme.read_text(encoding="utf-8")
        errors.extend(validate_toc_table(readme_text, guide.name))

    if errors:
        print(f"README/include mismatches: {len(errors)}", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"OK — README TOC matches includes for {len(guide_dirs())} guides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
