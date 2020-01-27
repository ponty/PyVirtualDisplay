import random


class Randomizer:
    """
    Class to generate random display numbers between a minimum and maximum
    value. Note that the maximum value can be exceeded if every value between
    the generated and maximum value is already in use.
    """

    def __init__(self, min_display_nr=1000, max_display_nr=1100):
        self.min = min_display_nr
        self.delta = max_display_nr - min_display_nr

        random.seed()

    def generate(self):
        """
        Generate a random display number

        :rtype: int
        """

        return self.min + random.randint(0, self.delta)
