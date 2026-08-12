#!/usr/bin/env python3
"""Machine-readable parser for docs/spec Markdown files.

Emits records in the contract Vera's spec-compliance audit expects (see
``scripts/spec_record.py`` in golem-works-ai/vera, issue #4028): a JSON array,
one compact record object per physical line, each record carrying exactly
``slug``, ``status``, ``issue_ref``, ``file``, ``line``.

This repo's spec format uses a feature-level emoji marker on a ``####``
heading (✅ done, 🚧 in progress) plus a ``**Done when:**`` block of bullets,
each bullet ending in a ``<!-- slug: ... -->`` comment. Bullets may also be
Markdown checkboxes (``- [x]``, ``- [#123]``, ``- [ ]``); when a bullet is a
checkbox its own state overrides the feature-level status.

This repo has no per-criterion issue links, so ``issue_ref`` is always
``None``. ``line`` is the 1-based line number of the bullet carrying the slug.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


# Match a bold "Done when:" line (e.g. "**Done when:**").
DONE_WHEN_RE = re.compile(r"^\*\*done when:\*\*$", re.IGNORECASE)

# Match a Markdown checkbox bullet, capturing the checkbox contents and text.
CHECKBOX_RE = re.compile(r"^\s*-\s*\[([^\]]*)\]\s+(.*)$")

# Match a plain Markdown bullet that may also be used for criteria.
PLAIN_BULLET_RE = re.compile(r"^\s*-\s+(.*)$")

# Extract the slug from an inline HTML comment.
SLUG_RE = re.compile(r"<!--\s*slug:\s*([\w.-]+)\s*-->")

# A spec feature section header uses an emoji status marker, e.g.
# "#### ✅ Power/Exponentiation" or "#### 🚧 Sine".
SECTION_HEADER_RE = re.compile(r"^####\s+([🚧✅])\s+(.+?)\s*$")

# Feature-level emoji -> status. ✅ is done; 🚧 marks the feature as actively
# under construction, i.e. in_progress. Anything else (no marker at all)
# defaults to pending.
FEATURE_STATUS_EMOJI_MAP = {
    "✅": "done",
    "🚧": "in_progress",
}

# Valid record statuses (see vera's scripts/spec_record.py STATUSES).
STATUSES = ("pending", "in_progress", "done")


def _checkbox_state_to_status(state: str) -> str:
    """Map a checkbox's inner text to a status.

    ``[x]``/``[X]`` is done. A state starting with ``#`` (e.g. ``[#123]``,
    the "explicit in-progress marker" convention) is in_progress. Anything
    else (empty, whitespace) is pending.
    """
    state = state.strip()
    if state.lower() == "x":
        return "done"
    if state.startswith("#"):
        return "in_progress"
    return "pending"


def parse_spec_file(spec_path: Path) -> list[dict[str, object]]:
    """Parse a single spec Markdown file into criterion records.

    Records carry exactly the fields the record contract requires:
    ``slug``, ``status``, ``issue_ref`` (always ``None`` — this spec has no
    per-criterion issue links), ``file`` (the path as given, so callers that
    pass a repo-root-relative ``--spec-dir`` get a repo-root-relative,
    ``/``-containing path), and ``line`` (1-based).
    """
    lines = spec_path.read_text(encoding="utf-8").splitlines()

    records: list[dict[str, object]] = []
    feature_status = "pending"
    in_done_when = False

    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Track feature headers (e.g., "#### ✅ Power/Exponentiation").
        section_match = SECTION_HEADER_RE.match(stripped)
        if section_match:
            emoji, _name = section_match.groups()
            feature_status = FEATURE_STATUS_EMOJI_MAP.get(emoji, "pending")
            in_done_when = False
            continue

        # Enter the "Done when:" block for the current feature.
        if DONE_WHEN_RE.match(stripped):
            in_done_when = True
            continue

        if not in_done_when:
            continue

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

        records.append(
            {
                "slug": slug_match.group(1),
                "status": status,
                "issue_ref": None,
                "file": str(spec_path),
                "line": line_no,
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


def dump_records(records: list[dict[str, object]]) -> str:
    """Serialize records to the line-greppable JSON array contract.

    Mirrors ``dump_records`` in vera's ``scripts/spec_record.py``: ``[`` on
    its own line, one compact ``json.dumps`` record per line, a trailing
    comma after every record except the last, and ``]`` on its own line.
    The empty list serializes as ``[]``.
    """
    if not records:
        return "[]"
    body = ",\n".join(json.dumps(r) for r in records)
    return f"[\n{body}\n]"


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
        help="Output records as JSON (the contract scripts/spec_record.py validates)",
    )
    args = parser.parse_args(argv)

    records = collect_spec_records(args.spec_dir)

    if args.json:
        print(dump_records(records))
    else:
        status_marker = {"done": "✅", "in_progress": "🚧", "pending": " "}
        for record in records:
            marker = status_marker.get(str(record["status"]), " ")
            print(f"{marker} {record['slug']} ({record['status']})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
