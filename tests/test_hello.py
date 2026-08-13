from src.hello import GREETING, hello


def test_hello_returns_hello():
    assert hello() == 'hello'


def test_greeting_constant():
    assert GREETING == 'hello'
    assert GREETING.__doc__
