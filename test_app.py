import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from calculator_core import Operation


class CalculatorAppTests(unittest.TestCase):
    def create_app(self) -> AppTest:
        app_path = Path(__file__).with_name("app.py")
        return AppTest.from_file(str(app_path)).run()

    def test_each_basic_operation_is_displayed(self) -> None:
        cases = (
            (Operation.ADD, "8 + 2 = 10"),
            (Operation.SUBTRACT, "8 - 2 = 6"),
            (Operation.MULTIPLY, "8 * 2 = 16"),
            (Operation.DIVIDE, "8 / 2 = 4"),
        )
        for operation, expected_equation in cases:
            with self.subTest(operation=operation):
                app = self.create_app()
                app.number_input[0].set_value(8)
                app.number_input[1].set_value(2)
                app.radio[0].set_value(operation)
                app.button[0].click().run()

                self.assertFalse(app.exception)
                self.assertIn(expected_equation, app.markdown[-1].value)

    def test_division_by_zero_preserves_operands(self) -> None:
        app = self.create_app()
        app.number_input[0].set_value(8)
        app.number_input[1].set_value(0)
        app.radio[0].set_value(Operation.DIVIDE)
        app.button[0].click().run()

        self.assertFalse(app.exception)
        self.assertEqual(app.error[0].value, "Cannot divide by zero.")
        self.assertEqual(app.number_input[0].value, 8)
        self.assertEqual(app.number_input[1].value, 0)

        app.number_input[1].set_value(2)
        app.button[0].click().run()

        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertIn("8 / 2 = 4", app.markdown[-1].value)

    def test_clear_resets_operands_and_operation(self) -> None:
        app = self.create_app()
        app.number_input[0].set_value(8)
        app.number_input[1].set_value(2)
        app.radio[0].set_value(Operation.MULTIPLY)
        app.button[0].click().run()

        app.button[1].click().run()

        self.assertFalse(app.exception)
        self.assertEqual(app.number_input[0].value, 0)
        self.assertEqual(app.number_input[1].value, 0)
        self.assertEqual(app.radio[0].value, Operation.ADD)
        self.assertFalse(app.error)
        self.assertNotIn("Your result", " ".join(item.value for item in app.markdown))


if __name__ == "__main__":
    unittest.main()