#!/usr/bin/env python3
"""Expand acronyms on first occurrence per file: CDC(Change Data Capture)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACRONYMS_PATH = ROOT / "acronyms.json"

# Files to process (GUIDE.md is rebuilt from includes — do not edit directly)
TARGET_GLOBS = [
    "**/includes/*.md",
    "**/README.md",
    "README.md",
    "GLOSSARY.md",
    "RUNBOOK-TEMPLATE.md",
    "RUNBOOK-EXAMPLE-orders-api.md",
]

SKIP_NAMES = {"GUIDE.md", "CHANGELOG.md"}

FENCE_RE = re.compile(r"```[\w-]*\n.*?```", re.DOTALL)
LINK_RE = re.compile(r"(\[[^\]]*\]\([^)]*\))")
INLINE_CODE_RE = re.compile(r"(`[^`]+`)")
GUIDE_SHORTHAND = frozenset({"ES", "HTS", "PG"})


def load_acronyms() -> dict[str, str]:
    data = json.loads(ACRONYMS_PATH.read_text(encoding="utf-8"))
    return dict(sorted(data.items(), key=lambda kv: len(kv[0]), reverse=True))


def build_pattern(acronyms: dict[str, str]) -> re.Pattern[str]:
    parts = [re.escape(k) for k in acronyms]
    return re.compile(r"\b(" + "|".join(parts) + r")\b")


def expand_segment(text: str, pattern: re.Pattern[str], acronyms: dict[str, str], seen: set[str]) -> str:
    if not text:
        return text

    result: list[str] = []
    last = 0
    for match in pattern.finditer(text):
        start, end = match.start(), match.end()
        acronym = match.group(1)

        result.append(text[last:start])

        if acronym in seen:
            result.append(acronym)
            last = end
            continue

        # Skip shorthand in parentheses: (DLQ), (2PC), (API)
        before_stripped = text[:start].rstrip()
        if before_stripped.endswith("("):
            result.append(acronym)
            last = end
            continue

        after = text[end:]
        if after.startswith("(") or (len(after) > 1 and after[0] == " " and after[1] == "("):
            result.append(acronym)
            seen.add(acronym)
            last = end
            continue

        # Skip guide shorthand: ES §5, HTS §1, PG §13
        after_acronym = text[end:].lstrip()
        if acronym in GUIDE_SHORTHAND and after_acronym.startswith("§"):
            result.append(acronym)
            last = end
            continue

        expansion = acronyms[acronym]
        result.append(f"{acronym}({expansion})")
        seen.add(acronym)
        last = end

    result.append(text[last:])
    return "".join(result)


def expand_text(text: str, pattern: re.Pattern[str], acronyms: dict[str, str], seen: set[str]) -> str:
    out: list[str] = []
    pos = 0
    for fence in FENCE_RE.finditer(text):
        before = text[pos:fence.start()]
        out.append(expand_prose_block(before, pattern, acronyms, seen))
        out.append(fence.group(0))
        pos = fence.end()
    out.append(expand_prose_block(text[pos:], pattern, acronyms, seen))
    return "".join(out)


def expand_prose_block(text: str, pattern: re.Pattern[str], acronyms: dict[str, str], seen: set[str]) -> str:
    if not text:
        return text

    parts = LINK_RE.split(text)
    expanded_parts: list[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            expanded_parts.append(part)
            continue
        expanded_parts.append(expand_without_links(part, pattern, acronyms, seen))
    return "".join(expanded_parts)


def expand_without_links(text: str, pattern: re.Pattern[str], acronyms: dict[str, str], seen: set[str]) -> str:
    if not text:
        return text

    lines = text.split("\n")
    expanded_lines: list[str] = []
    for line in lines:
        if re.match(r"^\s*#{1,6}\s", line):
            for match in pattern.finditer(line):
                seen.add(match.group(1))
            expanded_lines.append(line)
            continue
        expanded_lines.append(expand_line_without_links(line, pattern, acronyms, seen))
    return "\n".join(expanded_lines)


def expand_line_without_links(
    text: str, pattern: re.Pattern[str], acronyms: dict[str, str], seen: set[str]
) -> str:
    if not text:
        return text

    parts = INLINE_CODE_RE.split(text)
    expanded_parts: list[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            expanded_parts.append(part)
            continue
        expanded_parts.append(expand_segment(part, pattern, acronyms, seen))
    return "".join(expanded_parts)


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


def process_file(path: Path, pattern: re.Pattern[str], acronyms: dict[str, str]) -> bool:
    original = path.read_text(encoding="utf-8")
    seen: set[str] = set()
    expanded = expand_text(original, pattern, acronyms, seen)
    if expanded != original:
        path.write_text(expanded, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand acronyms on first use per file.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any file would change (CI dry-run).",
    )
    args = parser.parse_args()

    if not ACRONYMS_PATH.exists():
        print(f"Missing {ACRONYMS_PATH}", file=sys.stderr)
        return 1

    acronyms = load_acronyms()
    pattern = build_pattern(acronyms)
    changed: list[Path] = []

    for path in iter_target_files():
        original = path.read_text(encoding="utf-8")
        seen: set[str] = set()
        expanded = expand_text(original, pattern, acronyms, seen)
        if expanded != original:
            changed.append(path)
            if not args.check:
                path.write_text(expanded, encoding="utf-8")

    if args.check and changed:
        print("Acronym expansions out of date — run: python3 scripts/expand-acronyms.py", file=sys.stderr)
        for p in changed:
            print(f"  {p.relative_to(ROOT)}", file=sys.stderr)
        return 1

    if not args.check and changed:
        print(f"Expanded acronyms in {len(changed)} file(s)")
        for p in changed:
            print(f"  {p.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
