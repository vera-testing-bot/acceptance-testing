"""Acceptance test 289bf93b: safe YAML loader.

This module exposes a YAML loader that rejects unsafe directives such as
``!!python/object`` to prevent arbitrary Python object construction.
"""

import yaml


def load_yaml(text: str) -> object:
    """Parse ``text`` as YAML using the safe loader.

    Args:
        text: YAML document to parse.

    Returns:
        The parsed YAML value.

    Raises:
        yaml.constructor.ConstructorError: If the document contains an
            unsafe constructor directive.
    """
    return yaml.safe_load(text)
