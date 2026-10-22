"""Shared helpers for acceptance test tasks.

Centralizes the implementations that were previously duplicated across the
per-task ``acceptance_test_*.py`` files so they cannot drift apart.
"""


def user_close() -> str:
    """Return the canceled status reported when a user closes the task."""
    return "canceled"
