"""Tests for acceptance_test_dcdf8a9e."""

from acceptance_test_dcdf8a9e import keep_running


def test_keep_running_after_human_assign() -> None:
    """The task reports that it is still running after a human assign."""
    assert keep_running() == "still running"
