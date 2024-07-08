
from loop_workflow import *
import items
from dungeon_generation import mapping as M
import player
import targets as T
import tiles as TI
from navigation_utility import shadowcasting
from character_implementation.classes import Rogue, Warrior, Mage
from stars import GreenBuck

from display_generation import *

"""
Theme: Loops is the central brain of which part of the program it is choosing.
Classes: 
    ColorDict --> Maps english to RGB colors
    ID --> Tags each unique entity (item, monster,etc) with an ID and puts subject in dict
    Memory --> Dictionary of everything important for saving
    Loops --> After input, controls what the game should do
"""


class Loops():
    """
    This is the brains of the game and after accepting an input from keyboard, will decide what needs to be done
    """

    def __init__(self, width, height, textSize, tileDict, display, keyboard, ascaii_data, dungeon_data):
        self.display = display
        self.update_screen = True
        self.currentLoop = LoopType.none

        self.width = width
        self.height = height
        self.textSize = textSize
        self.items = False
        self.screen_focus = None
        self.floor_level = 0
        self.branch = ""
        self.memory = Memory()
        self.tile_map = None
        self.tileDict = tileDict
        self.ascii_data = ascaii_data
        self.dungeon_data = dungeon_data
        self.keyboard = keyboard

        self.generator = None  # Dungeon Generator
        self.messages = []
        self.dirty_messages = True  # ;)
        self.targets = T.Target()
        self.target_to_display = None

        self.screen_focus = None
        self.current_stat = 0  # index of stat for levelling up
        self.timer = 0
        self.total_time = 0
        self.day = "Daytime"
        self.taking_stairs = False
        self.npc_focus = None
        self.class_selection = None
        self.quest_recieved = False
        self.quest_completed = False
        self.stars = [GreenBuck()]

        # variables for npc interaction
        self.next_dialogue = False # if true, give next dialogue box
        self.dialogue_options = 0 # number of dialogue options currently presented to player
        self.player_choice = -1 # if > 0, represents the dialogue option chosen by the player

        # variables for pathing
        self.rest_count = 0 # how many turns have you been resting for
        self.after_rest = LoopType.action # what loop type to revert to after finishing resting, default action
        self.pathing_count = 0 # how many turns have you been exploring for
        dummy_function = (lambda x: False)
        self.after_pathing = dummy_function

        self.create_display_options = {LoopType.action: create_display,
                                       LoopType.targeting: create_display,
                                       LoopType.examine: create_display,
                                       LoopType.inventory: create_inventory,
                                       LoopType.enchant: create_inventory,
                                       LoopType.level_up: create_level_up,
                                       LoopType.victory: create_victory_screen,
                                       LoopType.equipment: create_equipment,
                                       LoopType.main: create_main_screen,
                                       LoopType.paused: create_pause_screen,
                                       LoopType.help: create_help_screen,
                                       LoopType.story: create_story_screen,
                                       LoopType.death: create_death_screen,
                                       LoopType.trade: create_trade_screen,
                                       LoopType.quest: create_quest_screen,
                                       LoopType.spell: create_spellcasting,
                                       LoopType.binding: create_binding_screen,
                                       LoopType.classes: create_class_screen,
                                       LoopType.spell_individual: create_spell_window,
                                       LoopType.quickcast: create_quickcast_select
                                       }
        self.update_display_options = {
                                       LoopType.victory: self.display.update_screen,
                                       LoopType.death: self.display.update_screen,
                                       LoopType.help: self.display.update_screen,
                                       LoopType.story: self.display.update_screen,
                                       LoopType.trade: self.display.update_screen_without_fill,
                                       LoopType.level_up: update_level_up,
                                       LoopType.equipment: self.display.update_screen,
                                       LoopType.main: self.display.update_main,
                                       LoopType.quest: self.display.update_screen_without_fill,
                                       LoopType.paused: self.display.update_screen_without_fill,
                                       LoopType.inventory: self.display.update_screen,
                                       LoopType.enchant: self.display.update_screen,
                                       LoopType.spell: self.display.update_screen,
                                       LoopType.binding: self.display.update_screen,
                                       LoopType.classes: self.display.update_screen,
                                       LoopType.spell_individual: update_spell_window,
                                       LoopType.quickcast: update_quickcast_select
                                       }
        self.action_options =          {LoopType.action: key_action,
                                       LoopType.inventory: key_inventory,
                                       LoopType.level_up: key_level_up,
                                       LoopType.victory: key_victory,
                                       LoopType.enchant: key_enchant,
                                       LoopType.equipment: key_equipment,
                                       LoopType.items: key_item_screen,#Need to do self.change_loop if change was made (put in keyboard)
                                       LoopType.examine: key_examine_screen,
                                       LoopType.targeting: key_targeting_screen,
                                       LoopType.specific_examine: key_specific_examine,
                                       LoopType.help: key_help,
                                       LoopType.story: key_help,
                                       LoopType.death: key_death,
                                       LoopType.main: key_main_screen,
                                       LoopType.paused: key_paused,
                                       LoopType.trade: key_trade,
                                       LoopType.quest: key_quest,
                                       LoopType.resting: key_rest,
                                       LoopType.pathing: key_explore,
                                       LoopType.spell: key_spell,
                                       LoopType.binding: key_binding,
                                       LoopType.classes: key_classes,
                                       LoopType.spell_individual: key_spell_individual,
                                       LoopType.quickcast: key_quickselect
                                       }

        # Start the game by going to the main screen

    # Sets the internal loop type, and does the initialization that it needs.
    # Mostly here to cache UI pieces, which shouldn't be remade every frame.
    def change_loop(self, newLoop):
        loop_type_mapping = {"victory": LoopType.victory,
                             "action": LoopType.action,
                             "trade": LoopType.trade,
                             "inventory":LoopType.inventory,
                             "enchant": LoopType.enchant}
        if newLoop in loop_type_mapping:
            newLoop = loop_type_mapping[newLoop]
        # self.clear_message()
        self.currentLoop = newLoop
        self.update_screen = True
        if newLoop in self.create_display_options:
            self.create_display_options[newLoop](self.display, self)
        elif newLoop == LoopType.items:
            self.display.update_entity(self, item_screen=True, create=True)

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
            elif event.type == pygame.KEYDOWN or (event.type == pygame_gui.UI_BUTTON_PRESSED and hasattr(event.ui_element, "action")):
                key = None
                if event.type == pygame.KEYDOWN:
                    if event.mod == pygame.KMOD_NONE:
                        key = keyboard.key_string(event.key, False)
                    elif event.mod & pygame.KMOD_SHIFT and event.key:
                        key = keyboard.key_string(event.key, True)
                    while keyboard.key_bindings.has_queue():
                        key = keyboard.key_bindings.next_key()
                        if self.currentLoop in self.action_options:
                            if key != None and self.action_options[self.currentLoop](self, key) == False:
                                return False

                else:
                    if hasattr(event.ui_element, "row"):
                        if event.ui_element.row != None:
                            self.current_stat = event.ui_element.row
                    key = event.ui_element.action

                if self.currentLoop in self.action_options:
                  #  print(key)
                    if key != None and self.action_options[self.currentLoop](self,key) == False:
                        return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x_tile, y_tile = display.screen_to_tile(self.player, x, y)
                if (self.currentLoop == LoopType.action):
                    keyboard.action_mouse_to_keyboard(self, x_tile, y_tile)
                elif (self.currentLoop == LoopType.targeting):
                    keyboard.targetting_mouse_to_keyboard(self,x_tile,y_tile)

            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                self.update_screen = True

            elif event.type == pygame.VIDEORESIZE:
                self.display.update_sizes()
                self.update_screen = True
                self.change_loop(self.currentLoop)

            self.update_screen = True

            display.uiManager.process_events(event)

        if self.currentLoop == LoopType.action:
            if self.rest_count != 0:
                # print(f"Rested for {self.rest_count} turns.")
                self.rest_count = 0

            if self.pathing_count != 0:
                # print(f"Explored for {self.pathing_count} turns.")
                self.pathing_count = 0

                # default after pathing behaviour
                dummy_function = (lambda loop: loop.change_loop(LoopType.action))
                self.after_pathing = dummy_function

                # clear path if we go back to action
                self.player.path = []
            
            # if self.stairs_count != 0:
            #     # print(f"Pathed to stairs for {self.stairs_count} turns")
            #     self.stairs_count = 0

        # check autoexplore and rest
        if self.currentLoop == LoopType.resting:
            self.player.character.rest(self, self.after_rest)
            self.rest_count += 1
        if self.currentLoop == LoopType.pathing:
            self.player.autopath(self)
            self.pathing_count += 1
            self.time_passes(100)
            # uncomment this to closely follow pathing
            # import time
            # time.sleep(0.2)
        # if self.currentLoop == LoopType.stairs:
        #     self.player.find_stairs(self)
        #     self.stairs_count += 1
            # uncomment this to closely follow pathing
            # import time
            # time.sleep(0.2)


        if self.player.character.energy < 0:
            self.time_passes(-self.player.character.energy)
            self.monster_loop(-self.player.character.energy)
            self.player.character.energy = 0

        if not self.player.character.is_alive() and not self.player.character.invincible and not self.player.invincible:
            if (self.currentLoop != LoopType.death):
                self.change_loop(LoopType.death)

        # After everything, update the display clock
        display.update_ui()
        return True

    def get_daytime(self):
        return self.day
    def monster_loop(self, energy, stairs = None):
        
        for monster in self.generator.monster_map.all_entities():
            if monster.character.alive:
                # do status effect stuff
                if self.generator.tile_map.track_map[monster.x][monster.y].seen:
                    monster.brain.is_awake = True

                # do action stuff
                if monster.brain.is_awake and not monster.asleep:
                    monster.character.energy += energy
                    while monster.character.energy > 0:
                        monster.brain.rank_actions(self)

        if len(self.generator.summoner) > 0:
            for generation in self.generator.summoner:
                placement = self.generator.nearest_empty_tile((generation[1], generation[2]))
                if placement != None:
                    self.generator.place_monster_at_location(generation[0], placement[0], placement[1])
                else:
                    self.add_message("The summoning fizzled.")
            self.generator.summoner = []

    def render_screen(self, display):
        if self.currentLoop in self.update_display_options:
            self.update_display_options[self.currentLoop](self)
        else:
            if self.currentLoop == LoopType.action:
                self.clean_up()
                shadowcasting.compute_fov(self)
                display.update_display(self)
                mos_x, mos_y = pygame.mouse.get_pos()
                (x, y) = display.screen_to_tile(self.player, mos_x, mos_y)
                draw_screen_focus = True
                if self.generator.tile_map.in_map(x, y):
                    if self.generator.tile_map.track_map[x][y].visible and self.generator.tile_map.get_passable(x,
                                                                                                                y) and (
                            (not self.generator.monster_map.get_passable(x, y)) or (
                    not self.generator.item_map.get_passable(x, y))):
                        # print(self.generator.monster_map.get_passable(x,y), self.generator.item_map.get_passable(x,y))
                        display.draw_examine_window((x, y), self)
                        draw_screen_focus = False
                if draw_screen_focus:
                    if self.screen_focus != None:
                        clear_target = display.draw_examine_window(self.screen_focus, self)
                        if clear_target:
                            self.screen_focus = None
            elif self.currentLoop == LoopType.items:
                display.update_entity(self)
            elif (self.currentLoop == LoopType.resting or self.currentLoop == LoopType.pathing):
                self.clean_up()
                shadowcasting.compute_fov(self)
                if self.render_exploration:
                    display.update_display(self)
            elif self.currentLoop == LoopType.examine or self.currentLoop == LoopType.targeting:
                display.update_display(self)
                mos_x, mos_y = pygame.mouse.get_pos()
                (x, y) = display.screen_to_tile(self.player, mos_x, mos_y)
                self.draw_screen_focus = True
                if self.generator.tile_map.in_map(x, y):
                    if self.generator.tile_map.track_map[x][y].visible and self.generator.tile_map.get_passable(x, y) and (
                            (not self.generator.monster_map.get_passable(x, y)) or (
                    not self.generator.item_map.get_passable(x, y))):
                        display.draw_examine_window((x, y), self)
                        self.draw_screen_focus = False
                if self.draw_screen_focus:
                    if self.screen_focus != None:
                        clear_target = display.draw_examine_window(self.screen_focus, self)
                        if clear_target:
                            self.screen_focus = None
                display.update_examine(self.targets.target_current, self)

            elif self.currentLoop == LoopType.specific_examine:
                display.update_entity(self, item_screen=False, create=True)

        if self.player.quest_recieved == True:
            display.update_questpopup_screen(self, "{} Recieved".format(self.player.quests[-1].name))
            self.player.quest_recieved = False

        # if self.quest_completed == True:
        #     for quest in self.player.quests:
        #         if quest.active and quest.check_
        #     display.update_questpopup_screen(self, "{} Recieved".format(self.player.quests[-1].name))

    

        tile = self.generator.tile_map.locate(self.player.x, self.player.y)
        if isinstance(tile, TI.Door):
            tile.open()
        pygame.display.update()
        self.update_screen = False

    def clean_up(self):
        destroyed_items = []
        item_dict = self.generator.item_map.dict
        for item in self.generator.item_map.all_entities():
            if item.destroy:
                destroyed_items.append(item)
        for item in destroyed_items:
            self.generator.item_map.remove_thing(item)

        dead_monsters = []
        for monster in self.generator.monster_map.all_entities():
            if not monster.character.is_alive():
                if monster.get_location() == self.screen_focus:  # on kill stop observing a space
                    self.screen_focus = None
                items_copy = [item for item in monster.get_inventory()]
                for item in items_copy:
                    if item.yendorb:
                        monster.do_drop(item, self.generator.item_map)
                        break  # only drop yendorb if monster had it
                    if item.equipped:
                        monster.character.unequip(item)
                    monster.do_drop(item, self.generator.item_map)
                monster_corpse = monster.die()
                self.generator.monster_map.remove_thing(monster)
                if isinstance(monster_corpse, items.Corpse):
                    self.generator.item_map.place_thing(monster_corpse)
                if monster.gold_value > 0:
                    gold = items.Gold(monster.gold_value, x = monster.x, y = monster.y)
                    self.generator.item_map.place_thing(gold)


    def change_floor(self, downward):
        self.taking_stairs = True
        playerx, playery = self.player.get_location()
        if self.player.character.energy < 0:
            self.time_passes(-self.player.character.energy)
            self.monster_loop(-self.player.character.energy)
            self.player.character.energy = 0

        print("The stairs you are taking is {}".format(self.generator.tile_map.track_map[playerx][playery]))
        current_stairs = self.generator.tile_map.locate(playerx, playery)
        if isinstance(current_stairs, TI.Stairs):
            if downward and isinstance(current_stairs, TI.DownStairs):
                if current_stairs.pair is None:
                    if current_stairs.downward: #Don't know why it wouldn't be but who knows
                        for other_stairs in self.memory.generators[self.branch][self.floor_level + 1].tile_map.get_stairs():
                            if (other_stairs.pair == None and not other_stairs.downward):
                                current_stairs.pair_stairs(other_stairs)
                                break
                self.floor_level += 1
            elif not downward and isinstance(current_stairs, TI.UpStairs) and self.floor_level != 1:
                if current_stairs.pair is None:
                    if not current_stairs.downward: #Don't know why it wouldn't be but who knows
                        for other_stairs in self.memory.generators[self.branch][self.floor_level - 1].tile_map.get_stairs():
                            if (other_stairs.pair == None and other_stairs.downward):
                                current_stairs.pair_stairs(other_stairs)
                                break
                self.floor_level -= 1
            self.player.x, self.player.y = (current_stairs.pair.get_location())
            self.player.visited_stairs = []
            self.generator = self.memory.generators[self.branch][self.floor_level]

        if self.branch == "Forest":
            if self.day == "Nighttime":
                for monster in self.generator.monster_map.all_entities():
                    monster.nightify()
            elif self.day == "Daytime":
                for monster in self.generator.monster_map.all_entities():
                    monster.dayify()

        self.taking_stairs = False

    def change_branch(self):
        self.taking_stairs = True
        playerx, playery = self.player.get_location()
        if self.player.character.energy < 0:
            self.time_passes(-self.player.character.energy)
            self.monster_loop(-self.player.character.energy)
            self.player.character.energy = 0

        gate = self.generator.tile_map.locate(playerx, playery)
        branch = gate.outgoing.get_branch()
        depth = gate.outgoing.get_depth()

        self.floor_level = depth
        print("The gateway you are taking is {}".format(self.generator.tile_map.track_map[playerx][playery]))
        self.player.x, self.player.y = (gate.outgoing.get_location())
        self.player.visited_stairs = []
        self.branch = branch
        self.generator = self.memory.generators[branch][self.floor_level]
        self.memory.floor_level = depth
        self.memory.branch = branch

        if self.branch == "Forest":
            if self.day == "Nighttime":
                for monster in self.generator.monster_map.all_entities():
                    monster.nightify()
            elif self.day == "Daytime":
                for monster in self.generator.monster_map.all_entities():
                    monster.dayify()

        self.taking_stairs = False

    def init_game(self, display):
        self.player = player.Player(0, 0)
        self.memory.player = self.player
        self.branch = "Throne"
        self.floor_level = 1

        gateway_data = self.dungeon_data.gateway_data
        dungeon_data = self.dungeon_data

        self.render_exploration = True
        self.memory.render_exploration = self.render_exploration

        for branch in dungeon_data.get_branches():
            self.memory.generators[branch] = {}
            for level in range(1, dungeon_data.get_depth(branch) + 1):
                generator = M.DungeonGenerator(level, self.player, branch, gateway_data, dungeon_data)
                if branch == "Ocean":
                    monsters = generator.monster_map.all_entities()
                    for monster in monsters:
                        print("Ocean monster x is {}, ocean monster y is {}".format(monster.x, monster.y))
                self.memory.generators[branch][level] = generator

        known_gateways = gateway_data.all_gateways()
        #for gateway in known_gateways:
         #   print("This is known {}".format(gateway))
        for lair in known_gateways:
            print("Investigating lair: {}".format(lair))
            gateway1 = -1
            for gateways in self.memory.generators[lair[0]][lair[1]].tile_map.get_gateway():
                print("Initial gateway is: {}".format(gateways))
                gateway1 = gateways
                if not gateway1.has_outgoing():
                    for lair2 in gateway_data.paired_gateway(lair):
                        print("Potential link is {}".format(lair2))
                        gateway2 = -1
                        for gateways in self.memory.generators[lair2[0]][lair2[1]].tile_map.get_gateway():
                            gateway2 = gateways
                            if not gateway2.has_incoming():
                                print("Linking {} with {}".format(gateway1, gateway2))
                                gateway1.pair_gateway(gateway2)
                                gateway2.pair_gateway(gateway1)
                                break
                        break



        self.memory.floor_level = 1
        self.memory.explored_levels = 1
        self.generator = self.memory.generators[self.branch][self.floor_level]

        for stairs in (self.generator.tile_map.get_stairs()):
            if not stairs.downward:
                x, y = stairs.get_location()
        self.player.x = x
        self.player.y = y


    def add_message(self, message, color = (255,255,255)):
        if len(self.messages) >= 5:
            self.messages.pop(0)
        self.messages.append((message, color))
        self.dirty_messages = True

    def clear_message(self):
        self.messages = []

    def add_target(self, target):
        self.prev_target = self.target_to_display
        self.target_to_display = target

    def void_target(self):
        if self.target_to_display == None:
            return
        if self.generator.monster_map.get_passable(self.target_to_display[0], self.target_to_display[
            1]):  # don't void if its a monster, cuz its a good QOL to keep monster health on screen
            self.target_to_display = None

    def start_targetting(self, start_on_player=False):
        self.change_loop(LoopType.targeting)
        if start_on_player:
            self.targets.start_target(self.player.get_location())
            self.add_target(self.player.get_location())
            self.screen_focus = self.player.get_location()
        else:
            closest_monster = self.player.character.get_closest_monster(self)
            self.targets.start_target(closest_monster.get_location())
            self.add_target(closest_monster.get_location())
            self.screen_focus = closest_monster.get_location()

    def init_new_game(self):
        self.display.create_game_ui(self.player)

    def load_game(self):
        self.update_screen = False
        self.floor_level = self.memory.floor_level

        self.generator = self.memory.generators[self.branch][self.floor_level]
        self.tile_map = self.generator.tile_map

        self.player = self.memory.player
        self.player.character.energy = 0
        self.change_loop(LoopType.action)
       # self.keyboard = self.memory.keyboard

        self.render_exploration = self.memory.render_exploration

    def clear_data(self):
        self.change_loop(LoopType.main)
        self.update_screen = True

        self.screen_focus = None
        self.floor_level = 0
        self.memory = Memory()
        self.tile_map = None

        self.generator = None
        self.messages = []

    def time_passes(self, time):
        self.timer += time
        for i in range(int(self.timer // 100)):
            self.player.statistics.add_turn_details()
            self.total_time += 1
            if self.total_time % 50 == 49:
                self.change_daytime()
            # do status effect stuff
            self.player.character.tick_all_status_effects(self)
            self.player.mage.tick_cooldowns()

            if self.branch != "Forest":
                self.player.character.tick_regen()

            for quest in self.player.quests:
                quest.check_for_progress(self)

            for star in self.stars:
                star.take_action(self)

            if self.generator.tile_map.locate(self.player.x,self.player.y).check_if_status_applies(self.player):
                for status_effect in self.generator.tile_map.locate(self.player.x,self.player.y).get_status_effects():
                    self.player.character.add_status_effect(status_effect)

            for monster in self.generator.monster_map.all_entities():
                monster.character.tick_all_status_effects(self)
                # tick skill cooldowns
                monster.character.tick_cooldowns()
                # tick regen
                monster.character.tick_regen()

                if self.generator.tile_map.locate(monster.x, monster.y).check_if_status_applies(monster):
                    for status_effect in self.generator.tile_map.locate(monster.x,
                                                                        monster.y).get_status_effects():
                        monster.character.add_status_effect(status_effect)

        self.timer = self.timer % 100

    def change_daytime(self):
        while self.total_time % 50 != 49:
            self.total_time += 1
        if self.day == "Daytime":
            self.day = "Nighttime"
            if self.branch == "Forest":
                for monster in self.generator.monster_map.all_entities():
                    monster.nightify()
        elif self.day == "Nighttime":
            self.day = "Daytime"
            if self.branch == "Forest":
                for monster in self.generator.monster_map.all_entities():
                    monster.dayify()

    def get_available_classes(self):
        return [Rogue(), Warrior(), Mage()]

    def implement_class(self):
        player = self.player
        chosen_class = self.class_selection
        endurance, intelligence, dexterity, strength = chosen_class.get_attributes()
        player.character.endurance += endurance
        player.character.intelligence += intelligence
        player.character.dexterity += dexterity
        player.character.strength += strength
        for spell in chosen_class.get_spells():
            player.mage.add_spell(spell(player))
        for item in chosen_class.get_items():
            player.inventory.get_item(item, self)
            player.do_equip(item)


