"""
    This Strategy interface declares operations relating to manipulating data stored in different locations
"""
from abc import ABC, abstractmethod

class DataManipulationStrategy(ABC):
    """
    This Strategy interface declares operations relating to manipulating data stored in different locations
    """

    @abstractmethod
    def append(self,entry):
        """Abstract method to append calculations to a specific data location"""

    @abstractmethod
    def clear_database(self):
        """Abstract method to delete the data stored at the specific location"""
