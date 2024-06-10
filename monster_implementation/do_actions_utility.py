from navigation_utility import pathfinding

def do_nothing(ai, loop):
    # print("doing nothing")
    pass

def do_flee(ai, loop):
    # print("Fleeing")
    tile_map = loop.generator.tile_map
    monster = ai.parent
    monster_map = loop.generator.monster_map
    player = loop.player

    if not monster.character.movable:
        monster.character.energy -= ai.parent.character.action_costs[
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
            monster.character.energy -= ai.parent.character.action_costs[
                "move"]  # (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} cowers in a corner since it can't run further.")
    if update_target:
        loop.add_target((monster.x, monster.y))
        loop.screen_focus = (monster.x, monster.y)

def do_item_pickup(ai, loop):
    item_map = loop.generator.item_map
    monster = ai.parent
    item = item_map.locate(monster.x, monster.y)
    monster.character.grab(item, loop)
    item.destroy = True
    loop.add_message("The slime gobbled up the {}.".format(item.name))

def do_ungroup(ai, loop):
    tile_map = loop.generator.tile_map
    monster = ai.parent
    monster_map = loop.generator.monster_map
    player = loop.player
    x, y = ai.parent.x, ai.parent.y

    if not monster.character.movable:
        monster.character.energy -= ai.parent.character.action_costs[
            "move"]  # (monster.character.move_cost - monster.character.dexterity)
        loop.add_message(f"{monster} is petrified and cannot move.")
        return

    update_target = False
    if loop.target_to_display == (monster.x, monster.y):
        update_target = True

    if player.get_distance(monster.x, monster.y) <= 2.5:
        moves = ai.move_path
    if len(moves) > 1:
        xmove, ymove = moves.pop(1)
        monster.move(xmove - monster.x, ymove - monster.y, loop)
        ai.grouped = False
    if update_target:
        loop.add_target((monster.x, monster.y))

def do_item_pickup(ai, loop):
    # print("Picking up item")
    item_map = loop.generator.item_map
    monster = ai.parent
    item = item_map.locate(monster.x, monster.y)
    monster.character.grab(item, loop)

def do_combat(ai, loop):
    # print("Attacking player")
    monster = ai.parent
    if not monster.character.movable:
        monster.character.energy -= ai.parent.character.action_costs[
            "move"]  # (monster.character.move_cost - monster.character.dexterity)
        loop.add_message(f"{monster} is petrified and cannot attack.")
        return
    monster.character.energy -= ai.parent.character.action_costs["attack"]
    if ai.target != None:
        damage = monster.character.melee(ai.target, loop)
        loop.add_message(f"{monster} attacked {ai.target.name} for {damage} damage")
    else:
        loop.add_message(f"{monster.name} can find no suitable target to attack.")

def do_skill(ai, loop):
    monster = ai.parent
    for i in range(len(monster.character.skills)):
        # use first castable skill
        if monster.character.skills[i].castable(loop.player):
            skill = monster.character.skills[i]
            skill_cast = monster.character.cast_skill(i, loop.player, loop)
            message_addition = "" if skill_cast else ". But it failed."
            loop.add_message(f"{monster} used {skill.name}" + message_addition)
            # print(f"{monster} used {skill.name}")
            break

def do_equip(ai, loop):
    # print("Equipping item")
    monster = ai.parent
    if len(monster.character.inventory) != 0:
        stuff = monster.character.inventory
        for i, item in enumerate(stuff):
            if item.equipable:
                if item.equipment_type == "Weapon" and monster.character.equipment_slots["hand_slot"][0] == None:
                    monster.character.equip(item)
                    loop.add_message(ai.parent.name + " is equipping " + item.name)
                    return
                elif item.equipment_type == "Shield" and monster.character.equipment_slots["hand_slot"][1] == None:
                    monster.character.equip(item)
                    loop.add_message(ai.parent.name + " is equipping " + item.name)
                    return
                elif item.equipment_type == "Body Armor" and monster.character.equipment_slots["body_armor_slot"][
                    0] == None:
                    monster.character.equip(item)
                    loop.add_message(ai.parent.name + " is equipping " + item.name)
                    return
                elif item.equipment_type == "Helmet" and monster.character.equipment_slots["helmet_slot"][
                    0] == None:
                    monster.character.equip(item)
                    loop.add_message(ai.parent.name + " is equipping " + item.name)
                    return
                elif item.equipment_type == "Boots" and monster.character.equipment_slots["boots_slot"][0] == None:
                    monster.character.equip(item)
                    loop.add_message(ai.parent.name + " is equipping " + item.name)
                    return
                elif item.equipment_type == "Gloves" and monster.character.equipment_slots["gloves_slot"][
                    0] == None:
                    monster.character.equip(item)
                    loop.add_message(ai.parent.name + " is equipping " + item.name)
                    return

def do_use_consumeable(ai, loop):
    # print("Using consumeable")
    monster = ai.parent
    if len(monster.character.inventory) != 0:
        stuff = monster.character.inventory
        for i, item in enumerate(stuff):
            if item.consumeable and item.equipment_type == "Potiorb":  # monster's can't read so no scrolls
                item.activate(monster.character)

def do_move(ai, loop):
    # print("Moving")
    tile_map = loop.generator.tile_map
    monster = ai.parent
    monster_map = loop.generator.monster_map
    player = loop.player

    if not monster.character.movable:
        monster.character.energy -= ai.parent.character.action_costs[
            "move"]  # (monster.character.move_cost - monster.character.dexterity)
        loop.add_message(f"{monster} is petrified and cannot move.")
        return

    update_target = False
    if loop.screen_focus == (monster.x, monster.y):
        update_target = True
    if ai.target is not None:
        start = (ai.target.x, ai.target.y)
    else:
        start = (monster.x, monster.y)
    end = (player.x, player.y)
    if player.get_distance(monster.x, monster.y) <= 2.5:
        moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player, monster_blocks=True)
    else:
        moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player)
    if len(moves) > 1:
        xmove, ymove = moves.pop(1)
        #print(ai.parent.get_location(), "-->", end, "with", xmove - monster.x, ymove - monster.y)
        if loop.generator.get_passable((xmove, ymove)):
            monster.move(xmove - monster.x, ymove - monster.y, loop)

    if update_target:
        loop.add_target((monster.x, monster.y))
        loop.screen_focus = (monster.x, monster.y)



def do_stairs(ai, loop):
    stairs = loop.generator.tile_map.locate(ai.stairs_location[0], ai.stairs_location[1])
    if stairs.downward:
        new_level = loop.floor_level + 1
    else:
        new_level = loop.floor_level - 1

    new_generator = loop.memory.generators[loop.branch][new_level]
    new_stairs = stairs.pair
    empty_tile = new_generator.nearest_empty_tile(new_stairs.get_location(), move=True)
    if empty_tile != None:
        loop.generator.monster_map.remove_thing(ai.parent)
        ai.parent.x = empty_tile[0]
        ai.parent.y = empty_tile[1]
        new_generator.monster_map.place_thing(ai.parent)
        ai.parent.character.energy = 0
        loop.add_message("The monster follows you on the stairs")


def do_find_item(ai, loop):
    monster = ai.parent
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
