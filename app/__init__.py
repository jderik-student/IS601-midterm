# pylint: disable=unnecessary-dunder-call, invalid-name, unnecessary-pass

'''
    Defines the Application which is a REPL defined to be an interactive calculator
'''

import logging
import logging.config
import os
import sys
from dotenv import load_dotenv
import singleton


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
                logging.info("Calculator History csv created at %s", singleton.calc_history_path_location)
        else:
            logging.info("Calculator History csv exists at %s", singleton.calc_history_path_location)

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


    def start(self):
        '''
            Starts app then exits
        '''
        logging.info("Application Started")

        logging.info("Application Exiting.")
        sys.exit("Exiting...")
