"""A simple hello world script."""


def greet(name: str = "World") -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet())
