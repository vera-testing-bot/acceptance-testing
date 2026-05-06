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

#### 🚧 Absolute Value

Return the absolute (non-negative) value of a number.

**Done when:**
- `absolute(n)` returns `n` for positive numbers <!-- slug: math-operations.utilities.absolute-positive -->
- `absolute(n)` returns `-n` for negative numbers <!-- slug: math-operations.utilities.absolute-negative -->
- `absolute(0)` returns `0` <!-- slug: math-operations.utilities.absolute-zero -->
- Tests are included in the test suite <!-- slug: math-operations.utilities.absolute-has-tests -->

---

## Trigonometry

#### ✅ Sine

Return the sine of an angle in radians without using math libraries.

**Done when:**
- `sin(x)` returns an approximation of sine for radian input <!-- slug: math-operations.trigonometry.sin-returns-approximation -->
- `sin(x)` is accurate within `1e-6` for representative values <!-- slug: math-operations.trigonometry.sin-accuracy -->
- Implementation does not rely on existing math libraries <!-- slug: math-operations.trigonometry.sin-no-math-library -->
- Tests are included in the test suite <!-- slug: math-operations.trigonometry.sin-has-tests -->
