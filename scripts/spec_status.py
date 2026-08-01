#!/usr/bin/env python3
"""Machine-readable spec parser for Vera spec-compliance audits.

Scans Markdown files under docs/spec, extracts "Done when:" criteria with
GitHub-style checkboxes and inline slug markers, and writes a JSON record set.

The parser recognizes the three-state checkbox convention used by Vera specs:

* ``- [ ]`` — not started
* ``- [#123]`` — in progress under GitHub issue #123
* ``- [x]`` — complete

Each criterion line is expected to carry an inline slug comment of the form
``<!-- slug: area.section.criterion -->``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SPEC_DIR = Path("docs/spec")

DONE_WHEN_RE = re.compile(r"^\s*\*\*Done when:\*\*\s*$")
CHECKBOX_RE = re.compile(r"^\s*-\s*\[([^\]]*)\]\s+(.*)$")
BULLET_RE = re.compile(r"^\s*-\s+(.*)$")
SLUG_RE = re.compile(r"<!--\s*slug:\s*([\w.-]+)\s*-->")
SECTION_STATUS_RE = re.compile(r"^####\s+([🚧✅])\s*(.*)$")
SECTION_TITLE_RE = re.compile(r"^####\s+(?:[🚧✅]\s+)?(.+?)\s*$")
ISSUE_REF_RE = re.compile(r"^#(\d+)$")


@dataclass(frozen=True)
class SpecCitation:
    spec_file: str
    spec_title: str
    section: str
    line: int
    status: str
    slug: str
    text: str
    issue_ref: str | None = None


def normalize_status(raw: str) -> tuple[str, str | None]:
    """Map a checkbox body to a Vera status and optional issue reference."""
    body = raw.strip().lower()
    if body in ("x", "✓", "done"):
        return "complete", None
    match = ISSUE_REF_RE.match(body)
    if match:
        return "in_progress", match.group(1)
    if body == "":
        return "not_started", None
    # Treat any other non-empty content as in-progress.
    return "in_progress", None


def parse_spec_file(path: Path) -> list[SpecCitation]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    spec_title = ""
    for line in lines:
        if line.startswith("# "):
            spec_title = line[2:].strip()
            break

    citations: list[SpecCitation] = []
    section = ""
    section_status = "not_started"
    in_done_when = False

    for lineno, line in enumerate(lines, start=1):
        title_match = SECTION_TITLE_RE.match(line)
        if title_match:
            section = title_match.group(1).strip()
            in_done_when = False

            status_match = SECTION_STATUS_RE.match(line)
            if status_match:
                emoji = status_match.group(1)
                section_status = "complete" if emoji == "✅" else "not_started"
            else:
                section_status = "not_started"
            continue

        if DONE_WHEN_RE.match(line):
            in_done_when = True
            continue

        if not in_done_when:
            continue

        # A blank line or new header ends the Done-when block.
        if not line.strip() or line.startswith("#"):
            in_done_when = False
            continue

        checkbox_match = CHECKBOX_RE.match(line)
        bullet_match = BULLET_RE.match(line)
        if not (checkbox_match or bullet_match):
            continue

        if checkbox_match:
            checkbox_body = checkbox_match.group(1)
            rest = checkbox_match.group(2)
            status, issue_ref = normalize_status(checkbox_body)
        else:
            rest = bullet_match.group(1)
            status = section_status
            issue_ref = None

        slug_match = SLUG_RE.search(rest)
        slug = slug_match.group(1).strip() if slug_match else ""
        text = SLUG_RE.sub("", rest).strip()
        text = text.rstrip(".").strip()

        citations.append(
            SpecCitation(
                spec_file=str(path),
                spec_title=spec_title,
                section=section,
                line=lineno,
                status=status,
                slug=slug,
                text=text,
                issue_ref=issue_ref,
            )
        )

    return citations


def collect_citations(spec_dir: Path) -> list[SpecCitation]:
    citations: list[SpecCitation] = []
    for path in sorted(spec_dir.rglob("*.md")):
        citations.extend(parse_spec_file(path))
    return citations


def build_report(citations: list[SpecCitation]) -> dict:
    by_status: dict[str, int] = {}
    for citation in citations:
        by_status[citation.status] = by_status.get(citation.status, 0) + 1

    spec_files = sorted({citation.spec_file for citation in citations})

    return {
        "citations": [asdict(citation) for citation in citations],
        "spec_files": spec_files,
        "summary": {
            "total": len(citations),
            "complete": by_status.get("complete", 0),
            "in_progress": by_status.get("in_progress", 0),
            "not_started": by_status.get("not_started", 0),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse Vera spec files into a machine-readable record set."
    )
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=Path("docs/spec"),
        help="Directory containing Markdown spec files (default: docs/spec)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Write the record set as JSON to stdout",
    )
    args = parser.parse_args(argv)

    spec_dir = args.spec_dir.resolve()
    if not spec_dir.exists():
        print(f"error: spec directory not found: {spec_dir}", file=sys.stderr)
        return 1

    citations = collect_citations(spec_dir)
    report = build_report(citations)

    if args.json:
        json.dump(report, sys.stdout, indent=2)
        print()
    else:
        for citation in citations:
            checkbox = {
                "complete": "[x]",
                "in_progress": "[#]",
                "not_started": "[ ]",
            }.get(citation.status, "[?]")
            print(
                f"{citation.spec_file}:{citation.line} {checkbox} "
                f"{citation.slug} — {citation.text}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
