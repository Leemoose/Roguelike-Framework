import random
import monster as M
import effect as E

class Skill():
    def __init__(self, name, parent, cooldown, cost, range=-1, action_cost=100):
        self.parent = parent
        self.cooldown = cooldown
        self.cost = cost
        self.ready = 0 # keeps track of how long before we can cast, ready = 0 means we can cast
        self.name = name
        self.range = range
        self.targetted = False
        self.action_cost = action_cost

    def activate(self, target, generator):
        self.parent.character.mana -= self.cost

    def try_to_activate(self, target, generator):
        # check cooldowns and costs
        if self.castable(target):
            self.ready = self.cooldown
            return self.activate(target, generator)
        return False
    
    def tick_cooldown(self):
        if self.ready > 0:
            self.ready -= 1

    def castable(self, target):
        self.basic_requirements()
    
    def basic_requirements(self):
        if self.ready == 0 and self.parent.character.mana >= self.cost:
            return True
        return False
    
    def in_range(self, target):
        targetx, targety = target.get_location()
        distance = self.parent.get_distance(targetx, targety)
        if distance < self.range:
            return True

    def __str__(self) -> str:
        return self.name

class Teleport(Skill):
    def __init__(self, parent, cooldown, cost):
        super().__init__("Teleport", parent, cooldown, cost)
        self.can_teleport = True

    def activate(self, target, generator):
        # teleport is assumed to be self-targetting for now, so target does nothing
        if self.can_teleport:
            tile_map = generator.tile_map
            width = generator.width
            height = generator.height
            startx = random.randint(0, width - 1)
            starty = random.randint(0, height - 1)

            while (tile_map.get_passable(startx, starty) == False):
                startx = random.randint(0, width - 1)
                starty = random.randint(0, height - 1)

            if isinstance(self.parent, M.Monster):
                monster_map = generator.monster_map
                x, y = self.parent.x, self.parent.y
                monster_map.clear_location(x, y)
                self.parent.x = startx
                self.parent.y = starty
                monster_map.place_thing(self.parent)
            else:
                self.parent.x = startx
                self.parent.y = starty

class BurningAttack(Skill):
    def __init__(self, parent, cooldown, cost, damage, burn_damage, burn_duration, range):
        super().__init__("Burning attack", parent, cooldown, cost, range)
        self.damage = damage
        self.burn_damage = burn_damage
        self.targetted = True
        self.burn_duration = burn_duration

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        defender.character.take_damage(self.parent, self.damage)
        effect = E.Burn(self.burn_duration, self.burn_damage, self.parent)
        defender.character.add_status_effect(effect)
        return True # return true if successfully cast, burningAttack cannot fail

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target)
    
class Petrify(Skill):
    def __init__(self, parent, cooldown, cost, duration, activation_chance, range):
        super().__init__("Petrify", parent, cooldown, cost, range)
        self.duration = duration
        self.targetted = True
        self.activation_chance = activation_chance

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        if random.random() < self.activation_chance:
            effect = E.Petrify(self.duration)
            defender.character.add_status_effect(effect)
            return True
        return False

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target) and not target.character.has_effect("Petrify")
    
class ShrugOff(Skill):
    def __init__(self, parent, cooldown, cost, activation_chance, action_cost):
        super().__init__("Shrug off", parent, cooldown, cost, -1, action_cost)
        self.activation_chance = activation_chance

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        if self.parent.character.has_negative_effects():
            if random.random() < self.activation_chance:
                negative_effects = [effect for effect in self.parent.character.status_effects if not effect.positive]
                random_effect = random.choice(negative_effects)
                random_effect.active = False
                self.parent.character.remove_status_effect(random_effect)
                return True
        return False

    def castable(self, target):
        return self.basic_requirements() and self.parent.character.has_negative_effects()

class Berserk(Skill):
    # self-might if below certain health percent
    def __init__(self, parent, cooldown, cost, activation_threshold, strength_increase, action_cost):
        super().__init__("Berserk", parent, cooldown, cost, -1, action_cost)
        self.threshold = activation_threshold
        self.strength_increase = strength_increase
    
    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        effect = E.Might(-100, self.strength_increase)
        self.parent.character.add_status_effect(effect)
        return True

    def below_threshold(self):
        return self.parent.character.health < self.threshold * self.parent.character.max_health

    def castable(self, target):
        return self.basic_requirements and self.below_threshold() and not self.parent.character.has_effect("Might")

# I only want this for playtesting, it's not a real skill
class Gun(Skill):
    def __init__(self, parent):
        super().__init__("Gun", parent, 0, 0, 10000)
        self.damage = 10000
        self.targetted = True

    def activate(self, defender, generator):
        self.parent.character.mana -= self.cost
        defender.character.take_damage(self.parent, self.damage)
        return True

    def castable(self, target):
        return self.basic_requirements() and self.in_range(target)