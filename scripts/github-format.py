#!/usr/bin/env python3
"""Prepare markdown for GitHub reading: clean headings, README TOC links, GLOSSARY links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACRONYMS_PATH = ROOT / "acronyms.json"

TARGET_GLOBS = [
    "**/includes/*.md",
    "**/README.md",
    "README.md",
    "GLOSSARY.md",
    "RUNBOOK-TEMPLATE.md",
    "RUNBOOK-EXAMPLE-orders-api.md",
]

SKIP_NAMES = {"CHANGELOG.md"}

GUIDE_ALIASES = {
    "pg": "postgresql-performance",
    "hts": "high-throughput-systems",
    "es": "event-sourcing-and-cqrs",
    "api-design": "api-design-and-protection",
    "deployment": "deployment-strategies",
    "tree": "tree-and-index-structures",
    "database-connection": "database-connection-and-security",
    "api-rate-limiting": "api-rate-limiting",
}

TOC_HEADER_RE = re.compile(r"^(\| # \| (?:Topic|Strategy|Section) \|) Include file \|$")
TOC_ROW_RE = re.compile(
    r"^(\| (?:—|\d+) \|) \[([^\]]+)\]\(#[^)]*\) \| \[(includes/[^\]]+)\]\(\3\) \|$"
)

SEE_ALSO_PART_RE = re.compile(
    r"^(?:(?P<alias>PG|HTS|ES|api-design|deployment|tree|database-connection|api-rate-limiting)"
    r"|(?P<guide>[a-z0-9-]+))"
    r"(?:\s*§(?P<section>\d+))?$",
    re.I,
)


def load_acronyms() -> list[str]:
    data = json.loads(ACRONYMS_PATH.read_text(encoding="utf-8"))
    return sorted(data.keys(), key=len, reverse=True)


def build_section_maps() -> dict[str, dict[int, str]]:
    maps: dict[str, dict[int, str]] = {}
    for guide in ROOT.iterdir():
        inc = guide / "includes"
        if not guide.is_dir() or not inc.is_dir():
            continue
        section_map: dict[int, str] = {}
        for path in sorted(inc.glob("*.md")):
            m = re.match(r"(\d+)-", path.name)
            if m:
                section_map[int(m.group(1))] = f"{guide.name}/includes/{path.name}"
        maps[guide.name] = section_map
    return maps


def resolve_guide(name: str) -> str | None:
    lower = name.lower()
    if lower in GUIDE_ALIASES:
        return GUIDE_ALIASES[lower]
    if (ROOT / name).is_dir() and (ROOT / name / "includes").is_dir():
        return name
    return None


def link_see_also_cell(cell: str, section_maps: dict[str, dict[int, str]]) -> str:
    if "[" in cell and "](" in cell:
        return cell

    parts = re.split(r"\s*,\s*|\s*·\s*", cell)
    linked: list[str] = []
    current_guide: str | None = None

    for raw in parts:
        part = raw.strip()
        if not part:
            continue

        sec_only = re.match(r"^§(?P<section>\d+)$", part)
        if sec_only and current_guide:
            sec_num = int(sec_only.group("section"))
            rel = section_maps.get(current_guide, {}).get(sec_num)
            label = f"§{sec_only.group('section')}"
            if rel:
                linked.append(f"[{label}]({rel})")
            else:
                linked.append(f"[{label}]({current_guide}/README.md)")
            continue

        m = SEE_ALSO_PART_RE.match(part)
        if not m:
            linked.append(part)
            continue

        alias = m.group("alias")
        guide_name = m.group("guide")
        section = m.group("section")

        if alias:
            guide = resolve_guide(alias)
            label = alias if alias != guide else guide_name or alias
        elif guide_name:
            guide = resolve_guide(guide_name)
            label = guide_name
        else:
            linked.append(part)
            continue

        if not guide:
            linked.append(part)
            continue

        current_guide = guide
        if section:
            sec_num = int(section)
            rel = section_maps.get(guide, {}).get(sec_num)
            if rel:
                linked.append(f"[{label} §{section}]({rel})")
            else:
                linked.append(f"[{label} §{section}]({guide}/README.md)")
        else:
            linked.append(f"[{label}]({guide}/README.md)")

    return ", ".join(linked)


def clean_heading_line(line: str, acronyms: list[str]) -> str:
    if not re.match(r"^#{1,6}\s", line):
        return line
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(a) for a in acronyms) + r")\([^)]*\)"
    )
    return pattern.sub(r"\1", line)


def clean_headings_in_text(text: str, acronyms: list[str]) -> str:
    return "\n".join(clean_heading_line(line, acronyms) for line in text.splitlines())


def fix_readme_toc(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if TOC_HEADER_RE.match(line):
            lines.append(TOC_HEADER_RE.sub(r"\1", line))
            continue
        if re.match(r"^\|---\|[-]+\|[-]+\|$", line):
            lines.append("|---|-------|")
            continue
        m = TOC_ROW_RE.match(line)
        if m:
            lines.append(f"{m.group(1)} [{m.group(2)}]({m.group(3)}) |")
            continue
        if line.startswith("> **On GitHub:** Click a topic"):
            lines.append("> **On GitHub:** Click a topic in the table above for the full section.")
            continue
        lines.append(line)
    return "\n".join(lines)


def link_glossary(text: str, section_maps: dict[str, dict[int, str]]) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if not line.startswith("| **") or line.count("|") < 4:
            lines.append(line)
            continue
        parts = line.split("|")
        if len(parts) < 5:
            lines.append(line)
            continue
        see_also = parts[3].strip()
        if see_also and not (see_also.startswith("[") and "](" in see_also):
            parts[3] = " " + link_see_also_cell(see_also, section_maps) + " "
        lines.append("|".join(parts))
    return "\n".join(lines)


def iter_target_files() -> list[Path]:
    files: set[Path] = set()
    for glob in TARGET_GLOBS:
        for path in ROOT.glob(glob):
            if path.name in SKIP_NAMES:
                continue
            if "scripts" in path.parts and path.parent.name == "scripts":
                continue
            files.add(path.resolve())
    return sorted(files)


def process_file(path: Path, acronyms: list[str], section_maps: dict[str, dict[int, str]]) -> bool:
    original = path.read_text(encoding="utf-8")
    text = clean_headings_in_text(original, acronyms)
    if path.name == "README.md":
        text = fix_readme_toc(text)
    if path.name == "GLOSSARY.md":
        text = link_glossary(text, section_maps)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    if not ACRONYMS_PATH.exists():
        print(f"Missing {ACRONYMS_PATH}", file=sys.stderr)
        return 1

    acronyms = load_acronyms()
    section_maps = build_section_maps()
    changed: list[Path] = []

    for path in iter_target_files():
        if process_file(path, acronyms, section_maps):
            changed.append(path)

    if changed:
        print(f"github-format: updated {len(changed)} file(s)")
        for p in changed:
            print(f"  {p.relative_to(ROOT)}")
    else:
        print("github-format: OK (no changes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
