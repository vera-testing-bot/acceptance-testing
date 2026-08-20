"""Acceptance test: a task that should not start."""


def should_not_start() -> str:
    """Return the start status of the task."""
    return "not started"


if __name__ == "__main__":
    print(should_not_start())
