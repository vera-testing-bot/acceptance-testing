import sys
import io
from src.hello_world import main


def test_hello_world_prints(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"
