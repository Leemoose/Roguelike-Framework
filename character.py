import random
import dice as R
import objects as O

class Character():
    def __init__(self, parent, endurance = 0, intelligence = 0, dexterity = 0, strength = 0, speed = 100, health = 100, mana = 0):
        self.endurance = endurance
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.strength = strength

        self.speed = speed
        self.health = health
        self.max_health = health
        self.mana = mana

        self.energy = 0
        self.alive = True
        self.inventory = []
        self.main_weapon = None

        self.parent = parent


    def is_alive(self):
        if self.health <= 0:
            self.alive = False
            return False
        return True

    def take_damage(self, damage):
        self.health -= damage
        return self.is_alive()

    def gain_health(self, heal):
        self.health += heal
        if self.health > self.max_health:
            self.health = self.max_health


    def defend(self):
        defense = R.roll_dice(1, 1)[0]
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
            if self.main_weapon != None:
                self.unequip(self.main_weapon)
            self.main_weapon = item
            item.equipped = True
            item.dropable = False

    def unequip(self, item):
        if item.equipped:
            self.main_weapon = None
            item.dropable = True
            item.equipped = False

    def wait(self):
        self.energy -=  100

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
        defender.character.take_damage(damage - defense)

    def quaff(self, potion, item_dict, item_map):
        if potion.consumeable:
            potion.activate(self)
            self.drop(potion, item_dict, item_map)
            potion.destroy = True
            return True

class Player(O.Objects):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 200, "Player")
        self.character = Character(self)
        self.character.max_health = 200
        self.character.health = 200

        self.level = 1
        self.max_level = 20
        self.experience = 0
        self.experience_to_next_level = 20

    def attack_move(self, move_x, move_y, loop):
        x = self.x + move_x
        y = self.y + move_y
        if (x >= 0) & (y >= 0) & (x < loop.generator.tile_map.width) & (y < loop.generator.tile_map.height):
            if (loop.generator.monster_map.track_map[x][y]) != -1:
                defender = loop.monster_dict.get_subject(loop.generator.monster_map.track_map[x][y])
                self.attack(defender, loop)
            else:
                self.move(move_x, move_y, loop)

    def move(self, move_x, move_y, loop):
       # speed = self.speed + self.dexterity // 10
        if loop.generator.tile_map.get_passable(self.x + move_x, self.y + move_y) and loop.generator.monster_map.get_passable(self.x + move_x, self.y + move_y):
            self.character.energy -= 100
            self.y += move_y
            self.x += move_x
        loop.add_message("The player moved.")


    def attack(self, defender, loop):
        self.character.energy -= 100
        self.character.melee(defender)
        if not defender.character.is_alive():
            self.experience += defender.experience_given
            self.check_for_levelup()
        loop.add_message("The player attacked!")

    def check_for_levelup(self):
        if self.level != self.max_level and self.experience >= self.experience_to_next_level:
            self.level += 1
            self.character.level_up()
            self.experience_to_next_level += 20 + self.experience_to_next_level // 4
            self.experience = 0
