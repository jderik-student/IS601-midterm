# pylint: disable=unnecessary-dunder-call, invalid-name
'''
    Defines the REPL command to exit program
'''
import logging
import sys
from app.commands import Command


class ExitCommand(Command):
    """
        This class extends the Abstract Command Class and exits the user from the application
    """
    def execute(self, user_input):
        """
            Exits the application

            @param user_input: not used by this method, added to adhere to Liskov substitution principle
        """
        logging.debug("User exited App with Exit Command")
        sys.exit("Exiting...")
