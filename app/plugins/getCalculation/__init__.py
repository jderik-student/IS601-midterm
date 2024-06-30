# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    Defines the REPL command to get a Calculation from the Calculator's History and compute it
'''

import logging
from app.calculator.data_manipulator.dataframe_data_manipulator import DataframeManipulator
from app.calculator.data_manipulator.memory_data_manipulator import MemoryDataManipulator
from app.commands import Command
from app.calculator import CalculatorHistory

class GetCalculationCommand(Command):
    """
        This class extends the Abstract Command Class and gets a Calculation from the Calculator's History and computes it
    """

    def execute(self, user_input):
        """
            Gets the specified calculation from the Calculator's history and computes it
            Calculation will not be re-added to the history

            @param user_input: number of the calculation to get and compute (shown after from the printHistory Command)
        """
        try:
            index = int(user_input[0]) - 1
            calculation = CalculatorHistory.get_ith_calculation(index)
            result = calculation.calculate()
            logging.debug("The result of %s is equal to %s", calculation, result)
            print(f"The result of {calculation} is equal to {result}")
        except IndexError:
            print(f"Invalid Calculation Number: {user_input[0]}")
            logging.error("IndexError: Failed to delete calculation at index: %s", index)
            logging.debug("Number of Calculations in history: %s", len(CalculatorHistory.get_history()))
        except ValueError as e:
            print(f"ValueError: {e}")
            logging.error("ValueError: %s", e)

    def __repr__(self):
        """
            String representation of how to use the GetCalculation Command

            @return: String representation how to use the GetCalculation Command
        """
        return "getCalculation <calculation#>"
