import pygame, pygame_gui
import display as D
import mapping as M
import character as C
import objects as O
import targets as T
import shadowcasting
from enum import Enum
import dill

"""
Theme: Loops is the central brain of which part of the program it is choosing.
Classes: 
    ColorDict --> Maps english to RGB colors
    ID --> Tags each unique entity (item, monster,etc) with an ID and puts subject in dict
    Memory --> Dictionary of everything important for saving
    Loops --> After input, controls what the game should do
"""

class LoopType(Enum):
    none = -1
    action = 0
    autoexplore = 1
    inventory = 2
    equipment = 3
    main = 4
    race = 5
    classes = 6
    items = 7
    examine = 8
    rest = 9
    paused = 10
    targeting = 11
    specific_examine = 12
    enchant = 13

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
            with open("data.dill", "wb") as f:
                dill.dump(save, f)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

    def load_objects(self):
        with open('data.dill', 'rb') as f:
            # Call load method to deserialze
            save = dill.load(f)
        self.explored_levels = save [0]
        self.floor_level = save [1]
        self.generators = save[2]
        self.player = save[3]


class Loops():
    """
    This is the brains of the game and after accepting an input from keyboard, will decide what needs to be done
    """
    def __init__(self, width, height, textSize, tileDict):
        self.update_screen = True
        self.limit_inventory = None

        self.currentLoop = LoopType.none

        self.width = width
        self.height = height
        self.textSize = textSize
        self.items = False
        self.screen_focus = None
        self.floor_level = 0
        self.memory = Memory()
        self.tile_map = None
        self.monster_map = None
        self.item_dict = None
        self.monster_dict = None
        self.generator = None #Dungeon Generator
        self.messages = []
        self.targets = T.Target()
        self.target_to_display = None
        self.tileDict = tileDict
        self.screen_focus = None

        #Start the game by going to the main screen
        self.change_loop(LoopType.main)

    #Sets the internal loop type, and does the initialization that it needs.
    #Mostly here to cache UI pieces, which shouldn't be remade every frame.
    def change_loop(self, newLoop):
        self.currentLoop = newLoop
        self.update_screen = True
        
        if newLoop == LoopType.action:
            self.display.create_action_display(self)
        elif newLoop == LoopType.autoexplore:
            pass
        elif newLoop == LoopType.inventory or newLoop == LoopType.enchant:
            self.display.create_inventory(self.player, self.limit_inventory)
        elif newLoop == LoopType.equipment:
            self.display.create_equipment(self.player, self.tileDict)
        elif newLoop == LoopType.main:
            pass
        elif newLoop == LoopType.race:
            pass
        elif newLoop == LoopType.classes:
            pass
        elif newLoop == LoopType.items:
            self.display.create_entity()
        elif newLoop == LoopType.examine:
            pass
        elif newLoop == LoopType.paused:
            self.display.create_pause_screen()
        elif newLoop == LoopType.specific_examine:
            pass

    def action_loop(self, keyboard, display):
        """
        This is responsible for undergoing any inputs when screen is clicked
        :param keyboard:
        :return: None (will do a keyboard action)
        """

        action = None
        if self.currentLoop == LoopType.autoexplore:
            all_seen, _ = self.generator.all_seen()
            if all_seen:
                self.change_loop(LoopType.action)
                self.add_message("You have explored the entire floor")
            else:
                self.player.autoexplore(self)
                self.monster_loop(0)
        
        if self.currentLoop == LoopType.rest:
            monster_present = False
            for monster_key in self.monster_dict.subjects:
                monster_loc = self.monster_dict.get_subject(monster_key).get_location()
                if self.generator.tile_map.track_map[monster_loc[0]][monster_loc[1]].visible:
                    self.add_message("You can't rest while enemies are near")
                    self.change_loop(LoopType.action)
                    monster_present = True
            if not monster_present:
                self.player.character.rest()
                self.change_loop(LoopType.action)
                self.add_message("You rest for a while")
                self.monster_loop(0)

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
                if self.currentLoop == LoopType.action:
                    keyboard.key_action(self.player, self.generator.tile_map, self.monster_dict, self.monster_map, self.item_dict,self, key, self.generator, display, self.memory)
                elif self.currentLoop == LoopType.inventory:
                    keyboard.key_inventory(self, self.player, self.item_dict,key)
                elif self.currentLoop == LoopType.enchant:
                    keyboard.key_enchant(self, self.player, self.item_dict, key)
                elif self.currentLoop == LoopType.equipment:
                    keyboard.key_equipment(self, self.player, self.item_dict, key)
                elif self.currentLoop == LoopType.main:
                    if keyboard.key_main_screen(key, self) == False:
                        return False
                elif self.currentLoop == LoopType.race:
                    keyboard.key_race_screen(key, self)
                elif self.currentLoop == LoopType.classes:
                    keyboard.key_class_screen(key, self)
                elif self.currentLoop == LoopType.items:
                    keyboard.key_item_screen(key, self, self.item_dict, self.player, self.screen_focus, self.generator.item_map)
                elif self.currentLoop == LoopType.examine:
                    keyboard.key_examine_screen(key, self)
                elif self.currentLoop == LoopType.targeting:
                    keyboard.key_targeting_screen(key, self)
                elif self.currentLoop == LoopType.autoexplore:
                    keyboard.key_autoexplore(key, self)
                elif self.currentLoop == LoopType.paused:
                    if (keyboard.key_paused(key, self, display) == False):
                        return False
                elif self.currentLoop == LoopType.specific_examine:
                    keyboard.key_specific_examine(key, self, display)

                self.update_screen = True

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if (self.currentLoop == LoopType.main):
                    return keyboard.key_main_screen(event.ui_element.action, self)
                elif (self.currentLoop == LoopType.inventory):
                    key = event.ui_element.action
                    keyboard.key_inventory(self, self.player, self.item_dict, key)
                elif (self.currentLoop == LoopType.equipment):
                    key = event.ui_element.action
                    keyboard.key_equipment(self, self.player, self.item_dict, key)
                elif (self.currentLoop == LoopType.items):
                    key = event.ui_element.action
                    keyboard.key_item_screen(self, self.player, self.item_dict, key)
                elif (self.currentLoop == LoopType.paused):
                    key = event.ui_element.action
                    if (keyboard.key_paused(key, self, display) == False):
                        return False
                elif (self.currentLoop == LoopType.action):
                    key = event.ui_element.action
                    keyboard.key_action(self.player, self.tile_map, self.generator.monster_dict, self.monster_map, self.generator.item_dict, self, key, self.generator, display, self.memory)

            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                self.update_screen = True

            elif event.type == pygame.VIDEORESIZE:
                self.display.update_sizes()
                self.update_screen = True
                self.change_loop(self.currentLoop)

            display.uiManager.process_events(event)

        if self.currentLoop == LoopType.action and self.player.character.energy < 0:
            self.generator.flood_map.update_flood_map(self.player)
            self.monster_loop(-self.player.character.energy)
            self.player.character.energy = 0
            
            # do status effect stuff
            self.player.character.tick_all_status_effects()
            status_messages = ["Player " + mes for mes in self.player.character.status_messages()]
            for message in status_messages:
                self.add_message(message)
            
            self.player.character.tick_cooldowns()

            self.player.character.tick_regen()

        if not self.player.character.is_alive() and not self.player.invincible:
            self.clear_data()
            self.init_game(display)

        #After everything, update the display clock
        display.update_ui()

        return True

    def monster_loop(self, energy):
        for monster_key in self.monster_dict.subjects:
            monster = self.monster_dict.subjects[monster_key]
            
            # do status effect stuff
            monster.character.tick_all_status_effects()
            status_messages = [monster.name + " " + mes for mes in monster.character.status_messages()]
            for message in status_messages:
                self.add_message(message)
            
            # tick skill cooldowns
            monster.character.tick_cooldowns()

            # tick regen
            monster.character.tick_regen()

            if self.generator.tile_map.track_map[monster.x][monster.y].seen:
                monster.brain.is_awake = True

            # do action stuff
            if monster.brain.is_awake == True:
                monster.character.energy += energy
                while monster.character.energy > 0:
                    monster.brain.rank_actions(monster, self.monster_map, self.generator.tile_map, self.generator.flood_map, self.player, self.generator, self.item_dict, self)

    def render_screen(self, keyboard, display, colors, tileDict):
        if self.currentLoop == LoopType.action or self.currentLoop == LoopType.autoexplore:
            self.clean_up()
            shadowcasting.compute_fov(self.player.get_location(), self.generator.tile_map.track_map)
            display.update_action_display(self)
        elif self.currentLoop == LoopType.inventory or self.currentLoop == LoopType.enchant:
            display.update_inventory(self.player, self.limit_inventory)
        elif self.currentLoop == LoopType.equipment:
            display.update_equipment(self.player, tileDict)
        elif self.currentLoop == LoopType.main:
            display.update_main()
        elif self.currentLoop == LoopType.items:
            display.update_entity(self.screen_focus, tileDict)
        elif self.currentLoop == LoopType.examine or self.currentLoop == LoopType.targeting:
            display.update_display(colors, self.generator.tile_map, tileDict, self.monster_dict, self.item_dict,
                                   self.monster_map, self.player, self.messages, self.target_to_display)
            display.update_examine(self.targets.target_list, tileDict, self.messages)
        elif self.currentLoop == LoopType.paused:
            display.update_pause_screen()
        elif self.currentLoop == LoopType.specific_examine:
            display.update_entity(self.screen_focus, tileDict, item_screen=False)
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

        dead_monsters = []
        for key in self.monster_dict.subjects:
            monster = self.monster_dict.get_subject(key)
            if not monster.character.is_alive():
                if monster.get_location() == self.target_to_display: # on kill stop observing a space
                    self.target_to_display = None
                dead_monsters.append(key)
                for item in monster.character.inventory:
                    if item.equipped:
                        monster.character.unequip(item)
                    monster.character.drop(item, self.item_dict, self.generator.item_map)
                self.monster_map.clear_location(monster.x, monster.y)
        for key in dead_monsters:
            self.monster_dict.subjects.pop(key)

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
        self.main_buttons = D.create_main_screen(display, self.width, self.height)
        self.player = C.Player(0, 0)
        self.memory.player = self.player
        self.display = display
        """
        self.race_buttons = D.create_race_screen(display)
        self.class_buttons = D.create_class_screen(display)
        """

    def add_message(self, message):
        if len(self.messages) >= 4:
            self.messages.pop(0)
        self.messages.append(message)

    def add_target(self, target):
        self.target_to_display = target
    
    def void_target(self):
        if self.target_to_display == None:
            return
        if self.monster_map.get_passable(self.target_to_display[0], self.target_to_display[1]): # don't void if its a monster, cuz its a good QOL to keep monster health on screen
            self.target_to_display = None

    def init_new_game(self):
        self.display.create_game_ui(self.player)

    def load_game(self):
        self.change_loop(LoopType.action)
        self.update_screen = False

#        self.items = False
#        self.screen_focus = None
        self.floor_level = self.memory.floor_level

        self.generator = self.memory.generators[self.floor_level]
        self.tile_map = self.generator.tile_map
        self.monster_map = self.generator.monster_map
        self.item_dict = self.generator.item_dict
        self.monster_dict = self.generator.monster_dict
        self.player = self.memory.player
        self.player.character.energy = 0

    def clear_data(self):
        self.change_loop(LoopType.main)
        self.update_screen = True

        self.screen_focus = None
        self.floor_level = 0
        self.memory = Memory()
        self.tile_map = None
        self.monster_map = None
        self.item_dict = None
        self.monster_dict = None
        self.generator = None
        self.messages = []



