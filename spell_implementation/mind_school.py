from .school import School
from .spell import Spell
from .effect import *

class MindSchool(School):
    def __init__(self):
        super().__init__()
        self.level = {1: self.Lullaby,
                      2: self.MassFear,
                      3: self.Charm}

    def random_spell(self):
        return self.level[3]

    class Lullaby(Spell):
        def __init__(self, parent, name="Lullaby", cooldown=10, cost=5, range=5, action_cost=100, duration = 5):
            super().__init__(parent, name, cooldown, cost, range, action_cost)
            self.targets_monster = True
            self.targetted = True
            self.duration = duration

        def castable(self, target):
            return super().castable(target) and self.in_range(target)

        def activate(self, target, loop):
            effect = Asleep(self.duration)
            target.character.add_status_effect(effect)

    class MassFear(Spell):
        def __init__(self, parent, name="Mass Fear", cooldown=30, cost=5, range=-1, action_cost=200, duration = 10):
            super().__init__(parent, name, cooldown, cost, range, action_cost)
            self.targets_monster = False
            self.targetted = False
            self.duration = duration

        def activate(self, target, loop):
            for monster in loop.generator.monsters_in_sight():
                print("When trying to do the mass fear effect, {} is in sight".format(monster))
                effect = E.Fear(self.duration, self.parent)
                monster.character.add_status_effect(effect)

    class Charm(Spell):
        def __init__(self, parent, name="Charm", cooldown=10, cost=5, range=2, action_cost=100, duration = 5):
            super().__init__(parent, name, cooldown, cost, range, action_cost)
            self.targets_monster = True
            self.targetted = True
            self.duration = duration

        def castable(self, target):
            return super().castable(target) and self.in_range(target)

        def activate(self, target, loop):
            effect = Charm(self.duration, self.parent)
            target.character.add_status_effect(effect)

