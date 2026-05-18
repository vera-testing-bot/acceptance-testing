from pathlib import Path

from src.spec_issue_creator import (
    build_issue_draft,
    collect_planned_spec_items,
    collect_planned_spec_items_from_dir,
)


def test_collect_planned_spec_items_reads_planned_sections(tmp_path: Path):
    spec_file = tmp_path / "example.md"
    spec_file.write_text(
        """
# Example Spec

#### 🚧 Power Function

Raise numbers to exponent.

**Done when:**
- `power(base, exp)` handles positive integers <!-- slug: spec.power.integers -->
- `power(base, exp)` handles zero exponent <!-- slug: spec.power.zero -->

#### ✅ Existing Feature

Already finished.
""".strip()
    )

    items = collect_planned_spec_items(spec_file)

    assert len(items) == 1
    assert items[0].title == "Power Function"
    assert items[0].spec_title == "Example Spec"
    assert items[0].summary == "Raise numbers to exponent."
    assert items[0].slugs == ["spec.power.integers", "spec.power.zero"]


def test_collect_planned_spec_items_ignores_completed_sections(tmp_path: Path):
    spec_file = tmp_path / "example.md"
    spec_file.write_text(
        """
# Example Spec

#### ✅ Existing Feature

Already finished.

**Done when:**
- Requirement one <!-- slug: spec.done.one -->
""".strip()
    )

    items = collect_planned_spec_items(spec_file)

    assert items == []


def test_build_issue_draft_formats_title_and_body():
    title, body = build_issue_draft(
        spec_title="Math Operations",
        item_title="Power Function",
        summary="Raise numbers to exponent.",
        slugs=["spec.power.integers", "spec.power.zero"],
    )

    assert title == "feat: implement power function"
    assert "Spec: Math Operations" in body
    assert "Raise numbers to exponent." in body
    assert "spec.power.integers" in body
    assert "spec.power.zero" in body


def test_collect_planned_spec_items_from_dir(tmp_path: Path):
    (tmp_path / "one.md").write_text(
        """
# One

#### 🚧 Feature One

Text.
""".strip()
    )
    (tmp_path / "two.md").write_text(
        """
# Two

#### ✅ Feature Two
""".strip()
    )

    items = collect_planned_spec_items_from_dir(tmp_path)

    assert len(items) == 1
    assert items[0].title == "Feature One"
