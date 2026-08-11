# Spec conventions

This directory holds the spec files that define expected behavior in the
acceptance-testing repo. Each criterion line must be machine-readable by the
Vera spec-compliance gate.

## Three-state checkboxes

Every "Done when:" criterion line carries a three-state checkbox:

- `- [ ]` — not started
- `- [#123]` — in progress under GitHub issue #123
- `- [x]` — complete

## Slug comments

"Done when:" bullets carry an inline slug comment:

```markdown
- [ ] criterion text <!-- slug: feature.section.criterion -->
```

The `slug:` token is required so the spec-status parser can track and report
the criterion.

## Completion

On completion, the `#NNN` in the checkbox is replaced by `x`. For example:

```markdown
- [x] criterion text <!-- slug: feature.section.criterion -->
```

No trailing issue reference is appended to the line; the issue number lives in
the checkbox token.
