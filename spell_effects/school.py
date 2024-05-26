import random

class School():
    def __init__(self):
        self.level = {}

    def random_spell(self):
        return self.level[random.randint(1,len(self.level))]
