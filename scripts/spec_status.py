#!/usr/bin/env python3
"""Machine-readable parser for docs/spec Markdown files.

Emits a JSON array describing every "Done when:" criterion found in the
repository's spec files. Each record includes the spec file, section/feature,
criterion text, slug, and completion status.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


# Match a bold "Done when:" line (e.g. "**Done when:**").
DONE_WHEN_RE = re.compile(r"^\*\*done when:\*\*$", re.IGNORECASE)

# Match a Markdown checkbox bullet, capturing the checkbox contents and text.
CHECKBOX_RE = re.compile(r"^\s*-\s*\[([^\]]*)\]\s+(.+)$")

# Match a plain Markdown bullet that may also be used for criteria.
PLAIN_BULLET_RE = re.compile(r"^\s*-\s+(.+)$")

# Extract the slug from an inline HTML comment.
SLUG_RE = re.compile(r"<!--\s*slug:\s*([\w.-]+)\s*-->")

# A spec feature section header uses an emoji status marker.
SECTION_HEADER_RE = re.compile(r"^####\s+([🚧✅])\s+(.+?)\s*$")

STATUS_EMOJI_MAP = {
    "🚧": "planned",
    "✅": "complete",
}


def _checkbox_state_to_status(state: str) -> str:
    state = state.strip()
    if state.lower() in {"x", "X"}:
        return "complete"
    if state.startswith("#"):
        return "in_progress"
    return "planned"


def _clean_criterion_text(text: str) -> str:
    # Strip trailing inline slug comments and surrounding whitespace.
    text = SLUG_RE.sub("", text)
    return text.strip(" \t")


def parse_spec_file(spec_path: Path) -> list[dict[str, object]]:
    """Parse a single spec Markdown file into criterion records."""
    text = spec_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    spec_title = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            spec_title = stripped[2:].strip()
            break

    records: list[dict[str, object]] = []
    current_section = ""
    current_feature = ""
    feature_status = ""
    in_done_when = False

    for line in lines:
        stripped = line.strip()

        # Track section headers (e.g., "## Arithmetic").
        if stripped.startswith("## ") and not stripped.startswith("### "):
            current_section = stripped[3:].strip()
            continue

        # Track feature headers (e.g., "#### ✅ Power/Exponentiation").
        section_match = SECTION_HEADER_RE.match(stripped)
        if section_match:
            emoji, name = section_match.groups()
            current_feature = name.strip()
            feature_status = STATUS_EMOJI_MAP.get(emoji, "planned")
            in_done_when = False
            continue

        # Enter the "Done when:" block for the current feature.
        if DONE_WHEN_RE.match(stripped):
            in_done_when = True
            continue

        if in_done_when:
            checkbox_match = CHECKBOX_RE.match(line)
            plain_match = PLAIN_BULLET_RE.match(line) if not checkbox_match else None
            line_match = checkbox_match or plain_match

            if not line_match:
                # A blank line or non-list item ends the criteria block.
                if stripped:
                    in_done_when = False
                continue

            if checkbox_match:
                checkbox_state, rest = checkbox_match.groups()
                status = _checkbox_state_to_status(checkbox_state)
            else:
                rest = plain_match.group(1)
                # Inherit status from the feature-level emoji marker.
                status = feature_status

            slug_match = SLUG_RE.search(rest)
            if not slug_match:
                continue

            criterion_text = _clean_criterion_text(rest)
            records.append(
                {
                    "file": str(spec_path),
                    "spec_title": spec_title,
                    "section": current_section,
                    "feature": current_feature,
                    "criterion": criterion_text,
                    "slug": slug_match.group(1),
                    "status": status,
                    "feature_status": feature_status,
                }
            )


    return records


def collect_spec_records(spec_dir: Path) -> list[dict[str, object]]:
    """Collect criterion records from every Markdown file in *spec_dir*."""
    records: list[dict[str, object]] = []
    if not spec_dir.exists():
        return records
    for spec_path in sorted(spec_dir.glob("*.md")):
        records.extend(parse_spec_file(spec_path))
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse docs/spec Markdown files into a JSON record set."
    )
    parser.add_argument(
        "--spec-dir",
        type=Path,
        default=Path("docs/spec"),
        help="Directory containing spec Markdown files (default: docs/spec)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output records as JSON",
    )
    args = parser.parse_args(argv)

    records = collect_spec_records(args.spec_dir)

    if args.json:
        print(json.dumps(records, indent=2))
    else:
        for record in records:
            status_marker = "✅" if record["status"] == "complete" else "🚧"
            print(f"{status_marker} {record['slug']}: {record['criterion']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
