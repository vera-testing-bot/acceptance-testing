"""Tests for acceptance_test_f232c18c."""

from acceptance_test_f232c18c import user_close


def test_user_close_reports_canceled() -> None:
    """The task reports the canceled status when a user closes it."""
    assert user_close() == "canceled"
