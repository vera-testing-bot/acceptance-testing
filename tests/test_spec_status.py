"""Tests for scripts/spec_status.py — the machine-readable spec parser.

Asserts the record contract Vera's spec-compliance audit relies on: exactly
the ``{slug, status, issue_ref, file, line}`` field set, the three-value
status enum, the one-record-per-line ``--json`` output layout, and a slug
count sanity check against the real spec file.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_STATUS = REPO_ROOT / "scripts" / "spec_status.py"
SPEC_FILE = REPO_ROOT / "docs" / "spec" / "math-operations.md"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import spec_status  # noqa: E402


EXPECTED_FIELDS = {"slug", "status", "issue_ref", "file", "line"}
VALID_STATUSES = {"pending", "in_progress", "done"}


@pytest.fixture(scope="module")
def records() -> list[dict[str, object]]:
    return spec_status.collect_spec_records(Path("docs/spec"))


def test_records_are_nonempty(records: list[dict[str, object]]) -> None:
    assert records


def test_record_field_set_is_exact(records: list[dict[str, object]]) -> None:
    for record in records:
        assert set(record.keys()) == EXPECTED_FIELDS


def test_status_values_are_in_enum(records: list[dict[str, object]]) -> None:
    for record in records:
        assert record["status"] in VALID_STATUSES
        # The legacy "complete"/"planned" values must never appear.
        assert record["status"] not in {"complete", "planned"}


def test_issue_ref_is_always_none(records: list[dict[str, object]]) -> None:
    # This spec carries no per-criterion issue links.
    for record in records:
        assert record["issue_ref"] is None


def test_file_is_repo_root_relative(records: list[dict[str, object]]) -> None:
    for record in records:
        assert "/" in record["file"]
        assert record["file"] == "docs/spec/math-operations.md"


def test_line_is_1_based_and_in_range(records: list[dict[str, object]]) -> None:
    line_count = len(SPEC_FILE.read_text(encoding="utf-8").splitlines())
    for record in records:
        assert isinstance(record["line"], int)
        assert 1 <= record["line"] <= line_count


def test_slug_count_matches_real_spec_file(records: list[dict[str, object]]) -> None:
    # Sanity check against the real spec: every "<!-- slug: ... -->" comment
    # in docs/spec/math-operations.md should produce exactly one record, and
    # slugs must be unique.
    text = SPEC_FILE.read_text(encoding="utf-8")
    expected_slugs = set(spec_status.SLUG_RE.findall(text))
    parsed_slugs = {record["slug"] for record in records}
    assert len(records) == len(parsed_slugs), "duplicate slug detected"
    assert parsed_slugs == expected_slugs


def test_math_operations_slugs_are_all_done(records: list[dict[str, object]]) -> None:
    # Every feature in docs/spec/math-operations.md is marked with the ✅
    # feature emoji and every criterion is a plain (non-checkbox) bullet, so
    # every record should resolve to "done".
    statuses = {record["status"] for record in records}
    assert statuses == {"done"}


def test_json_output_layout_is_one_record_per_line() -> None:
    result = subprocess.run(
        [sys.executable, str(SPEC_STATUS), "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.strip("\n").split("\n")
    assert lines[0] == "["
    assert lines[-1] == "]"

    record_lines = lines[1:-1]
    parsed = json.loads(result.stdout)
    assert len(record_lines) == len(parsed)

    for raw in record_lines:
        candidate = raw.rstrip(",")
        obj = json.loads(candidate)
        assert isinstance(obj, dict)
        # Not pretty-printed: json.dumps of a small flat dict never contains
        # a newline, so round-tripping the exact candidate text confirms the
        # object was emitted compactly on this single line.
        assert json.dumps(obj) == candidate


def test_json_output_is_a_json_array() -> None:
    result = subprocess.run(
        [sys.executable, str(SPEC_STATUS), "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    parsed = json.loads(result.stdout)
    assert isinstance(parsed, list)
    assert len(parsed) == 35
