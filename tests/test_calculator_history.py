# pylint: disable=unnecessary-dunder-call, invalid-name, unused-argument, line-too-long, duplicate-code
'''
    This file contains tests to test the CalculationHistory class (Core functionality and the MemoryDataManipulator)
'''

from decimal import Decimal
import pandas as pd
import pytest
import singleton
from app.calculator.calculation import Calculation
from app.calculator.calculator_history import CalculatorHistory
from app.calculator.data_manipulator.memory_data_manipulator import \
    MemoryDataManipulator
from app.calculator.operations import add, divide, multiply, subtract


@pytest.fixture(name="setup")
def setup_history():
    """First clears the history and setups the history for each test"""
    CalculatorHistory.delete_history(MemoryDataManipulator())
    CalculatorHistory.append(Calculation.create(Decimal('1'), Decimal('2'), add), MemoryDataManipulator())
    CalculatorHistory.append(Calculation.create(Decimal('3'), Decimal('4'), subtract), MemoryDataManipulator())
    CalculatorHistory.append(Calculation.create(Decimal('5'), Decimal('6'), multiply), MemoryDataManipulator())
    CalculatorHistory.append(Calculation.create(Decimal('7'), Decimal('8'), divide), MemoryDataManipulator())

def test_append(setup):
    """Test appending a Calculation to the history list"""
    calculation = Calculation.create(Decimal('9'), Decimal('10'), add)
    CalculatorHistory.append(calculation, MemoryDataManipulator())

    assert CalculatorHistory.get_last_calculation() == calculation, "Failed to append the Calculation to the history list"

def test_get_last_calculation(setup):
    """Test getting the most recent calculation in the history list"""
    last_calculation = CalculatorHistory.get_last_calculation()
    assert last_calculation.a == Decimal('7') and last_calculation.b == Decimal('8') and last_calculation.operation.__name__ == "divide", "Failed to get the correct most recent Calculation"

def test_get_last_calculation_with_empty_history():
    """Test getting the most recent calculation in the history with an empty history list"""
    CalculatorHistory.delete_history(MemoryDataManipulator())
    last_calculation = CalculatorHistory.get_last_calculation()
    assert last_calculation is None, "Expected None to be returned"

def test_get_history(setup):
    """Test getting the entire calculation history"""
    assert len(CalculatorHistory.get_history()) == 4, "History list does not contain the expected number of calculations (4)"

def test_delete_calculation_at_index(setup):
    """Test getting the entire calculation history"""
    CalculatorHistory.delete_calculation_at_index(1, MemoryDataManipulator())
    second_calculation = CalculatorHistory.get_ith_calculation(1)
    assert len(CalculatorHistory.get_history()) == 3, "History list does not contain the expected number of calculations (3)"
    assert second_calculation.a == Decimal('5') and second_calculation.b == Decimal('6') and second_calculation.operation.__name__ == "multiply", "Failed to delete the correct Calculation in history list"

def test_delete_history(setup):
    """Test deleting the entire calculation history"""
    CalculatorHistory.delete_history(MemoryDataManipulator())
    assert len(CalculatorHistory.get_history()) == 0, "Failed to delete history list"

def test_find_by_operation(setup):
    """Test getting the history by each opearation"""
    add_operation = CalculatorHistory.find_by_opreation("add")
    subtract_operation = CalculatorHistory.find_by_opreation("subtract")
    multiply_operation = CalculatorHistory.find_by_opreation("multiply")
    divide_operation = CalculatorHistory.find_by_opreation("divide")

    assert len(add_operation) == 1, "Did not find the correct number of calculations with the add operation"
    assert len(subtract_operation) == 1, "Did not find the correct number of calculations with the subtract operation"
    assert len(multiply_operation) == 1, "Did not find the correct number of calculations with the mulitply operation"
    assert len(divide_operation) == 1, "Did not find the correct number of calculations with the divide operation"

def test_get_ith_calculation(setup):
    """Test getting the ith Calculation in the history"""
    first_calculation = CalculatorHistory.get_ith_calculation(0)
    second_calculation = CalculatorHistory.get_ith_calculation(1)
    third_calculation = CalculatorHistory.get_ith_calculation(2)
    fourth_calculation = CalculatorHistory.get_ith_calculation(3)
    assert first_calculation.a == Decimal('1') and first_calculation.b == Decimal('2') and first_calculation.operation.__name__ == "add", "Failed to get the Calculation at index 0"
    assert second_calculation.a == Decimal('3') and second_calculation.b == Decimal('4') and second_calculation.operation.__name__ == "subtract", "Failed to get the Calculation at index 1"
    assert third_calculation.a == Decimal('5') and third_calculation.b == Decimal('6') and third_calculation.operation.__name__ == "multiply", "Failed to get the Calculation at index 2"
    assert fourth_calculation.a == Decimal('7') and fourth_calculation.b == Decimal('8') and fourth_calculation.operation.__name__ == "divide", "Failed to get the Calculation at index 3"

def test_load_from_csv(setup):
    """Tests that the CalculatorHistory is properly populated from a csv file"""
    CalculatorHistory.load_history_from_csv("tests/csv_test_data_read_input.csv")
    first_calculation = CalculatorHistory.get_ith_calculation(0)
    second_calculation = CalculatorHistory.get_ith_calculation(1)
    third_calculation = CalculatorHistory.get_ith_calculation(2)
    fourth_calculation = CalculatorHistory.get_ith_calculation(3)
    assert first_calculation.a == Decimal('1') and first_calculation.b == Decimal('2') and first_calculation.operation.__name__ == "add", "Failed to load the Calculation at index 0 in History List"
    assert second_calculation.a == Decimal('3') and second_calculation.b == Decimal('4') and second_calculation.operation.__name__ == "subtract", "Failed to load the Calculation at index 1 in History List"
    assert third_calculation.a == Decimal('5') and third_calculation.b == Decimal('6') and third_calculation.operation.__name__ == "multiply", "Failed to load Calculation at index 2 in History List"
    assert fourth_calculation.a == Decimal('7') and fourth_calculation.b == Decimal('8') and fourth_calculation.operation.__name__ == "divide", "Failed to load Calculation at index 3 in History List"
    df = CalculatorHistory.get_dataframe()
    first_calculation = df.iloc[0]
    second_calculation = df.iloc[1]
    third_calculation = df.iloc[2]
    fourth_calculation = df.iloc[3]
    assert first_calculation["Operand1"] == Decimal('1') and first_calculation["Operand2"] == Decimal('2') and first_calculation["Operation"]== "add", "Failed to load the Calculation at row 1 of the dataframe"
    assert second_calculation["Operand1"] == Decimal('3') and second_calculation["Operand2"] == Decimal('4') and second_calculation["Operation"] == "subtract", "Failed to load the Calculation at row 2 of the dataframe"
    assert third_calculation["Operand1"] == Decimal('5') and third_calculation["Operand2"] == Decimal('6') and third_calculation["Operation"] == "multiply", "Failed to load Calculation at row 3 of the dataframe"
    assert fourth_calculation["Operand1"] == Decimal('7') and fourth_calculation["Operand2"] == Decimal('8') and fourth_calculation["Operation"] == "divide", "Failed to load Calculation at row 4 of the dataframe"
    assert pd.read_csv("tests/csv_test_data_read_input.csv").equals(pd.read_csv(singleton.calc_history_path_location)), "Calc_history.csv write failed"
