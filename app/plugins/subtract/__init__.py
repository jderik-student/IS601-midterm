# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    Defines the REPL command to preform subtraction on two numbers
'''

from decimal import Decimal
import logging
from app.commands import Command
from app.calculator import Calculator

class SubtractCommand(Command):
    """
        This class extends the Abstract Command Class and preforms subtraction based on user input
    """
    def execute(self, user_input):
        """
            Preforms subtraction on the first two numbers defined in the user_input list and prints the result of the calculation

            @param user_input: a list of numbers to be subtracted specified by the user, expectation is that there should be only two elements in the list
        """
        operand_1 = Decimal(user_input[0])
        operand_2 = Decimal(user_input[1])
        result = Calculator.subtract(operand_1, operand_2)
        logging.debug("Appended '%s,%s,divide' to CalculatorHistory", operand_1, operand_2)
        logging.debug("The result of %s minus %s is equal to %s", operand_1, operand_2, result)
        print(f"The result of {operand_1} minus {operand_2} is equal to {result}")

    def __repr__(self):
        """
            String representation of how to use the Subtract Command

            @return: String representation how to use the Subtract Command
        """
        return "subtract <operand1> <operand2>"
