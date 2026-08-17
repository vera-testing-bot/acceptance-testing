"""Tests for acceptance_test_e97d961e."""

from acceptance_test_e97d961e import human_owned


def test_human_owned_task() -> None:
    """The task reports that it is owned by a human."""
    assert human_owned() == "human owned"
