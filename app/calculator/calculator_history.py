# pylint: disable=unnecessary-dunder-call, invalid-name
"""
    Class used to store and access past Calculations that were inputted into the Calculator in both a csv file and in memory.
    The most recent Calculation would appear at the end of the list
"""

from decimal import Decimal
import logging
from typing import List
import pandas as pd
import singleton
from app.calculator.calculation import Calculation
from app.calculator.data_manipulator import DataManipulationStrategy


class CalculatorHistory:
    """
        Class used to store and access past Calculations that were inputted into the Calculator in both a csv file and in memory.
        The most recent Calculation would appear at the end of the list
    """
    history: List[Calculation] = []
    dataframe = pd.DataFrame(columns = ['Operand1', 'Operand2', 'Operation'])

    @classmethod
    def append(cls, calculation: Calculation, dataManipulationStrategy: DataManipulationStrategy):
        """
            Adds a Calculation to the history or dataframe and csv file

            @param calculation: the Calculation to add to the history
            @param DataManipulationStrategy: the desired DataManipulation Strategy to define where to perform the append
        """
        dataManipulationStrategy.append(calculation)

    @classmethod
    def get_history(cls) -> List[Calculation]:
        """
            Returns the entire history list

           @return: a list of all Calculations in the history
        """
        return cls.history

    @classmethod
    def get_dataframe(cls) -> pd.DataFrame:
        """
            Returns the entire history dataframe

           @return: the CalculatorHistory's dataframe
        """
        return cls.dataframe

    @classmethod
    def delete_history(cls, dataManipulationStrategy: DataManipulationStrategy):
        """
           Clears all Calculations stored in the history list or dataframe and the csv file

           @param DataManipulationStrategy: the desired DataManipulation Strategy to define where to perform the delete
        """
        dataManipulationStrategy.clear_database()

    @classmethod
    def delete_calculation_at_index(cls, index, dataManipulationStrategy: DataManipulationStrategy):
        """
           Clears the Calculation at the specified index in the history list or dataframe and the csv file

           @param DataManipulationStrategy: the desired DataManipulation Strategy to define where to perform the delete
        """
        dataManipulationStrategy.delete_entry_at_index(index=index)

    @classmethod
    def get_ith_calculation(cls, i: int) -> Calculation:
        """
           Gets the ith Calculation in the history list and returns it

           @param i: the desired position of the Caluclation to be retrieved
           @return: the Calculation at position i
        """
        return cls.history[i]

    @classmethod
    def load_history_from_csv(cls, file_path: str):
        """
            Reads in a csv file and stores the information into the dataframe and history list

            @param file_path: the desired csv file's path 
        """
        hist = []
        df = pd.read_csv(file_path)
        try:
            for _, row in df.iterrows():
                calc = Calculation.create(Decimal(row["Operand1"]), Decimal(row["Operand2"]), singleton.OPERATION_MAPPINGS[row["Operation"]])
                hist.append(calc)
            cls.dataframe = df
            cls.history = hist
            df.to_csv(singleton.CALC_HISTORY_FILE_PATH, mode= "w", index=  False, header = True)
            print(f"History loaded from {file_path}")
            logging.info("History loaded from %s", file_path)
        except KeyError as e:
            print(f"Failed to load history from {file_path}")
            logging.error("Failed to load history from %s", file_path)
            print(f"CSV Invalid Format | Column Not Found {e}")
            logging.error("CSV Invalid Format | Column Not Found %s", e)
        except Exception as e: #pragma: no cover
            print(f"Failed to load history from {file_path}")
            logging.error("Failed to load history from %s | Error %s", file_path, e)

    @classmethod
    def save_to_csv(cls, file_path):
        """
            Saves the stored dataframe to the specified csv file

            @param file_path: the desired csv file's path 
        """
        cls.dataframe.to_csv(file_path, mode= "w", index=  False, header = True)
