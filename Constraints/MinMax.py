from Constraints.Constraint import Constraint


class MinMax(Constraint):

    def __init__(self, minimum, maximum):
        self.min = minimum
        self.max = maximum
        super().__init__()

    def produce_valid_value(self):
        return self.get_random_number(self.min, self.max)

    def is_valid_value(self, value):
        return (value >= self.min) and (value <= self.max)


