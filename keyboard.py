import pygame

class Keyboard():
    """
    Keyboard translates any player input into either a change of gamestate or an action. Any complicated checks
    should be done in the action, not here.
    First the player input or key is translated to a keyboard input (this allows inputs to change if we want).
    Then, depending on which mode the game is in, it will do a series of if else statements to pick correct action.
    """
    def __init__(self):
        keys_to_string = {}
        keys_to_string[pygame.K_w] = "w"
        keys_to_string[pygame.K_a] = "a"
        keys_to_string[pygame.K_s] = "s"
        keys_to_string[pygame.K_d] = "d"
        keys_to_string[pygame.K_UP] = "up"
        keys_to_string[pygame.K_LEFT] = "left"
        keys_to_string[pygame.K_DOWN] = "down"
        keys_to_string[pygame.K_RIGHT] = "right"
        keys_to_string[pygame.K_i] = "i"
        keys_to_string[pygame.K_g] = "g"
        keys_to_string[pygame.K_u] = "u"
        keys_to_string[pygame.K_e] = "e"
        keys_to_string[pygame.K_f] = "f"
        keys_to_string[pygame.K_q] = "q"
        keys_to_string[pygame.K_o] = "o"
        keys_to_string[pygame.K_l] = "l"
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
        keys_to_string[146] = ">"
        keys_to_string[144] = "<"

        self.keys_to_string = keys_to_string

    def key_string(self, key, shift_pressed):
        if not shift_pressed:
            return self.keys_to_string[key]
        else:
            return self.keys_to_string[key + 100]

#Any actions done in the battle screen
    def key_action(self, player, floormap, monsterID, monster_map, item_ID, loop, key, generated_maps, memory):
        if key == "up":
            player.attack_move(0, -1, loop)
        elif key == "left":
            player.attack_move(-1, 0, loop)
        elif key == "down":
            player.attack_move(0, 1, loop)
        elif key == "right":
            player.attack_move(1, 0, loop)
        elif key == "g":
            for item_key in item_ID.subjects:
                item = item_ID.subjects[item_key]
                if item.x == player.x and item.y == player.y:
                    player.character.grab(item_key, item_ID, generated_maps, loop)
                    break
        elif key == "i":
            loop.action = False
            loop.inventory = True
            loop.update_screen = True
        elif key == ">":
            loop.down_floor()
        elif key == "<":
            loop.up_floor()
        elif key == ".":
            player.character.wait()
        elif key == 'f':
            loop.action = False
            loop.targeting = True
            loop.update_screen = True
            loop.targets.start_target(loop.player.get_location())
        elif key == "o":
            loop.add_message("You wish you could autoexplore.")
        elif key == "s":
            memory.save_objects()


    def key_inventory(self, loop, player, item_dict, key):
            if key == "esc":
                loop.inventory = False
                loop.action = True
                loop.update_screen = True

            for i in range(len(player.character.inventory)):
                if str(i + 1) == key:
                    loop.inventory = False
                    loop.items = True
                    loop.item_for_item_screen = player.character.inventory[i]

    def key_main_screen(self, key, loop):
        if key == "esc":
            return False
        elif key == "l":
            loop.memory.load_objects()
            loop.load_game()
        else:
            loop.main = False
            loop.race = True
            loop.update_screen = True

    def key_race_screen(self, key, loop):
        if key == "esc":
            loop.race = False
            loop.main = True
            loop.update_screen = True
        else:
            loop.race = False
            loop.classes = True
            loop.update_screen = True

    def key_class_screen(self, key, loop):
        if key == "esc":
            loop.classes = False
            loop.race = True
            loop.update_screen = True        
        else:
            loop.classes = False
            loop.action = True
            loop.update_screen = True
            loop.down_floor()

    def key_item_screen(self, key, loop, item_dict, player, item, item_map):
            if key == "esc":
                loop.items = False
                loop.inventory = True
                loop.update_screen = True
            elif key == "d":
                player.character.drop(item, item_dict, item_map)
                loop.items = False
                loop.inventory = True
                loop.update_screen = True
            elif key == "e":
                player.character.equip(item)
            elif key == "u":
                player.character.unequip(item)
            elif key == 'q':
                if player.character.quaff(item, item_dict, item_map):
                    loop.update_screen = True
                    loop.inventory = True
                    loop.items = False

#Not currently being used
    def key_targeting_screen(self, key, loop):
        loop.update_screen = True
        targets = loop.targets
        if key == "w":
            targets.adjust(0, -1)
        elif key == "a":
            targets.adjust(-1, 0)
        elif key == "s":
            targets.adjust(0, 1)
        elif key == "d":
            targets.adjust(1, 0)
        elif key == "esc":
            loop.targeting = False
            loop.action = True
            loop.update_screen = True
