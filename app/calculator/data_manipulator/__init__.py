"""
    This Strategy interface declares operations relating to manipulating data stored in different locations
"""
from abc import ABC, abstractmethod

from app.calculator.calculation import Calculation

class DataManipulationStrategy(ABC):
    """
        This Strategy interface declares operations relating to manipulating data stored in different locations
    """

    @abstractmethod
    def append(self,entry: Calculation):
        """Abstract method to append calculations to a specific data location"""

    @abstractmethod
    def clear_database(self):
        """Abstract method to delete all data stored at the specific location"""

    @abstractmethod
    def delete_entry_at_index(self, index: int):
        """Abstract method to delete the entry stored at the specific index"""
