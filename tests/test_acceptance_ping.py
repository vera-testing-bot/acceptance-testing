from pathlib import Path


def test_readme_ends_with_acceptance_ping():
    readme = Path(__file__).parent.parent / "README.md"
    lines = readme.read_text().splitlines()
    assert lines[-1] == "# acceptance-ping"
