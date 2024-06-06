from .school import School
from .spell import Spell
from .effect import Burn

class FireSchool(School):
    def __init__(self):
        super().__init__()

        self.level = {1: BurningAttack,
                      2: BurningCircle,
                      3: Fireball}

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
        effect = Burn(self.burn_duration + self.parent.character.skill_duration_increase(),
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

    def full_description(self):
        desc = "Throw a small bolt of fire at a target that sets the target ablaze.\n\n"
        desc += f"Deals {self.damage} at range {self.range}\n"
        desc += f"Burns target for {self.burn_damage} burn damage every turn for {self.burn_duration} turns\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc



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
    
    def full_description(self):
        desc = "Emit a ring of fire at all targets around you, setting adjacent spaces ablaze.\n\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc

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
                effect = Burn(self.burn_duration + self.parent.character.skill_duration_increase(),
                                self.burn_damage + self.parent.character.skill_damage_increase(), self.parent)
                monster.character.add_status_effect(effect)
            if loop.generator.tile_map.get_passable(target[0] + x, target[1] + y):
                loop.generator.tile_map.track_map[target[0] + x][target[1] + y].on_fire = True

        return True  # return true if successfully cast, burningAttack cannot fail

    def castable(self, target):
        return super().castable(target) and self.in_range(target)
    
    def full_description(self):
        desc = "Throw a giant ball of fire at a target that hits a 3x3 area centered on the target, setting all enemies in range ablaze.\n\n"
        desc += f"Deals {self.damage} at range {self.range}\n"
        desc += f"Burns target for {self.burn_damage} burn damage every turn for {self.burn_duration} turns\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc


