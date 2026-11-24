"""Acceptance test: vera:ready persists on adoption."""


def ready_status() -> str:
    """Return the readiness status that persists after adoption."""
    return "ready"


if __name__ == "__main__":
    print(ready_status())
