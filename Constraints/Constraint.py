from abc import ABC, abstractmethod
import random


class Constraint(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def produce_valid_value(self):
        pass

    @abstractmethod
    def is_valid_value(self, value):
        pass

    @staticmethod
    def get_random_number(min_number, max_number):
        return random.randint(min_number, max_number)
