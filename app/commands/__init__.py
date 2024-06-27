# pylint: disable=unnecessary-dunder-call, invalid-name, unnecessary-pass
'''
    Defines the logic for a Command and the CommandHandler to register and execute these commands
'''

from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
import logging
from typing import List
from icecream import ic

class Command(ABC):
    """
        Abstract class that defines what a Command is
    """
    @abstractmethod
    def execute(self, user_input):
        """
            Abstract method that will be overriden by its subclasses to define Command execution

            @param user_input: a list of strings specified by the user, expectation is that there should be zero to two elements in the list
        """
        pass # pragma: no cover

class CommandHandler:
    """
    This class will be used by the application to register and execute all REPL commands.
    Implements the Singleton Design Pattern.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CommandHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'commands'):
            self.commands = {}

    def register_command(self, command_name, command):
        """
            Adds a command to the CommandHandler's commands dictionary

            @param command_name: the name of the command
            @param command: the function to call when the command is typed by the user
        """
        self.commands[command_name] = command

    def remove_command(self, command_name):
        """
        Removes a command from the CommandHandler's commands dictionary
        Only used for test clean up

        @param command_name: the name of the command to remove
        """
        try:
            del self.commands[command_name]
            logging.info("Command '%s' removed.", command_name)
        except KeyError: # pragma: no cover
            logging.warning("Attempted to remove non-existent command '%s'.", command_name)

    def list_commands(self):
        """
            Prints all the commands registered in the CommandHandler
        """
        print("Commands:")
        for key in self.commands:
            print(f"- {key}")

    def execute_command(self, user_input: List[str]):
        """
            Based on user input, will call the method associated with the command specified by the user with any user defined arguments
            Prints the result

            @param user_input: User specified input, with each value stored in its own element
        """
        try:
            self.commands[user_input[0]].execute(user_input[1:3])
            logging.info("Command called %s with arguments %s", user_input[0], ic.format(user_input[1:]))
        except IndexError:
            print("Invalid number of arguments for specified command")
            logging.error("Index Error | Command: %s Arguments: %s", user_input[0], ic.format(user_input[1:]))
        except ValueError:
            print("Cannot divide by zero")
            logging.error("Value Error | Command: %s Arguments: %s", user_input[0], ic.format(user_input[1:]))
            logging.warning("Divide by zero added to Calculator History")
        except InvalidOperation:
            print(f"Invalid number input: one of {user_input[1:3]} is not a valid number.")
            logging.error("InvalidOperation | Command: %s Arguments: %s", user_input[0], ic.format(user_input[1:]))
        except KeyError:
            print(f"No such command: {user_input[0]}")
            logging.error("KeyError | No such command: %s", user_input[0])
        except FileNotFoundError:
            print(f"No such file or directory: {user_input[1]}")
            logging.error("FileNotFoundError | No such file or directory: %s", user_input[1])
        except Exception as e: # pragma: no cover
            print(f"An error occurred: {e}")
            logging.error("Error Occured: %s | Command: %s Arguments: %s", ic.format(e), user_input[0], ic.format(user_input[1:]))
