import pygame
import display as D
import mapping as M
import character as C
import items as I
import objects as O
import monster as Mon
import objects as O
import shadowcasting

import random

"""
Theme: Loops is the central brain of which part of the program it is choosing.
Classes: 
    ColorDict --> Maps english to RGB colors
    ID --> Tags each unique entity (item, monster,etc) with an ID and puts subject in dict
    Memory --> Dictionary of everything important for saving
    Loops --> After input, controls what the game should do
"""

class ColorDict():
    """
    Just a dictionary of colors that I decide to use
    Can get RGB by inputting English into getColor
    """
    def __init__(self):
        colors = {}
        colors["white"] = (255,255,255)
        colors["green"] = (0,255,0)
        colors["blue"] = (0,0,128)
        colors["black"] = (0,0,0)
        self.colors = colors

    def getColor(self, color):
        return self.colors[color]

class ID():
    """
    All unique entities are tagged with an ID and put into dictionary.
    IDs are generally used in arrays and other places and then the ID can be used to get actual object
    """
    def __init__(self):
        self.subjects = {}
        self.ID_count = 0

    def tag_subject(self, subject):
        self.ID_count += 1
        subject.gain_ID(self.ID_count)
        self.add_subject(subject)

    def get_subject(self, key):
        return self.subjects[key]

    def remove_subject(self, key):
        self.subjects.pop(key)

    def add_subject(self, subject):
        self.subjects[subject.id_tag] = subject

class Memory():
    """
    Used to save the game
    """
    def __init__(self):
        self.generated_maps = {}
        self.item_dicts = {}
        self.monster_dicts = {}
        self.explored_levels = 0

class Loops():
    """
    This is the brains of the game and after accepting an input from keyboard, will decide what needs to be done
    """
    def __init__(self, width, height, textSize):
        self.action = False
        self.inventory = False
        self.race = False
        self.update_screen = True
        self.main = True
        self.classes = False
        self.width = width
        self.height = height
        self.textSize = textSize
        self.items = False
        self.item_for_item_screen = None
        self.floor_level = 0
        self.memory = Memory()
        self.tile_map = None
        self.monster_map = None
        self.item_dict = None
        self.monster_dict = None
        self.generator = None #Dungeon Generator
        self.monster_ai =  Mon.Monster_AI() #I just realize there is a bug here and it actually creates a... wait... what's that noise... hello?... Nooo!!! Bluglaaaaaaaaaa     

    def action_loop(self, keyboard):
        """
        This is responsible for undergoing any inputs when screen is clicked
        :param keyboard:
        :return: None (will do a keyboard action)
        """
        action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                try:
                    if event.mod & pygame.KMOD_SHIFT:
                        key = keyboard.key_string(event.key, True)
                    else:
                        key = keyboard.key_string(event.key, False)
                except:
                    break
                if self.action == True:
                    keyboard.key_action(self.player, self.generator.tile_map, self.monster_dict, self.monster_map, self.item_dict,self, key, self.generator)
                elif self.inventory == True:
                    keyboard.key_inventory(self, self.player, self.item_dict,key)
                elif self.main == True:
                    keyboard.key_main_screen(key, self)
                elif self.race == True:
                    keyboard.key_race_screen(key, self)
                elif self.classes == True:
                    keyboard.key_class_screen(key, self)
                elif self.items == True:
                    keyboard.key_item_screen(key, self, self.item_dict, self.player, self.item_for_item_screen, self.generator.item_map)
                self.update_screen = True

            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if self.main == True:
                    for button in self.main_buttons.buttons:
                        if self.main_buttons.buttons[button].clicked(x, y):
                            key = self.main_buttons.buttons[button].action
                            keyboard.key_main_screen(key, self)
                            break

                elif self.race == True:
                    for button in self.race_buttons.buttons:
                        if self.race_buttons.buttons[button].clicked(x, y):
                            key = self.race_buttons.buttons[button].action
                            keyboard.key_race_screen(key, self)
                            break

                elif self.classes == True:
                    for button in self.class_buttons.buttons:
                        if self.class_buttons.buttons[button].clicked(x, y):
                            key = self.class_buttons.buttons[button].action
                            keyboard.key_class_screen(key, self)
                            break
                self.update_screen = True

        if self.action == True and self.player.character.energy < 0:
            self.generator.flood_map.update_flood_map(self.player)
            self.monster_loop(-self.player.character.energy)
            self.player.character.energy = 0

        if not self.player.character.is_alive():
            return False

        return True

    def monster_loop(self, energy):
        for monster_key in self.monster_dict.subjects:
            monster = self.monster_dict.subjects[monster_key]
            if self.generator.tile_map.track_map[monster.x][monster.y].seen:
                monster.brain.is_awake = True
            if monster.brain.is_awake == True:
                monster.character.energy += energy
                monster.brain.rank_actions(monster, self.monster_map, self.generator.tile_map, self.generator.flood_map, self.player, self.generator, self.item_dict)
    def change_screen(self, keyboard, display, colors, tileDict):
        if self.action == True:
            shadowcasting.compute_fov(self.player.get_location(), self.generator.tile_map.track_map)
            display.update_display(colors, self.generator.tile_map, tileDict, self.monster_dict, self.item_dict, self.monster_map, self.player)
        elif self.inventory == True:
            display.update_inventory(self.player)
        elif self.main == True:
            display.update_main()
        elif self.race == True:
            display.update_race()
        elif self.classes == True:
            display.update_class()
        elif self.items == True:
            display.update_item(self.item_for_item_screen, tileDict)
        pygame.display.update()
        self.update_screen = False

    def down_floor(self):
        playerx, playery = self.player.get_location()
        if self.floor_level == 0 or (isinstance(self.generator.tile_map.track_map[playerx][playery], O.Stairs) and self.generator.tile_map.track_map[playerx][playery].downward):
            self.floor_level += 1
            if self.floor_level > self.memory.explored_levels:
                wid = 20
                hei = 20
                generator = M.DungeonGenerator(wid, hei)
                generated_map = generator.get_map()
                self.monster_map = generator.monster_map
                self.item_dict = generator.item_dict
                self.monster_dict = generator.monster_dict
                temp_stair = None
                for stairs in (generator.tile_map.get_stairs()):
                    if not stairs.downward:
                        temp_stair = stairs
                        if self.floor_level != 1:
                            old_stairs = self.generator.tile_map.track_map[playerx][playery]
                            old_stairs.pair = stairs
                            stairs.pair = old_stairs
                        break
                self.player.x = temp_stair.x
                self.player.y = temp_stair.y
                self.memory.explored_levels += 1
                self.memory.generated_maps[self.floor_level] = generator
                self.memory.item_dicts[self.floor_level] = self.item_dict
                self.memory.monster_dicts[self.floor_level] = self.monster_dict
                self.generator = generator

            else:
                self.player.x, self.player.y = (self.generator.tile_map.track_map[playerx][playery]).pair.get_location()
                self.generator = self.memory.generated_maps[self.floor_level]
                self.monster_map = self.memory.generated_maps[self.floor_level].monster_map
                self.item_dict = self.memory.item_dicts[self.floor_level]
                self.monster_dict = self.memory.monster_dicts[self.floor_level]


    def up_floor(self):
        playerx, playery = self.player.get_location()
        tile = self.generator.tile_map.track_map[playerx][playery]
        if self.floor_level != 1 and isinstance(tile, O.Stairs) and not tile.downward:
            self.floor_level -= 1
            self.player.x, self.player.y = (self.generator.tile_map.track_map[playerx][playery]).pair.get_location()
            self.generator = self.memory.generated_maps[self.floor_level]
            self.monster_map = self.memory.generated_maps[self.floor_level].monster_map
            self.item_dict = self.memory.item_dicts[self.floor_level]
            self.monster_dict = self.memory.monster_dicts[self.floor_level]

    def init_game(self, display):
        self.main_buttons = D.create_main_screen(display)
        self.race_buttons = D.create_race_screen(display)
        self.class_buttons = D.create_class_screen(display)
        self.player = C.Player(0,0)

