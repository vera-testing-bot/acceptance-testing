import subprocess
import os


def test_hello_script_prints_hello_world():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(
        ["python3", os.path.join(repo_root, "hello.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout == "Hello, World!\n"
