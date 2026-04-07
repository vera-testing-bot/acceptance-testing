from src.hello_world import hello_world


def test_hello_world_prints_caps(capsys):
    hello_world()
    captured = capsys.readouterr()
    assert captured.out == "HELLO WORLD\n"
