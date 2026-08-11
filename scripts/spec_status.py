#!/usr/bin/env python3
"""Machine-readable spec status parser for Vera spec compliance.

Scans `docs/spec/*.md` for "Done when:" criterion lines written with GitHub-style
checkboxes. Emits a JSON status report keyed by state.

States:
  - [ ]      -> not_started
  - [#NNN]  -> in_progress (linked to issue NNN)
  - [x]      -> complete
Each line must end with an inline slug comment: `<!-- slug: dotted.slug -->`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# Match lines like "- [x] description text <!-- slug: some.slug -->"
CRITERION_RE = re.compile(
    r"^\s*-\s*\[(?P<checkbox>[^\]]*)\]\s+"
    r"(?P<text>.*?)\s*"
    r"<!--\s*slug:\s*(?P<slug>[\w.-]+)\s*-->\s*$"
)


def parse_status(checkbox: str) -> tuple[str, int | None]:
    """Map a checkbox token into a state and optional in-progress issue number."""
    token = checkbox.strip()
    lowered = token.lower()

    if lowered == "x":
        return "complete", None

    if lowered.startswith("#"):
        digits = lowered.lstrip("#").strip() or None
        issue: int | None = int(digits) if digits and digits.isdigit() else None
        return "in_progress", issue

    return "not_started", None


def scan_spec_dir(spec_dir: Path) -> dict[str, list[dict]]:
    """Collect every criterion line from the spec directory."""
    status_groups: dict[str, list[dict]] = {
        "not_started": [],
        "in_progress": [],
        "complete": [],
    }

    if not spec_dir.exists():
        return status_groups

    for spec_file in sorted(spec_dir.glob("*.md")):
        in_code_block = False
        for line in spec_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            match = CRITERION_RE.match(line)
            if not match:
                continue

            status, issue = parse_status(match.group("checkbox"))
            item = {
                "slug": match.group("slug"),
                "text": match.group("text").strip(),
                "file": str(spec_file),
            }
            if issue is not None:
                item["issue"] = issue

            status_groups[status].append(item)

    return status_groups


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Emit a machine-readable spec status report."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of plain text.",
    )
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=Path("docs/spec"),
        help="Directory containing spec markdown files",
    )

    args = parser.parse_args(argv)
    report = scan_spec_dir(args.spec_dir)

    if args.json:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for state in ("complete", "in_progress", "not_started"):
            items = report[state]
            print(f"[{state}] {len(items)} item(s)")
            for item in items:
                suffix = f" (issue #{item['issue']})" if "issue" in item else ""
                print(f"  - {item['slug']}: {item['text']}{suffix}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
