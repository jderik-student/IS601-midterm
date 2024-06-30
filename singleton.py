# pylint: disable=invalid-name
'''
    Stores singleton variables that are to be used throughout the app
'''
from app.calculator.operations import add, subtract, multiply, divide


CALC_HISTORY_FILE_PATH = ""
OPERATION_MAPPINGS = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
