import math
import sys
import unittest

from calculator_core import (
    CalculationOverflowError,
    DivisionByZeroError,
    InvalidOperandError,
    Operation,
    UnsupportedOperationError,
    calculate,
    format_result,
)
from main import add


class CalculateTests(unittest.TestCase):
    def test_basic_operations(self) -> None:
        cases = (
            (7, 3, Operation.ADD, 10),
            (7, 3, Operation.SUBTRACT, 4),
            (7, 3, Operation.MULTIPLY, 21),
            (7, 2, Operation.DIVIDE, 3.5),
        )
        for first, second, operation, expected in cases:
            with self.subTest(operation=operation):
                self.assertEqual(calculate(first, second, operation), expected)

    def test_decimal_and_negative_operands(self) -> None:
        self.assertAlmostEqual(calculate(-1.25, 0.5, Operation.ADD), -0.75)
        self.assertEqual(calculate(-2.5, 4, Operation.MULTIPLY), -10)
        self.assertEqual(calculate(5.5, 2, Operation.DIVIDE), 2.75)

    def test_operation_strings_are_supported(self) -> None:
        self.assertEqual(calculate(8, 5, "subtract"), 3)

    def test_add_compatibility_helper(self) -> None:
        self.assertEqual(add(num1=2.5, num2=1.5), 4)

    def test_division_by_positive_or_negative_zero_fails(self) -> None:
        for zero in (0.0, -0.0):
            with self.subTest(zero=zero):
                with self.assertRaises(DivisionByZeroError) as raised:
                    calculate(1, zero, Operation.DIVIDE)
                self.assertEqual(raised.exception.code, "division_by_zero")

    def test_non_finite_and_non_numeric_operands_fail(self) -> None:
        invalid_operands = (math.inf, -math.inf, math.nan, "2", True, 10**1000)
        for value in invalid_operands:
            with self.subTest(value=repr(value)):
                with self.assertRaises(InvalidOperandError):
                    calculate(value, 1, Operation.ADD)

    def test_unsupported_operation_fails_with_code(self) -> None:
        with self.assertRaises(UnsupportedOperationError) as raised:
            calculate(1, 2, "modulo")
        self.assertEqual(raised.exception.code, "unsupported_operation")

    def test_non_finite_results_fail(self) -> None:
        with self.assertRaises(CalculationOverflowError) as raised:
            calculate(sys.float_info.max, sys.float_info.max, Operation.ADD)
        self.assertEqual(raised.exception.code, "non_finite_result")


class FormatResultTests(unittest.TestCase):
    def test_default_precision_and_decimal_rounding(self) -> None:
        self.assertEqual(format_result(0.1 + 0.2), "0.3")
        self.assertEqual(format_result(1.23456789012345), "1.23456789012")

    def test_small_large_and_zero_values(self) -> None:
        self.assertEqual(format_result(0.000000123456789), "1.23456789e-07")
        self.assertEqual(format_result(1e100), "1e+100")
        self.assertEqual(format_result(-0.0), "0")

    def test_significant_digits_are_limited(self) -> None:
        for digits in (0, 18, True, 1.5):
            with self.subTest(digits=digits):
                with self.assertRaises(ValueError):
                    format_result(1.25, digits)

    def test_non_finite_values_cannot_be_formatted(self) -> None:
        with self.assertRaises(InvalidOperandError):
            format_result(math.inf)


if __name__ == "__main__":
    unittest.main()