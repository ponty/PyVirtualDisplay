import random

class Randomizer():
    def __init__(self, min_display_nr=1000, max_display_nr=1100):
        self.min = min_display_nr
        self.delta = max_display_nr - min_display_nr

        random.seed()

    def generate(self):
        """
        Get a random display number
        """

        return self.min + random.randint(0, self.delta)