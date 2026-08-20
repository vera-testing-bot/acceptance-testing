"""Tests for acceptance_test_d527b13b."""

from acceptance_test_d527b13b import ready_status


def test_ready_persists_on_adoption() -> None:
    """The vera:ready status persists after adoption."""
    assert ready_status() == "ready"
