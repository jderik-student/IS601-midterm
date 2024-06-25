"""Temp Doc String"""
from abc import ABC, abstractmethod

class DataManipulationStrategy(ABC):
    """
    This Strategy interface declares operations relating to manipulating data stored in different locations
    """

    @abstractmethod
    def append(self,entry):
        """Temp Doc String"""

    @abstractmethod
    def clear_database(self):
        """Temp Doc String"""
