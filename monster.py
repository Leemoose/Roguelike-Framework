import objects as O
import character as C
import dice as R
import random

import pathfinding
import skills as S


class Monster_AI():
    def __init__(self, parent):
        self.frontier = None
        self.is_awake = False
        self.parent = parent

    """
    Think it would be better to first rank each action depending on the circumstances with a number between 1-100 and 
    then pick the action that ranks the highest
    """
    def rank_actions(self, monster, monster_map, tile_map, flood_map, player, generated_maps, item_dict, loop):
        item_map = generated_maps.item_map
        max_utility = 0
        called_function = self.do_nothing

        utility = self.rank_combat(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_combat

        utility = self.rank_pickup(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_item_pickup

        utility = self.rank_equip_item(loop) #Needs to be fixed so that works with shields and swords
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_equip

        utility = self.rank_use_consumeable(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_use_consumeable

        utility = self.rank_move(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_move

        utility = self.rank_skill(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_skill

        # print(max_utility)
        self.parent.character.energy -= 1

        called_function(loop)


    def rank_combat(self, loop):
        player=loop.player
        playerx, playery = player.get_location()
        monster = self.parent
        monsterx, monstery = monster.get_location()
        distance = self.parent.get_distance(playerx, playery)
        if distance < 1.5:
            return 75
        else:
            return -1

    def rank_pickup(self, loop):
        item_map = loop.generator.item_map
        monster = self.parent
        if item_map.locate(monster.x, monster.y) != -1:
            return 60
        else:
            return -1

    def rank_equip_item(self, loop): #Needs to be fixed
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.equipable and monster.character.main_weapon == None:
                    return 80
        return -1

    def rank_use_consumeable(self, loop):
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable:
                    return 10
        return -1

    def rank_move(self, loop):
        return 20
    
    def rank_skill(self, loop):
        for skill in self.parent.character.skills:
            if skill.castable(loop.player):
                return 95
        return -1        


    def do_item_pickup(self, loop):
        # print("Picking up item")
        item_map = loop.generator.item_map
        item_dict = loop.generator.item_dict
        generated_maps = loop.generator
        monster = self.parent
        item_key = item_map.locate(monster.x, monster.y)
        monster.character.grab(item_key, item_dict, generated_maps, loop)

    def do_combat(self, loop):
        # print("Attacking player")
        player=loop.player
        monster = self.parent
        if not monster.character.movable:
            monster.character.energy -= (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot attack.")
            return
        if not player.character.dodge():
            damage = monster.character.melee(player)
            loop.add_message(f"{monster} attacked you for {damage} damage")
        else:
            loop.add_message("You dodged the monsters attack")

    def do_skill(self, loop):
        monster = self.parent
        for i in range(len(monster.character.skills)):
            # use first castable skill
            if monster.character.skills[i].castable(loop.player):
                skill = monster.character.skills[i]
                skill_cast = monster.character.cast_skill(i, loop.player, loop)
                message_addition = "" if skill_cast else ". But it failed."
                loop.add_message(f"{monster} used {skill.name}" + message_addition)
                print(f"{monster} used {skill.name}")
                break

    def do_equip(self, loop):
        # print("Equipping item")
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if monster.character.main_weapon == None and item.equipable:
                    monster.character.equip(item)

    def do_use_consumeable(self, loop):
        # print("Using consumeable")
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable:
                    item.activate(monster.character)

    def do_move(self, loop):
        # print("Moving")
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player

        if not monster.character.movable:
            monster.character.energy -= (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.target_to_display == (monster.x, monster.y):
            update_target = True

        start = (monster.x, monster.y)
        end = (player.x, player.y)
        moves = pathfinding.astar(tile_map.track_map, start, end)
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            monster.move(xmove - monster.x, ymove-monster.y, tile_map, monster, monster_map, player)
        if update_target:
            loop.add_target((monster.x, monster.y))

    def do_nothing(self,loop):
        # print("doing nothing")
        pass



class Monster(O.Objects):
    def __init__(self, number_tag, x, y, name="Unknown monster"):
        super().__init__(x, y, 0, number_tag, name)
        self.character = C.Character(self)
        self.character.experience_given = 10
        self.brain = Monster_AI(self)
        self.skills = []

    def move(self, move_x, move_y, floormap, monster, monster_map, player):
        # print(self.character.movable)
        # print(move_x)
        # print(move_y)
        if not self.character.movable:
            self.character.energy -= (self.character.move_cost - self.character.dexterity)
            return

        self.character.energy -= (self.character.move_cost - self.character.dexterity)
        #Monsters can move ontop of players
        if floormap.get_passable(monster.x + move_x, monster.y + move_y) and monster_map.get_passable(monster.x + move_x, monster.y + move_y):
            self.character.energy -= self.character.move_cost
            monster_map.track_map[monster.x][monster.y] = -1
            monster.y += move_y
            monster.x += move_x
            monster_map.track_map[monster.x][monster.y] = monster.id_tag
    
    def description(self):
        # default description for a monster is just its name
        return f"This is a {self.name}. It wants to eat you."

    def __str__(self):
        return self.name

class Kobold(Monster):
    def __init__(self, x, y):
        super().__init__(107, x, y, "Kobold")
        self.skills = []
        self.character.skills.append(S.BurningAttack(self, 10, 0, 10, 5, 5, 1.5))
        self.character.experience_given = 10

class Gargoyle(Monster):
    def __init__(self, x, y):
        super().__init__(108, x, y, "Gargoyle")
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.skills = []
        # 20% chance to petrify for 2 turns
        self.character.skills.append(S.Petrify(self, 10, 0, 2, 0.2, 3))
        self.character.experience_given = 10

class Raptor(Monster):
    def __init__(self, x, y):
        super().__init__(109, x, y, "Velociraptor")
        self.character = C.Character(self)
        self.character.move_cost = 100
        self.character.attack_cost = 100
        self.brain = Monster_AI(self)
        self.character.experience_given = 10

class Minotaur(Monster):
    def __init__(self, x, y):
        super().__init__(110, x, y, "Minotaur")
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.skills.append(S.ShrugOff(self, cooldown=3, cost=0, activation_chance=0.75, action_cost=1))
        self.character.experience_given = 10