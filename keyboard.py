import pygame
from loops import LoopType

class Keyboard():
    """
    Keyboard translates any player input into either a change of gamestate or an action. Any complicated checks
    should be done in the action, not here.
    First the player input or key is translated to a keyboard input (this allows inputs to change if we want).
    Then, depending on which mode the game is in, it will do a series of if else statements to pick correct action.
    """
    def __init__(self):
        keys_to_string = {}
        keys_to_string[pygame.K_a] = "a"
        keys_to_string[pygame.K_b] = "b"
        keys_to_string[pygame.K_c] = "c"
        keys_to_string[pygame.K_d] = "d"
        keys_to_string[pygame.K_e] = "e"
        keys_to_string[pygame.K_f] = "f"
        keys_to_string[pygame.K_g] = "g"
        keys_to_string[pygame.K_h] = "h"
        keys_to_string[pygame.K_i] = "i"
        keys_to_string[pygame.K_e] = "e"

        keys_to_string[pygame.K_w] = "w"
        keys_to_string[pygame.K_s] = "s"
        keys_to_string[pygame.K_UP] = "up"
        keys_to_string[pygame.K_LEFT] = "left"
        keys_to_string[pygame.K_DOWN] = "down"
        keys_to_string[pygame.K_RIGHT] = "right"

        keys_to_string[pygame.K_y] = "y"
        keys_to_string[pygame.K_n] = "n"

        keys_to_string[pygame.K_u] = "u"
        keys_to_string[pygame.K_q] = "q"
        keys_to_string[pygame.K_o] = "o"
        keys_to_string[pygame.K_l] = "l"
        keys_to_string[pygame.K_x] = "x"
        keys_to_string[pygame.K_t] = "t"
        keys_to_string[pygame.K_z] = "z"
        keys_to_string[pygame.K_ESCAPE] = "esc"
        keys_to_string[pygame.K_1] = "1"
        keys_to_string[pygame.K_2] = "2"
        keys_to_string[pygame.K_3] = "3"
        keys_to_string[pygame.K_4] = "4"
        keys_to_string[pygame.K_5] = "5"
        keys_to_string[pygame.K_6] = "6"
        keys_to_string[pygame.K_7] = "7"
        keys_to_string[pygame.K_8] = "8"
        keys_to_string[pygame.K_PERIOD] = "."
        keys_to_string[pygame.K_RETURN] = "return"
        keys_to_string[146] = ">"
        keys_to_string[144] = "<"

        self.keys_to_string = keys_to_string

    def key_string(self, key, shift_pressed):
        if not shift_pressed:
            return self.keys_to_string[key]
        else:
            return self.keys_to_string[key + 100]

#Any actions done in the battle screen
    def key_action(self, player, floormap, monsterID, monster_map, item_ID, loop, key, generated_maps, display, memory):
        if key == "up":
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
        elif key == "g":
            for item_key in item_ID.subjects:
                item = item_ID.subjects[item_key]
                if item.x == player.x and item.y == player.y:
                    player.character.grab(item_key, item_ID, generated_maps, loop)
                    break
        elif key == "i":
            loop.change_loop(LoopType.inventory)
        elif key == "e":
            loop.change_loop(LoopType.equipment)
        elif key == "q":
            loop.limit_inventory = "Potiorb"
            loop.change_loop(LoopType.inventory)
        elif key == "p":
            loop.display.set_visual_debug_mode(True)
        elif key == ">":
            loop.down_floor()
        elif key == "<":
            loop.up_floor()
        elif key == ".":
            player.character.wait()
            loop.add_message("The player waits.")
        elif key == 'x':
            loop.change_loop(LoopType.examine)
            loop.targets.start_target(loop.player.get_location())
            loop.add_target(loop.player.get_location())
        elif key == "o":
            loop.change_loop(LoopType.autoexplore)
        elif key == "s":
            memory.save_objects()
        elif key == "t":
            player.skills.teleport(loop.generator)
            loop.update_screen = True
        elif key == "esc":
            loop.change_loop(LoopType.paused)
        elif key == "z":
            loop.change_loop(LoopType.rest)
        elif key.isdigit():
            # cast a skill
            skill_num = int(key) - 1
            if skill_num < len(player.character.skills):
                if not player.character.skills[skill_num].targetted:
                    if player.character.skills[skill_num].castable(player):
                        player.character.cast_skill(skill_num, loop.player, loop)
                    else:
                        loop.add_message("You can't cast " + player.character.skills[skill_num].name + " right now.")
                else:
                    loop.change_loop(LoopType.targeting)
                    closest_dist = 100000
                    closest_monster = player
                    for monster_key in monsterID.subjects:
                        monster = monsterID.subjects[monster_key]
                        dist = player.get_distance(monster.x, monster.y)
                        
                        if dist < closest_dist and loop.generator.tile_map.track_map[monster.x][monster.y].visible:
                            closest_dist = dist
                            closest_monster = monster
                    # change closest_monster to targetted monster, maybe start at closest monster and let targetting begin
                    loop.targets.start_target(closest_monster.get_location())
                    loop.add_target(closest_monster.get_location())
                    loop.targets.store_skill(skill_num, player.character.skills[skill_num], player.character)

    def key_inventory(self, loop, player, item_dict, key):
            if key == "esc":
                if loop.limit_inventory == None:
                    loop.change_loop(LoopType.action)
                else:
                    loop.change_loop(LoopType.equipment)
                loop.limit_inventory = None

            for i in range(len(player.character.inventory)):
                if chr(ord("a")+i) == key:
                    loop.item_for_item_screen = player.character.inventory[i]
                    loop.change_loop(LoopType.items)

    def key_equipment(self, loop, player, item_dict, key):
        if key == "esc":
            loop.limit_inventory = None
            loop.change_loop(LoopType.action)
        elif key == "q":
            loop.limit_inventory = "Shield"
            loop.change_loop(LoopType.inventory)
        elif key == "a":
            loop.limit_inventory = "Ring"
            loop.change_loop(LoopType.inventory)
        elif key == "z":
            loop.limit_inventory = "Ring"
            loop.change_loop(LoopType.inventory)
        elif key == "w":
            loop.limit_inventory = "Helmet"
            loop.change_loop(LoopType.inventory)
        elif key == "s":
            loop.limit_inventory = "Armor"
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

    def key_main_screen(self, key, loop):
        if key == "esc":
            return False
        elif key == "l":
            loop.memory.load_objects()
            loop.load_game()
        else:
            loop.change_loop(LoopType.action)
            loop.init_new_game()
            loop.down_floor()
        return True
    
    def key_race_screen(self, key, loop):
        if key == "esc":
            loop.change_loop(LoopType.main)
        else:
            loop.change_loop(LoopType.classes)

    def key_class_screen(self, key, loop):
        if key == "esc":
            loop.change_loop(LoopType.race)   
        else:
            loop.change_loop(LoopType.action)
            loop.down_floor()

    def key_item_screen(self, key, loop, item_dict, player, item, item_map):
            if key == "esc":
                if loop.limit_inventory == None:
                    loop.change_loop(LoopType.inventory)
                else:
                    loop.change_loop(LoopType.equipment)
            elif key == "d":
                player.character.drop(item, item_dict, item_map)
                loop.change_loop(LoopType.inventory)
            elif key == "e":
                player.character.equip(item)
            elif key == "u":
                player.character.unequip(item)
            elif key == 'q':
                if player.character.quaff(item, item_dict, item_map):
                    loop.change_loop(LoopType.inventory)

    def key_paused(self, key, loop, display):
        if key == "esc":
            loop.change_loop(LoopType.action)
        elif key == "m":
            loop.change_loop(LoopType.main)
        elif key == "q":
            return False

        return True

    def key_targeting_screen(self, key, loop):
        loop.update_screen = True
        targets = loop.targets
        if key == "up":
            targets.adjust(0, -1)
            loop.add_target(targets.target_list)
        elif key == "left":
            targets.adjust(-1, 0)
            loop.add_target(targets.target_list)
        elif key == "down":
            targets.adjust(0, 1)
            loop.add_target(targets.target_list)
        elif key == "right":
            targets.adjust(1, 0)
            loop.add_target(targets.target_list)
        elif key == "y":
            targets.adjust(-1, -1)
            loop.add_target(targets.target_list)
        elif key == "u":
            targets.adjust(1, -1)
            loop.add_target(targets.target_list)
        elif key == "b":
            targets.adjust(-1, 1)
            loop.add_target(targets.target_list)
        elif key == "n":
            targets.adjust(1, 1)
            loop.add_target(targets.target_list)
        elif key == "esc":
            targets.void_skill()
            loop.void_target()
            loop.change_loop(LoopType.action)
        elif key == "return":
            if loop.currentLoop == LoopType.examine:
                targets.explain_target(loop)
            else:
                targets.cast_on_target(loop)
                loop.change_loop(LoopType.action)
                loop.void_target()

    def key_autoexplore(self, key, loop):
        if key == "o":
            loop.player.autoexplore(loop)
        else:
            loop.change_loop(LoopType.action)

