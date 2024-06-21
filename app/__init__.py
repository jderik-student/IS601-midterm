# pylint: disable=unnecessary-dunder-call, invalid-name, unnecessary-pass

'''
    Defines the Application which is a REPL defined to be an interactive calculator
'''

import logging
import logging.config
import os
import sys
from dotenv import load_dotenv

class App:
    '''
        The Application is a REPL defined to be an interactive calculator
    '''
    def __init__(self): # Constructor
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
            Loads environment variables, configues logging, then exits
        '''
        # Register commands here
        logging.info("Application Started")


        logging.info("Application Exiting.")
        sys.exit("Exiting...")
