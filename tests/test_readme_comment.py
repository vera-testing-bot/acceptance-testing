from pathlib import Path


def test_readme_contains_hello_world_comment():
    readme = Path(__file__).parent.parent / "README.md"
    content = readme.read_text(encoding="utf-8")

    assert "<!-- hello world -->" in content
