import pathlib


def test_changelog_entry_exists():
    changelog = pathlib.Path("CHANGELOG.md")
    assert changelog.exists()
    assert changelog.stat().st_size > 0
    content = changelog.read_text(encoding="utf-8")
    assert "Acceptance test run 2eefbcf1: add CHANGELOG entry line" in content
