"""Tests for acceptance_test_67ee1d9b."""

from acceptance_test_67ee1d9b import user_close


def test_user_close_reports_canceled() -> None:
    """The task reports the canceled status when a user closes it."""
    assert user_close() == "canceled"
