"""Acceptance test: write a hello world Python script."""


def hello_world() -> str:
    """Return the hello world greeting."""
    return "Hello, World!"


if __name__ == "__main__":
    print(hello_world())
