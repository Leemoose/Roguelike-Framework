import random
from navigation_utility import pathfinding

def rank_skill(ai, loop):
    return - 1
    if ai.tendencies["skill"] == -1:
        return -1
    for skill in ai.parent.character.skills:
        if skill.castable(loop.player):
            return ai.randomize_action("skill")
    return -1


def rank_ungroup(ai, loop):
    player = loop.player
    x, y = ai.parent.x, ai.parent.y
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
                ai.grouped = True
                goals = [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer + ydiff)]
            for position in [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer + ydiff)]:
                xposition, yposition = position
                if not monster_map.get_passable(xposition, yposition):
                    try:
                        monster = loop.generator.monster_dict.get_subject(
                            monster_map.track_map[xposition][yposition])
                        if monster.brain.grouped:
                            ai.grouped = True
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
                ai.grouped = True
                goals = [(xplayer + 1, yplayer), (xplayer - 1, yplayer), (xplayer + xdiff, yplayer + ydiff)]
            for position in [(xplayer + 1, yplayer), (xplayer - 1, yplayer), (xplayer + xdiff, yplayer + ydiff)]:
                xposition, yposition = position
                if not monster_map.get_passable(xposition, yposition):
                    try:
                        monster = loop.generator.monster_dict.get_subject(
                            monster_map.track_map[xposition][yposition])
                        if monster.brain.grouped:
                            ai.grouped = True
                            xdiff = xplayer - monster.x
                            ydiff = yplayer - monster.y
                            goals = [(xplayer + xdiff, yplayer + ydiff)]
                            break
                    except:
                        return -1
        if (ai.grouped == True):
            ai.move_path = (pathfinding.astar_multi_goal(tile_map.track_map, (x, y), goals,
                                                           monster_map, player, True, True))
            if len(ai.move_path) > 0:
                return random.randint(60, 100)
    return -1

def rank_combat(ai, loop):
    ai.target = None
    utility = -1
    player = loop.player
    monster_map = loop.generator.monster_map
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for xdiff, ydiff in directions:
        x = ai.parent.x + xdiff
        y = ai.parent.y + ydiff
        if (x, y) == player.get_location():
            if utility < -ai.personality["Player"]:
                utility = -ai.personality["Player"]
                ai.target = player
        elif loop.generator.tile_map.get_passable(x, y) and not monster_map.get_passable(x, y):
            #print(monster_map.locate(x, y), "want to attack this monster")
            other_monster = loop.generator.monster_map.locate(x, y)
            if other_monster.name in ai.personality and utility < -ai.personality[other_monster.name]:
                utility = -ai.personality[other_monster.name]
                ai.target = other_monster
                # print("{} is going to attack {}".format(ai.parent.name, ai.target.name))
    if ai.target != None:
        return ai.randomize_action("combat")
    else:
        return -1

def rank_pickup(ai, loop):
    item_map = loop.generator.item_map
    monster = ai.parent
    if item_map.locate(monster.x, monster.y) != -1:
        return ai.randomize_action("pickup")
    else:
        return -1

def rank_equip_item(ai, loop):  # Needs to be fixed
    return -1
    monster = ai.parent
    if monster.inventory.get_inventory_size() != 0:
        utility = -1
        stuff = monster.get_inventory()
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
        if ai.tendencies["equip"][0] != -1:
            return random.randint(utility - 10, utility + 10)
    return -1

def rank_use_consumeable(ai, loop):
    monster = ai.parent
    if monster.inventory.get_inventory_size() != 0:
        stuff = monster.get_inventory()
        for i, item in enumerate(stuff):
            if item.consumeable and item.equipment_type == "Potiorb":  # monsters can't read so no scrolls
                return -1
    return -1

def rank_move(ai, loop):
    return ai.randomize_action("move")

def rank_stairs(ai, loop):
    if loop.taking_stairs == True:
        playerx, playery = loop.player.get_location()
        monsterx, monstery = ai.parent.get_location()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for x, y in directions:
            if loop.generator.tile_map.locate(monsterx + x, monstery + y).has_trait("stairs") and monsterx + x == playerx and monstery + y == playery:
                ai.stairs_location = (monsterx + x, monstery + y)
                return ai.randomize_action("stairs")
    return -1

def rank_flee(ai, loop):
    # print("Does this monster have the flee condition? {}".format(ai.parent.flee))
    if ai.parent.flee or ai.parent.character.health / ai.parent.character.max_health < .25:
        return ai.randomize_action("flee")  # must flee if flag is set
    return -1

def rank_find_item(ai, loop):
    if loop.generator.item_map.num_entities() > 0:
        return ai.randomize_action("find_item")
    return -1

def rank_nothing(ai, loop):
    return ai.randomize_action("nothing")
