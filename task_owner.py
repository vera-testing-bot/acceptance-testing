def is_human_owner(owner):
    """Return True when the task owner is a human rather than a bot."""
    if not owner:
        return False
    name = owner.strip().lower()
    if name.endswith("[bot]"):
        return False
    return not name.endswith("bot")


if __name__ == "__main__":
    print(is_human_owner("jasonsurratt"))
