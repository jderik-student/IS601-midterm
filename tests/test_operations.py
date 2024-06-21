# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    This file contains tests to test the Operations file
'''

import pytest
from app.calculator.operations import add, multiply, subtract, divide

def test_add():
    '''Test that addition function works '''    
    assert add(6,2) == 8, "Addition failed"

def test_subtract():
    '''Test that subtraction function works '''    
    assert subtract(6,2) == 4, "Subtraction failed"

def test_multiply():
    '''Test that multiplication function works '''    
    assert multiply(6,2) == 12, "Multiplication failed"

def test_division_nonZero_divisor():
    '''Test that division function works with a non-zero Divisor'''    
    assert divide(6,2) == 3, "Division Failed"

def test_division_zero_divisor():
    '''Test that division function works '''    
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(6,0)
