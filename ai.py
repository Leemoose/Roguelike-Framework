import random
from navigation_utility import pathfinding

class Monster_AI():
    def __init__(self, parent):
        self.frontier = None
        self.is_awake = False
        self.parent = parent
        self.grouped = False
        self.target = None
        self.stairs_location = None
        self.old_key = None

        self.personality = {"Goblin": 0,
                            "Kobold": 0,
                            "Player": -90,
                            "Hobgoblin": -10,
                            "Gargoyle": 10,
                            "Orc": -100,
                            "Golem": 50,
                            "Slime": 50
                            }

        # first number is average, second is spread
        self.tendencies = {"combat": (90, 10),
                           "pickup": (30, 5),
                           "find_item": (20, 10),
                           "equip": (40, 5),
                           "consume": (40, 5),
                           "move": (40, 20),
                           "ungroup": (60, 20),
                           "skill": (-1, 0),
                           "flee": (100, 20),
                           "stairs": (100, 10)
                           }

        self.options = {"combat": (self.rank_combat, self.do_combat),
                        "pickup": (self.rank_pickup, self.do_item_pickup),
                        "find_item": (self.rank_find_item, self.do_find_item),
                        "equip": (self.rank_equip_item, self.do_equip),  # need to be fixed
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
    def change_tendency(self, type, new_value):
        if type in self.tendencies:
            self.tendencies[type] = new_value
        else:
            print("That {} cannot change their tendency ({})".format(self.parent, type))

    def get_tendency(self, type):
        if type in self.tendencies:
            return self.tendencies[type]
        else:
            print("That {} does not have that tendency ({})".format(self.parent, type))
            return -1

    def randomize_action(self, action):
        average, spread = self.tendencies[action]
        return max(-1, random.randint(average - spread, average + spread))

    def rank_actions(self, loop):
        # print(self.parent.character.energy)
        max_utility = 0
        called_function = (0, self.do_nothing)

        for action in self.options:
            utility = self.options[action][0](loop)
            if utility > max_utility:
                max_utility = utility
                called_function = action

        # print(max_utility)
        self.parent.character.energy -= 1
        # print(f"{self.parent} is doing {called_function} with utility {max_utility}")
        self.options[called_function][1](loop)

    def rank_stairs(self, loop):
        if loop.taking_stairs == True:
            playerx, playery = loop.player.get_location()
            monsterx, monstery = self.parent.get_location()
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for x, y in directions:
                if loop.generator.tile_map.locate(monsterx + x, monstery + y).has_trait("stairs") and monsterx + x == playerx and monstery + y == playery:
                    self.stairs_location = (monsterx + x, monstery + y)
                    return self.randomize_action("stairs")
        return -1

    def do_stairs(self, loop):
        stairs = loop.generator.tile_map.locate(self.stairs_location[0], self.stairs_location[1])
        if stairs.downward:
            new_level = loop.floor_level + 1
        else:
            new_level = loop.floor_level - 1

        new_generator = loop.memory.generators[loop.branch][new_level]
        new_stairs = stairs.pair
        empty_tile = new_generator.nearest_empty_tile(new_stairs.get_location(), move=True)
        if empty_tile != None:
            loop.generator.monster_map.remove_thing(self.parent)
            self.parent.x = empty_tile[0]
            self.parent.y = empty_tile[1]
            new_generator.monster_map.place_thing(self.parent)
            self.parent.character.energy = 0
            loop.add_message("The monster follows you on the stairs")

    def rank_flee(self, loop):
        # print("Does this monster have the flee condition? {}".format(self.parent.flee))
        if self.parent.flee or self.parent.character.health / self.parent.character.max_health < .25:
            return self.randomize_action("flee")  # must flee if flag is set
        return -1

    def rank_find_item(self, loop):
        if loop.generator.item_map.num_entities() > 0:
            return self.randomize_action("find_item")
        return -1

    def rank_combat(self, loop):
        self.target = None
        utility = -1
        player = loop.player
        monster_map = loop.generator.monster_map
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for xdiff, ydiff in directions:
            x = self.parent.x + xdiff
            y = self.parent.y + ydiff
            if (x, y) == player.get_location():
                if utility < -self.personality["Player"]:
                    utility = -self.personality["Player"]
                    self.target = player
            elif loop.generator.tile_map.get_passable(x, y) and not monster_map.get_passable(x, y):
                #print(monster_map.locate(x, y), "want to attack this monster")
                other_monster = loop.generator.monster_map.locate(x, y)
                if other_monster.name in self.personality and utility < -self.personality[other_monster.name]:
                    utility = -self.personality[other_monster.name]
                    self.target = other_monster
                    # print("{} is going to attack {}".format(self.parent.name, self.target.name))
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

    def rank_equip_item(self, loop):  # Needs to be fixed
        monster = self.parent
        if len(monster.character.inventory) != 0:
            utility = -1
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.equipable:
                    if item.equipment_type == "Weapon" and monster.character.free_equipment_slots("hand_slot") > 0:
                        utility = 70
                    elif item.equipment_type == "Shield" and monster.character.free_equipment_slots("hand_slot") > 0:
                        if utility < 60:
                            utility = 60
                    elif item.equipment_type == "Body Armor" and monster.character.free_equipment_slots("body_armor_slot") > 0:
                        if utility < 60:
                            utility = 60
                    elif item.equipment_type == "Helmet" and monster.character.free_equipment_slots("helmet_slot") > 0:
                        if utility < 40:
                            utility = 40
                    elif item.equipment_type == "Boots" and monster.character.free_equipment_slots("boots_slot") > 0:
                        if utility < 20:
                            utility = 20
                    elif item.equipment_type == "Gloves" and monster.character.free_equipment_slots("gloves_slot") > 0:
                        if utility < 20:
                            utility = 20
                # elif item.equipment_type == "Ring" and (monster.character.ring_1 == None or monster.character.ring_2 == None):
                #    return -1
            if self.tendencies["equip"][0] != -1:
                return random.randint(utility - 10, utility + 10)
        return -1

    def rank_use_consumeable(self, loop):
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable and item.equipment_type == "Potiorb":  # monsters can't read so no scrolls
                    return -1
        return -1

    def rank_move(self, loop):
        return random.randint(20, 40)

    def do_find_item(self, loop):
        monster = self.parent
        distance = 1000
        item = None
        for temp_item in loop.generator.item_map.all_entities():
            temp_distance = monster.get_distance(temp_item.x, temp_item.y)
            if temp_distance < distance:
                distance = temp_distance
                item = temp_item
        if item == None:
            return
        else:
            moves = pathfinding.astar(loop.generator.tile_map.track_map, monster.get_location(), item.get_location(),
                                      loop.generator.monster_map.track_map, loop.player)
            if len(moves) > 1:
                xmove, ymove = moves.pop(1)
                monster.move(xmove - monster.x, ymove - monster.y, loop)

    def rank_ungroup(self, loop):
        player = loop.player
        x, y = self.parent.x, self.parent.y
        tile_map = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        if player.get_distance(x, y) < 1.5:
            xplayer, yplayer = player.get_location()
            xdiff = xplayer - x
            ydiff = yplayer - y
            grouped = False
            goals = []
            if xdiff != 0:
                if (not tile_map.get_passable(x, y + 1) and not tile_map.get_passable(x,
                                                                                      y - 1) and not monster_map.get_passable(
                        x - xdiff, y)):
                    self.grouped = True
                    goals = [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer + ydiff)]
                for position in [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer + ydiff)]:
                    xposition, yposition = position
                    if not monster_map.get_passable(xposition, yposition):
                        try:
                            monster = loop.generator.monster_dict.get_subject(
                                monster_map.track_map[xposition][yposition])
                            if monster.brain.grouped:
                                self.grouped = True
                                xdiff = xplayer - monster.x
                                ydiff = yplayer - monster.y
                                goals = [(xplayer + xdiff, yplayer + ydiff)]
                                break
                        except:
                            return -1
            elif ydiff != 0:
                if not tile_map.get_passable(x - 1, y) and not tile_map.get_passable(x + 1,
                                                                                     y) and not monster_map.get_passable(
                        x, y - ydiff):
                    self.grouped = True
                    goals = [(xplayer + 1, yplayer), (xplayer - 1, yplayer), (xplayer + xdiff, yplayer + ydiff)]
                for position in [(xplayer + 1, yplayer), (xplayer - 1, yplayer), (xplayer + xdiff, yplayer + ydiff)]:
                    xposition, yposition = position
                    if not monster_map.get_passable(xposition, yposition):
                        try:
                            monster = loop.generator.monster_dict.get_subject(
                                monster_map.track_map[xposition][yposition])
                            if monster.brain.grouped:
                                self.grouped = True
                                xdiff = xplayer - monster.x
                                ydiff = yplayer - monster.y
                                goals = [(xplayer + xdiff, yplayer + ydiff)]
                                break
                        except:
                            return -1
            if (self.grouped == True):
                self.move_path = (pathfinding.astar_multi_goal(tile_map.track_map, (x, y), goals,
                                                               monster_map, player, True, True))
                if len(self.move_path) > 0:
                    return random.randint(60, 100)
        return -1

    def rank_skill(self, loop):
        return - 1
        if self.tendencies["skill"] == -1:
            return -1
        for skill in self.parent.character.skills:
            if skill.castable(loop.player):
                return self.randomize_action("skill")
        return -1

    def do_item_pickup(self, loop):
        # print("Picking up item")
        item_map = loop.generator.item_map
        monster = self.parent
        item = item_map.locate(monster.x, monster.y)
        monster.character.grab(item, loop)

    def do_combat(self, loop):
        # print("Attacking player")
        monster = self.parent
        if not monster.character.movable:
            monster.character.energy -= self.parent.character.action_costs[
                "move"]  # (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot attack.")
            return
        monster.character.energy -= self.parent.character.action_costs["attack"]
        if self.target != None:
            damage = monster.character.melee(self.target, loop)
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
                if item.consumeable and item.equipment_type == "Potiorb":  # monster's can't read so no scrolls
                    item.activate(monster.character)

    def do_move(self, loop):
        # print("Moving")
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player

        if not monster.character.movable:
            monster.character.energy -= self.parent.character.action_costs[
                "move"]  # (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.screen_focus == (monster.x, monster.y):
            update_target = True
        if self.target is not None:
            start = (self.target.x, self.target.y)
        else:
            start = (monster.x, monster.y)
        end = (player.x, player.y)
        if player.get_distance(monster.x, monster.y) <= 2.5:
            moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player, monster_blocks=True)
        else:
            moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player)
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            #print(self.parent.get_location(), "-->", end, "with", xmove - monster.x, ymove - monster.y)
            if loop.generator.get_passable((xmove, ymove)):
                monster.move(xmove - monster.x, ymove - monster.y, loop)

        if update_target:
            loop.add_target((monster.x, monster.y))
            loop.screen_focus = (monster.x, monster.y)

    def do_ungroup(self, loop):
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player
        x, y = self.parent.x, self.parent.y

        if not monster.character.movable:
            monster.character.energy -= self.parent.character.action_costs[
                "move"]  # (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.target_to_display == (monster.x, monster.y):
            update_target = True

        if player.get_distance(monster.x, monster.y) <= 2.5:
            moves = self.move_path
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            monster.move(xmove - monster.x, ymove - monster.y, loop)
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
            monster.character.energy -= self.parent.character.action_costs[
                "move"]  # (monster.character.move_cost - monster.character.dexterity)
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
                monster.move(opposite_move[0], opposite_move[1], loop)
            elif tile_map.get_passable(monster.x, monster.y + opposite_move[1]):
                monster.move(0, opposite_move[1], loop)
            elif tile_map.get_passable(monster.x + opposite_move[0], monster.y):
                monster.move(opposite_move[0], 0, loop)
            else:
                monster.character.energy -= self.parent.character.action_costs[
                    "move"]  # (monster.character.move_cost - monster.character.dexterity)
                loop.add_message(f"{monster} cowers in a corner since it can't run further.")
        if update_target:
            loop.add_target((monster.x, monster.y))
            loop.screen_focus = (monster.x, monster.y)

    def do_nothing(self, loop):
        # print("doing nothing")
        pass

class Goblin_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (60, 10),
                           "pickup": (100, 5),
                           "find_item": (80, 10),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (60, 20),
                           "skill": (80, 10),
                           "flee": (105, 10),
                           "stairs": (-1, 0)
                           }

        self.personality["Goblin"] =  100

class Stumpy_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (90, 10),
                           "pickup": (-1, 0),
                           "find_item": (-1, 00),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (80, 20),
                           "skill": (80, 10),
                           "flee": (-1, 0),
                           "stairs": (-1, 0)
                           }
        
class Dummy_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (-1, 0),
                           "pickup": (-1, 0),
                           "find_item": (-1, 0),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (100, 10),
                           "ungroup": (-1, 0),
                           "skill": (-1, 0),
                           "flee": (-1, 0),
                           "stairs": (-1, 0)
                           }
    
    def do_move(self, loop):
        return

class Slime_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "pickup": (100, 0),
                           "find_item": (-1, 0),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (-1, 0),
                           "skill": (-1, 0),
                           "flee": (-1, 0),
                           "stairs": (-1, 0)
                           }

    def do_item_pickup(self, loop):
        item_map = loop.generator.item_map
        monster = self.parent
        item = item_map.locate(monster.x, monster.y)
        monster.character.grab(item, loop)
        item.destroy = True
        loop.add_message("The slime gobbled up the {}.".format(item.name))

class Friendly_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "pickup": (-1, 0),
                           "find_item": (-1, 0),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (-1, 0),
                           "skill": (-1, 0),
                           "flee": (-1, 0),
                           "stairs": (100, 10)
                           }

        self.personality = {"Goblin": -100,
                            "Kobold": -100,
                            "Player": 100,
                            "Hobgoblin": -100,
                            "Gargoyle": -100,
                            "Orc": -100,
                            "Golem": -100,
                            "Slime": -50,
                            "Stumpy": -100
                            }


