# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    Defines the REPL command to Save the Calculator's History
'''

import logging
from app.commands import Command
from app.calculator import CalculatorHistory

class SaveHistoryCommand(Command):
    """
        This class extends the Abstract Command Class and saves the history to the specified csv file
    """

    def execute(self, user_input):
        """
            Deletes all calculations from the Calculator's history

            @param user_input: csv file to save the stored history to
        """
        CalculatorHistory.save_to_csv(user_input[0])
        logging.debug("History Saved to %s", user_input[0])
        print(f"History Saved to {user_input[0]}")

    def __repr__(self):
        """
            String representation of how to use the SaveHistory Command

            @return: String representation how to use the SaveHistory Command
        """
        return "saveHistory <csvFile>"
