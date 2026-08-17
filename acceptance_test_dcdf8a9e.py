"""Acceptance test: a task that keeps running after human assign."""


def keep_running() -> str:
    """Return the running status after a human assign."""
    return "still running"


if __name__ == "__main__":
    print(keep_running())
