import sys
import io
from src.hello_world import main, hello_german


def test_hello_world_prints(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"


def test_hello_german_prints(capsys):
    hello_german()
    captured = capsys.readouterr()
    assert captured.out == "Hallo Welt\n"
