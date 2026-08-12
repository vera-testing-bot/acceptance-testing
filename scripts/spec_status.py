#!/usr/bin/env python3
"""Machine-readable spec parser for compliance checks.

Reads ``docs/spec/*.md`` and emits one record per ``<!-- slug: ... -->``
criterion. Section-level status is derived from the heading prefix:

* ``#### ✅`` -> complete
* ``#### 🚧`` -> not_started

A ``--json`` flag outputs a JSON object with a ``records`` array suitable for
the Vera spec-compliance gate.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SLUG_RE = re.compile(r"<!--\s*slug:\s*([\w.-]+)\s*-->")
SECTION_RE = re.compile(r"^####\s+([✅🚧])\s*(.+)$")
DONE_WHEN_RE = re.compile(r"^\s*[*\-]\s+(?:`[^`]+`\s+)?(.+)\s+<!--")


def _status_for_marker(marker: str) -> str:
    if marker == "✅":
        return "complete"
    if marker == "🚧":
        return "not_started"
    return "not_started"


def parse_spec_file(path: Path) -> list[dict]:
    records: list[dict] = []
    spec_title = ""
    section_status = "not_started"
    section_title = ""

    for raw_line in path.read_text().splitlines():
        line = raw_line.rstrip("\n")
        if line.startswith("# "):
            spec_title = line[2:].strip()
            continue
        section_match = SECTION_RE.match(line)
        if section_match:
            section_status = _status_for_marker(section_match.group(1))
            section_title = section_match.group(2).strip()
            continue
        slug_match = SLUG_RE.search(line)
        if not slug_match:
            continue
        # Ignore lines that look like plain prose before "Done when:" bullets;
        # require a bullet marker so narrative text with a slug does not count.
        if not (line.strip().startswith("-") or line.strip().startswith("*")):
            continue
        records.append(
            {
                "spec": spec_title,
                "section": section_title,
                "slug": slug_match.group(1),
                "status": section_status,
                "source": str(path),
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse spec files and emit a machine-readable status report."
    )
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=Path("docs/spec"),
        help="Directory containing Markdown spec files (default: docs/spec).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output instead of a plain text table.",
    )
    args = parser.parse_args()

    records: list[dict] = []
    if args.spec_dir.is_dir():
        for spec_file in sorted(args.spec_dir.glob("*.md")):
            records.extend(parse_spec_file(spec_file))

    if args.json:
        print(json.dumps({"records": records}, indent=2))
    else:
        status_width = max((len(r["status"]) for r in records), default=0)
        for r in records:
            print(f"{r['status']:<{status_width}}  {r['slug']}  ({r['spec']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
