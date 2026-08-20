"""Tests for acceptance_test_7cd64b1d."""

from acceptance_test_7cd64b1d import in_progress_appears


def test_in_progress_appears_during_implement() -> None:
    """The vera:in-progress status appears during implement."""
    assert in_progress_appears() == "in progress"
