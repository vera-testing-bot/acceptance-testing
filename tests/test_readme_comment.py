from pathlib import Path


def test_readme_contains_hello_world_comment():
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "<!-- hello world -->" in readme
