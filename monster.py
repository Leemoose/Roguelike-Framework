import monster as M
import objects as O
import character as C
import dice as R
import items as I
import random

import pathfinding
import skills as S


class Monster_AI():
    def __init__(self, parent):
        self.frontier = None
        self.is_awake = False
        self.parent = parent
        self.grouped = False
        self.target = None
        self.stairs_location = None
        self.old_key = None

        self.personality = {"Goblin":0,
                       "Kobold": 0,
                       "Player": -100,
                        "Hobgoblin": -10,
                        "Gargoyle": 10,
                        "Orc":-100,
                        "Golem":50
                       }

        #first number is average, second is spread
        self.tendencies = {"combat": (90, 10),
                           "pickup": (30,5),
                           "find_item": (20,10),
                           "equip": (40,5),
                           "consume": (40,5),
                           "move": (40, 20),
                           "ungroup": (60,20),
                           "skill": (100,10),
                           "flee":(100,20),
                           "stairs":(100,10)
                           }

        self.options = {"combat": (self.rank_combat, self.do_combat),
                   "pickup": (self.rank_pickup, self.do_item_pickup),
                   "find_item":(self.rank_find_item, self.do_find_item),
                   "equip": (self.rank_equip_item, self.do_equip), #need to be fixed
                   "consume": (self.rank_use_consumeable, self.do_use_consumeable),
                   "move": (self.rank_move, self.do_move),
                   "ungroup": (self.rank_ungroup, self.do_ungroup),
                   "skill": (self.rank_skill, self.do_skill),
                   "flee": (self.rank_flee, self.do_flee),
                   "stairs": (self.rank_stairs, self.do_stairs),
                   }

    """
    Think it would be better to first rank each action depending on the circumstances with a number between 1-100 and 
    then pick the action that ranks the highest
    """
    def randomize_action(self, action):
        average, spread = self.tendencies[action]
        return max(-1, random.randint(average - spread, average + spread))

    def rank_actions(self, loop):
        print(self.parent.character.energy)
        max_utility = 0
        called_function = (0,self.do_nothing)

        for action in self.options:
            utility = self.options[action][0](loop)
            if utility > max_utility:
                max_utility = utility
                called_function = action

        # print(max_utility)
        self.parent.character.energy -= 1
        print(f"{self.parent} is doing {called_function} with utility {max_utility}")
        self.options[called_function][1](loop)

    def rank_stairs(self, loop):
        if loop.taking_stairs == True:
            playerx, playery = loop.player.get_location()
            monsterx, monstery = self.parent.get_location()
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for x, y in directions:
                if isinstance(loop.generator.tile_map.locate(monsterx+x,monstery+y), O.Stairs) and monsterx+x == playerx and monstery + y == playery:
                    self.stairs_location = (monsterx + x, monstery + y)
                    return self.randomize_action("stairs")
        return -1

    def do_stairs(self, loop):
        stairs = loop.generator.tile_map.locate(self.stairs_location[0], self.stairs_location[1])
        if stairs.downward:
            new_level = loop.floor_level + 1
        else:
            new_level = loop.floor_level - 1

        new_generator = loop.memory.generators[new_level]
        monsterx, monstery = self.parent.get_location()
        new_stairs = stairs.pair
        empty_tile = new_generator.nearest_empty_tile(new_stairs.get_location(), move = True)
        if empty_tile != None:
            loop.generator.monster_map.clear_location(monsterx, monstery)
            self.old_key = self.parent.id_tag
            new_generator.monster_dict.tag_subject(self.parent)
            self.parent.x = empty_tile[0]
            self.parent.y = empty_tile[1]
            new_generator.monster_map.place_thing(self.parent)
            self.parent.character.energy = 0
            loop.add_message("The monster follows you on the stairs")


    def rank_flee(self, loop):
        if self.parent.character.flee:
            return self.randomize_action("flee") # must flee if flag is set
        return -1

    def rank_find_item(self, loop):
        if len(loop.item_dict.subjects) > 0:
            return self.randomize_action("find_item")
        return -1

    def rank_combat(self, loop):
        self.target = None
        utility = -1
        player = loop.player
        monster_map = loop.generator.monster_map
        directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        for xdiff,ydiff in directions:
            x = self.parent.x + xdiff
            y = self.parent.y + ydiff
            if (x,y) == player.get_location():
                if utility < -self.personality["Player"]:
                    utility = -self.personality["Player"]
                    self.target = player
            elif loop.generator.tile_map.get_passable(x,y) and not monster_map.get_passable(x,y):
                print(monster_map.locate(x,y), "want to attack this monster")
                other_monster = loop.generator.monster_dict.get_subject(monster_map.locate(x,y))
                if other_monster.name in self.personality and utility < -self.personality[other_monster.name]:
                    utility = -self.personality[other_monster.name]
                    self.target = other_monster
        if self.target != None:
            return self.randomize_action("combat")
        else:
            return -1

    def rank_pickup(self, loop):
        item_map = loop.generator.item_map
        monster = self.parent
        if item_map.locate(monster.x, monster.y) != -1:
            return self.randomize_action("pickup")
        else:
            return -1

    def rank_equip_item(self, loop): #Needs to be fixed
        monster = self.parent
        if len(monster.character.inventory) != 0:
            utility = -1
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.equipable:
                    if item.equipment_type == "Weapon" and monster.character.equipment_slots["hand_slot"][0] == None:
                        utility = 70
                    elif item.equipment_type == "Shield" and monster.character.equipment_slots["hand_slot"][1] == None:
                        if utility < 60:
                            utility = 60
                    elif item.equipment_type == "Body Armor" and monster.character.equipment_slots["body_armor_slot"][0] == None:
                        if utility < 60:
                            utility = 60
                    elif item.equipment_type == "Helmet" and monster.character.equipment_slots["helmet_slot"][0] == None:
                        if utility < 40:
                            utility = 40
                    elif item.equipment_type == "Boots" and monster.character.equipment_slots["boots_slot"][0] == None:
                        if utility < 20:
                            utility = 20
                    elif item.equipment_type == "Gloves" and monster.character.equipment_slots["gloves_slot"][0] == None:
                        if utility < 20:
                            utility = 20
                   # elif item.equipment_type == "Ring" and (monster.character.ring_1 == None or monster.character.ring_2 == None):
                    #    return -1
            if utility != -1:
                return random.randint(utility-10,utility+10)
        return -1

    def rank_use_consumeable(self, loop):
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable and item.equipment_type == "Potiorb": # monsters can't read so no scrolls
                    return -1
        return -1

    def rank_move(self, loop):
        return random.randint(20,40)

    def do_find_item(self, loop):
        monster = self.parent
        item_dict = loop.generator.item_dict
        distance = 1000
        item = None
        for key in item_dict.subjects:
            temp_item = item_dict.get_subject(key)
            temp_distance = monster.get_distance(temp_item.x, temp_item.y)
            if temp_distance < distance:
                distance = temp_distance
                item = temp_item
        if item == None:
            return
        else:
            moves = pathfinding.astar(loop.generator.tile_map.track_map,monster.get_location(), item.get_location(),loop.generator.monster_map.track_map, loop.player)
            if len(moves) > 1:
                xmove, ymove = moves.pop(1)
                monster.move(xmove - monster.x, ymove - monster.y, loop.generator.tile_map, monster, loop.generator.monster_map, loop.player)

    def rank_ungroup(self, loop):
        player = loop.player
        x,y = self.parent.x, self.parent.y
        tile_map = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        if player.get_distance(x,y) < 1.5:
            xplayer, yplayer = player.get_location()
            xdiff = xplayer - x
            ydiff = yplayer - y
            grouped = False
            goals = []
            if xdiff != 0:
                if (not tile_map.get_passable(x,y + 1) and not tile_map.get_passable(x,y - 1) and not monster_map.get_passable(x-xdiff,y)):
                    self.grouped = True
                    goals = [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer +ydiff)]
                for position in [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer +ydiff)]:
                    xposition, yposition = position
                    if not monster_map.get_passable(xposition,yposition):
                        try:
                            monster = loop.generator.monster_dict.get_subject(monster_map.track_map[xposition][yposition])
                            if monster.brain.grouped:
                                self.grouped = True
                                xdiff = xplayer - monster.x
                                ydiff = yplayer - monster.y
                                goals = [(xplayer + xdiff, yplayer + ydiff)]
                                break
                        except:
                            return -1
            elif ydiff != 0:
                if not tile_map.get_passable(x - 1,y) and not tile_map.get_passable(x + 1,y) and not monster_map.get_passable(x,y-ydiff):
                    self.grouped = True
                    goals = [(xplayer + 1, yplayer), (xplayer -1, yplayer), (xplayer + xdiff, yplayer + ydiff)]
                for position in [(xplayer + 1, yplayer), (xplayer -1, yplayer), (xplayer + xdiff, yplayer + ydiff)]:
                    xposition, yposition = position
                    if not monster_map.get_passable(xposition,yposition):
                        try:
                            monster = loop.generator.monster_dict.get_subject(monster_map.track_map[xposition][yposition])
                            if monster.brain.grouped:
                                self.grouped = True
                                xdiff = xplayer - monster.x
                                ydiff = yplayer - monster.y
                                goals = [(xplayer + xdiff, yplayer + ydiff)]
                                break
                        except: return -1
            if (self.grouped == True):
                self.move_path = (pathfinding.astar_multi_goal(tile_map.track_map, (x, y), goals,
                                             monster_map, player, True, True))
                if len(self.move_path) > 0:
                    return random.randint(60,100)
        return -1
    
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
        monster = self.parent
        if not monster.character.movable:
            monster.character.energy -= self.parent.character.action_costs["move"] #(monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot attack.")
            return
        monster.character.energy -= self.parent.character.action_costs["attack"]
        if self.target != None:
            damage = monster.character.melee(self.target)
            loop.add_message(f"{monster} attacked {self.target.name} for {damage} damage")
        else:
            loop.add_message(f"{monster.name} can find no suitable target to attack.")


    def do_skill(self, loop):
        monster = self.parent
        for i in range(len(monster.character.skills)):
            # use first castable skill
            if monster.character.skills[i].castable(loop.player):
                skill = monster.character.skills[i]
                skill_cast = monster.character.cast_skill(i, loop.player, loop)
                message_addition = "" if skill_cast else ". But it failed."
                loop.add_message(f"{monster} used {skill.name}" + message_addition)
                # print(f"{monster} used {skill.name}")
                break

    def do_equip(self, loop):
        # print("Equipping item")
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.equipable:
                    if item.equipment_type == "Weapon" and monster.character.equipment_slots["hand_slot"][0] == None:
                        monster.character.equip(item)
                        loop.add_message(self.parent.name + " is equipping " + item.name)
                        return
                    elif item.equipment_type == "Shield" and monster.character.equipment_slots["hand_slot"][1] == None:
                        monster.character.equip(item)
                        loop.add_message(self.parent.name + " is equipping " + item.name)
                        return
                    elif item.equipment_type == "Body Armor" and monster.character.equipment_slots["body_armor_slot"][
                        0] == None:
                        monster.character.equip(item)
                        loop.add_message(self.parent.name + " is equipping " + item.name)
                        return
                    elif item.equipment_type == "Helmet" and monster.character.equipment_slots["helmet_slot"][
                        0] == None:
                        monster.character.equip(item)
                        loop.add_message(self.parent.name + " is equipping " + item.name)
                        return
                    elif item.equipment_type == "Boots" and monster.character.equipment_slots["boots_slot"][0] == None:
                        monster.character.equip(item)
                        loop.add_message(self.parent.name + " is equipping " + item.name)
                        return
                    elif item.equipment_type == "Gloves" and monster.character.equipment_slots["gloves_slot"][
                        0] == None:
                        monster.character.equip(item)
                        loop.add_message(self.parent.name + " is equipping " + item.name)
                        return

    def do_use_consumeable(self, loop):
        # print("Using consumeable")
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable and item.equipment_type == "Potiorb": # monster's can't read so no scrolls
                    item.activate(monster.character)

    def do_move(self, loop):
        # print("Moving")
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player

        if not monster.character.movable:
            monster.character.energy -= self.parent.character.action_costs["move"] #(monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.screen_focus == (monster.x, monster.y):
            update_target = True

        start = (monster.x, monster.y)
        end = (player.x, player.y)
        if player.get_distance(monster.x, monster.y) <= 2.5:
            moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player, monster_blocks=True)
        else:
            moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player)
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            monster.move(xmove - monster.x, ymove-monster.y, tile_map, monster, monster_map, player)
        if update_target:
            loop.add_target((monster.x, monster.y))
            loop.screen_focus = (monster.x, monster.y)

    def do_ungroup(self, loop):
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player
        x,y = self.parent.x, self.parent.y

        if not monster.character.movable:
            monster.character.energy -= self.parent.character.action_costs["move"] #(monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.target_to_display == (monster.x, monster.y):
            update_target = True

        if player.get_distance(monster.x, monster.y) <= 2.5:
            moves = self.move_path
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            monster.move(xmove - monster.x, ymove-monster.y, tile_map, monster, monster_map, player)
            self.grouped = False
        if update_target:
            loop.add_target((monster.x, monster.y))
    def do_flee(self, loop):
        # print("Fleeing")
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player


        if not monster.character.movable:
            monster.character.energy -= self.parent.character.action_costs["move"] #(monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.screen_focus == (monster.x, monster.y):
            update_target = True

        start = (monster.x, monster.y)
        end = (player.x, player.y)
        moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player)
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            # if one direciton is blocked, still move in the other
            opposite_move = (-xmove + monster.x, -ymove + monster.y)
            if tile_map.get_passable(monster.x + opposite_move[0], monster.y + opposite_move[1]):
                monster.move(opposite_move[0], opposite_move[1], tile_map, monster, monster_map, player)
            elif tile_map.get_passable(monster.x, monster.y + opposite_move[1]):
                monster.move(0, opposite_move[1], tile_map, monster, monster_map, player)
            elif tile_map.get_passable(monster.x + opposite_move[0], monster.y):
                monster.move(opposite_move[0], 0, tile_map, monster, monster_map, player)
            else:
                monster.character.energy -= self.parent.character.action_costs["move"]#(monster.character.move_cost - monster.character.dexterity)
                loop.add_message(f"{monster} cowers in a corner since it can't run further.")
        if update_target:
            loop.add_target((monster.x, monster.y))
            loop.screen_focus = (monster.x, monster.y)
        

    def do_nothing(self,loop):
        # print("doing nothing")
        pass



class Monster(O.Objects):
    def __init__(self, x=-1, y = -1, render_tag = -1, name="Unknown monster"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.character = C.Character(self)
        self.asleep = False
        self.character.experience_given = 0
        self.brain = Monster_AI(self)
        self.skills = []
        self.orb = False
        self.kill_count = 0
        self.rarity = "Common"

        self.description = f"This is a {self.name}. It wants to eat you."

    def die(self):
        return

    def move(self, move_x, move_y, floormap, monster, monster_map, player):
        # print(self.character.movable)
        # print(move_x)
        # print(move_y)
        if not self.character.movable:
            self.character.energy -= self.character.action_costs["move"]#(self.character.move_cost - self.character.dexterity)
            return

        #Monsters can move ontop of players
        if floormap.get_passable(monster.x + move_x, monster.y + move_y) and monster_map.get_passable(monster.x + move_x, monster.y + move_y):
            self.character.energy -= self.character.action_costs["move"]
            monster_map.track_map[monster.x][monster.y] = -1
            monster.y += move_y
            monster.x += move_x
            monster_map.track_map[monster.x][monster.y] = monster.id_tag
    

    def __str__(self):
        return self.name

class Kobold(Monster):
    def __init__(self, x=-1, y=-1, render_tag=105, name="Kobold"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.skills = []
        self.character.skills.append(S.BurningAttack(self, cooldown=10, cost=0, damage=10, burn_damage=4, burn_duration=5, range=1.5))
        self.character.experience_given = 10
        self.character.health = 10
        self.character.max_health = 10
        self.endurance = 0
        self.strength = 0
        self.dexterity = 4
        self.intelligence = 4

        self.description = "A small, scaly creature with a mysterious satchel on its back."
class Goblin(Monster):
    def __init__(self, x = -1, y=-1, render_tag=103, name="Goblin", activation_threshold=0.4):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.skills.append(S.Escape(self, cooldown=100, 
                                              cost=0, self_fear=True, 
                                              dex_buff=20, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=activation_threshold, 
                                              action_cost=1))
        self.character.experience_given = 10

        self.character.action_costs["move"] = 75
        self.character.action_costs["grab"] = 20

        self.description = "A cowardly creature that some adventurers nicknamed \"Loot Pinata\"."
        self.character.health = 10
        self.character.max_health = 10

        self.strength = 1
        self.dexterity = 1
        self.endurance = 0
        self.intelligence = 0
        self.character.armor = 0

    def die(self):
        corpse = I.Corpse(self.x, self.y, -1, 199, self.name + " Monster Corpse")
        corpse.monster_type = self.name #Should be fixed to monster type at some point
        return corpse

class GoblinShaman(Monster):
    def __init__(self, x=-1, y=-1, render_tag=162, name="Goblin Shaman", activation_threshold=0.4):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.orb = True
        self.character.skills = []
        self.character.skills.append(S.SummonGoblin(self, cooldown=15, cost=0, range=4,action_cost=20))
        self.character.skills.append(S.Escape(self, cooldown=100,
                                              cost=0, self_fear=True,
                                              dex_buff=20, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=activation_threshold,
                                              action_cost=1))
        self.character.experience_given = 25
        self.description = "What's more cowardly than summoning your pals?"
        self.character.health = 20
        self.character.max_health = 20
        self.strength = 1
        self.dexterity = 1
        self.endurance = 1
        self.intelligence = 1
        self.character.armor = 0

class Hobgoblin(Monster):
    def __init__(self, x=-1, y=-1, render_tag=104, name="Hobgoblin"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.skills.append(S.BlinkStrike(self, cooldown=10, cost=0, damage=15, range=5, action_cost=1))
        self.character.skills.append(S.Escape(self, cooldown=100, 
                                              cost=0, self_fear=True, 
                                              dex_buff=30, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=0.3, 
                                              action_cost=1))
        self.character.experience_given = 10
        self.description = "The older cousin of its smaller green relatives."
        self.character.health = 25
        self.character.max_health = 25
        self.strength = 5
        self.dexterity = 1
        self.endurance = 3
        self.intelligence = 0
        self.character.armor = 0

class Gargoyle(Monster):
    def __init__(self, x=-1, y=-1, render_tag=106, name="Gargoyle"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.endurance = 5
        self.strength = 3
        self.dexterity = 1
        self.intelligence = 1
        self.skills = []
        # 30% chance to petrify for 3 turns
        self.character.skills.append(S.Petrify(self, cooldown=10, cost=0, duration=3, activation_chance=0.3, range=3))
        self.character.experience_given = 20

        self.description = "A stone creature that you feel could petrify you if it was rounder."
        self.character.health = 20
        self.character.max_health = 20
        self.strength = 2
        self.dexterity = 0
        self.endurance = 6
        self.intelligence = 5
        self.character.armor = 3

class Minotaur(Monster):
    def __init__(self, x=-1, y=-1, render_tag=108, name="Minotaur"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.skills.append(S.ShrugOff(self, cooldown=3, cost=0, activation_chance=0.75, action_cost=1))
        self.character.experience_given = 20
        self.description = "A large, angry bull with mighty horns."
        self.character.health = 40
        self.character.max_health = 40
        self.character.move_cost = 80
        self.strength = 5
        self.dexterity = 2
        self.endurance = 3
        self.intelligence = 0
        self.character.armor = 0

class Orc(Monster):
    def __init__(self, x=-1, y=-1, render_tag=101, name="Orc"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        # below 25% health, gains 25 strength
        self.character.skills.append(S.Berserk(self, cooldown=0, cost=0, duration=-100, activation_threshold=0.25, strength_increase=10, action_cost=1))
        self.character.experience_given = 20
        self.description = "A strong humanoid with anger issues."
        self.character.health = 30
        self.character.max_health = 30
        self.strength = 3
        self.dexterity = 0
        self.endurance = 3
        self.intelligence = 0
        self.character.armor = 1
class Golem(Monster):
    def __init__(self, x=-1, y=-1, render_tag=102, name="Golem"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.experience_given = 30
        self.description = "A large, slow creature made of stone."
        self.character.health = 25
        self.character.max_health = 25
        self.character.move_cost = 200
        self.strength = 2
        self.dexterity = 10
        self.endurance = 2
        self.intelligence = 2
        self.character.armor = 1

class Raptor(Monster):
    def __init__(self, x=-1, y=-1, render_tag=107, name="Velociraptor"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.character.move_cost = 50
        self.character.health = 20
        self.character.max_health = 20
        self.strength = 5
        self.dexterity = 12
        self.endurance = 0
        self.intelligence = 0
        self.character.armor = 0

        self.brain = Monster_AI(self)
        self.character.experience_given = 30
        self.description = "A very fast and very angry dinosaur."

class Tormentorb(Monster):
    def __init__(self, x=-1, y=-1, render_tag=159, name="Tormentorb"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.orb = True
        # self, parent, cooldown, cost, slow_duration, damage_percent, slow_amount, range, action_cost
        self.character.skills.append(S.Torment(self, cooldown=10, cost=0, slow_duration=3, damage_percent=0.5, slow_amount=5, range=4, action_cost=100))
        self.character.experience_given = 65
        self.description = "A floating orb that can torment and slow you with its gaze."
        self.character.health = 45
        self.character.max_health = 45
        self.strength = 8
        self.dexterity = 8
        self.endurance = 8
        self.intelligence = 8
        self.character.armor = 6

class BossOrb(Monster):
    def __init__(self, x=-1, y=-1, render_tag=160, name="ORB OF YENDORB"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.inventory.append(I.OrbOfYendorb())
        self.orb = True
        # self, parent, cooldown, cost, slow_duration, damage_percent, slow_amount, range, action_cost
        self.character.skills.append(S.Torment(self, cooldown=10, cost=0, slow_duration=3, damage_percent=0.5, slow_amount=5, range=4, action_cost=100))
        self.character.skills.append(S.SummonGoblin(self, cooldown=20, cost=0, range=4,action_cost=20))
        self.character.skills.append(S.Heal(self, cooldown = 20, cost = 10, heal_amount = 40, activation_threshold = .25, action_cost = 100))
        self.character.skills.append(S.Invinciblity(self, cooldown=1000, cost=0, duration=8, activation_threshold=0.1, by_scroll=False))

        self.character.experience_given = 0 # otherwise this inflates the outputted final levle
        self.description = "The orb of all orbs, the orbiest of orbs, the archetype of orbs... you get the idea."
        self.character.health = 45
        self.character.max_health = 45

        self.character.move_cost = 75
        self.character.attack_cost = 75
        self.strength = 18
        self.dexterity = 18
        self.endurance = 18
        self.intelligence = 18
        self.character.armor = 10

