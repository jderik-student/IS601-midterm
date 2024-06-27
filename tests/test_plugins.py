# pylint: disable=unnecessary-dunder-call, invalid-name, unused-variable, unused-argument, line-too-long, duplicate-code
'''
    This file contains tests to test the all the Commands in the commands directory except the ExitCommand which is tested in test_app.py
'''

import os
from decimal import Decimal

import pandas as pd
import pytest

from app.plugins.deleteCalculation import DeleteCalculationCommand
from app.plugins.getCalculation import GetCalculationCommand
import singleton
from app.calculator.calculator_history import CalculatorHistory
from app.commands import CommandHandler
from app.plugins.add import AddCommand
from app.plugins.clearHistory import ClearHistoryCommand
from app.plugins.divide import DivideCommand
from app.plugins.loadHistory import LoadHistoryCommand
from app.plugins.menu import MenuCommand
from app.plugins.multiply import MultiplyCommand
from app.plugins.printHistory import PrintHistoryCommand
from app.plugins.saveHistory import SaveHistoryCommand
from app.plugins.subtract import SubtractCommand


@pytest.fixture(scope="class", autouse=True)
def setup_calc_history_path_location():
    """Sets up the tests by registering one command and setting up csv output file"""
    singleton.calc_history_path_location = "tests/csv_test_data_output.csv"
    yield

    if os.path.exists(singleton.calc_history_path_location):
        os.remove(singleton.calc_history_path_location)


def test_add_command(capfd):
    """Tests the AddCommand"""
    command = AddCommand()
    command.execute([Decimal(1), Decimal(2)])
    out, err = capfd.readouterr()
    assert out == "The result of 1 plus 2 is equal to 3\n", "The AddCommand should print 'The result of 1 plus 2 is equal to 3'"


def test_subtract_command(capfd):
    """Tests the SubtractCommand"""
    command = SubtractCommand()
    command.execute([Decimal(3), Decimal(2)])
    out, err = capfd.readouterr()
    assert out == "The result of 3 minus 2 is equal to 1\n", "The SubtractCommand should print 'The result of 3 minus 2 is equal to 1'"

def test_multiply_command(capfd):
    """Tests the MultiplyCommand"""
    command = MultiplyCommand()
    command.execute([Decimal(2), Decimal(4)])
    out, err = capfd.readouterr()
    assert out == "The result of 2 times 4 is equal to 8\n", "The MultiplyCommand should print 'The result of 2 times 4 is equal to 8'"

def test_divide_command(capfd):
    """Tests the DivideCommand"""
    command = DivideCommand()
    command.execute([Decimal(12), Decimal(4)])
    out, err = capfd.readouterr()
    assert out == "The result of 12 divided by 4 is equal to 3\n", "The DivideCommand should print 'The result of 12 divided by 4 is equal to 3'"

def test_print_history_command(capfd):
    """Tests the PrintHistoryCommand"""
    command = PrintHistoryCommand()
    command.execute([])
    out, err = capfd.readouterr()
    assert out == "1) Calculation(1, 2, add)\n2) Calculation(3, 2, subtract)\n3) Calculation(2, 4, multiply)\n4) Calculation(12, 4, divide)\n", "The GetHistoryCommand should've printed 4 Calculations"

def test_get_calculation_command(capfd):
    """Tests the PrintHistoryCommand"""
    command = GetCalculationCommand()
    command.execute([1])
    out, err = capfd.readouterr()
    assert out == "The result of Calculation(1, 2, add) is equal to 3\n", "The GetCalculationCommand should've printed 'The result of Calculation(1, 2, add) is equal to 3'"
    command.execute([100])
    out, err = capfd.readouterr()
    assert out == "Invalid Calculation Number: 100\n", "The GetCalculationCommand should've printed 'Invalid Calculation Number: 100'"
    command.execute(["a"])
    out, err = capfd.readouterr()
    assert "ValueError" in out, "The GetCalculationCommand should have got a ValueError"

def test_delete_calculation_command(capfd):
    """Tests the PrintHistoryCommand"""
    command = DeleteCalculationCommand()
    command.execute([1])
    out, err = capfd.readouterr()
    assert out == "Calculation #1 was deleted\n", "The GetCalculationCommand should've printed 'The result of Calculation(1, 2, add) is equal to 3'"
    command.execute([100])
    out, err = capfd.readouterr()
    assert out == "Invalid Calculation Number: 100\n", "The GetCalculationCommand should've printed 'Invalid Calculation Number: 100'"
    command.execute(["a"])
    out, err = capfd.readouterr()
    assert "a is not a valid number\n" == out, "The GetCalculationCommand should've printed 'a is not a valid number'"

def test_clear_history_command(capfd):
    """Tests the ClearHistoryCommand"""
    command = ClearHistoryCommand()
    command.execute([])
    out, err = capfd.readouterr()
    assert out == "History Cleared\n", "The ClearHistoryCommand should have been deleted the history"
    assert len(CalculatorHistory.get_history()) == 0, "The History List should have been cleared"
    assert len(CalculatorHistory.get_dataframe()) == 0, "The Calculator History Dataframe should have been cleared"
    assert len(pd.read_csv(singleton.calc_history_path_location)) == 0, "The CSV file should been cleared"

def test_load_history_command(capfd):
    """Tests the LoadHistoryCommand"""
    command = LoadHistoryCommand()
    command.execute(["tests/csv_test_data_read_input.csv"])
    out, err = capfd.readouterr()
    assert out == "History Loaded from tests/csv_test_data_read_input.csv\n", "The ClearHistoryCommand should have been deleted the history"
    df = CalculatorHistory.get_dataframe()
    first_calculation = df.iloc[0]
    second_calculation = df.iloc[1]
    third_calculation = df.iloc[2]
    fourth_calculation = df.iloc[3]
    assert first_calculation["Operand1"] == Decimal('1') and first_calculation["Operand2"] == Decimal('2') and first_calculation["Operation"]== "add", "Failed to load the Calculation at row 1 of the dataframe"
    assert second_calculation["Operand1"] == Decimal('3') and second_calculation["Operand2"] == Decimal('4') and second_calculation["Operation"] == "subtract", "Failed to load the Calculation at row 2 of the dataframe"
    assert third_calculation["Operand1"] == Decimal('5') and third_calculation["Operand2"] == Decimal('6') and third_calculation["Operation"] == "multiply", "Failed to load Calculation at row 3 of the dataframe"
    assert fourth_calculation["Operand1"] == Decimal('7') and fourth_calculation["Operand2"] == Decimal('8') and fourth_calculation["Operation"] == "divide", "Failed to load Calculation at row 4 of the dataframe"
    first_calculation = CalculatorHistory.get_ith_calculation(0)
    second_calculation = CalculatorHistory.get_ith_calculation(1)
    third_calculation = CalculatorHistory.get_ith_calculation(2)
    fourth_calculation = CalculatorHistory.get_ith_calculation(3)
    assert first_calculation.a == Decimal('1') and first_calculation.b == Decimal('2') and first_calculation.operation.__name__ == "add", "Failed to load the Calculation at index 0 in History List"
    assert second_calculation.a == Decimal('3') and second_calculation.b == Decimal('4') and second_calculation.operation.__name__ == "subtract", "Failed to load the Calculation at index 1 in History List"
    assert third_calculation.a == Decimal('5') and third_calculation.b == Decimal('6') and third_calculation.operation.__name__ == "multiply", "Failed to load Calculation at index 2 in History List"
    assert fourth_calculation.a == Decimal('7') and fourth_calculation.b == Decimal('8') and fourth_calculation.operation.__name__ == "divide", "Failed to load Calculation at index 3 in History List"
    assert pd.read_csv("tests/csv_test_data_read_input.csv").equals(pd.read_csv(singleton.calc_history_path_location)), "Calc_history.csv write failed"

def test_save_history_command(capfd):
    """Tests the SaveHistoryCommand"""
    df = pd.DataFrame({'Operand1': [1, 2, 3],
                         'Operand2': [4, 5, 6],
                         'Operation': ['add', 'subtract', 'add']})
    CalculatorHistory.dataframe = df
    command = SaveHistoryCommand()
    command.execute([singleton.calc_history_path_location])
    out, err = capfd.readouterr()
    assert out == f"History Saved to {singleton.calc_history_path_location}\n", "The ClearHistoryCommand should have been deleted the history"
    CalculatorHistory.load_history_from_csv(singleton.calc_history_path_location)
    first_calculation = CalculatorHistory.get_ith_calculation(0)
    second_calculation = CalculatorHistory.get_ith_calculation(1)
    third_calculation = CalculatorHistory.get_ith_calculation(2)
    assert first_calculation.a == Decimal('1') and first_calculation.b == Decimal('4') and first_calculation.operation.__name__ == "add", "Failed to load the Calculation at index 0 in History List"
    assert second_calculation.a == Decimal('2') and second_calculation.b == Decimal('5') and second_calculation.operation.__name__ == "subtract", "Failed to load the Calculation at index 1 in History List"
    assert third_calculation.a == Decimal('3') and third_calculation.b == Decimal('6') and third_calculation.operation.__name__ == "add", "Failed to load Calculation at index 2 in History List"

def test_menu_command(capfd):
    """Tests the MenuCommand"""
    handler = CommandHandler()
    handler.register_command("Command1", None)
    handler.register_command("Command2", None)
    handler.register_command("Command3", None)
    command = MenuCommand(handler)
    command.execute([])
    out, err = capfd.readouterr()
    assert out == "Commands:\n- Command1\n- Command2\n- Command3\n", "The MenuCommand should have printed three commands"
    handler.remove_command("Command1")
    handler.remove_command("Command2")
    handler.remove_command("Command3")
