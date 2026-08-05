import json
import subprocess
import sys
from pathlib import Path


def test_spec_status_emits_non_empty_json_records_for_repo_spec():
    """The machine-readable parser must produce a non-empty JSON record set."""
    repo_root = Path(__file__).parent.parent
    result = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "spec_status.py"), "--json"],
        capture_output=True,
        text=True,
        cwd=repo_root,
        check=True,
    )
    records = json.loads(result.stdout)

    assert isinstance(records, list)
    assert records, "expected at least one spec record"

    for record in records:
        assert "slug" in record
        assert "status" in record
        assert "criterion" in record


def test_spec_status_parses_checkbox_and_inherited_status(tmp_path: Path):
    """The parser respects explicit GitHub-style checkboxes and falls back to
    the feature-level emoji marker for plain bullets.
    """
    spec_file = tmp_path / "sample.md"
    spec_file.write_text(
        """
# Sample Spec

#### ✅ Completed

**Done when:**
- [x] Checkbox complete <!-- slug: sample.completed.checkbox -->
- Plain complete <!-- slug: sample.completed.plain -->

#### 🚧 Planned

**Done when:**
- [ ] Checkbox planned <!-- slug: sample.planned.checkbox -->
- Plain planned <!-- slug: sample.planned.plain -->
""".strip(),
        encoding="utf-8",
    )

    repo_root = Path(__file__).parent.parent
    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "spec_status.py"),
            "--json",
            "--spec-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    records = json.loads(result.stdout)

    assert len(records) == 4
    statuses = {r["slug"]: r["status"] for r in records}
    assert statuses["sample.completed.checkbox"] == "complete"
    assert statuses["sample.completed.plain"] == "complete"
    assert statuses["sample.planned.checkbox"] == "planned"
    assert statuses["sample.planned.plain"] == "planned"
