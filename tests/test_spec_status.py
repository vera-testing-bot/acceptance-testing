from pathlib import Path

from scripts.spec_status import parse_spec_file


def test_parse_spec_file_collects_complete_sections(tmp_path: Path):
    spec = tmp_path / "example.md"
    spec.write_text(
        """
# Example Spec

#### ✅ Power Function

Raise numbers to exponent.

**Done when:**
- `power(base, exp)` handles positive integers <!-- slug: spec.power.integers -->
- `power(base, exp)` handles zero exponent <!-- slug: spec.power.zero -->

#### 🚧 Future Feature

Coming later.

**Done when:**
- one thing <!-- slug: spec.future.one -->
""".strip()
    )

    records = parse_spec_file(spec)

    assert {r["slug"] for r in records} == {
        "spec.power.integers",
        "spec.power.zero",
        "spec.future.one",
    }
    complete = [r for r in records if r["slug"].startswith("spec.power")]
    assert all(r["status"] == "complete" for r in complete)
    future = [r for r in records if r["slug"].startswith("spec.future")]
    assert all(r["status"] == "not_started" for r in future)


def test_parse_spec_file_ignores_slugs_without_bullet(tmp_path: Path):
    spec = tmp_path / "example.md"
    spec.write_text(
        """
# Example Spec

#### ✅ Section

This paragraph has a slug comment <!-- slug: prose.should.not.count --> but is not a criterion.

**Done when:**
- real criterion <!-- slug: section.real -->
""".strip()
    )

    records = parse_spec_file(spec)

    assert len(records) == 1
    assert records[0]["slug"] == "section.real"
