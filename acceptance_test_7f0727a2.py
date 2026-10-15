import sys

import yaml


def main() -> int:
    with open(".vera/settings.yaml") as f:
        settings = yaml.safe_load(f)

    if not isinstance(settings.get("auto_manage_issues"), bool):
        print(
            "Invalid settings value: auto_manage_issues must be a boolean",
            file=sys.stderr,
        )
        return 1

    max_attempts = settings.get("max_attempts")
    if not isinstance(max_attempts, int) or not (1 <= max_attempts <= 20):
        print(
            "Invalid settings value: max_attempts must be an integer in [1, 20]",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
