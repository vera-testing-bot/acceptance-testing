"""Tests for acceptance_test_8dff4ff7."""

from acceptance_test_8dff4ff7 import ready_status


def test_ready_persists_on_adoption() -> None:
    """The vera:ready status persists after adoption."""
    assert ready_status() == "ready"
