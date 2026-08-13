import pathlib


def test_changelog_entry_exists():
    changelog = pathlib.Path("CHANGELOG.md")
    assert changelog.exists()
    assert changelog.stat().st_size > 0
