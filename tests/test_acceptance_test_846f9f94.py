"""Tests for acceptance_test_846f9f94."""

from acceptance_test_846f9f94 import should_not_start


def test_task_should_not_start() -> None:
    """The task reports that it should not start."""
    assert should_not_start() == "not started"
