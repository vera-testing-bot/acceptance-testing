from src.kvstore.utils import reverse


def test_reverse():
    assert reverse("abc") == "cba"


def test_reverse_empty():
    assert reverse("") == ""


def test_reverse_single():
    assert reverse("a") == "a"
