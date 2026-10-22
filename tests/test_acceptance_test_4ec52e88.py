"""Tests for acceptance_test_4ec52e88."""

from acceptance_test_4ec52e88 import should_not_start


def test_task_should_not_start() -> None:
    """The task reports that it should not start."""
    assert should_not_start() == "not started"
