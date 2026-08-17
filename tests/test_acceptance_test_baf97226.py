"""Tests for acceptance_test_baf97226."""

from acceptance_test_baf97226 import in_progress_appears


def test_in_progress_appears_during_implement() -> None:
    """The task reports that vera:in-progress appeared during implement."""
    assert in_progress_appears() == "in progress"
