from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from src.spec_issue_creator import (
    build_issue_draft,
    collect_planned_spec_items_from_dir,
)


def list_open_issue_data(repo: str) -> list[dict[str, str]]:
    command = [
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--state",
        "open",
        "--limit",
        "200",
        "--json",
        "title,body",
    ]
    output = subprocess.check_output(command, text=True)
    return json.loads(output)


def create_issue(repo: str, title: str, body: str) -> None:
    subprocess.check_call(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            repo,
            "--title",
            title,
            "--body",
            body,
            "--label",
            "vera:ready",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--spec-dir", default="docs/spec")
    parser.add_argument("--create", action="store_true")
    args = parser.parse_args()

    open_issues = list_open_issue_data(args.repo)
    existing_titles = {issue["title"] for issue in open_issues}
    existing_bodies = [issue.get("body", "") for issue in open_issues]
    planned_items = collect_planned_spec_items_from_dir(Path(args.spec_dir))

    created = 0
    for item in planned_items:
        title, body = build_issue_draft(
            spec_title=item.spec_title,
            item_title=item.title,
            summary=item.summary,
            slugs=item.slugs,
        )
        if title in existing_titles:
            continue
        if any(slug in body for slug in item.slugs for body in existing_bodies):
            continue

        if args.create:
            create_issue(args.repo, title, body)
            created += 1
        else:
            print(f"[dry-run] would create issue: {title}")
            print(body)
            print("-" * 40)

        existing_titles.add(title)
        existing_bodies.append(body)

    print(f"planned items found: {len(planned_items)}")
    print(f"issues created: {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
