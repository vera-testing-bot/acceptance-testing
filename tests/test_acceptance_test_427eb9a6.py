"""Tests for acceptance_test_427eb9a6."""

from acceptance_test_427eb9a6 import ready_status


def test_ready_persists_on_adoption() -> None:
    """The vera:ready status persists after adoption."""
    assert ready_status() == "ready"
