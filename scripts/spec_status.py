#!/usr/bin/env python3
"""Machine-readable spec status parser for Vera spec compliance.

Scans ``docs/spec/*.md`` for "Done when:" criterion lines written with
GitHub-style checkboxes and emits a JSON array of ``SpecRecord`` objects.

States:
  - ``[ ]``       -> ``not_started``
  - ``[#NNN]``    -> ``in_progress`` (linked to issue NNN)
  - ``[x]``       -> ``complete``

Each line must end with an inline slug comment: ``<!-- slug: dotted.slug -->``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if __package__ is None:
    from spec_record import SpecRecord
else:
    from scripts.spec_record import SpecRecord


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
        if digits and digits.isdigit():
            issue = int(digits)
            if issue > 0:
                return "in_progress", issue

    return "not_started", None


def scan_spec_dir(spec_dir: Path) -> list[SpecRecord]:
    """Collect every criterion line from the spec directory into records."""
    records: list[SpecRecord] = []

    if not spec_dir.exists():
        return records

    repo_root = Path.cwd().resolve()
    for spec_file in sorted(spec_dir.glob("*.md")):
        in_code_block = False
        file_path = str(
            spec_file.resolve().relative_to(repo_root)
            if spec_file.is_absolute()
            else spec_file
        )
        for line_number, line in enumerate(
            spec_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
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
            records.append(
                SpecRecord(
                    slug=match.group("slug"),
                    text=match.group("text").strip(),
                    file=file_path,
                    state=status,
                    line=line_number,
                    issue=issue,
                )
            )

    return records


def group_records(
    records: list[SpecRecord],
) -> dict[str, list[SpecRecord]]:
    """Group records by state for plain-text rendering."""
    grouped: dict[str, list[SpecRecord]] = {
        "not_started": [],
        "in_progress": [],
        "complete": [],
    }
    for record in records:
        grouped[record.state].append(record)
    return grouped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Emit a machine-readable spec status report."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output a JSON array of line-greppable spec records.",
    )
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=Path("docs/spec"),
        help="Directory containing spec markdown files",
    )

    args = parser.parse_args(argv)
    records = scan_spec_dir(args.spec_dir)

    if args.json:
        json.dump([record.to_json() for record in records], sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        grouped = group_records(records)
        for state in ("complete", "in_progress", "not_started"):
            items = grouped[state]
            print(f"[{state}] {len(items)} item(s)")
            for item in items:
                suffix = f" (issue #{item.issue})" if item.issue is not None else ""
                print(f"  - {item.slug}: {item.text}{suffix}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
