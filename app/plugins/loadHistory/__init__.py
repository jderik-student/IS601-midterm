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
        CalculatorHistory.load_history_from_csv(user_input[0])

    def __repr__(self):
        """
            String representation of how to use the LoadHistory Command

            @return: String representation how to use the LoadHistory Command
        """
        return "loadHistory <csvFile>"
