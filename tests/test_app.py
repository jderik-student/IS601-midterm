# pylint: disable=unnecessary-dunder-call, invalid-name, unused-argument
'''
    This file contains tests to test app.py
'''
import os
from unittest import mock
import logging
import pandas as pd
import pytest

import singleton
from app import App
from app.commands import CommandHandler

def test_app_start(monkeypatch):
    """Test that the app starts correctly and intailizes everything needed to run the app."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    current_env = app.get_environment_variable('ENVIRONMENT')
    current_user = app.get_environment_variable('USERNAME')
    assert current_env in ['DEV', 'PROD'], f"Invalid ENVIRONMENT: {current_env}"
    assert current_user in ['jderik-local', 'jderik-dev', 'jderik-prod'], f"Invalid USERNAME: {current_user}"
    assert os.path.exists(os.path.dirname(singleton.calc_history_path_location)), "Data directory was not created"
    assert os.path.exists(singleton.calc_history_path_location), "Calculator History csv file was not created"
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

def test_keyboard_interrupt(monkeypatch, caplog):
    """Test that the REPL exits correctly with a keyboard interrupt"""
    monkeypatch.setattr('builtins.input', mock.Mock(side_effect=KeyboardInterrupt))
    app = App()

    with caplog.at_level(logging.INFO):
        with pytest.raises(SystemExit) as e:
            app.start()

    assert e.type == SystemExit

def test_app_get_environment_variable():
    """Tests if the .env file was loaded correctly"""
    app = App()
    current_env = app.get_environment_variable('ENVIRONMENT')
    assert current_env in ['DEV', 'TESTING', 'PROD'], f"Invalid ENVIRONMENT: {current_env}"

@pytest.fixture(scope="class", autouse=True)
def setup():
    """Sets up the test_app_full_workflow test"""
    singleton.calc_history_path_location = "data/calc_history.csv"
    with open(singleton.calc_history_path_location, encoding="utf-8", mode='w') as file:
        file.write("Operand1,Operand2,Operation\n1,2,add\n3,4,subtract")
    yield

    print(singleton.calc_history_path_location)
    if os.path.exists(singleton.calc_history_path_location): # pragma: no cover
        os.remove(singleton.calc_history_path_location)
    CommandHandler().commands.clear()


def test_app_full_workflow(capfd, monkeypatch):
    """Test that the goes through a sample workflow of the REPL app"""
    output_test_file = "tests/test_output.csv"

    inputs = iter([
        'printHistory',
        'getCalculation 2',
        'deleteCalculation 1',
        'printHistory',
        'add 1 2',
        'subtract 3 1',
        'divide 12 4',
        'multiply 2 4',
        'printHistory',
        'clearHistory',
        'printHistory',
        'loadHistory tests/csv_test_data_read_input.csv',
        f"saveHistory {output_test_file}",
        'menu',
        'exit'
    ])

    expected_output = [
        "History loaded from",
        "\nCommands:\n- add\n- clearHistory\n- deleteCalculation\n- divide\n- exit\n" \
        "- getCalculation\n- loadHistory\n- menu\n- multiply\n- printHistory\n- saveHistory\n- subtract\nType 'exit' to exit.\n",
        "1) Calculation(1, 2, add)\n2) Calculation(3, 4, subtract)\n",
        "The result of Calculation(3, 4, subtract) is equal to -1\n",
        "Calculation #1 was deleted\n",
        "1) Calculation(3, 4, subtract)\n",
        "The result of 1 plus 2 is equal to 3\n",
        "The result of 3 minus 1 is equal to 2\n",
        "The result of 12 divided by 4 is equal to 3\n",
        "The result of 2 times 4 is equal to 8\n",
        "1) Calculation(3, 4, subtract)\n2) Calculation(1, 2, add)\n3) Calculation(3, 1, subtract)\n4) Calculation(12, 4, divide)\n5) Calculation(2, 4, multiply)\n",
        "\n",
        "",
        "History loaded from tests/csv_test_data_read_input.csv\n",
        f"History Saved to {output_test_file}\n",
        "Commands:\n- add\n- clearHistory\n- deleteCalculation\n- divide\n- exit\n- getCalculation\n- loadHistory\n- menu\n- multiply\n- printHistory\n- saveHistory\n- subtract\n"
    ]

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()

    with pytest.raises(SystemExit) as e:
        app.start()

    captured = capfd.readouterr()
    for output in expected_output:
        assert output in captured.out, f"Expected: {output}"
    assert e.type == SystemExit
    assert str(e.value) == "Exiting...", "The app did not exit as expected"
    assert pd.read_csv(output_test_file).equals(pd.read_csv("tests/csv_test_data_read_input.csv")), "loadHistory command failed"

    if os.path.exists(output_test_file): # pragma: no cover
        os.remove(output_test_file)
