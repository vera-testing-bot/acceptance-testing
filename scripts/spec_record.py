#!/usr/bin/env python3
"""Typed record definition for Vera spec status parsing.

``scripts/spec_status.py --json`` emits a JSON array of these records, one per
"Done when:" criterion line found in ``docs/spec/*.md``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpecRecord:
    """One line-greppable criterion record.

    Each record maps a single "Done when:" bullet to its current state so the
    Vera spec-compliance gate can compare implementation against the spec.
    """

    slug: str
    """Dotted criterion identifier from the ``<!-- slug: ... -->`` comment."""

    text: str
    """Human-readable criterion text."""

    file: str
    """Spec file path, relative to the repository root."""

    state: str
    """One of ``not_started``, ``in_progress``, or ``complete``."""

    line: int
    """One-based line number of the criterion in ``file``."""

    issue: int | None = None
    """Linked GitHub issue number when the checkbox is ``[#NNN]``."""

    def to_json(self) -> dict[str, str | int | None]:
        """Return a JSON-serializable dictionary for this record."""
        return {
            "slug": self.slug,
            "text": self.text,
            "file": self.file,
            "state": self.state,
            "line": self.line,
            "issue": self.issue,
        }
