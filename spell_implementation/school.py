import random

class School():
    def __init__(self):
        self.level = {}

    def random_spell(self):
        return self.level[random.randint(1,len(self.level))]

    def level_spell(self, num):
        if num in self.level:
            return self.level[num]
        else:
            print("You attempted to get a level {} spell but there are only {} levels in this spell school".format(num, len(self.level)))
            return False
