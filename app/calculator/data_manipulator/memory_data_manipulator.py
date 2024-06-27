'''
        This is a Concrete Strategy that defines the logic to manpiulate logic stored in CalculatorHistory's history list
'''
from app.calculator.calculation import Calculation
from app.calculator.calculator_history import CalculatorHistory
from app.calculator.data_manipulator import DataManipulationStrategy

class MemoryDataManipulator(DataManipulationStrategy):
    '''
        This is a Concrete Strategy that defines the logic to manpiulate logic stored in CalculatorHistory's history list
    '''
    def append(self, entry: Calculation):
        '''
            Appends a calculation to the CalculatorHistory history list
        '''
        CalculatorHistory.get_history().append(entry)

    def clear_database(self):
        '''
            Deletes all calculations in the CalculatorHistory history list
        '''
        CalculatorHistory.get_history().clear()

    def delete_entry_at_index(self, index):
        '''
            Deletes the Calculation at the specified index in the CalculatorHistory history list
        '''
        CalculatorHistory.get_history().pop(index)
