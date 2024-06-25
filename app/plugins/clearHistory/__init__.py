# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    Defines the REPL command to delete the Calculator's History
'''

import logging
from app.calculator.data_manipulator.dataframe_data_manipulator import DataframeManipulator
from app.calculator.data_manipulator.memory_data_manipulator import MemoryDataManipulator
from app.commands import Command
from app.calculator import CalculatorHistory

class ClearHistoryCommand(Command):
    """
        This class extends the Abstract Command Class and deletes all calcualtions from the Calculator's History
    """

    def execute(self, user_input):
        """
            Deletes all calculations from the Calculator's history

            @param user_input: not used by this method, added to adhere to Liskov substitution principle
        """
        logging.debug("Dataframe and csv cleared")
        CalculatorHistory.delete_history(DataframeManipulator())
        logging.debug("History list cleared")
        CalculatorHistory.delete_history(MemoryDataManipulator())
        print("History Cleared")
