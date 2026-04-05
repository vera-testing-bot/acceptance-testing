from double import double

def test_double():
    assert double(5) == 10

def test_double_zero():
    assert double(0) == 0
