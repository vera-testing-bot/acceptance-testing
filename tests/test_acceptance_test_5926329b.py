"""Tests for acceptance_test_5926329b."""

from acceptance_test_5926329b import refining_status


def test_complex_issue_enters_refining() -> None:
    """A complex issue enters the vera:refining review-plan phase."""
    assert refining_status() == "refining"
