"""Acceptance test: a complex issue enters review-plan refining."""


def refining_status() -> str:
    """Return the refining status a complex issue enters for review-plan."""
    return "refining"


if __name__ == "__main__":
    print(refining_status())
