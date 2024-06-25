# pylint: disable=unnecessary-dunder-call, invalid-name, unused-argument
'''
    This file contains tests to test the CalculationHistory class
'''

import os
from decimal import Decimal
import pandas as pd
import pytest
import singleton
from app.calculator.calculation import Calculation
from app.calculator.calculator_history import CalculatorHistory
from app.calculator.data_manipulator.dataframe_data_manipulator import DataframeManipulator
from app.calculator.operations import add, divide, multiply, subtract


@pytest.fixture(scope="session", autouse=True)
def setup_calc_history_path_location():
    """Sets up the csv files needed to run the tests"""
    singleton.calc_history_path_location = "tests/csv_test_data_output.csv"
    yield

    if os.path.exists(singleton.calc_history_path_location):
        os.remove(singleton.calc_history_path_location)

@pytest.fixture(name="setup")
def setup_history():
    """First clears the history and setups the history for each test"""
    CalculatorHistory.delete_history(DataframeManipulator())
    CalculatorHistory.append(Calculation.create(Decimal('1'), Decimal('2'), add), DataframeManipulator())
    CalculatorHistory.append(Calculation.create(Decimal('3'), Decimal('4'), subtract), DataframeManipulator())
    CalculatorHistory.append(Calculation.create(Decimal('5'), Decimal('6'), multiply), DataframeManipulator())
    CalculatorHistory.append(Calculation.create(Decimal('7'), Decimal('8'), divide), DataframeManipulator())

def test_append(setup):
    """Test appending a Calculation to the history"""
    calculation = Calculation.create(Decimal('9'), Decimal('10'), add)
    CalculatorHistory.append(calculation, DataframeManipulator())

    df = CalculatorHistory.get_dataframe()
    last_calc = df.iloc[-1]
    assert len(df) == 5, "Calculation was not appended to dataframe"
    assert last_calc["Operation"] == "add", "Calculation's operation was not appended dataframe"
    assert last_calc["Operand1"] == 9, "Calculation's Operand1 was not appended to dataframe correctly"
    assert last_calc["Operand2"] == 10, "Calculation's Operand2 was not appended to dataframe correctly"

    df = pd.read_csv(singleton.calc_history_path_location, header=0)
    last_calc = df.iloc[-1]
    assert len(df) == 5, "Calculation was not appended to csv"
    assert last_calc["Operation"] == "add", "Calculation's operation was not appended to csv correctly"
    assert last_calc["Operand1"] == 9, "Calculation's Operand1 was not appended to csv correctly"
    assert last_calc["Operand2"] == 10, "Calculation's Operand2 was not appended to csv correctly"

def test_get_history(setup):
    """Test getting the entire calculation history"""
    assert len(CalculatorHistory.get_dataframe()) == 4, "Dataframe does not contain the expected number of calculations (4)"
    df = pd.read_csv(singleton.calc_history_path_location, header=0)
    assert len(df) == 4, "csv does not contain the expected number of calculations (4)"

def test_delete_history(setup):
    """Test deleting the entire calculation history"""
    CalculatorHistory.delete_history(DataframeManipulator())
    assert len(CalculatorHistory.get_dataframe()) == 0, "Failed to delete dataframe"
    df = pd.read_csv(singleton.calc_history_path_location, header=0)
    assert len(df) == 0, "Failed to clear csv"
