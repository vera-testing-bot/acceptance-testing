import subprocess
import sys


def test_hello_acceptance_test_4d0ac8a9_prints():
    result = subprocess.run(
        [sys.executable, "hello_acceptance_test_4d0ac8a9.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == "Hello, World!"
    assert result.stderr == ""
