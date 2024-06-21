# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    This code defines the logic to preform the four mathematical operations:
    add, subtract, multiply, and divide 
'''

from decimal import Decimal

def add(a: Decimal,b: Decimal) -> Decimal:
    """
        Adds the Decimal in the a variable with the Decimal stored in the b variable.

        @param a: the first Addend
        @param b: the second Addend
        @return: the Sum of the computed addition
    """
    return a + b

def subtract(a: Decimal,b: Decimal) -> Decimal:
    """
        Subtracts the Decimal in the b variable from the Decimal stored in the a variable.

        @param a: the Minuened
        @param b: the Subtrahend
        @return: the Difference of of the computed subtraction
    """
    return a - b

def multiply(a: Decimal,b: Decimal) -> Decimal:
    """
        Multiplies the Decimal in the a variable by the Decimal stored in the b variable.

        @param a: the Multiplicand
        @param b: the Multiplicator
        @return: the Product of the computed multiplication
    """
    return a * b

def divide(a: Decimal,b: Decimal) -> Decimal:
    """
        Divides the Decimal in the a variable by the Decimal stored in the b variable.

        @param a: the Dividend
        @param b: the Divisor
        @return: the Quotient of the computed division
        @raise: Value Error if b is 0
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
