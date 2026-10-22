"""Acceptance test: a task owned by a human."""


def human_owned() -> str:
    """Return the ownership status of the task."""
    return "human owned"


if __name__ == "__main__":
    print(human_owned())
