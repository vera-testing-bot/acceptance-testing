from dataclasses import dataclass
import re
from pathlib import Path


SECTION_HEADER_RE = re.compile(r"^####\s+🚧\s+(.+?)\s*$")
SLUG_RE = re.compile(r"slug:\s*([\w.-]+)")


@dataclass(frozen=True)
class PlannedSpecItem:
    title: str
    spec_title: str
    summary: str
    slugs: list[str]


def normalize_feature_title(item_title: str) -> str:
    return item_title.strip().lower()


def build_issue_draft(
    spec_title: str,
    item_title: str,
    summary: str,
    slugs: list[str],
) -> tuple[str, str]:
    title = f"feat: implement {normalize_feature_title(item_title)}"
    slug_lines = "\n".join(f"- `{slug}`" for slug in slugs) if slugs else "- None"
    body = "\n".join(
        [
            f"Spec: {spec_title}",
            "",
            summary or "Implement this planned feature from the spec.",
            "",
            "Done when:",
            slug_lines,
        ]
    )
    return title, body


def collect_planned_spec_items(spec_file: Path) -> list[PlannedSpecItem]:
    lines = spec_file.read_text().splitlines()
    items: list[PlannedSpecItem] = []
    spec_title = ""

    for line in lines:
        if line.startswith("# "):
            spec_title = line[2:].strip()
            break

    index = 0
    while index < len(lines):
        match = SECTION_HEADER_RE.match(lines[index])
        if not match:
            index += 1
            continue

        title = match.group(1).strip()
        index += 1

        while index < len(lines) and not lines[index].strip():
            index += 1

        summary = ""
        if index < len(lines) and not lines[index].startswith("#### "):
            summary = lines[index].strip()
            index += 1

        slugs: list[str] = []
        while index < len(lines) and not lines[index].startswith("#### "):
            slug_match = SLUG_RE.search(lines[index])
            if slug_match:
                slugs.append(slug_match.group(1))
            index += 1

        items.append(
            PlannedSpecItem(
                title=title,
                spec_title=spec_title,
                summary=summary,
                slugs=slugs,
            )
        )

    return items


def collect_planned_spec_items_from_dir(spec_dir: Path) -> list[PlannedSpecItem]:
    items: list[PlannedSpecItem] = []
    for file_path in sorted(spec_dir.glob("*.md")):
        items.extend(collect_planned_spec_items(file_path))
    return items
