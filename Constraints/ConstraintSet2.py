from Constraints.Constraint import Constraint
from typing import Dict


class ConstraintSet:
    constraints: Dict[str, Constraint] = {}

    def add(self, name, constraint: Constraint):
        self.constraints[name] = constraint

    def remove(self, name):
        try:
            del self.constraints[name]
        except KeyError:
            print("Key not found: " + name)

    def get(self, name):
        return self.constraints[name]

    def generate_value(self, name):
        return self.get(name).produce_valid_value()

    def has_constraint(self, name):
        if name in self.constraints:
            return True
        else:
            return False
