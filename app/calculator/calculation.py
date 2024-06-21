# pylint: disable=unnecessary-dunder-call, invalid-name
"""
    Class representing a calculation which stores the two Decimal values to be used and the operation to be preformed 
"""

from decimal import Decimal
from typing import Callable

class Calculation:
    """
        Class representing a calculation which stores the two Decimal values to be used and the operation to be preformed 
    """

    def __init__(self, a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """
            Initalizes a Calculation

            @param a: the first Decimal number to be used in the calculation
            @param b: the second Decimal number to be used in the calculation
            @param operation: the mathemtical operation to be performed (add, subtract, multiply, or divide)
        """
        self.a = a
        self.b = b
        self.operation = operation

    @staticmethod
    def create(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """
            Factory method used to create instances of a Calculation

            @param a: the first Decimal number to be used in the calculation
            @param b: the second Decimal number to be used in the calculation
            @param operation: the mathemtical operation to be performed (add, subtract, multiply, or divide)
            @return: the newly created instance of a Calculation 
        """
        return Calculation(a, b, operation)

    def calculate(self) -> Decimal:
        """
            Preforms the calclation based on the two terms and the operation function stored in the Calculation object

            @return: the Decimal result of the preformed calculation
        """
        return self.operation(self.a, self.b)

    def __repr__(self):
        """
            String representation of a Calculation

            @return: String representation of a Calculation
        """
        return f"Calculation({self.a}, {self.b}, {self.operation.__name__})"
