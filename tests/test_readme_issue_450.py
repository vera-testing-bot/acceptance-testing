from pathlib import Path


def test_readme_contains_issue_450_comment() -> None:
    readme_text = Path("README.md").read_text(encoding="utf-8")

    assert "<!-- Issue #450: triage behavior check -->" in readme_text
