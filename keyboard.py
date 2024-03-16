import pygame
from loops import LoopType
import skills as S
import objects as O

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
        keys_to_string[pygame.K_j] = "j"
        keys_to_string[pygame.K_k] = "k"
        keys_to_string[pygame.K_l] = "l"
        keys_to_string[pygame.K_m] = "m"
        keys_to_string[pygame.K_n] = "n"
        keys_to_string[pygame.K_o] = "o"
        keys_to_string[pygame.K_p] = "p"
        keys_to_string[pygame.K_q] = "q"
        keys_to_string[pygame.K_r] = "r"
        keys_to_string[pygame.K_s] = "s"
        keys_to_string[pygame.K_t] = "t"
        keys_to_string[pygame.K_u] = "u"
        keys_to_string[pygame.K_v] = "v"
        keys_to_string[pygame.K_w] = "w"
        keys_to_string[pygame.K_x] = "x"
        keys_to_string[pygame.K_y] = "y"
        keys_to_string[pygame.K_z] = "z"

        keys_to_string[pygame.K_UP] = "up"
        keys_to_string[pygame.K_LEFT] = "left"
        keys_to_string[pygame.K_DOWN] = "down"
        keys_to_string[pygame.K_RIGHT] = "right"

        keys_to_string[pygame.K_ESCAPE] = "esc"
        keys_to_string[pygame.K_1] = "1"
        keys_to_string[pygame.K_2] = "2"
        keys_to_string[pygame.K_3] = "3"
        keys_to_string[pygame.K_4] = "4"
        keys_to_string[pygame.K_5] = "5"
        keys_to_string[pygame.K_6] = "6"
        keys_to_string[pygame.K_7] = "7"
        keys_to_string[pygame.K_8] = "8"
        keys_to_string[pygame.K_9] = "9"
        keys_to_string[pygame.K_PERIOD] = "."
        keys_to_string[pygame.K_RETURN] = "return"
        keys_to_string[">"] = ">"
        keys_to_string["<"] = "<"

        self.keys_to_string = keys_to_string

    def key_string(self, key, shift_pressed):
        if not shift_pressed:
            return self.keys_to_string[key]
        else:
            try:
                src = r"`1234567890-=qwertyuiop[]\asdfghjkl;\'zxcvbnm,./"
                dest = r'~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
                if key <= 10000:
                    print(key)
                    ch = chr(key)
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT] and ch in src:
                        ch = dest[src.index(ch) -1]
                        print(ch)
                        return self.keys_to_string[ch]
            except:
                return -1
        return -1

#Any actions done in the battle screen
    def key_action(self, loop, key):
        player = loop.player
        item_ID = loop.generator.item_dict
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
        elif key == "g":
            for item_key in item_ID.subjects:
                item = item_ID.subjects[item_key]
                if item.x == player.x and item.y == player.y:
                    player.character.grab(item_key, item_ID, generated_maps, loop)
                    break
        elif key == "i":
            loop.change_loop(LoopType.inventory)
        elif key == "e" or key == "c":
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
        elif key == "p":
            if loop.player.invincible:
                loop.display.uiManager.set_visual_debug_mode(True)
        elif key == "s":
            # find stairs
            if loop.generator.tile_map.track_map[loop.generator.tile_map.stairs[0].x][loop.generator.tile_map.stairs[0].y].seen:
                player.find_stairs(loop)
            else:
                loop.add_message("You haven't found the way down yet")
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
            loop.screen_focus = loop.targets.target_current
            loop.update_screen = True
        elif key == "o":
            loop.player.autoexplore(loop)
        elif key == "m":
            memory.save_objects()
        # elif key == "t":
        #     escape_test = S.Escape(player, 0, 0, False, 1.1, 1)
        #     player.character.add_skill(escape_test)
        #     player.character.cast_skill_by_name("Escape", player, loop)
        #     player.character.remove_skill("Escape")
        #     loop.update_screen = True
        elif key == "esc":
            loop.change_loop(LoopType.paused)
        elif key == "z":
            player.character.rest(loop, loop.currentLoop)
        elif key.isdigit():
            # cast a skill
            skill_num = int(key) - 1
            if skill_num < len(player.character.skills):
                if not player.character.skills[skill_num].targetted:
                    print(player.character.skills[skill_num].castable(player))
                    if player.character.skills[skill_num].castable(player):
                        player.character.cast_skill(skill_num, loop.player, loop)
                    else:
                        loop.add_message("You can't cast " + player.character.skills[skill_num].name + " right now.")
                else:
                    loop.start_targetting(start_on_player=(not player.character.skills[skill_num].targets_monster))
                    loop.screen_focus = loop.targets.target_current
                    loop.targets.store_skill(skill_num, player.character.skills[skill_num], player.character)

    def key_inventory(self, loop, key):
        player = loop.player
        if key == "esc":
            if loop.limit_inventory == None or loop.limit_inventory == "Potiorb" or loop.limit_inventory == "Scrorb":
                loop.change_loop(LoopType.action)
            else:
                loop.change_loop(LoopType.equipment)
            loop.limit_inventory = None

        for i in range(len(player.character.inventory)):
            if chr(ord("a")+i) == key:
                if loop.limit_inventory == None or player.character.inventory[i].equipment_type == loop.limit_inventory:
                    loop.screen_focus = player.character.inventory[i]
                    loop.change_loop(LoopType.items)

    def key_enchant(self, loop, key):
        player = loop.player
        if key == "esc":
            loop.change_loop(LoopType.action)
            loop.limit_inventory = None
            player.character.ready_scroll = None
        for i in range(len(player.character.inventory)):
            if chr(ord("a")+i) == key:
                item = player.character.inventory[i]
                player.character.ready_scroll.consume_scroll(player.character)
                item.level_up()

                loop.change_loop(LoopType.action)
                loop.limit_inventory = None
                loop.update_screen = True

    def key_level_up(self, loop, key):
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
            

    def key_equipment(self, loop, key):
        player = loop.player
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
            player.character.force_ring_2 = True # equip to second slot
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

    def key_main_screen(self, loop, key):
        if key == "esc":
            return False
        elif key == "l":
            try:
                loop.memory.load_objects()
                loop.load_game()
            except:
                pass
        elif key == "h":
            loop.change_loop(LoopType.help)
        elif key == "s":
            loop.change_loop(LoopType.story)
        else:
            loop.down_floor()
            loop.change_loop(LoopType.action)
        return True


    def key_item_screen(self, loop, key):
        item_dict = loop.generator.item_dict
        player = loop.player
        item = loop.screen_focus
        item_map = loop.generator.item_map
        if key == "esc":
            if loop.limit_inventory == None:
                loop.change_loop(LoopType.inventory)
            else:
                if item.equipable and item.equipped:
                    loop.change_loop(LoopType.equipment)
                else:
                    loop.change_loop(LoopType.inventory)
        elif key == "d":
            if player.character.drop(item, item_dict, item_map):
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
                
    def key_victory(self, loop, key):
        display = loop,display
        loop.change_loop(LoopType.main)
        loop.clear_data()
        loop.init_game(display)

    def key_paused(self, loop, key):
        display = loop.display
        if key == "esc":
            loop.change_loop(LoopType.action)
        elif key == "m":
            loop.change_loop(LoopType.main)
            loop.clear_data()
            loop.init_game(display)
        elif key == 's':
            loop.memory.save_objects()
        elif key == "q":
            return False
        return True

    def key_targeting_screen(self, loop, key):
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

    def key_examine_screen(self, loop, key):
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
                    loop.screen_focus = loop.generator.monster_dict.get_subject(loop.generator.monster_map.track_map[x][y])
                    loop.change_loop(LoopType.specific_examine)
                elif loop.generator.item_map.track_map[x][y] != -1:
                    loop.screen_focus = loop.generator.item_dict.get_subject(loop.generator.item_map.track_map[x][y])
                    loop.change_loop(LoopType.specific_examine)
                else:
                    loop.screen_focus = loop.generator.tile_map.track_map[x][y]
                    loop.change_loop(LoopType.specific_examine)


    def key_specific_examine(self, loop, key):
        if key == "esc":
            loop.change_loop(LoopType.examine)
            loop.screen_focus = loop.targets.target_current

    def key_help(self, loop, key):
        if key == "esc":
            loop.change_loop(LoopType.main)

    def key_death(self, loop, key):
        if key == "esc":
            loop.clear_data()
            loop.init_game(loop.display)

    def action_mouse_to_keyboard(self, loop, x_tile, y_tile):
        player = loop.player
        if player.get_distance(x_tile, y_tile) == 0:
            if not loop.generator.item_map.get_passable(player.x, player.y):
               return self.key_action(loop, "g")
            elif isinstance(loop.generator.tile_map.track_map[player.x][player.y], O.Stairs):
                return self.key_action(loop, ">") #Needs to be able to work with upstairs as well
        elif loop.player.get_distance(x_tile, y_tile) < 1.5:
            xdiff = x_tile - player.x
            ydiff = y_tile - player.y
            options = {(1,1): "n",
                       (1,0): "right",
                       (1,-1): "u",
                       (0,1): "down",
                       (0,-1): "up",
                       (-1,1): "b",
                       (-1,0): "left",
                       (-1,-1): "y"}
            self.key_action(loop, options[(xdiff, ydiff)])

    def targetting_mouse_to_keyboard(self, loop, x_tile, y_tile):
        if loop.generator.tile_map.in_map(x_tile, y_tile):
            if x_tile != loop.targets.target_current[0] or y_tile != loop.targets.target_current[1]:
                if loop.generator.tile_map.get_passable(x_tile, y_tile):
                    loop.targets.target_current = (x_tile, y_tile)
                    loop.add_target((x_tile, y_tile))
                    loop.screen_focus = (x_tile, y_tile)
                    loop.update_screen = True
            else:
                self.key_targeting_screen("return", self)
