"""Tests for acceptance_test_289bf93b.yaml safety loader."""

import pytest
import yaml

from acceptance_test_289bf93b import load_yaml


def test_load_yaml_parses_safe_yaml() -> None:
    """Safe YAML is parsed into native Python objects."""
    assert load_yaml("answer: 42") == {"answer": 42}


def test_load_yaml_rejects_python_object_tag() -> None:
    """Unsafe !!python/object directives are rejected."""
    with pytest.raises(yaml.constructor.ConstructorError):
        load_yaml("!!python/object:os.system ['echo pwned']")
