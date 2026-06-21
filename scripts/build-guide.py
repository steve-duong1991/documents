#!/usr/bin/env python3
"""Rebuild GUIDE.md from includes/*.md for one or all guides."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADER_TITLES = {
    "api-design-and-protection": "API Design & Protection Guide",
    "api-rate-limiting": "API Rate Limiting Guide",
    "database-connection-and-security": "Database Connection & Security",
    "deployment-strategies": "Deployment Strategies Guide",
    "event-sourcing-and-cqrs": "Event Sourcing & CQRS Guide",
    "high-throughput-systems": "High Throughput Systems Guide",
    "postgresql-performance": "PostgreSQL Performance Guide",
    "tree-and-index-structures": "Trees and Index Structures Guide",
}


def extract_see_also(readme: Path) -> str:
    text = readme.read_text(encoding="utf-8")
    m = re.search(r"(---\s*\n\s*## See also\s*\n[\s\S]*)$", text)
    return m.group(1).strip() if m else ""


def rewrite_links_for_guide(text: str) -> str:
    """includes/ use ../../sibling — GUIDE.md at guide root needs ../sibling."""
    return re.sub(
        r"\]\(\.\./\.\./([a-z0-9-]+)/",
        r"](../\1/",
        text,
    )


def demote_headings(text: str) -> str:
    """Demote each heading one level so stitched sections nest under GUIDE title."""
    lines: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s", line)
        if m and len(m.group(1)) < 6:
            lines.append("#" + line)
        else:
            lines.append(line)
    return "\n".join(lines)


def build_guide(guide_dir: Path) -> None:
    name = guide_dir.name
    includes = sorted((guide_dir / "includes").glob("*.md"))
    if not includes:
        print(f"skip {name}: no includes", file=sys.stderr)
        return

    title = HEADER_TITLES.get(name, name.replace("-", " ").title())
    parts = [
        f"# {title} (Full)",
        "",
        "> Combined view of all sections. Modular sources live in `includes/`.",
        "> On GitHub, use the guide **README** table of contents for direct section links.",
        "",
        "---",
        "",
    ]
    for inc in includes:
        body = demote_headings(
            rewrite_links_for_guide(inc.read_text(encoding="utf-8").rstrip())
        )
        parts.append(body)
        parts.extend(["", "---", ""])

    see_also = extract_see_also(guide_dir / "README.md")
    if see_also:
        parts.extend(["", see_also, ""])

    out = guide_dir / "GUIDE.md"
    out.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"built {out.relative_to(ROOT)} ({len(includes)} sections)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild GUIDE.md from includes")
    parser.add_argument(
        "guides",
        nargs="*",
        help="Guide folder names (default: all with includes/)",
    )
    args = parser.parse_args()

    if args.guides:
        dirs = [ROOT / g for g in args.guides]
    else:
        dirs = sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "includes").is_dir())

    for d in dirs:
        if not d.is_dir():
            print(f"unknown guide: {d}", file=sys.stderr)
            return 1
        build_guide(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
