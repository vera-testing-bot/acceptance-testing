import subprocess
import sys
from src.hello_world import main


def test_hello_world_prints(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"


def test_hello_world_script():
    result = subprocess.run(
        [sys.executable, "src/hello_world.py"],
        capture_output=True,
        text=True,
        cwd="/home/runner/_work/acceptance-testing/acceptance-testing",
    )
    assert result.returncode == 0
    assert result.stdout == "hello world\n"
