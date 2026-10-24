"""Tests for acceptance_test_27ab8627."""

from pathlib import Path

import pytest

from acceptance_test_27ab8627 import check_settings_size


def test_rejects_oversized_settings(tmp_path: Path) -> None:
    """Reject a settings file larger than the 10 KB limit."""
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_bytes(b"x" * 10_241)

    with pytest.raises(ValueError, match="exceeds"):
        check_settings_size(settings_file)


def test_accepts_normal_settings(tmp_path: Path) -> None:
    """Accept a settings file within the 10 KB limit."""
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_bytes(b"x" * 10_240)

    check_settings_size(settings_file)
