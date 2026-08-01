"""Tests for the calculator HTML template."""

import re
from pathlib import Path

import pytest

CALCULATOR_HTML = Path(__file__).resolve().parents[1] / "templates" / "calculator.html"


def test_calculator_template_exists():
    assert CALCULATOR_HTML.exists(), "calculator.html template should exist"


@pytest.mark.spec("accessibility.equals-button.aria-label")
def test_equals_button_has_aria_label():
    html = CALCULATOR_HTML.read_text(encoding="utf-8")
    match = re.search(r'<button\b[^>]*aria-label="equals"', html, re.IGNORECASE)
    assert match is not None, "equals button must carry aria-label=\"equals\""
