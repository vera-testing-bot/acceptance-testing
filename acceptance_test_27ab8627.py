"""Acceptance test: verify .vera/settings.yaml is within the size limit."""

import sys
from pathlib import Path

SETTINGS_SIZE_LIMIT = 10_240


def check_settings_size(settings_path: Path) -> None:
    """Raise ValueError if the settings file exceeds the size limit."""
    size = settings_path.stat().st_size
    if size > SETTINGS_SIZE_LIMIT:
        msg = (
            f"Settings file {settings_path} is {size} bytes, "
            f"which exceeds the {SETTINGS_SIZE_LIMIT} byte limit."
        )
        raise ValueError(msg)


def main() -> int:
    """Check the size of .vera/settings.yaml relative to this script."""
    script_dir = Path(__file__).resolve().parent
    settings_path = script_dir / ".vera" / "settings.yaml"

    try:
        check_settings_size(settings_path)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
