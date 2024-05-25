import random
import player
import ai
import monster as M
import effect as E

class Mage():
    def __init__(self, parent):
        self.parent = parent
        self.known_spells = []

    def add_spell(self, spell):
        self.known_spells.append(spell)

    def cast_spell(self, skill_num, target, loop):
        spell = self.known_spells[skill_num]
        self.parent.character.energy -= spell.action_cost
        return spell.try_to_activate(target, loop)

    def tick_cooldowns(self):
        for skill in self.parent.mage.known_spells:
            skill.tick_cooldown()


class Spell():
    def __init__(self, parent, name = "Unknown spell", cooldown=0, cost=0, range=-1, action_cost=100, required_intelligence = 0):
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
        self.required_intelligence = required_intelligence

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
        # print(target)
        if isinstance(target, tuple):
            targetx, targety = target
        else:
            targetx, targety = target.get_location()
        distance = self.parent.get_distance(targetx, targety)
        if distance < self.range:
            return True

    def __str__(self):
        return self.name

    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown"

    def can_learn(self):
        return self.parent.character.intelligence >= self.required_intelligence

class School():
    def __init__(self):
        self.level = {}

    def random_spell(self):
        return self.level[random.randint(1,len(self.level))]

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

            if isinstance(target, player.Player):
                target.x = startx
                target.y = starty
                loop.add_message("You teleported somewhere randomly!")
                return
            elif isinstance(target, M.Monster):
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

                if isinstance(self.parent, player.Player):
                    self.parent.x = startx
                    self.parent.y = starty
                    loop.add_message("You teleported somewhere randomly!")
                    return
                elif isinstance(self.parent, M.Monster):
                    monster_map = loop.generator.monster_map
                    x, y = self.parent.x, self.parent.y
                    monster_map.clear_location(x, y)
                    self.parent.x = startx
                    self.parent.y = starty
                    monster_map.place_thing(self.parent)

class FireSchool(School):
    def __init__(self):
        super().__init__()

        self.level = {1: self.BurningAttack,
                      2: self.BurningCircle,
                      3: self.Fireball}

    class BurningAttack(Spell):
        def __init__(self, parent, name = "Burning Attack", cooldown = 10, cost= 5, range = 5, action_cost = 50, damage = 3, burn_damage = 3, burn_duration=5):
            super().__init__(parent, name, cooldown, cost, range, action_cost)
            self.damage = damage
            self.burn_damage = burn_damage
            self.targetted = True
            self.targets_monster = True
            self.burn_duration = burn_duration
            self.render_tag = 904

        def activate(self, defender, loop):
            self.parent.character.mana -= self.cost
            defender.character.take_damage(self.parent, self.damage + self.parent.character.skill_damage_increase())
            effect = E.Burn(self.burn_duration + self.parent.character.skill_duration_increase(),
                            self.burn_damage + self.parent.character.skill_damage_increase(), self.parent)
            defender.character.add_status_effect(effect)
            return True  # return true if successfully cast, burningAttack cannot fail

        def castable(self, target):
            return super().castable(target) and self.in_range(target)

        def description(self):
            if self.burn_duration == -100:
                return self.name + "(" + str(self.cost) + " cost, " + str(
                    self.cooldown) + " turn cooldown" + ", " + str(self.damage) + " damage at range " + str(
                    self.range) + ", " + str(self.burn_damage) + " burn damage permanently)"
            return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown" + ", " + str(
                self.damage) + " damage at range " + str(self.range) + ", " + str(
                self.burn_damage) + " burn damage for " + str(self.burn_duration) + " turns)"

    class BurningCircle(Spell):
        def __init__(self, parent, name = "Burning Circle", cooldown = 10, cost= 5, range = 5, action_cost = 50, damage = 3, burn_damage = 3, burn_duration=5):
            super().__init__(parent, name, cooldown, cost, range, action_cost)
            self.damage = damage
            self.burn_damage = burn_damage
            self.burn_duration = burn_duration
          #  self.render_tag = 904

        def activate(self, defender, loop):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for x, y in directions:
                if loop.generator.tile_map.get_passable(self.parent.x + x, self.parent.y + y):
                    loop.generator.tile_map.track_map[self.parent.x + x][self.parent.y + y].on_fire = True
            self.parent.character.mana -= self.cost
            return True  # return true if successfully cast, burningAttack cannot fail

    class Fireball(Spell):
        def __init__(self, parent, name = "Fireball", cooldown = 20, cost= 10, range = 10, action_cost = 150, damage = 10, burn_damage = 3, burn_duration=2, required_intelligence = 5):
            super().__init__(parent, name, cooldown, cost, range, action_cost, required_intelligence)
            self.damage = damage
            self.burn_damage = burn_damage
            self.burn_duration = burn_duration
            self.targetted = True
            #Needs to change target so it can target the ground not just monsters

          #  self.render_tag = 904

        def activate(self, target, loop):
            self.parent.character.mana -= self.cost
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1), (0,0)]
            for x, y in directions:
                if not loop.generator.monster_map.get_passable(target[0] + x,target[1] + y):
                    monster = loop.generator.monster_map.locate(target[0] + x, target[1] + y)
                    monster.character.take_damage(self.parent,
                                                   self.damage + self.parent.character.skill_damage_increase())
                    effect = E.Burn(self.burn_duration + self.parent.character.skill_duration_increase(),
                                    self.burn_damage + self.parent.character.skill_damage_increase(), self.parent)
                    monster.character.add_status_effect(effect)
                if loop.generator.tile_map.get_passable(target[0] + x, target[1] + y):
                    loop.generator.tile_map.track_map[target[0] + x][target[1] + y].on_fire = True

            return True  # return true if successfully cast, burningAttack cannot fail

        def castable(self, target):
            return super().castable(target) and self.in_range(target)

class HypnosisSchool(School):
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
            effect = E.Asleep(self.duration)
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
            effect = E.Charm(self.duration, self.parent)
            target.character.add_status_effect(effect)




