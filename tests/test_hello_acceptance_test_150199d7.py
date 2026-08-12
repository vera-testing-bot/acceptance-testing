import subprocess
import sys


def test_script_prints_hello_world():
    result = subprocess.run(
        [sys.executable, "hello_acceptance_test_150199d7.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == "Hello, World!\n"
