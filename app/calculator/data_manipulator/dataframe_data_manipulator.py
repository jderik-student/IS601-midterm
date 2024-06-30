'''
    This is a Concrete Strategy that defines the logic to manpiulate data stored in the CalculatorHistory's dataframe and the associated csv file
'''
import singleton
from app.calculator.calculation import Calculation
from app.calculator.calculator_history import CalculatorHistory
from app.calculator.data_manipulator import DataManipulationStrategy


class DataframeManipulator(DataManipulationStrategy):
    '''
        This is a Concrete Strategy that defines the logic to manpiulate data stored in the CalculatorHistory's dataframe and the associated csv file
    '''
    def append(self, entry: Calculation):
        '''
            Appends a calculation to the CalculatorHistory dataframe and the associated csv file

            @param entry: the Calculation to append to the dataframe
        '''
        df = CalculatorHistory.get_dataframe()
        df.loc[len(df)] = {"Operation": entry.operation.__name__, "Operand1": float(entry.a), "Operand2": float(entry.b)}
        df.to_csv(singleton.CALC_HISTORY_FILE_PATH, mode= "w", index=  False, header = True)

    def clear_database(self):
        '''
            Deletes all calculations in the CalculatorHistory dataframe and the associated csv file
        '''
        df = CalculatorHistory.get_dataframe()
        df.drop(df.index, inplace=True)
        df.to_csv(singleton.CALC_HISTORY_FILE_PATH, mode= "w", index=  False, header = True)

    def delete_entry_at_index(self, index: int):
        '''
            Deletes the Calculation at the specified index in the CalculatorHistory dataframe and the associated csv file

            @param index: the index of the calculation to delete from the dataframe
        '''
        df = CalculatorHistory.get_dataframe()
        df.drop(index=index, inplace=True)
        df.to_csv(singleton.CALC_HISTORY_FILE_PATH, mode= "w", index=  False, header = True)
