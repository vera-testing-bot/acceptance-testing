"""Tests for acceptance_test_a4a4521c."""

from acceptance_test_a4a4521c import in_progress_appears


def test_in_progress_appears_during_implement() -> None:
    """The vera:in-progress status appears during implement."""
    assert in_progress_appears() == "in progress"
