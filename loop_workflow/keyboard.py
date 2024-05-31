import pygame
from .key_screens import key_targeting_screen, key_action
from .bindings import Bindings

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
        keys_to_string[pygame.K_TAB] = "tab"

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
        self.key_bindings = Bindings()

    def key_string(self, key, shift_pressed):
        if not shift_pressed:
            try:
                print(key)
                if self.key_bindings.has_binding(self.keys_to_string[key]):
                    self.key_bindings.use_keybinding(self.keys_to_string[key])
                    print(self.key_bindings.key_queue)
                else:
                    return self.keys_to_string[key]
            except:
                return -1
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

    def action_mouse_to_keyboard(self, loop, x_tile, y_tile):
        player = loop.player
        if player.get_distance(x_tile, y_tile) == 0:
            if not loop.generator.item_map.get_passable(player.x, player.y):
               return key_action(loop, "g")
            elif loop.generator.tile_map.track_map[player.x][player.y].has_trait("stairs"):
                return key_action(loop, ">") #Needs to be able to work with upstairs as well
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
            key_action(loop, options[(xdiff, ydiff)])

    def targetting_mouse_to_keyboard(self, loop, x_tile, y_tile):
        if loop.generator.tile_map.in_map(x_tile, y_tile):
            if x_tile != loop.targets.target_current[0] or y_tile != loop.targets.target_current[1]:
                if loop.generator.tile_map.get_passable(x_tile, y_tile):
                    loop.targets.target_current = (x_tile, y_tile)
                    loop.add_target((x_tile, y_tile))
                    loop.screen_focus = (x_tile, y_tile)
                    loop.update_screen = True
            else:
                key_targeting_screen("return", self)

