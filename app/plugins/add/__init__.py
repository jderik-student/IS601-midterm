# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    Defines the REPL command to add two numbers together
'''

from decimal import Decimal
import logging
from app.commands import Command
from app.calculator import Calculator

class AddCommand(Command):
    """
        This class extends the Abstract Command Class and preforms addition based on user input
    """
    def execute(self, user_input):
        """
            Adds the first two numbers defined in the user_input list and prints the result of the calculation

            @param user_input: a list of numbers to be added specified by the user, expectation is that there should be only two elements in the list
        """
        operand_1 = Decimal(user_input[0])
        operand_2 = Decimal(user_input[1])
        result = Calculator.add(operand_1, operand_2)
        logging.debug("The result of %s plus %s is equal to %s", operand_1, operand_2, result)
        print(f"The result of {operand_1} plus {operand_2} is equal to {result}")
