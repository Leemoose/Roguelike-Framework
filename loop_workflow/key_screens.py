from .looptype import LoopType
from character_implementation import talk

def key_targeting_screen(loop, key):
    loop.update_screen = True
    targets = loop.targets
    if key == "up":
        targets.adjust(0, -1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "left":
        targets.adjust(-1, 0, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "down":
        targets.adjust(0, 1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "right":
        targets.adjust(1, 0, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "y":
        targets.adjust(-1, -1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "u":
        targets.adjust(1, -1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "b":
        targets.adjust(-1, 1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "n":
        targets.adjust(1, 1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "esc":
        targets.void_skill()
        loop.void_target()
        loop.player.character.ready_scroll = None
        loop.change_loop(LoopType.action)
    elif key == "return":
        targets.cast_on_target(loop)
        loop.change_loop(LoopType.action)
        loop.void_target()

def key_examine_screen(loop, key):
    loop.update_screen = True
    targets = loop.targets
    if key == "up":
        targets.adjust(0, -1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "left":
        targets.adjust(-1, 0, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "down":
        targets.adjust(0, 1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "right":
        targets.adjust(1, 0, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "y":
        targets.adjust(-1, -1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "u":
        targets.adjust(1, -1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "b":
        targets.adjust(-1, 1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "n":
        targets.adjust(1, 1, loop.generator.tile_map, loop)
        loop.add_target(targets.target_current)
    elif key == "esc":
        targets.void_skill()
        loop.void_target()
        loop.change_loop(LoopType.action)
    elif key == "return":
        if targets.explain_target(loop):
            x, y = targets.target_current
            if loop.generator.monster_map.track_map[x][y] != -1:
                loop.screen_focus = loop.generator.monster_map.locate(x,y)
                loop.change_loop(LoopType.specific_examine)
            elif loop.generator.item_map.track_map[x][y] != -1:
                loop.screen_focus = loop.generator.item_map.locate(x,y)
                loop.change_loop(LoopType.specific_examine)
            else:
                loop.screen_focus = loop.generator.tile_map.track_map[x][y]
                loop.change_loop(LoopType.specific_examine)


def key_specific_examine(loop, key):
    if key == "esc":
        loop.change_loop(LoopType.examine)
        loop.screen_focus = loop.targets.target_current

def key_help(loop, key):
    if key == "esc":
        loop.change_loop(LoopType.main)
def key_quest(loop, key):
    print("Key that you are inputting for quest is: {}".format(key))
    if key == "esc":
        loop.change_loop(LoopType.action)
    if key in ("1","2","3","4","5","6","7","8","9"):
        loop.display.quest_number = int(key)
        print("The new quest number is {}".format(int(key)))
        loop.change_loop(loop.currentLoop)
def key_death(loop, key):
    if key == "esc":
        loop.clear_data()
        loop.init_game(loop.display)


# Any actions done in the battle screen
def key_action(loop, key):
    player = loop.player
    item_ID = loop.generator.item_map.dict
    generated_maps = loop.generator
    memory = loop.memory
    if key == -1:
        return
    elif key == "up":
        player.attack_move(0, -1, loop)
    elif key == "left":
        player.attack_move(-1, 0, loop)
    elif key == "down":
        player.attack_move(0, 1, loop)
    elif key == "right":
        player.attack_move(1, 0, loop)
    elif key == "y":
        player.attack_move(-1, -1, loop)
    elif key == "u":
        player.attack_move(1, -1, loop)
    elif key == "b":
        player.attack_move(-1, 1, loop)
    elif key == "n":
        player.attack_move(1, 1, loop)
    elif key == "g": #This could be so much simpler to grab, should change to just checking if item at location
        for item in loop.generator.item_map.all_entities():
            if item.x == player.x and item.y == player.y:
                player.do_grab(item, loop)
                break
    elif key == "f":
        for weapon in player.character.get_items_in_equipment_slot("hand_slot"):
            if weapon.has_trait("ranged_weapon"):
               # loop.start_targetting(start_on_player=True)
               # player.character.melee(loop.targets.target_current, loop)
                pass #change to targeting screen
    elif key == "i":
        #  loop.limit_inventory = None
        loop.change_loop(LoopType.inventory)
    elif key == "e":
        loop.change_loop(LoopType.equipment)
    elif key == "q":
        loop.limit_inventory = "Potiorb"
        loop.change_loop(LoopType.inventory)
    elif key == "r":
        loop.limit_inventory = "Scrorb"
        loop.change_loop(LoopType.inventory)
    elif key == "l":
        if loop.player.stat_points > 0:
            loop.change_loop(LoopType.level_up)
    #elif key == "p":
    #    if loop.player.invincible:
    #        loop.display.uiManager.set_visual_debug_mode(True)
    elif key == "s":
        loop.player.find_stairs(loop)
        if loop.player.path:
            loop.change_loop(LoopType.pathing)
    elif key == "p":
        loop.change_loop(LoopType.spell)
    elif key == ">":
        loop.player.down_stairs(loop)
    elif key == "<":
        loop.player.up_stairs(loop)
    elif key == ".":
        player.character.wait()
        loop.add_message("The player waits.")
    elif key == 'x':
        loop.change_loop(LoopType.examine)
        loop.targets.start_target(loop.player.get_location())
        loop.add_target(loop.player.get_location())
        loop.screen_focus = loop.targets.target_current
        loop.update_screen = True
    elif key == "o":
        print(loop.generator.tile_map)
        # loop.player.autoexplore(loop)
        loop.player.autoexplore(loop)
        if loop.player.path:
            loop.change_loop(LoopType.pathing)
    elif key == "t":
        talk(loop.player, loop)
    elif key == "esc":
        loop.change_loop(LoopType.paused)
    elif key == "z":
        loop.after_rest = LoopType.action
        loop.change_loop(LoopType.resting)
    elif key == 'c':
        loop.change_loop(LoopType.quest)
    elif key == "tab":
        player.smart_attack(loop)
    elif key in "12345678": # upto 8 quick cast skills
        # cast a skill
        skill_num = int(key) - 1
        if skill_num < len(player.mage.quick_cast_spells):
            if player.mage.quick_cast_spells[skill_num] == None:
                return
            if not player.mage.quick_cast_spells[skill_num].targetted:
                if player.mage.quick_cast_spells[skill_num].castable(player):
                    print("Casted a spell.")
                    player.mage.cast_spell(skill_num, loop.player, loop, quick_cast=True)
                else:
                    loop.add_message("You can't cast " + player.mage.quick_cast_spells[skill_num].name + " right now.")
            else:
                loop.start_targetting(start_on_player=(not player.mage.quick_cast_spells[skill_num].targets_monster))
                loop.screen_focus = loop.targets.target_current
                loop.targets.store_skill(skill_num, player.mage.quick_cast_spells[skill_num], player.character, quick_cast=True)

def key_inventory(loop, key):
    player = loop.player
    if key == "esc":
        if loop.limit_inventory == None or loop.limit_inventory == "Potiorb" or loop.limit_inventory == "Scrorb":
            loop.change_loop(LoopType.action)
        else:
            loop.change_loop(LoopType.equipment)
        loop.limit_inventory = None

    for i in range(len(player.get_inventory())):
        if chr(ord("a") + i) == key:
            if loop.limit_inventory == None or player.inventory[i].equipment_type == loop.limit_inventory:
                loop.screen_focus = player.get_inventory()[i]
                loop.change_loop(LoopType.items)


def key_rest(loop, key):
    loop.add_message("Input detected. Ending rest early.")
    loop.change_loop(LoopType.action)


def key_explore(loop, key):
    loop.add_message("Input detected. Ending exploration early.")
    loop.player.path = []
    loop.change_loop(LoopType.action)


def key_enchant(loop, key):
    player = loop.player
    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.limit_inventory = None
        player.character.ready_scroll = None
    enchantable = player.character.get_enchantable()
    for i in range(len(player.get_inventory())):
        if chr(ord("a") + i) == key and player.get_inventory()[i] in enchantable:
            item = player.get_inventory()[i]
            player.character.ready_scroll.consume_scroll(player.character)
            item.level_up()

            loop.change_loop(LoopType.action)
            loop.limit_inventory = None
            loop.update_screen = True


def key_trade(loop, key):
    player = loop.player
    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.next_dialogue = False
        loop.dialogue_options = 0
        loop.player_choice = -1
        return
    elif key == "return" and loop.dialogue_options == 0:
        loop.next_dialogue = True
    elif loop.dialogue_options > 0 and key in "123456789": # almost definitely don't have this many dialogue options but jic
        loop.npc_focus.change_purpose(int(key), loop)
        loop.player_choice = int(key)
        loop.next_dialogue = False
    elif loop.npc_focus.purpose == "trade":
        for i in range(len(loop.npc_focus.items)):
            if chr(ord("a") + i) == key:
                loop.npc_focus.take_gold(i, loop)
                break
    elif loop.npc_focus.talking and loop.dialogue_options == 0:
        loop.next_dialogue = True


def key_level_up(loop, key):
    player = loop.player
    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.current_stat = 0
        player.stat_decisions = [0, 0, 0, 0]
    elif key == "up":
        if loop.current_stat > 0:
            loop.current_stat -= 1
    elif key == "down":
        if loop.current_stat < 3:
            loop.current_stat += 1
    elif key == "left":
        player.modify_stat_decisions(loop.current_stat, increase=False)
    elif key == "right":
        player.modify_stat_decisions(loop.current_stat, increase=True)
    elif key == "return":
        player.apply_level_up()
        loop.current_stat = 0
        loop.change_loop(LoopType.action)


def key_equipment(loop, key):
    player = loop.player
    if key == "esc":
        loop.limit_inventory = None
        loop.change_loop(LoopType.action)
    elif key == "q":
        loop.limit_inventory = "Shield"
        loop.change_loop(LoopType.inventory)
    elif key == "a":
        loop.limit_inventory = "Amulet"
        loop.change_loop(LoopType.inventory)
    elif key == "z":
        loop.limit_inventory = "Ring"
        player.character.force_ring = 2  # equip to second slot
        loop.change_loop(LoopType.inventory)
    elif key == "w":
        loop.limit_inventory = "Helmet"
        loop.change_loop(LoopType.inventory)
    elif key == "s":
        loop.limit_inventory = "Body Armor"
        loop.change_loop(LoopType.inventory)
    elif key == "x":
        loop.limit_inventory = "Boots"
        loop.change_loop(LoopType.inventory)
    elif key == "d":
        loop.limit_inventory = "Weapon"
        loop.change_loop(LoopType.inventory)
    elif key == "c":
        loop.limit_inventory = "Gloves"
        loop.change_loop(LoopType.inventory)
    elif key == "p":
        loop.limit_inventory = "Pants"
        loop.change_loop(LoopType.inventory)
    elif key == "r":
        loop.limit_inventory = "Ring"
        player.character.force_ring = 1
        loop.change_loop(LoopType.inventory)


def key_main_screen(loop, key):
    if key == "esc":
        return False
    elif key == "l":
        loop.memory.load_objects()
        loop.load_game()
    elif key == "h":
        loop.change_loop(LoopType.help)
    elif key == "s":
        loop.change_loop(LoopType.story)
    else:
        loop.change_loop(LoopType.classes)
    return True


def key_item_screen(loop, key):
    player = loop.player
    item = loop.screen_focus
    item_map = loop.generator.item_map
    item_dict = None #Should not be used
    if key == "esc":
        player.character.force_ring = -1
        if loop.limit_inventory == None:
            loop.change_loop(LoopType.inventory)
        else:
            if item.equipable and item.equipped:
                loop.change_loop(LoopType.equipment)
            else:
                loop.change_loop(LoopType.inventory)
    elif key == "d":
        if player.do_drop(item, item_map):
            loop.change_loop(LoopType.inventory)
    elif key == "e":
        player.character.equip(item)
    elif key == "u":
        player.character.unequip(item)
    elif key == 'q':
        if player.character.quaff(item, item_dict, item_map):
            loop.change_loop(LoopType.inventory)
    elif key == "r":
        player.character.read(item, loop, item_dict, item_map)
        # loop.currentLoop = LoopType.action
    loop.change_loop(loop.currentLoop)


def key_victory(loop, key):
    display = loop.display
    loop.change_loop(LoopType.main)
    loop.clear_data()
    loop.init_game(display)


def key_paused(loop, key):
    display = loop.display
    if key == "esc":
        loop.change_loop(LoopType.action)
    elif key == "m":
        loop.change_loop(LoopType.main)
        loop.clear_data()
        loop.init_game(display)
    elif key == 's':
        loop.memory.keyboard =  loop.keyboard
        loop.memory.save_objects()
    elif key == "q":
        return False
    elif key == "b":
        loop.change_loop(LoopType.binding)
        loop.add_message("Please enter the key you want to map from (click return when done):")
    return True

def key_spell(loop, key):
    player = loop.player
    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.current_spell = None
    else:
        if isinstance(key, str) and len(key) == 1:
            skill_num = (ord(key) - 97)
            if skill_num < len(player.mage.known_spells) and skill_num >= 0:
                loop.current_spell = skill_num
                loop.change_loop(LoopType.spell_individual)

def key_spell_individual(loop, key):
    player = loop.player
    skill_num = loop.current_spell
    if key == "esc":
        loop.change_loop(LoopType.spell)
        loop.current_spell = None
    elif key == "c":
        if not player.mage.known_spells[skill_num].targetted:
            if player.mage.known_spells[skill_num].castable(player):
                print("Casted a spell.")
                player.cast_spell(skill_num, loop.player, loop)
                loop.current_spell = None
            else:
                loop.add_message("You can't cast " + player.mage.known_spells[skill_num].name + " right now.")
                loop.current_spell = None
        else:
            loop.start_targetting(start_on_player=(not player.mage.known_spells[skill_num].targets_monster))
            loop.screen_focus = loop.targets.target_current
            loop.targets.store_skill(skill_num, player.mage.known_spells[skill_num], player.character)
            loop.current_spell = None
    elif key == "q":
        loop.change_loop(LoopType.quickcast)


def key_quickselect(loop, key):
    player = loop.player
    spell = player.mage.known_spells[loop.current_spell]
    if key == "esc":
        loop.change_loop(LoopType.spell_individual)
    elif key == "p":
        loop.change_loop(LoopType.spell)
    elif key in "12345678": # upto 8 quick cast skills
        # cast a skill
        skill_num = int(key) - 1
        if skill_num < len(player.mage.quick_cast_spells):
            player.mage.set_quick_cast(spell, skill_num)
            loop.change_loop(LoopType.action)

def key_binding(loop, key):
    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.clear_message()
    else:
        if loop.keyboard.key_bindings.accepting_binding == False:
            if key == "return":
                loop.keyboard.key_bindings.accepting_binding = True
                loop.clear_message()
                loop.add_message("Please enter the keys you want to map to (click return when done): ")
            else:
                loop.keyboard.key_bindings.temp_binding = key
                loop.clear_message()
                loop.add_message("The key you have chosen is: " + key)
        else:
            if key == "return":
                loop.keyboard.key_bindings.save_key_binding()
                loop.change_loop(LoopType.action)
                loop.clear_message()
            else:
                loop.keyboard.key_bindings.temp_binding_map.append(key)
                loop.clear_message()
                messages = ""
                for m in loop.keyboard.key_bindings.temp_binding_map:
                    messages += m + " "
                loop.add_message("The keys you have chosen are: " + messages)
    return True

def key_classes(loop, key):
    if key == "esc":
        loop.change_loop(LoopType.main)
    elif key == "return" and loop.class_selection != None:
        loop.implement_class()
        loop.change_loop(LoopType.action)
    if key in ("1","2","3","4","5","6","7","8","9"):
        classes = loop.get_available_classes()
        if int(key) <= len(classes):
            loop.class_selection = classes[int(key) - 1]
        loop.change_loop(loop.currentLoop)