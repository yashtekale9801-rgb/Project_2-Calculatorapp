import math
from enum import Enum
from numbers import Real


DEFAULT_SIGNIFICANT_DIGITS = 12
MAX_SIGNIFICANT_DIGITS = 17


class CalculatorError(Exception):
    code = "calculation_error"


class InvalidOperandError(CalculatorError):
    code = "invalid_operand"

    def __init__(self, operand_name: str) -> None:
        self.operand_name = operand_name
        super().__init__(f"{operand_name} must be a finite real number.")


class UnsupportedOperationError(CalculatorError):
    code = "unsupported_operation"

    def __init__(self, operation: object) -> None:
        self.operation = operation
        super().__init__(f"Unsupported operation: {operation!r}.")


class DivisionByZeroError(CalculatorError):
    code = "division_by_zero"

    def __init__(self) -> None:
        super().__init__("Cannot divide by zero.")


class CalculationOverflowError(CalculatorError):
    code = "non_finite_result"

    def __init__(self) -> None:
        super().__init__("The calculation result is outside the supported numeric range.")


class Operation(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

    @property
    def symbol(self) -> str:
        return {
            Operation.ADD: "+",
            Operation.SUBTRACT: "-",
            Operation.MULTIPLY: "*",
            Operation.DIVIDE: "/",
        }[self]


def _finite_float(value: Real, operand_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise InvalidOperandError(operand_name)

    try:
        number = float(value)
    except (OverflowError, ValueError):
        raise InvalidOperandError(operand_name) from None

    if not math.isfinite(number):
        raise InvalidOperandError(operand_name)
    return number


def _normalize_operation(operation: Operation | str) -> Operation:
    try:
        return operation if isinstance(operation, Operation) else Operation(operation)
    except (TypeError, ValueError):
        raise UnsupportedOperationError(operation) from None


def calculate(
    first_operand: Real,
    second_operand: Real,
    operation: Operation | str,
) -> float:
    """Calculate one basic arithmetic operation using finite binary64 values."""
    first = _finite_float(first_operand, "First operand")
    second = _finite_float(second_operand, "Second operand")
    selected_operation = _normalize_operation(operation)

    if selected_operation is Operation.DIVIDE and second == 0:
        raise DivisionByZeroError

    try:
        if selected_operation is Operation.ADD:
            result = first + second
        elif selected_operation is Operation.SUBTRACT:
            result = first - second
        elif selected_operation is Operation.MULTIPLY:
            result = first * second
        else:
            result = first / second
    except OverflowError:
        raise CalculationOverflowError from None

    if not math.isfinite(result):
        raise CalculationOverflowError
    return result


def add(num1: Real, num2: Real) -> float:
    """Compatibility helper for the original addition API."""
    return calculate(num1, num2, Operation.ADD)


def format_result(value: Real, significant_digits: int = DEFAULT_SIGNIFICANT_DIGITS) -> str:
    """Format a finite result to 1-17 significant digits (12 by default)."""
    if isinstance(significant_digits, bool) or not isinstance(significant_digits, int):
        raise ValueError("Significant digits must be an integer from 1 to 17.")
    if not 1 <= significant_digits <= MAX_SIGNIFICANT_DIGITS:
        raise ValueError("Significant digits must be an integer from 1 to 17.")

    number = _finite_float(value, "Result")
    if number == 0:
        return "0"
    return format(number, f".{significant_digits}g")