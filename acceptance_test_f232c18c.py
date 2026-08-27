"""Acceptance test: a task that verifies vera:canceled on user close."""

from acceptance_test_helpers import user_close

__all__ = ["user_close"]


if __name__ == "__main__":
    print(user_close())
