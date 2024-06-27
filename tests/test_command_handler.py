# pylint: disable=unnecessary-dunder-call, invalid-name, unused-argument, unused-variable
'''
    This file contains tests to test the CommandHandler class
'''

import os
import pytest
import singleton
from app.commands import CommandHandler
from app.plugins.add import AddCommand
from app.plugins.clearHistory import ClearHistoryCommand
from app.plugins.divide import DivideCommand
from app.plugins.loadHistory import LoadHistoryCommand


@pytest.fixture(scope="class", autouse=True)
def setup_calc_history_path_location():
    """Sets up the tests by registering one command and setting up csv output file"""
    handler = CommandHandler()
    handler.register_command("add", AddCommand())
    singleton.calc_history_path_location = "tests/csv_test_data_output.csv"
    yield

    if os.path.exists(singleton.calc_history_path_location): # pragma: no cover
        os.remove(singleton.calc_history_path_location)

def test_register_command_and_list_command(capfd):
    """Tests registering a command to the CommandHandler and listing out all the registered commands"""
    handler = CommandHandler()
    handler.list_commands()
    out, err = capfd.readouterr()
    assert out == "Commands:\n- add\n", "Did not succesfully register and list out the AddCommand"

def test_execute_command(capfd):
    """Tests the execute_command method as well as the exceptions it catches"""
    handler = CommandHandler()
    handler.register_command("divide", DivideCommand())
    handler.register_command("loadHistory", LoadHistoryCommand())

    handler.execute_command(["add", "1", "2"])
    out, err = capfd.readouterr()
    assert out == "The result of 1 plus 2 is equal to 3\n", "The AddCommand should print 'The result of 1 plus 2 is equal to 3'"

    handler.execute_command(["add"])
    out, err = capfd.readouterr()
    assert out == "ERROR Usage: <operation> <number1> <number2>\n", "IndexError was expected"

    handler.execute_command(["divide", "1", "0"])
    out, err = capfd.readouterr()
    assert out == "Cannot divide by zero\n", "ValueError was expected"

    handler.execute_command(["divide", "a", "b"])
    out, err = capfd.readouterr()
    assert out == "Invalid number input: a or b is not a valid number.\n", "InvalidOperation was expected"

    handler.execute_command(["notACommand", "1", "2"])
    out, err = capfd.readouterr()
    assert out == "No such command: notACommand\n", "KeyError was expected"

    handler.execute_command(["loadHistory", "notARealFile.csv"])
    out, err = capfd.readouterr()
    assert out == "No such file or directory: notARealFile.csv\n", "FileNotFoundError was expected"

    handler.execute_command(["loadHistory", "tests/csv_invalid_format.csv"])
    out, err = capfd.readouterr()
    assert out == "Failed to load history from tests/csv_invalid_format.csv\nCSV Invalid Format | Column Not Found 'Operand1'\n", "CSV Invalid Format (KeyError) was expected"

    handler.remove_command("add")
    handler.remove_command("divide")
    handler.remove_command("loadHistory")
    ClearHistoryCommand().execute([])
