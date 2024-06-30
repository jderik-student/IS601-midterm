# pylint: disable=unnecessary-dunder-call, invalid-name
"""
    This code defines a Calculator that can add, subtract, multiply, and divide on Decimal numbers
    This Calculator also keeps history of past calculations.
"""

from decimal import Decimal
from typing import Callable
from app.calculator.calculation import Calculation
from app.calculator.calculator_history import CalculatorHistory
from app.calculator.data_manipulator.dataframe_data_manipulator import DataframeManipulator
from app.calculator.data_manipulator.memory_data_manipulator import MemoryDataManipulator
from app.calculator.operations import add, subtract, multiply, divide

class Calculator:
    """
        Class representing a calculator that can add, subtract, multiply, and divide on Decimal numbers.
        This Calculator also keeps history of past calculations. 
    """

    @staticmethod
    def _perform_calculation(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> Decimal:
        """
            Creates an instance of Calculation object based on the two Decimals and operation function given.
            Appends the created Calculation to the Calcultor's history list, dataframe, and csv file.
            Computes the calculation and returns the Decimal value. 

            @param a: the first Decimal number to be used in the calculation
            @param b: the second Decimal number to be used in the calculation
            @param operation: the mathemtical operation to be performed (add, subtract, multiply, or divide)
            @return: the Decimal value of the computed calculation 
        """
        calculation = Calculation.create(a, b, operation)
        CalculatorHistory.append(calculation, MemoryDataManipulator())
        CalculatorHistory.append(calculation, DataframeManipulator())
        return calculation.calculate()

    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        """
            Adds the Decimal in the a variable with the Decimal stored in the b variable.
            Stores the calculation in the calculator's history and returns the result of the addition.

            @param a: the first Addend
            @param b: the second Addend
            @return: the Sum of the computed addition
        """
        return Calculator._perform_calculation(a, b, add)

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        """
            Subtracts the Decimal in the b variable from the Decimal stored in the a variable.
            Stores the calculation in the calculator's history and returns the result of the subtraction.

            @param a: the Minuened
            @param b: the Subtrahend
            @return: the Difference of of the computed subtraction
        """
        return Calculator._perform_calculation(a, b, subtract)

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        """
            Multiplies the Decimal in the a variable by the Decimal stored in the b variable.
            Stores the calculation in the calculator's history and returns the result of the multiplication.

            @param a: the Multiplicand
            @param b: the Multiplicator
            @return: the Product of the computed multiplication
        """
        return Calculator._perform_calculation(a, b, multiply)

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        """
            Divides the Decimal in the a variable by the Decimal stored in the b variable.
            Stores the calculation in the calculator's history and returns the result of the division.

            @param a: the Dividend
            @param b: the Divisor
            @return: the Quotient of the computed division
            @raise: Value Error if b is 0
        """
        return Calculator._perform_calculation(a, b, divide)
