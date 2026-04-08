import random


def hello_world() -> str:
    """Return 'hello world' with random capitalization."""
    return "".join(random.choice([c.upper(), c.lower()]) for c in "hello world")


if __name__ == "__main__":
    print(hello_world())
