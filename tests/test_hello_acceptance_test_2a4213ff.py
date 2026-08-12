import subprocess
import sys


def test_hello_acceptance_script_prints_hello_world():
    result = subprocess.run(
        [sys.executable, "hello_acceptance_test_2a4213ff.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout == "Hello, World!\n"
    assert result.stderr == ""
