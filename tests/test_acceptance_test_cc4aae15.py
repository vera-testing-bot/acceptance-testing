"""Tests for acceptance_test_cc4aae15."""

from acceptance_test_cc4aae15 import ready_status


def test_ready_persists_on_adoption() -> None:
    """The vera:ready status persists after adoption."""
    assert ready_status() == "ready"
