# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    Defines the REPL command to Load the History from the a specified csv file
'''

import logging
from app.commands import Command
from app.calculator import CalculatorHistory

class LoadHistoryCommand(Command):
    """
        This class extends the Abstract Command Class and loads history form a specified csv file
    """

    def execute(self, user_input):
        """
            Deletes all calculations from the Calculator's history

            @param user_input: csv file to load history from
        """
        try:
            CalculatorHistory.load_history_from_csv(user_input[0])
            logging.debug("History Loaded from %s", user_input[0])
            print(f"History Loaded from {user_input[0]}")
        except KeyError as e:
            print(f"CSV Invalid Format | Column Not Found: {e}")
            logging.error("CSV Invalid Format | Column Not Found: %s", e)
