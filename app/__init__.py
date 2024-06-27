# pylint: disable=unnecessary-dunder-call, invalid-name, unnecessary-pass

'''
    Defines the Application which is a REPL defined to be an interactive calculator
'''

import importlib
import logging
import logging.config
import os
import pkgutil
import sys
from icecream import ic
from dotenv import load_dotenv
import singleton
from app.calculator.calculator_history import CalculatorHistory
from app.commands import Command, CommandHandler


class App:
    '''
        The Application is a REPL defined to be an interactive calculator
    '''
    def __init__(self): # Constructor
        '''
            Initializes the logging, environment variables, directory, and files needed to run this application
        '''
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        if self.get_environment_variable("ENVIRONMENT") == "DEV": # pragma: no cover
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            for handler in logger.handlers:
                handler.setLevel(logging.DEBUG)
            logging.debug("Logging level set to DEBUG")
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info("The directory '%s is created", data_dir)

        elif not os.access(data_dir, os.W_OK):
            logging.error("The directory '%s' is not writable.", data_dir)
            sys.exit("Exiting: The directory '%s' is not writable.", data_dir)

        calc_history_file = self.get_environment_variable('CSVFILENAME')
        path_abs_hist_folder = os.path.abspath(data_dir)
        path_abs_hist_file = os.path.join(path_abs_hist_folder, calc_history_file)
        singleton.calc_history_path_location = path_abs_hist_file
        logging.debug("Calculator History File Absolute Path: %s", path_abs_hist_file)

        if not os.path.exists(singleton.calc_history_path_location):
            with open(singleton.calc_history_path_location,encoding="utf-8", mode='w') as file:
                file.write("Operand1,Operand2,Operation")
                logging.info("Calculator History csv file was not found, created file at %s", singleton.calc_history_path_location)
        else:
            logging.info("Calculator History csv exists at %s", singleton.calc_history_path_location)

        self.command_handler = CommandHandler()
        logging.info("Command Handler Initialized")

    def configure_logging(self):
        '''
            Configures logging
        '''
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else: # pragma: no cover
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info("Logging configured")

    def load_environment_variables(self):
        '''
            Loads environment variables from .env file
        '''
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        '''
            Returns the specified environment variable 
        '''
        logging.info(self.settings.get(env_var, None))
        return self.settings.get(env_var, None)

    def load_plugins(self):
        '''
            Dynamically load all plugins in the plugins directory
        '''
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path): # pragma: no cover
            logging.warning("Plugins directory '%s' not found.", plugins_path)
            print("Plugins directory '%s' not found.", plugins_path)
            sys.exit(0)
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)) and item is not Command:  # Added extra condition as it was registering the command twice
                            try:
                                if plugin_name == "menu":
                                    self.command_handler.register_command(plugin_name, item(self.command_handler))
                                else:
                                    self.command_handler.register_command(plugin_name, item())
                                logging.info("Command %s from plugin %s registered.", plugin_name, plugin_module)
                            except Exception as e: # pragma: no cover
                                logging.error("Failed to import plugin %s: %s", plugin_name, ic.format(e))
                    except TypeError:
                        continue  # If item is not a class or unrelated class, just ignore

    def start(self):
        '''
            Starts app then exits
        '''
        self.load_plugins()
        try:
            CalculatorHistory.load_history_from_csv(singleton.calc_history_path_location)
        except Exception as e:
            print(f"Failed to load from {singleton.calc_history_path_location}")
            logging.error("Failed to load from %s | Error: %s", singleton.calc_history_path_location, e)
        logging.info("Application Started")
        self.command_handler.list_commands()
        print("Type 'exit' to exit.")
        try:
            while True:  #REPL Read, Evaluate, Print, Loop
                self.command_handler.execute_command(input(">>> ").split())
        except KeyboardInterrupt:
            logging.info("Application interrupted and exiting gracefully.")
            sys.exit(0)
        finally:
            logging.info("Application shutdown.")
