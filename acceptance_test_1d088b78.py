"""Acceptance test: a task that verifies vera:canceled on user close."""


def user_close() -> str:
    """Return the canceled status reported when a user closes the task."""
    return "canceled"


if __name__ == "__main__":
    print(user_close())
