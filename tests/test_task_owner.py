from task_owner import is_human_owner


def test_is_human_owner_true_for_human_name():
    assert is_human_owner("jasonsurratt") is True


def test_is_human_owner_false_for_bot_account():
    assert is_human_owner("vera-testing-bot") is False


def test_is_human_owner_false_for_bot_suffix():
    assert is_human_owner("github-actions[bot]") is False


def test_is_human_owner_false_for_none():
    assert is_human_owner(None) is False
