from acceptance_test_a879aa5d import auto_managed_marker


def test_auto_managed_marker_returns_marker():
    assert auto_managed_marker() == "a879aa5d"
