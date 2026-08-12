import subprocess


def test_hello_acceptance_test_ad52f328_output():
    result = subprocess.run(
        ["python", "hello_acceptance_test_ad52f328.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout == "Hello, World!\n"
