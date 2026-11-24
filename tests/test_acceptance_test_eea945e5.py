"""Tests for acceptance_test_eea945e5."""

from acceptance_test_eea945e5 import ready_status


def test_ready_persists_on_adoption() -> None:
    """The vera:ready status persists after adoption."""
    assert ready_status() == "ready"
