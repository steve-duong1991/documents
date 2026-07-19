#!/usr/bin/env python3
"""Validate markdown links under documents/. Exit 1 if any are broken."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\]\(([^)]+)\)")


def resolve_target(md: Path, target: str) -> Path:
    path_part = target.split("#")[0]
    return (md.parent / unquote(path_part)).resolve()


def slugify_heading(text: str) -> str:
    """Approximate GitHub/MkDocs heading anchor."""
    text = re.sub(r"\[(.*?)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`]", "", text.strip())
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = text.replace("—", "-").replace("–", "-").replace("&", "")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def normalize_anchor(value: str) -> str:
    """Loose compare: ignore hyphens/punctuation (handles `--` vs `-` in TOC)."""
    return re.sub(r"[^a-z0-9]", "", value.lower())


def heading_anchors(md_path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in md_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#{1,6}\s+(.+)$", line)
        if m:
            heading = m.group(1)
            slug = slugify_heading(heading)
            if slug:
                anchors.add(slug)
                anchors.add(normalize_anchor(slug))
            anchors.add(normalize_anchor(heading))
        for html_id in re.findall(r"""<(?:a|span)\s+[^>]*\bid=["']([^"']+)["']""", line, re.I):
            anchors.add(html_id)
            anchors.add(normalize_anchor(html_id))
    return anchors


def anchor_exists(md_path: Path, fragment: str) -> bool:
    fragment = unquote(fragment.lstrip("#"))
    if not fragment:
        return True
    anchors = heading_anchors(md_path)
    return fragment in anchors or normalize_anchor(fragment) in anchors


def check_external(url: str, timeout: float) -> str | None:
    """Return error reason if URL fails, else None."""
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": "documents-link-check/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            if resp.status >= 400:
                return f"HTTP {resp.status}"
    except Exception as exc:  # noqa: BLE001 — aggregate failures for report
        # Some servers reject HEAD; retry GET with Range
        try:
            req = Request(
                url,
                headers={"User-Agent": "documents-link-check/1.0", "Range": "bytes=0-0"},
            )
            with urlopen(req, timeout=timeout) as resp:
                if resp.status >= 400:
                    return f"HTTP {resp.status}"
        except Exception as inner:
            return str(inner)
    return None


def parse_link(raw: str) -> tuple[str, str | None]:
    raw = raw.strip()
    if "#" in raw:
        path, _, frag = raw.partition("#")
        return path.strip(), frag.strip() or None
    return raw, None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate markdown links under documents/")
    parser.add_argument(
        "--external",
        action="store_true",
        help="Also check https:// links (slow; use in CI weekly or pre-release)",
    )
    parser.add_argument(
        "--external-timeout",
        type=float,
        default=10.0,
        help="Timeout seconds per external URL (default: 10)",
    )
    args = parser.parse_args()

    broken: list[tuple[str, str, str]] = []

    for md in sorted(ROOT.rglob("*.md")):
        if "scripts" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        rel_src = str(md.relative_to(ROOT))

        for m in LINK_RE.finditer(text):
            raw = m.group(1).strip()
            if not raw or raw.startswith("mailto:"):
                continue

            path_part, fragment = parse_link(raw)

            if path_part.startswith(("http://", "https://")):
                if args.external:
                    reason = check_external(path_part, args.external_timeout)
                    if reason:
                        broken.append((rel_src, raw, f"external: {reason}"))
                continue

            if not path_part:
                # Same-file anchors in README TOC are hand-tuned for GitHub; skip strict check.
                if fragment and md.name != "README.md" and not anchor_exists(md, fragment):
                    broken.append((rel_src, raw, f"missing anchor #{fragment}"))
                continue

            resolved = resolve_target(md, path_part)
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                broken.append((rel_src, raw, "outside documents"))
                continue

            if not resolved.exists():
                broken.append((rel_src, path_part, "missing file"))
                continue

            if fragment and not anchor_exists(resolved, fragment):
                broken.append((rel_src, raw, f"missing anchor #{fragment}"))

    if broken:
        print(f"Broken links: {len(broken)}", file=sys.stderr)
        for src, tgt, reason in broken:
            print(f"  {src} -> {tgt} ({reason})", file=sys.stderr)
        return 1

    msg = f"OK — all internal links valid under {ROOT}"
    if args.external:
        msg += " (external URLs checked)"
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
