#!/usr/bin/env python3
"""Validate the portable subset of an Agent Skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_skill.py <skill-directory>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    source = root / "SKILL.md"
    failures: list[str] = []
    if not source.is_file():
        failures.append("SKILL.md is missing")
    else:
        text = source.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
        if not match:
            failures.append("YAML frontmatter is missing")
        else:
            frontmatter = match.group(1)
            names = re.findall(r"^name:\s*([^\n]+)$", frontmatter, flags=re.MULTILINE)
            descriptions = re.findall(r"^description:\s*(.+)$", frontmatter, flags=re.MULTILINE)
            if names != [root.name]:
                failures.append(f"frontmatter name must be {root.name!r}")
            if len(descriptions) != 1 or not descriptions[0].strip():
                failures.append("frontmatter description is required")
        if "TODO" in text or "TBD" in text:
            failures.append("unfinished placeholder found")
    if failures:
        for failure in failures:
            print(f"FAIL {root}: {failure}")
        return 1
    print(f"PASS {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
