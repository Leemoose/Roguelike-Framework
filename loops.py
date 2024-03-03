import pygame
import display as D
import mapping as M
import character as C
import objects as O
import targets as T
import shadowcasting
import pickle

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
    All unique entities (monsters and items) are tagged with an ID and put into dictionary.
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
        return self.subjects.pop(key)

    def add_subject(self, subject):
        self.subjects[subject.id_tag] = subject

class Memory():
    """
    Used to save the game
    """
    def __init__(self):
        self.explored_levels = 0
        self.floor_level = 0
        self.generators = {}
        self.player = None

    def save_objects(self):
        save = [self.explored_levels, self.floor_level, self.generators, self.player]
        try:
            with open("data.pickle", "wb") as f:
                pickle.dump(save, f)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

    def load_objects(self):
        with open('data.pickle', 'rb') as f:
            # Call load method to deserialze
            save = pickle.load(f)
        self.explored_levels = save [0]
        self.floor_level = save [1]
        self.generators = save[2]
        self.player = save[3]


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
        self.examine = False

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
        self.messages = []
        self.targets = T.Target()
    def action_loop(self, keyboard, display):
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
                    keyboard.key_action(self.player, self.generator.tile_map, self.monster_dict, self.monster_map, self.item_dict,self, key, self.generator, self.memory)
                elif self.inventory == True:
                    keyboard.key_inventory(self, self.player, self.item_dict,key)
                elif self.main == True:
                    if keyboard.key_main_screen(key, self) == False:
                        return False
                elif self.race == True:
                    keyboard.key_race_screen(key, self)
                elif self.classes == True:
                    keyboard.key_class_screen(key, self)
                elif self.items == True:
                    keyboard.key_item_screen(key, self, self.item_dict, self.player, self.item_for_item_screen, self.generator.item_map)
                elif self.examine == True:
                    keyboard.key_targeting_screen(key, self)
                self.update_screen = True

            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if self.main == True:
                    for button in self.main_buttons.buttons:
                        if self.main_buttons.buttons[button].clicked(x, y):
                            key = self.main_buttons.buttons[button].action
                            if keyboard.key_main_screen(key, self) == False:
                                return False
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
            
            # do status effect stuff
            self.player.character.apply_all_status_effects()
            status_messages = ["Player " + mes for mes in self.player.character.status_messages()]
            for message in status_messages:
                self.add_message(message)

        if not self.player.character.is_alive():
            self.clear_data()
            self.init_game(display)

        return True

    def monster_loop(self, energy):
        for monster_key in self.monster_dict.subjects:
            monster = self.monster_dict.subjects[monster_key]
            
            # do status effect stuff
            monster.character.apply_all_status_effects()
            status_messages = [monster.name + " " + mes for mes in monster.character.status_messages()]
            for message in status_messages:
                self.add_message(message)

            # do action stuff
            if self.generator.tile_map.track_map[monster.x][monster.y].seen:
                monster.brain.is_awake = True
            if monster.brain.is_awake == True:
                monster.character.energy += energy
                monster.brain.rank_actions(monster, self.monster_map, self.generator.tile_map, self.generator.flood_map, self.player, self.generator, self.item_dict, self)
    def change_screen(self, keyboard, display, colors, tileDict):
        if self.action == True:
            self.clean_up()
            shadowcasting.compute_fov(self.player.get_location(), self.generator.tile_map.track_map)
            display.update_display(colors, self.generator.tile_map, tileDict, self.monster_dict, self.item_dict, self.monster_map, self.player, self.messages)
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
        elif self.examine == True:
            display.update_display(colors, self.generator.tile_map, tileDict, self.monster_dict, self.item_dict,
                                   self.monster_map, self.player, self.messages)
            display.update_examine(self.targets.target_list, tileDict, self.messages)
        pygame.display.update()
        self.update_screen = False

    def clean_up(self):
        destroyed_items = []
        for key in (self.item_dict.subjects):
            item = self.item_dict.get_subject(key)
            if item.destroy:
                destroyed_items.append(key)
        for key in destroyed_items:
            item = self.item_dict.remove_subject(key)
            self.generator.item_map.clear_location(item.x, item.y)
    """
        dead_monsters = []
        for key in (self.monster_dict.subjects):
            monster = self.monster_dict.get_subject(key)
            if not monster.character.is_alive():
                dead_monsters.append(key)
        for key in dead_monsters:
            monster = self.monster_dict.remove_subject(key)
            self.generator.monster_map.clear_location(monster.x, monster.y)
            """

    def down_floor(self):
        playerx, playery = self.player.get_location()
        if self.floor_level == 0 or (isinstance(self.generator.tile_map.track_map[playerx][playery], O.Stairs) and self.generator.tile_map.track_map[playerx][playery].downward):
            self.floor_level += 1
            if self.floor_level > self.memory.explored_levels:
                generator = M.DungeonGenerator(self.floor_level)
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
                self.generator = generator
                self.memory.generators[self.floor_level] = generator

            else:
                self.player.x, self.player.y = (self.generator.tile_map.track_map[playerx][playery]).pair.get_location()
                self.generator = self.memory.generators[self.floor_level]
                self.monster_map = self.generator.monster_map
                self.item_dict = self.generator.item_dict
                self.monster_dict = self.generator.monster_dict

            self.memory.floor_level += 1


    def up_floor(self):
        playerx, playery = self.player.get_location()
        tile = self.generator.tile_map.track_map[playerx][playery]
        if self.floor_level != 1 and isinstance(tile, O.Stairs) and not tile.downward:
            self.floor_level -= 1
            self.memory.floor_level -= 1
            self.player.x, self.player.y = (self.generator.tile_map.track_map[playerx][playery]).pair.get_location()
            self.generator = self.memory.generators[self.floor_level]
            self.monster_map = self.generator.monster_map
            self.item_dict = self.generator.item_dict
            self.monster_dict = self.generator.monster_dict

    def init_game(self, display):
        self.main_buttons = D.create_main_screen(display)
        self.race_buttons = D.create_race_screen(display)
        self.class_buttons = D.create_class_screen(display)
        self.player = C.Player(0,0)
        self.memory.player = self.player

    def add_message(self, message):
        if len(self.messages) >= 5:
            self.messages.pop(0)
        self.messages.append(message)

    def load_game(self):
        self.action = True
        self.inventory = False
        self.race = False
        self.update_screen = False
        self.main = True
        self.classes = False
        self.targeting = False

#        self.items = False
#        self.item_for_item_screen = None
        self.floor_level = self.memory.floor_level

        self.generator = self.memory.generators[self.floor_level]
        self.tile_map = self.generator.tile_map
        self.monster_map = self.generator.monster_map
        self.item_dict = self.generator.item_dict
        self.monster_dict = self.generator.monster_dict
        self.player = self.memory.player

    def clear_data(self):
        self.action = False
        self.update_screen = True
        self.main = True

        self.items = False
        self.item_for_item_screen = None
        self.floor_level = 0
        self.memory = Memory()
        self.tile_map = None
        self.monster_map = None
        self.item_dict = None
        self.monster_dict = None
        self.generator = None
        self.messages = []



