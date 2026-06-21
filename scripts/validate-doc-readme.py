#!/usr/bin/env python3
"""Ensure each guide README.md lists every includes/*.md file (and vice versa)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE_RE = re.compile(r"\]\((includes/\d{2}-[a-z0-9-]+\.md)\)")


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

        # Each include should have a "See full details" link (except 00-overview optional)
        readme_text = readme.read_text(encoding="utf-8")
        for name in disk:
            if name == "00-overview.md":
                continue
            if f"includes/{name}" not in readme_text:
                errors.append(
                    f"{guide.name}/README.md: no link to includes/{name} in body"
                )

    if errors:
        print(f"README/include mismatches: {len(errors)}", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"OK — README TOC matches includes for {len(guide_dirs())} guides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
