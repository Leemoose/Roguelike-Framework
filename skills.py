import random
import monster as M
import effect as E

class Skill():
    def __init__(self, name, parent, cooldown, cost):
        self.parent = parent
        self.cooldown = cooldown
        self.cost = cost
        self.ready = 0 # keeps track of how long before we can cast, ready = 0 means we can cast
        self.name = name

    def activate(self, target, generator):
        pass

    def try_to_activate(self, target, generator, loop):
        # check cooldowns and costs
        if self.castable(loop):
            self.activate(target, generator)
            self.ready = self.cooldown
            return True
        return False

    def castable(self, loop):
        # in current loop state, is it castable
        if self.ready == 0:
            return True
        return False

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
    def __init__(self, parent, cooldown, cost, damage, burn_damage, burn_duration):
        super().__init__("Burning attack", parent, cooldown, cost)
        self.damage = damage
        self.burn_damage = burn_damage
        self.burn_duration = burn_duration

    def activate(self, defender, generator):
        defender.character.take_damage(self.damage)
        effect = E.Burn(self.burn_duration, self.burn_damage)
        defender.character.add_status_effect(effect)

    def castable(self, loop):
        player=loop.player
        playerx, playery = player.get_location()
        monster = self.parent
        monsterx, monstery = monster.get_location()
        distance = self.parent.get_distance(playerx, playery)
        if distance < 1.5:
            if self.ready == 0:
                return True
        return False