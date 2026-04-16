"""
Create GitHub issues from YAML spec files in the specs/ directory.

Usage:
    python scripts/create_issues_from_specs.py \
        --repo OWNER/REPO \
        --specs-dir specs/ \
        [--dry-run]

Each spec file must be a YAML document with the keys:
    title  (str)       GitHub issue title
    body   (str)       GitHub issue body (markdown)
    labels (list[str]) Labels to apply (optional)

The script skips specs whose title already matches an open issue in the
repository so it is safe to run repeatedly.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml


def load_spec(path: Path) -> dict:
    """Load and validate a single spec YAML file."""
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping, got {type(data).__name__}")
    if "title" not in data:
        raise ValueError(f"{path}: missing required key 'title'")
    if "body" not in data:
        raise ValueError(f"{path}: missing required key 'body'")
    return data


def load_specs(specs_dir: Path) -> list[dict]:
    """Load all *.yaml / *.yml spec files from *specs_dir*."""
    specs = []
    for path in sorted(specs_dir.glob("*.yaml")) + sorted(specs_dir.glob("*.yml")):
        specs.append(load_spec(path))
    return specs


def fetch_open_issue_titles(repo: str) -> set[str]:
    """Return the set of titles for all open issues in *repo* (via gh CLI)."""
    result = subprocess.run(
        ["gh", "issue", "list", "--repo", repo, "--state", "open", "--json", "title", "--limit", "500"],
        capture_output=True,
        text=True,
        check=True,
    )
    issues = json.loads(result.stdout)
    return {issue["title"] for issue in issues}


def create_issue(repo: str, title: str, body: str, labels: list[str]) -> str:
    """Create a GitHub issue and return its URL."""
    cmd = ["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body]
    for label in labels:
        cmd += ["--label", label]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def run(repo: str, specs_dir: Path, dry_run: bool = False) -> list[str]:
    """
    Create GitHub issues for every spec not already present in *repo*.

    Returns a list of created issue URLs (or spec titles when *dry_run* is True).
    """
    specs = load_specs(specs_dir)
    if not specs:
        print(f"No spec files found in {specs_dir}", file=sys.stderr)
        return []

    existing_titles = fetch_open_issue_titles(repo)
    created: list[str] = []

    for spec in specs:
        title = spec["title"]
        if title in existing_titles:
            print(f"  skip  {title!r} (already open)")
            continue

        labels: list[str] = spec.get("labels", [])
        body: str = spec["body"]

        if dry_run:
            print(f"  [dry-run] would create: {title!r}  labels={labels}")
            created.append(title)
        else:
            url = create_issue(repo, title, body, labels)
            print(f"  created {url}")
            created.append(url)

    return created


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, help="GitHub repository in OWNER/REPO format")
    parser.add_argument("--specs-dir", default="specs", help="Directory containing spec YAML files (default: specs)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be created without actually creating issues")
    args = parser.parse_args(argv)

    specs_dir = Path(args.specs_dir)
    if not specs_dir.is_dir():
        print(f"error: specs directory not found: {specs_dir}", file=sys.stderr)
        return 1

    created = run(repo=args.repo, specs_dir=specs_dir, dry_run=args.dry_run)
    print(f"\n{'Would create' if args.dry_run else 'Created'} {len(created)} issue(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
