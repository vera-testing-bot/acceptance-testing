"""Tests for acceptance_test_7a6b7788."""

from acceptance_test_7a6b7788 import ready_set_on_adoption


def test_ready_is_set_on_adoption() -> None:
    """The vera:ready status is set when the task is adopted."""
    assert ready_set_on_adoption() == "ready"
