# pylint: disable=invalid-name
'''
    Stores singleton variables that are to be used throughout the app
'''
from app.calculator.operations import add, subtract, multiply, divide


calc_history_path_location = ""
operation_mappings = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
