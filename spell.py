import random

import ai
import monster as M

class Mage():
    def __init__(self, parent):
        self.parent = parent
        self.known_spells = []

    def add_spell(self, spell):
        self.known_spells.append(spell)

    def cast_spell(self, skill_num, target, loop):
        spell = self.known_spells[skill_num]
        print(spell.name)
        self.parent.character.energy -= spell.action_cost
        return spell.try_to_activate(target, loop)

    def tick_cooldowns(self):
        for skill in self.parent.mage.known_spells:
            skill.tick_cooldown()


class Spell():
    def __init__(self, parent, name = "Unknown spell", cooldown=0, cost=0, range=-1, action_cost=100):
        self.parent = parent
        self.cooldown = cooldown
        self.cost = cost
        self.ready = 0  # keeps track of how long before we can cast, ready = 0 means we can cast
        self.name = name
        self.range = range
        self.targetted = False
        self.targets_monster = False
        self.action_cost = action_cost
        self.threshold = 0.0
        self.render_tag = 902  # placeholder icon, skill assets are fixed so not given in user input

    def activate(self, target, generator):
        self.parent.character.mana -= self.cost

    def try_to_activate(self, target, loop):
        # check cooldowns and costs
        if self.castable(target):
            self.ready = self.cooldown
            print("Spell is activated")
            return self.activate(target, loop)
        loop.add_message("You were unable to cast the spell due to certain conditions.")
        return False

    def tick_cooldown(self):
        if self.ready > 0:
            self.ready -= 1

    def castable(self, target):
        if self.ready == 0 and self.parent.character.mana >= self.cost:
            return True
        return False

    def in_range(self, target):
        targetx, targety = target.get_location()
        distance = self.parent.get_distance(targetx, targety)
        if distance < self.range:
            return True

    def __str__(self):
        return self.name

    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown"

class SummonSchool():
    def __init__(self):
        self.level = {1: self.SummonGoblin,
                      2: self.SummonHobGoblin,
                      3: self.SummonGargoyle,
                      4: self.SummonStumpy,
                      5: self.SummonRaptor,
                      6: self.SummonGolem}

    def random_spell(self):
        return self.level[random.randint(1,len(self.level))]

    class Summon(Spell):
        def __init__(self, parent, name = "Summon", cooldown=3, cost=3, range=-1, action_cost=100):
            super().__init__(parent, name, cooldown, cost, range, action_cost)
            self.targetted = False
            self.targets_monster = False
            self.monster = M.Kobold

        def create_monster(self):
            monster = self.monster()
            monster.brain = ai.Friendly_AI(monster)
            return monster

        def activate(self, target, loop):
            self.parent.character.mana -= self.cost
            x, y = self.parent.get_location()
            location = loop.generator.nearest_empty_tile((x, y), move=True,search = True)
            print("Activated a spell.")
            if location != None:
                monster = self.create_monster()
                loop.generator.place_monster_at_location(monster, location[0], location[1])
                loop.add_message("A {} was summoned!".format(monster.name))
                return True
            else:
                loop.add_message("The summoning fizzled")
            return False

    class SummonGoblin(Summon):
        def __init__(self, parent, cooldown=10, cost=3, range=-1, action_cost=100):
            super().__init__(parent, "Summon Goblin", cooldown, cost, range, action_cost)
            self.monster = M.Goblin

    class SummonHobGoblin(Summon):
        def __init__(self, parent, cooldown=25, cost=3, range=-1, action_cost=100):
            super().__init__(parent, "Summon Hobgoblin", cooldown, cost, range, action_cost)
            self.monster = M.Hobgoblin

    class SummonGargoyle(Summon):
        def __init__(self, parent, cooldown=25, cost=3, range=-1, action_cost=100):
            super().__init__(parent, "Summon Gargoyle", cooldown, cost, range, action_cost)
            self.monster = M.Gargoyle

    class SummonRaptor(Summon):
        def __init__(self, parent, cooldown=50, cost=3, range=-1, action_cost=100):
            super().__init__(parent, "Summon Raptor", cooldown, cost, range, action_cost)
            self.monster = M.Raptor

    class SummonStumpy(Summon):
        def __init__(self, parent, cooldown=50, cost=3, range=-1, action_cost=100):
            super().__init__(parent, "Summon Stumpy", cooldown, cost, range, action_cost)
            self.monster = M.Stumpy

    class SummonGolem(Summon):
        def __init__(self, parent, cooldown=75, cost=3, range=-1, action_cost=100):
            super().__init__(parent, "Summon Golem", cooldown, cost, range, action_cost)
            self.monster = M.Golem

class SummonSchool():
    def __init__(self):
        self.level = {1: self.SummonGoblin}

    def random_spell(self):
        return self.level[random.randint(1,len(self.level))]

    class Blink(Spell):
        def __init__(self, parent, name = "Blink", cooldown=3, cost=3, range=5, action_cost=100):
            super().__init__(parent, name, cooldown, cost, range, action_cost)
            self.targetted = False
            self.targets_monster = False

        def activate(self, target, loop):
            self.parent.character.mana -= self.cost
            x, y = self.parent.get_location()
            location = loop.generator.nearest_empty_tile((x, y), move=True,search = True)
            print("Activated a spell.")
            if location != None:
                monster = self.create_monster()
                loop.generator.place_monster_at_location(monster, location[0], location[1])
                loop.add_message("A {} was summoned!".format(monster.name))
                return True
            else:
                loop.add_message("The summoning fizzled")
            return False

