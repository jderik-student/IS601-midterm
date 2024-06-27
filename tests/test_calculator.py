# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    This file contains tests to test the Calculator
'''

import os
import pytest
import singleton
from app.calculator import Calculator


@pytest.fixture(scope="class", autouse=True)
def setup_calc_history_path_location():
    """Sets up the csv files needed to run the tests"""
    singleton.calc_history_path_location = "tests/csv_test_data_output.csv"
    yield

    if os.path.exists(singleton.calc_history_path_location):
        os.remove(singleton.calc_history_path_location)

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
