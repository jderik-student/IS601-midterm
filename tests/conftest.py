# conftest.py
# pylint: disable=unnecessary-dunder-call, invalid-name

'''
    This file contains adds a pytest command num_records which generates N number of randomized test data sets
    to test methods that contain the following paramaters ("a", "b", "expected"). If num_records is not specified, it
    is defaulted to produce 10 randome records
'''

from decimal import Decimal
from faker import Faker
from app.calculator.operations import add, subtract, multiply, divide

fake = Faker()

def generate_test_data(num_records):
    """
        Creates N number of randomized test data and the expected value of the randomized calculation

        @param num_records: the specified number of randomized test data sets to produce
    """
    operation_mappings = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2))
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_name]

        if operation_func.__name__ == "divide":
            b = Decimal('1') if b == Decimal('0')  else b

        expected = operation_func(a,b)

        yield a, b, operation_name, operation_func, expected

def pytest_addoption(parser):
    """
        Adds the num_records command to pytest
    """
    parser.addoption("--num_records", action="store", default=10, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    """
        Generates and passes in the specified number of test data sets to functions with following paramaters ("a", "b", "expected")
    """
    if {"a", "b", "expected"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))
        modified_parameters = [(a, b, op_name if 'operation_name' in metafunc.fixturenames else op_func, expected) for a, b, op_name, op_func, expected in parameters]
        metafunc.parametrize("a,b,operation,expected", modified_parameters)
