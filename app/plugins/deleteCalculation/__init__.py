# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    Defines the REPL command to delete a Calculation from the Calculator's History
'''

import logging
from app.calculator.data_manipulator.dataframe_data_manipulator import DataframeManipulator
from app.calculator.data_manipulator.memory_data_manipulator import MemoryDataManipulator
from app.commands import Command
from app.calculator import CalculatorHistory

class DeleteCalculationCommand(Command):
    """
        This class extends the Abstract Command Class and deletes the specified calculation from the Calculator's History
    """

    def execute(self, user_input):
        """
            Deletes deletes the specified calculation from the Calculator's history

            @param user_input: listed order number of the calculation to delete (shown after from the printHistory)
        """
        try:
            index = int(user_input[0]) - 1
            CalculatorHistory.delete_calculation_at_index(index, DataframeManipulator())
            logging.debug("Calculation at index %s was deleted from the Dataframe and csv", index)
            CalculatorHistory.delete_calculation_at_index(index, MemoryDataManipulator())
            logging.debug("Calculation at index %s was deleted from the History list", index)
            print(f"Calculation #{user_input[0]} was deleted")
        except KeyError:
            print(f"Invalid Calculation Number: {user_input[0]}")
            logging.error("IndexError: Failed to delete calculation at index: %s", index)
            logging.debug("Number of Calculations in history: %s", len(CalculatorHistory.get_history()))
        except ValueError:
            print(f"{user_input[0]} is not a valid number")
            logging.error("ValueError: %s is not a valid number", user_input[0])
