import pygame

class Keyboard():
    def __init__(self):
        #Defining pygame keys to keyboard
        keys_to_string = {}
        keys_to_string[pygame.K_w] = "w"
        keys_to_string[pygame.K_a] = "a"
        keys_to_string[pygame.K_s] = "s"
        keys_to_string[pygame.K_d] = "d"
        keys_to_string[pygame.K_UP] = "w"
        keys_to_string[pygame.K_LEFT] = "a"
        keys_to_string[pygame.K_DOWN] = "s"
        keys_to_string[pygame.K_RIGHT] = "d"
        keys_to_string[pygame.K_i] = "i"
        keys_to_string[pygame.K_g] = "g"
        keys_to_string[pygame.K_u] = "u"
        keys_to_string[pygame.K_e] = "e"
        keys_to_string[pygame.K_ESCAPE] = "esc"
        keys_to_string[pygame.K_1] = "1"
        keys_to_string[pygame.K_2] = "2"
        keys_to_string[pygame.K_3] = "3"
        keys_to_string[pygame.K_4] = "4"
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
    def key_action(self, player, floormap, monsterID, monster_map, item_ID, loop, key, generated_maps):
        if key == "w":
            player.attack_move(0, -1, loop)
        elif key == "a":
            player.attack_move(-1, 0, loop)
        elif key == "s":
            player.attack_move(0, 1, loop)
        elif key == "d":
            player.attack_move(1, 0, loop)
        elif key == "g":
            for item_key in item_ID.subjects:
                item = item_ID.subjects[item_key]
                if item.x == player.x and item.y == player.y:
                    player.character.grab(item_key, item_ID, generated_maps)
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
        if key == "1":
            loop.main = False
            loop.race = True
            loop.update_screen = True

    def key_race_screen(self, key, loop):
        if key == "esc":
            loop.race = False
            loop.main = True
            loop.update_screen = True
        elif key == "1":
            loop.race = False
            loop.classes = True
            loop.update_screen = True

    def key_class_screen(self, key, loop):
        if key == "esc":
            loop.classes = False
            loop.race = True
            loop.update_screen = True        
        elif key == "1":
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
                player.character.drop(item, item_dict, player.x, player.y, item_map)
                loop.items = False
                loop.inventory = True
                loop.update_screen = True
            elif key == "e":
                player.character.equip(item)
            elif key == "u":
                player.character.unequip(item)