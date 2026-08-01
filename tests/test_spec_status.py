"""Tests for scripts/spec_status.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from spec_status import (  # type: ignore[import-not-found]
    collect_citations,
    normalize_status,
    parse_spec_file,
)


SAMPLE_SPEC = """# Sample Spec

#### ✅ Feature

A sample feature.

**Done when:**
- [x] `foo(a)` works <!-- slug: sample.feature.foo -->
- [#42] `bar(a)` works <!-- slug: sample.feature.bar -->
- [ ] Unslotted requirement
"""


def test_normalize_status_maps_checkbox_values():
    assert normalize_status("x") == ("complete", None)
    assert normalize_status("X") == ("complete", None)
    assert normalize_status("") == ("not_started", None)
    assert normalize_status("#42") == ("in_progress", "42")
    assert normalize_status("in-progress") == ("in_progress", None)


def test_parse_spec_file_extracts_citations(tmp_path: Path):
    spec_file = tmp_path / "sample.md"
    spec_file.write_text(SAMPLE_SPEC)

    citations = parse_spec_file(spec_file)

    assert len(citations) == 3

    foo, bar, unslotted = citations

    assert foo.slug == "sample.feature.foo"
    assert foo.status == "complete"
    assert foo.issue_ref is None
    assert "foo(a)" in foo.text

    assert bar.slug == "sample.feature.bar"
    assert bar.status == "in_progress"
    assert bar.issue_ref == "42"

    assert unslotted.slug == ""
    assert unslotted.status == "not_started"


def test_collect_citations_empty_directory(tmp_path: Path):
    assert collect_citations(tmp_path) == []


def test_json_output_is_array_of_records(tmp_path: Path):
    """The Vera spec-compliance gate expects a JSON array of records."""
    spec_file = tmp_path / "docs" / "spec" / "sample.md"
    spec_file.parent.mkdir(parents=True)
    spec_file.write_text(SAMPLE_SPEC)

    script = Path(__file__).parent.parent / "scripts" / "spec_status.py"
    result = subprocess.run(
        [sys.executable, str(script), "--json", "--spec-dir", str(tmp_path / "docs" / "spec")],
        check=True,
        capture_output=True,
        text=True,
    )

    records = json.loads(result.stdout)
    assert isinstance(records, list)
    assert len(records) == 3
    for record in records:
        assert isinstance(record, dict)
        assert "spec_file" in record
        assert "line" in record
        assert "slug" in record
        assert "status" in record
