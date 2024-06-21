# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    This file contains tests to test the Calculation class
'''

import pytest
from app.calculator.calculation import Calculation
from app.calculator.operations import add, divide

def test_operations(a, b, operation, expected):
    """
        Tests Calculations with all four operations aginst both integers and Decimals.
        This test verifies that the Calculation class and the operation class are working as intended

        @param a: the first operand of the calculation
        @param b: the second operand of the calculation
        @param operation: the operation function to be used in th calculation
        @param expected: the expected result of the calculation
    """

    calc = Calculation.create(a, b, operation)
    assert calc.calculate() == expected, f"Failed {operation.__name__} operation with {a} and {b}"

def test_repr():
    """
        Tests the string representation of the Calculation class
    """
    calc = Calculation.create(6, 2, add)
    expected = "Calculation(6, 2, add)"
    assert calc.__repr__() == expected, "The __repr__ method output does not match the expected string."

def test_divide_by_zero_test():
    """
        Tests division by zero to verify that it returns a ValueError
    """
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Calculation(3, 0, divide).calculate()
