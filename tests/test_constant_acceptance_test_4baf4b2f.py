import subprocess

import constant_acceptance_test_4baf4b2f


EXPECTED_VALUE = "Hello, World!"
EXPECTED_DOCSTRING = "A friendly greeting for the acceptance test."


def test_constant_is_defined_and_equals_expected_value():
    assert constant_acceptance_test_4baf4b2f.GREETING == EXPECTED_VALUE


def test_constant_has_attribute_docstring():
    assert constant_acceptance_test_4baf4b2f.GREETING.__doc__ is not None
    assert isinstance(constant_acceptance_test_4baf4b2f.GREETING.__doc__, str)
    assert constant_acceptance_test_4baf4b2f.GREETING.__doc__ == EXPECTED_DOCSTRING


def test_module_runs_without_runtime_errors():
    result = subprocess.run(
        ["python", "constant_acceptance_test_4baf4b2f.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stderr == ""
