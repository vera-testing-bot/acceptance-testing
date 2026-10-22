"""Acceptance test: a task that should keep running after human assign."""


def keep_running() -> str:
    """Return the running status after a human assign."""
    return "still running"


if __name__ == "__main__":
    print(keep_running())
