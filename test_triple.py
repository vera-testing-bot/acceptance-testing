from triple import triple


def test_triple_positive():
    assert triple(4) == 12


def test_triple_zero():
    assert triple(0) == 0
