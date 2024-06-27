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
            Adds a Calculation to the history, dataframe, and csv file

            @param calculation: the Calculation to add to the history
        """
        dataManipulationStrategy.append(calculation)

    @classmethod
    def get_last_calculation(cls) -> Calculation:
        """
            Returns the Calculation at the end of the history list from the list.

           @return: the most recent Calculation (the Calculation at the end of the history list), returns None if the history is empty
        """
        if cls.history:
            return cls.history[-1]
        return None

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

           @return: a list of all Calculations in the history
        """
        return cls.dataframe

    @classmethod
    def delete_history(cls, dataManipulationStrategy: DataManipulationStrategy):
        """
           Clears all Calculations stored in the history list, dataframe, and in the csv file
        """
        dataManipulationStrategy.clear_database()

    @classmethod
    def delete_calculation_at_index(cls, index, dataManipulationStrategy: DataManipulationStrategy):
        """
           Clears the Calculation at the specified index in the history list, dataframe, and in the csv file
        """
        dataManipulationStrategy.delete_entry_at_index(index=index)

    @classmethod
    def find_by_opreation(cls, operation_name: str) -> List[Calculation]:
        """
           Finds and returns a list of all the Calculations with a specific operation

           @param operation_name: the desired operation to find
           @return: a list of Calculations with the speicified operation type
        """
        return [calc for calc in cls.history if calc.operation.__name__ == operation_name]

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
        """
        hist = []
        df = pd.read_csv(file_path)
        try:
            for _, row in df.iterrows():
                calc = Calculation.create(Decimal(row["Operand1"]), Decimal(row["Operand2"]), singleton.operation_mappings[row["Operation"]])
                hist.append(calc)
            cls.dataframe = df
            cls.history = hist
            df.to_csv(singleton.calc_history_path_location, mode= "w", index=  False, header = True)
        except Exception as e:
            print(f"Failed to load history from {file_path}")
            logging.error("Failed to load history from %s | Error %s", file_path, e)

    @classmethod
    def save_to_csv(cls, file_path):
        """
            Saves the stored dataframe to the specified csv file
        """
        cls.dataframe.to_csv(file_path, mode= "w", index=  False, header = True)
