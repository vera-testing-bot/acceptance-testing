"""Tests for scripts/create_issues_from_specs.py"""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

# Add project root to path so we can import the script directly.
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.create_issues_from_specs import (
    create_issue,
    fetch_open_issue_titles,
    load_spec,
    load_specs,
    run,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def write_spec(tmp_path: Path, name: str, data: dict) -> Path:
    path = tmp_path / name
    path.write_text(yaml.dump(data), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# load_spec
# ---------------------------------------------------------------------------


def test_load_spec_valid(tmp_path):
    path = write_spec(tmp_path, "s.yaml", {"title": "feat: foo", "body": "do foo", "labels": ["l1"]})
    spec = load_spec(path)
    assert spec["title"] == "feat: foo"
    assert spec["body"] == "do foo"
    assert spec["labels"] == ["l1"]


def test_load_spec_missing_title_raises(tmp_path):
    path = write_spec(tmp_path, "s.yaml", {"body": "do foo"})
    with pytest.raises(ValueError, match="missing required key 'title'"):
        load_spec(path)


def test_load_spec_missing_body_raises(tmp_path):
    path = write_spec(tmp_path, "s.yaml", {"title": "feat: foo"})
    with pytest.raises(ValueError, match="missing required key 'body'"):
        load_spec(path)


def test_load_spec_not_a_mapping_raises(tmp_path):
    path = tmp_path / "s.yaml"
    path.write_text("- item1\n- item2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected a YAML mapping"):
        load_spec(path)


def test_load_spec_labels_optional(tmp_path):
    path = write_spec(tmp_path, "s.yaml", {"title": "feat: bar", "body": "do bar"})
    spec = load_spec(path)
    assert spec.get("labels") is None or "labels" not in spec


# ---------------------------------------------------------------------------
# load_specs
# ---------------------------------------------------------------------------


def test_load_specs_picks_up_yaml_and_yml(tmp_path):
    write_spec(tmp_path, "a.yaml", {"title": "A", "body": "body A"})
    write_spec(tmp_path, "b.yml", {"title": "B", "body": "body B"})
    specs = load_specs(tmp_path)
    titles = {s["title"] for s in specs}
    assert titles == {"A", "B"}


def test_load_specs_ignores_non_yaml(tmp_path):
    write_spec(tmp_path, "a.yaml", {"title": "A", "body": "body A"})
    (tmp_path / "readme.md").write_text("# hi")
    (tmp_path / "notes.txt").write_text("notes")
    specs = load_specs(tmp_path)
    assert len(specs) == 1


def test_load_specs_empty_dir(tmp_path):
    assert load_specs(tmp_path) == []


def test_load_specs_sorted_order(tmp_path):
    write_spec(tmp_path, "c.yaml", {"title": "C", "body": "body C"})
    write_spec(tmp_path, "a.yaml", {"title": "A", "body": "body A"})
    write_spec(tmp_path, "b.yaml", {"title": "B", "body": "body B"})
    specs = load_specs(tmp_path)
    titles = [s["title"] for s in specs]
    assert titles == ["A", "B", "C"]


# ---------------------------------------------------------------------------
# fetch_open_issue_titles
# ---------------------------------------------------------------------------


def test_fetch_open_issue_titles(monkeypatch):
    fake_issues = [{"title": "feat: bar"}, {"title": "feat: baz"}]
    mock_result = MagicMock()
    mock_result.stdout = json.dumps(fake_issues)

    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: mock_result)

    titles = fetch_open_issue_titles("owner/repo")
    assert titles == {"feat: bar", "feat: baz"}


def test_fetch_open_issue_titles_empty_repo(monkeypatch):
    mock_result = MagicMock()
    mock_result.stdout = json.dumps([])

    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: mock_result)

    titles = fetch_open_issue_titles("owner/repo")
    assert titles == set()


# ---------------------------------------------------------------------------
# create_issue
# ---------------------------------------------------------------------------


def test_create_issue_calls_gh(monkeypatch):
    mock_result = MagicMock()
    mock_result.stdout = "https://github.com/owner/repo/issues/42\n"
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        return mock_result

    monkeypatch.setattr(subprocess, "run", fake_run)

    url = create_issue("owner/repo", "feat: new", "some body", ["vera:ready"])
    assert url == "https://github.com/owner/repo/issues/42"
    assert "--title" in captured["cmd"]
    assert "feat: new" in captured["cmd"]
    assert "--label" in captured["cmd"]
    assert "vera:ready" in captured["cmd"]


def test_create_issue_no_labels(monkeypatch):
    mock_result = MagicMock()
    mock_result.stdout = "https://github.com/owner/repo/issues/43\n"
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        return mock_result

    monkeypatch.setattr(subprocess, "run", fake_run)

    url = create_issue("owner/repo", "feat: bare", "body", [])
    assert url == "https://github.com/owner/repo/issues/43"
    assert "--label" not in captured["cmd"]


# ---------------------------------------------------------------------------
# run — integration of load / fetch / create
# ---------------------------------------------------------------------------


def test_run_creates_new_issues(tmp_path, monkeypatch):
    write_spec(tmp_path, "f1.yaml", {"title": "feat: one", "body": "body1", "labels": ["l1"]})
    write_spec(tmp_path, "f2.yaml", {"title": "feat: two", "body": "body2", "labels": []})

    created_titles: list[str] = []

    def fake_fetch(repo):
        return set()

    def fake_create(repo, title, body, labels):
        created_titles.append(title)
        return f"https://github.com/{repo}/issues/99"

    monkeypatch.setattr("scripts.create_issues_from_specs.fetch_open_issue_titles", fake_fetch)
    monkeypatch.setattr("scripts.create_issues_from_specs.create_issue", fake_create)

    results = run(repo="owner/repo", specs_dir=tmp_path)
    assert len(results) == 2
    assert set(created_titles) == {"feat: one", "feat: two"}


def test_run_skips_existing_issues(tmp_path, monkeypatch):
    write_spec(tmp_path, "f1.yaml", {"title": "feat: one", "body": "body1"})
    write_spec(tmp_path, "f2.yaml", {"title": "feat: two", "body": "body2"})

    def fake_fetch(repo):
        return {"feat: one"}

    created_titles: list[str] = []

    def fake_create(repo, title, body, labels):
        created_titles.append(title)
        return f"https://github.com/{repo}/issues/99"

    monkeypatch.setattr("scripts.create_issues_from_specs.fetch_open_issue_titles", fake_fetch)
    monkeypatch.setattr("scripts.create_issues_from_specs.create_issue", fake_create)

    results = run(repo="owner/repo", specs_dir=tmp_path)
    assert len(results) == 1
    assert created_titles == ["feat: two"]


def test_run_dry_run_does_not_create(tmp_path, monkeypatch):
    write_spec(tmp_path, "f1.yaml", {"title": "feat: one", "body": "body1"})

    def fake_fetch(repo):
        return set()

    create_called = []

    def fake_create(repo, title, body, labels):
        create_called.append(title)
        return "https://github.com/owner/repo/issues/99"

    monkeypatch.setattr("scripts.create_issues_from_specs.fetch_open_issue_titles", fake_fetch)
    monkeypatch.setattr("scripts.create_issues_from_specs.create_issue", fake_create)

    results = run(repo="owner/repo", specs_dir=tmp_path, dry_run=True)
    assert results == ["feat: one"]
    assert create_called == []


def test_run_empty_specs_dir(tmp_path, monkeypatch):
    def fake_fetch(repo):
        return set()

    monkeypatch.setattr("scripts.create_issues_from_specs.fetch_open_issue_titles", fake_fetch)

    results = run(repo="owner/repo", specs_dir=tmp_path)
    assert results == []


def test_run_all_existing_skipped(tmp_path, monkeypatch):
    write_spec(tmp_path, "f1.yaml", {"title": "feat: existing", "body": "body1"})

    def fake_fetch(repo):
        return {"feat: existing"}

    create_called = []

    def fake_create(repo, title, body, labels):
        create_called.append(title)
        return "https://github.com/owner/repo/issues/99"

    monkeypatch.setattr("scripts.create_issues_from_specs.fetch_open_issue_titles", fake_fetch)
    monkeypatch.setattr("scripts.create_issues_from_specs.create_issue", fake_create)

    results = run(repo="owner/repo", specs_dir=tmp_path)
    assert results == []
    assert create_called == []


# ---------------------------------------------------------------------------
# Spec files in the real specs/ directory
# ---------------------------------------------------------------------------


REPO_ROOT = Path(__file__).parent.parent
SPECS_DIR = REPO_ROOT / "specs"


@pytest.mark.skipif(not SPECS_DIR.is_dir(), reason="specs/ directory not present")
def test_real_specs_are_valid():
    """All YAML files in specs/ must be valid specs."""
    specs = load_specs(SPECS_DIR)
    assert len(specs) > 0, "Expected at least one spec file in specs/"
    for spec in specs:
        assert "title" in spec
        assert "body" in spec


@pytest.mark.skipif(not SPECS_DIR.is_dir(), reason="specs/ directory not present")
def test_real_specs_have_vera_ready_label():
    """All real specs should carry the vera:ready label."""
    specs = load_specs(SPECS_DIR)
    for spec in specs:
        labels = spec.get("labels", [])
        assert "vera:ready" in labels, f"Spec {spec['title']!r} missing 'vera:ready' label"
