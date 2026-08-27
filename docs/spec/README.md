# Spec

This directory holds the specification files for the acceptance-testing
repository. Each spec file describes *what* the system does — the expected
behaviors and acceptance criteria — while implementation agents decide
architecture, file layout, and code structure.

## Spec conventions

Each "Done when:" criterion line carries a three-state checkbox:

* **`- [ ]`** — not started
* **`- [#123]`** — in progress under GitHub issue #123
* **`- [x]`** — complete

Formatting rules:

* "Done when:" bullets carry an inline slug comment:
  `- [ ] criterion text <!-- slug: area.section.criterion -->`
* On completion the `#NNN` in the checkbox is replaced by `x` — no trailing
  issue reference is appended to the line.

## Status markers

Individual spec sections use status markers to communicate readiness:

* **🚧** — Planned feature, not yet implemented
* **✅** — Verified complete
