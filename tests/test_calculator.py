# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    This file contains tests to test the Calculator
'''

import pytest
from app.calculator import Calculator


def test_add():
    '''Test that addition function works '''    
    assert Calculator.add(6,2) == 8, "Addition failed"

def test_subtract():
    '''Test that subtraction function works '''    
    assert Calculator.subtract(6,2) == 4, "Subtraction failed"

def test_multiply():
    '''Test that multiplication function works '''    
    assert Calculator.multiply(6,2) == 12, "Multiplication failed"

def test_division_nonZero_Divisor():
    '''Test that division function works with a non-zero Divisor'''    
    assert Calculator.divide(6,2) == 3, "Division failed"

def test_division_Zero_Divisor():
    '''Test that division function works '''    
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Calculator.divide(6,0)
