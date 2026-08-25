import subprocess


def test_invalid_settings_fail_fast():
    result = subprocess.run(
        ["python", "acceptance_test_7f0727a2.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Invalid" in (result.stdout + result.stderr)
