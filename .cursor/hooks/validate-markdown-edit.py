#!/usr/bin/env python3
"""After markdown edits, run make validate and surface results to the agent."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def edited_markdown_path(payload: dict) -> Path | None:
    candidates: list[str | None] = [
        payload.get("file_path"),
        payload.get("filePath"),
        payload.get("path"),
    ]
    tool_input = payload.get("tool_input") or {}
    if isinstance(tool_input, dict):
        candidates.extend(
            [
                tool_input.get("file_path"),
                tool_input.get("filePath"),
                tool_input.get("path"),
            ]
        )
    for raw in candidates:
        if not raw:
            continue
        path = Path(raw)
        if path.suffix != ".md":
            continue
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            continue
        return path
    return None


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0

    if edited_markdown_path(payload) is None:
        return 0

    result = subprocess.run(
        ["make", "validate"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=90,
    )
    if result.returncode == 0:
        print(
            json.dumps(
                {
                    "additional_context": (
                        "Engineering Guides validation passed (`make validate`) "
                        "after the markdown edit."
                    )
                }
            )
        )
        return 0

    output = (result.stderr or result.stdout).strip()
    if len(output) > 4000:
        output = output[:4000] + "\n… (truncated)"

    print(
        json.dumps(
            {
                "additional_context": (
                    "Engineering Guides validation failed after the markdown edit. "
                    "Fix these issues before finishing:\n\n"
                    f"```\n{output}\n```"
                )
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
