import random
import dice as R
import objects as O

class Character():
    def __init__(self, endurance = 0, intelligence = 0, dexterity = 0, strength = 0, speed = 100, health = 100, mana = 0):
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

        self.level = 1
        self.max_level = 20
        self.experience = 10
        self.experience_to_next_level = 20

    def is_alive(self):
        if self.health <= 0:
            self.alive = False
            return False
        return True

    def take_damage(self, damage):
        self.health -= damage
        return self.is_alive()

    def attack_move(self, move_x, move_y, floormap, monster, monsterID, monster_map, item_ID):
        x = monster.x + move_x
        y = monster.y + move_y
        if ((x>=0) & (y>=0) & (x < floormap.width) & (y < floormap.height)):
            if (monster_map.track_map[x][y]) != -1:
                defender = monsterID.get_subject(monster_map.track_map[x][y])
                self.attack(defender)
            else:
                self.move(move_x, move_y, floormap, monster, monster_map)


    def move(self, move_x, move_y, floormap, monster, monster_map):
        speed = self.speed + self.dexterity // 10
        if floormap.get_passable(monster.x + move_x, monster.y + move_y) and monster_map.get_passable(monster.x + move_x, monster.y + move_y):
            self.energy -= 100
            monster_map.track_map[monster.x][monster.y] = -1
            monster.y += move_y
            monster.x += move_x
            monster_map.track_map[monster.x][monster.y] = monster.id_tag


    def attack(self, defender):
        self.energy -= 100
        if self.main_weapon == None:
            damage = R.roll_dice(1, 20)[0]
        else:
            damage = self.main_weapon.attack()
        defense = defender.character.defend()
        if damage - defense > 0:
            alive = defender.character.take_damage(damage - defense)
            if not alive:
                self.experience += defender.character.experience
                self.check_for_levelup()

    def defend(self):
        defense = R.roll_dice(1, 1)[0]
        return defense

    def grab(self, key, item_ID, generated_maps):
        item = item_ID.get_subject(key)
        self.inventory.append(item)
        item_ID.remove_subject(key)
        itemx, itemy = item.get_location()
        generated_maps.item_map.clear_location(itemx, itemy)

    def drop(self, item, item_dict, x, y, item_map):
        if len(self.inventory) != 0 and item.dropable:
            i = 0
            while self.inventory[i].id_tag != item.id_tag and i < len(self.inventory):
                i += 1
            if i < len(self.inventory):
                self.inventory.pop(i)
                item_dict.add_subject(item)
                item.x = x
                item.y = y
                item_map.place_thing(item)


    def equip(self, item):
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

    def check_for_levelup(self):
        if self.level != self.max_level and self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.endurance += 1
        self.intelligence += 1
        self.dexterity += 1
        self.strength += 1
        self.experience = 0
        self.experience_to_next_level += 20 + self.experience_to_next_level // 4
        self.health = self.max_health

class Player(O.Objects):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 200, "Player")
        self.character = Character()
        self.character.max_health = 200
        self.character.health = 200

