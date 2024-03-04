import random
import dice as R
import objects as O
import effect as E
import pathfinding
import skills as S

class Character():
    def __init__(self, parent, endurance = 0, intelligence = 0, dexterity = 0, strength = 0, health = 100, mana = 0):
        self.endurance = endurance
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.strength = strength

        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana

        self.movable = True

        self.energy = 0
        self.move_cost = 100
        self.equip_cost = 20
        self.quaff_cost = 10
        self.attack_cost = 100

        self.alive = True
        self.inventory = []
        self.main_weapon = None
        self.main_shield = None

        self.base_damage = 0

        self.parent = parent
        self.status_effects = []

        self.skills = []

        self.experience_given = 0 # monsters will overwrite this attribute, it just makes some class stuff easier if its stored in character
        self.experience = None

    def is_alive(self):
        if self.health <= 0:
            self.alive = False
            return False
        return True

    def take_damage(self, dealer, damage):
        self.health -= damage
        if not self.is_alive():
            if hasattr(dealer, "experience"): # acts as a check for it its a player
                dealer.experience += self.experience_given
                dealer.check_for_levelup()
        return self.is_alive()

    def gain_health(self, heal):
        self.health += heal
        if self.health > self.max_health:
            self.health = self.max_health

    def gain_mana(self, mana):
        self.mana += mana
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def defend(self):
        defense = self.endurance
        return defense

    def grab(self, key, item_ID, generated_maps, loop):
        item = item_ID.get_subject(key)
        self.inventory.append(item)
        item_ID.remove_subject(key)
        itemx, itemy = item.get_location()
        generated_maps.item_map.clear_location(itemx, itemy)
        loop.add_message("The " + str(self.parent.name) + " picked up an item!")

    def drop(self, item, item_dict,  item_map):
        if len(self.inventory) != 0 and item.dropable:
            i = 0
            while self.inventory[i].id_tag != item.id_tag and i < len(self.inventory):
                i += 1
            if i < len(self.inventory):
                self.inventory.pop(i)
                item_dict.add_subject(item)
                item.x = self.parent.x
                item.y = self.parent.y
                item_map.place_thing(item)

    def equip(self, item):
        if item.equipable:
            item.equip(self)
            item.equipped = True
            item.dropable = False
            self.energy -= self.equip_cost

    def unequip(self, item):
        if item.equipped:
            item.unequip(self)
            item.dropable = True
            item.equipped = False

    def wait(self):
        self.energy -=  self.move_cost

    def level_up(self):
        self.endurance += 1
        self.intelligence += 1
        self.dexterity += 1
        self.strength += 1
        self.health = self.max_health

    def melee(self, defender):
        if self.main_weapon == None:
            damage = R.roll_dice(1, 20)[0]
        else:
            damage = self.main_weapon.attack()
        defense = defender.character.defend()
        defender.character.take_damage(self.parent, self.base_damage + self.strength+ damage - defense)
        self.energy -= self.attack_cost
        return (self.base_damage + damage +self.strength - defense)

    def dodge(self):
        dodge_chance = random.randint(1,100)
        if dodge_chance <= self.dexterity:
            return True
        else:
            return False

    def quaff(self, potion, item_dict, item_map):
        if potion.consumeable:
            potion.activate(self)
            self.drop(potion, item_dict, item_map)
            potion.destroy = True
            self.energy -= self.quaff_cost
            return True
    
    def tick_all_status_effects(self):
        for effect in self.status_effects:
            effect.tick(self)
        for effect in self.status_effects:
            if not effect.active:
                self.remove_status_effect(effect)

    def remove_status_effect(self, effect):
        if not effect.active:
            effect.remove(self)
            self.status_effects.remove(effect)

    def add_status_effect(self, effect):
        if effect.id_tag not in [x.id_tag for x in self.status_effects]:
            effect.apply_effect(self)
            self.status_effects.append(effect)
        else:
            # refresh duration of existing status effect
            for x in self.status_effects:
                if x.id_tag == effect.id_tag:
                    x.duration = effect.duration
    
    def status_messages(self):
        messages = []
        for effect in self.status_effects:
            messages.append(effect.message)
        return messages
    
    def tick_cooldowns(self):
        for skill in self.skills:
            skill.tick_cooldown()

    def cast_skill(self, skill_num, target, loop):
        skill = self.skills[skill_num]
        self.energy -= skill.action_cost
        return skill.try_to_activate(target, loop.generator)
        


class Player(O.Objects):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 200, "Player")
        self.character = Character(self)
        self.character.skills = []
        self.character.skills.append(S.BurningAttack(self, cooldown=0, cost=10, damage=20, burn_damage=5, burn_duration=3, range=10))
        self.character.skills.append(S.Petrify(self, cooldown=0, cost=10, duration=3, activation_chance=1, range=10))

        self.level = 1
        self.max_level = 20
        self.experience = 0
        self.experience_to_next_level = 20

        self.path = []

        self.invincible = True

    def attack_move(self, move_x, move_y, loop):
        if not self.character.movable:
            self.character.energy -= (self.character.move_cost - self.character.dexterity)
            loop.add_message("The player is petrified and cannot move.")
            return
        x = self.x + move_x
        y = self.y + move_y
        if (x >= 0) & (y >= 0) & (x < loop.generator.tile_map.width) & (y < loop.generator.tile_map.height):
            if (loop.generator.monster_map.track_map[x][y]) != -1:
                defender = loop.monster_dict.get_subject(loop.generator.monster_map.track_map[x][y])
                self.attack(defender, loop)
            else:
                self.move(move_x, move_y, loop)

    def move(self, move_x, move_y, loop):
        if loop.generator.tile_map.get_passable(self.x + move_x, self.y + move_y) and loop.generator.monster_map.get_passable(self.x + move_x, self.y + move_y):
            self.character.energy -= (self.character.move_cost - self.character.dexterity)
            self.y += move_y
            self.x += move_x
        loop.add_message("The player moved.")

    def random_move(self, loop):
        random_move = [(0,1),(1,0),(-1,0),(0,-1)]
        rand_i = random.randint(0,3)
        move_x,move_y = random_move[rand_i]
        self.move(move_x,move_y, loop)

    def attack(self, defender, loop):
        self.character.energy -= (self.character.attack_cost - self.character.dexterity)
        if not self.character.dodge():
            damage = self.character.melee(defender)
            # if not defender.character.is_alive():
            #     self.experience += defender.experience_given
            #     self.check_for_levelup()
            loop.add_message(f"The player attacked for {damage} damage")
        else:
            loop.add_message("The monster dodged the attack")

    def autoexplore(self, loop):
        monster_dict = loop.monster_dict
        tile_map = loop.generator.tile_map
        for monster_key in monster_dict.subjects:
            if monster_dict.get_subject(monster_key).brain.is_awake:
                return
        while len(self.path) <= 1:
            start = (self.x, self.y)
            endx = random.randint(0, tile_map.width - 1)
            endy = random.randint(0, tile_map.height - 1)
            while (not tile_map.get_passable(endx, endy)) and not (tile_map.track_map[endx][endy].seen):
                if self.x == endx and self.y == endy:
                    loop.action = True
                    loop.autoexplore = False
                    loop.update_screen = True
                    return
                if endx != tile_map.width - 1:
                    endx += 1
                else:
                    endx = 0
                    if endy == tile_map.height - 1:
                        endy = 0
                    else:
                        endy += 1
            end = (endx, endy)
            self.path = pathfinding.astar(tile_map.track_map, start, end)
        x, y = self.path.pop(0)
        self.move(x-self.x, y-self.y, loop)
        loop.update_screen = True


    def check_for_levelup(self):
        if self.level != self.max_level and self.experience >= self.experience_to_next_level:
            self.level += 1
            self.character.level_up()
            self.experience_to_next_level += 20 + self.experience_to_next_level // 4
            self.experience = 0

