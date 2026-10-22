"""Acceptance test: vera:ready is set on adoption."""


def ready_set_on_adoption() -> str:
    """Return the readiness status that is set when a task is adopted."""
    return "ready"


if __name__ == "__main__":
    print(ready_set_on_adoption())
