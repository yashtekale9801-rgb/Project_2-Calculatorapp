# -*- coding: utf-8 -*-

from calculator_core import CalculatorError, add

if __name__ == "__main__":
    num1 = float(input("First number "))
    num2 = float(input("Second number "))
    try:
        print(add(num1, num2))
    except CalculatorError as error:
        print(f"Error: {error}")