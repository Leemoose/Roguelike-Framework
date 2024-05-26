import random

from .school import School
from .spell import Spell

class SpaceSchool(School):
    """
    Maybe add in spells:
    1. Can attack from anywhere on screen
    2. Can make weapons / armor etc disappear from monster
    3. Non targetted blink
    """
    def __init__(self):
        super().__init__()
        self.level = {1: self.Teleport,
                      2: self.TeleportOther,
                      3: self.Blink}

class TeleportOther(Spell):
    def __init__(self, parent, name = "Teleport Other", cooldown=20, cost=5, range=5, action_cost=300):
        super().__init__(parent, name, cooldown, cost, range, action_cost)
        self.targets_monster = True
        self.targetted = True

    def activate(self, target, loop):
        # teleport is assumed to be self-targetting for now, so target does nothing
        tile_map = loop.generator.tile_map
        width = loop.generator.width
        height = loop.generator.height
        startx = random.randint(0, width - 1)
        starty = random.randint(0, height - 1)

        while (tile_map.get_passable(startx, starty) == False):
            startx = random.randint(0, width - 1)
            starty = random.randint(0, height - 1)

        if target.type == "Player":
            target.x = startx
            target.y = starty
            loop.add_message("You teleported somewhere randomly!")
            return
        elif target.type == "Monster":
            monster_map = loop.generator.monster_map
            x, y = target.x, target.y
            monster_map.clear_location(x, y)
            target.x = startx
            target.y = starty
            monster_map.place_thing(target)

class Blink(Spell):
    def __init__(self, parent, name = "Blink", cooldown=20, cost=5, range=5, action_cost=300):
        super().__init__(parent, name, cooldown, cost, range, action_cost)
        self.targets_monster = False
        self.targetted = True

    def activate(self, target, generator):
        self.parent.character.mana -= self.cost
        self.parent.x, self.parent.y = target[0], target[1]  # if targets_monster is false, target is a tuple
        return True

    def in_range(self, target):
        return self.parent.get_distance(target[0], target[1]) <= self.range

    def castable(self, target):
        if type(target) != tuple:
            return False  # if targets_monster is false, target is a tuple, so if we are not targetting a tuple, we can't cast
        return self.in_range(target) and super().castable(target)

    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(
            self.cooldown) + " turn cooldown" + ", blink to empty space in range " + str(self.range) + ")"

class Teleport(Spell):
    def __init__(self, parent, name = "Teleport", cooldown=20, cost=5, range=-1, action_cost=300):
        super().__init__(parent, name, cooldown, cost, range, action_cost)
        self.can_teleport = True
        self.render_tag = 914

    def activate(self, target, loop):
        # teleport is assumed to be self-targetting for now, so target does nothing
        if self.can_teleport:
            tile_map = loop.generator.tile_map
            width = loop.generator.width
            height = loop.generator.height
            startx = random.randint(0, width - 1)
            starty = random.randint(0, height - 1)

            while (tile_map.get_passable(startx, starty) == False):
                startx = random.randint(0, width - 1)
                starty = random.randint(0, height - 1)

            if self.parent.has_trait("player"):
                self.parent.x = startx
                self.parent.y = starty
                loop.add_message("You teleported somewhere randomly!")
                return
            elif self.parent.has_trait("monster"):
                monster_map = loop.generator.monster_map
                x, y = self.parent.x, self.parent.y
                monster_map.clear_location(x, y)
                self.parent.x = startx
                self.parent.y = starty
                monster_map.place_thing(self.parent)
