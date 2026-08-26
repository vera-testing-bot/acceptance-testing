"""Tests for acceptance_test_1d088b78."""

from acceptance_test_1d088b78 import user_close


def test_user_close_reports_canceled() -> None:
    """The task reports the canceled status when a user closes it."""
    assert user_close() == "canceled"
