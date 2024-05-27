"""

class SummonSchool(School):
    def __init__(self):
        super().__init__()
        self.level = {1: self.SummonGoblin,
                      2: self.SummonHobGoblin,
                      3: self.SummonGargoyle,
                      4: self.SummonStumpy,
                      5: self.SummonRaptor,
                      6: self.SummonGolem}

    class Summon(Spell):
        def __init__(self, parent, name = "Summon", cooldown=3, cost=3, range=-1, action_cost=100, required_intelligence = 0):
            super().__init__(parent, name, cooldown, cost, range, action_cost, required_intelligence)
            self.targetted = False
            self.targets_monster = False
            self.monster = M.Kobold

        def create_monster(self):
            monster = self.monster()
            monster.make_friendly()
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

"""