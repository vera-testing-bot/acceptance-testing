# Math Operations

A Python library of basic arithmetic and numeric utility functions with full test coverage.

## Arithmetic

#### 🚧 Power/Exponentiation

Raise a number to a power.

**Done when:**
- `power(base, exp)` returns `base ** exp` for positive integers <!-- slug: math-operations.arithmetic.power-integers -->
- `power(base, exp)` handles `exp = 0` returning 1 <!-- slug: math-operations.arithmetic.power-zero -->
- `power(base, exp)` raises `ValueError` for negative exponents <!-- slug: math-operations.arithmetic.power-negative-exp -->
- Tests are included in the test suite <!-- slug: math-operations.arithmetic.power-has-tests -->

---

#### ✅ Subtraction

Subtract one number from another.

**Done when:**
- `subtract(a, b)` returns `a - b` for integers <!-- slug: math-operations.arithmetic.subtract-integers -->
- `subtract(a, b)` works with floats <!-- slug: math-operations.arithmetic.subtract-floats -->

---

#### ✅ Addition

Add two numbers together.

**Done when:**
- `add(a, b)` returns `a + b` for integers <!-- slug: math-operations.arithmetic.add-integers -->
- `add(a, b)` works with floats <!-- slug: math-operations.arithmetic.add-floats -->
- Tests are included in the test suite <!-- slug: math-operations.arithmetic.add-has-tests -->

---

#### 🚧 Multiplication

Multiply two numbers together.

**Done when:**
- `multiply(a, b)` returns `a * b` for integers <!-- slug: math-operations.arithmetic.multiply-integers -->
- `multiply(a, b)` works with floats <!-- slug: math-operations.arithmetic.multiply-floats -->
- Tests are included in the test suite <!-- slug: math-operations.arithmetic.multiply-has-tests -->

---

#### 🚧 Division

Divide one number by another with safe zero-division handling.

**Done when:**
- `divide(a, b)` returns `a / b` for non-zero `b` <!-- slug: math-operations.arithmetic.divide-non-zero -->
- `divide(a, b)` raises `ValueError` when `b` is zero <!-- slug: math-operations.arithmetic.divide-raises-on-zero -->
- Tests cover both the happy path and the zero-division case <!-- slug: math-operations.arithmetic.divide-has-tests -->

---

## Utilities

#### ✅ Regular Hexagon Area

Calculate the area of a regular hexagon from side length.

**Done when:**
- `regular_hexagon_area(side_length)` returns `(3 * sqrt(3) / 2) * side_length^2` <!-- slug: math-operations.utilities.regular-hexagon-area-formula -->
- `regular_hexagon_area(side_length)` works with integers and floats <!-- slug: math-operations.utilities.regular-hexagon-area-numeric-types -->
- `regular_hexagon_area(0)` returns `0.0` <!-- slug: math-operations.utilities.regular-hexagon-area-zero -->

---

#### 🚧 Absolute Value

Return the absolute (non-negative) value of a number.

**Done when:**
- `absolute(n)` returns `n` for positive numbers <!-- slug: math-operations.utilities.absolute-positive -->
- `absolute(n)` returns `-n` for negative numbers <!-- slug: math-operations.utilities.absolute-negative -->
- `absolute(0)` returns `0` <!-- slug: math-operations.utilities.absolute-zero -->
- Tests are included in the test suite <!-- slug: math-operations.utilities.absolute-has-tests -->
