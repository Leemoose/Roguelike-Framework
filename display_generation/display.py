from .ui import *
import pygame
import pygame_gui

class Display:
    """
    Display is responsible for put images in the screen. Currently have it set that each function will update a
    seperate part of the game.
    """
    def __init__(self, width, height, textSize, textWidth, textHeight):
        pygame.display.set_caption('Tiles')
        self.win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen_width = width
        self.screen_height = height
        self.textWidth = textWidth
        self.textHeight = textHeight
        self.textSize = textSize

        action_screen_width = self.screen_width * 3 // 4
        action_screen_height = self.screen_height * 5 // 6
        num_tiles_wide = action_screen_width // self.textSize
        num_tiles_height = action_screen_height // self.textSize
        self.r_x = num_tiles_wide // 2
        self.r_y = num_tiles_height // 2

        self.uiManager = pygame_gui.UIManager((width, height), "./assets/theme.json")
        self.windows = []
        self.clock = pygame.time.Clock()
        self.colorDict = None

        self.quest_number = -1
        

    def screen_to_tile(self, player, x, y):
        xplayerscreen, yplayerscreen = self.r_x * self.textSize + self.textSize // 2, self.r_y * self.textSize + self.textSize // 2
        xdiff = x - xplayerscreen + 10
        ydiff = y - yplayerscreen + 10
        return (player.x + xdiff // self.textSize, player.y + ydiff//self.textSize)
    def update_sizes(self):
        self.screen_width, self.screen_height = self.win.get_size()

    def update_main(self, loop):
        # Main Screen
        self.win.fill((0, 0, 0))
        self.uiManager.draw_ui(self.win)
        image_size = 100
        image_offset_from_left = (self.screen_width - image_size) // 2
        image_offset_from_top = self.screen_height // 2
        self.win.blit(pygame.transform.scale(pygame.image.load('display_generation/yendorb_deactivated.png'),
                                             (image_size, image_size)), (image_offset_from_left, image_offset_from_top))
        font = pygame.font.Font('freesansbold.ttf', 12)


    def update_display(self, loop):
        self.win.fill((0,0,0))

        floormap = loop.generator.tile_map
        tileDict = loop.tileDict
        monsterID = loop.generator.monster_map.dict
        item_ID = loop.generator.item_map.dict
        npc_ID = loop.generator.npc_dict
        monster_map = loop.monster_map
        player = loop.player
        messages = loop.messages
        target_to_display = loop.screen_focus

        action_screen_offset_from_left = 0
        action_screen_offset_from_top = 0
        action_screen_width = self.screen_width * 3 // 4
        action_screen_height = self.screen_height * 5 // 6
        num_tiles_wide = action_screen_width // self.textSize
        num_tiles_height = action_screen_height // self.textSize

        self.r_x = num_tiles_wide // 2
        self.r_y = num_tiles_height // 2

        self.x_start = player.x - self.r_x
        self.x_end = player.x + self.r_x
        self.y_start = player.y - self.r_y
        self.y_end = player.y + self.r_y

        stats_offset_from_left = action_screen_width
        stats_offset_from_top = 0
        stats_width = self.screen_width - stats_offset_from_left
        stats_height = self.screen_height // 3

        map_tile_size = 5
        map_offset_from_left = action_screen_width
        map_offset_from_top = stats_height
        map_width = self.screen_width - action_screen_width
        map_message_width = 30
        map_height = self.screen_height // 4
        map_message_height = 15
        num_map_tiles_wide = map_width // map_tile_size
        num_map_tiles_height = map_height // map_tile_size
        r_map_x = num_map_tiles_wide // 2
        r_map_y = num_map_tiles_height // 2
        x_map_start = player.x - r_map_x
        x_map_end = player.x + r_map_x
        y_map_start = player.y - r_map_y
        y_map_end = player.y + r_map_y

        message_offset_from_left = 0
        message_offset_from_top = action_screen_height
        message_width = action_screen_width // 2 - 2 * message_offset_from_left
        message_height = self.screen_height - action_screen_height

        skill_bar_height = self.screen_height - action_screen_height
        skill_bar_offset_from_left = message_offset_from_left + message_width
        skill_bar_width = stats_offset_from_left - skill_bar_offset_from_left
        skill_bar_offset_from_top = action_screen_height

        num_skill_buttons = 6
        skill_button_width = (action_screen_width - skill_bar_offset_from_left) // (num_skill_buttons + 1)
        skill_button_height = (self.screen_height - action_screen_height) * 3 // 4
        skill_button_offset_from_top = (self.screen_height - action_screen_height) // 8 + skill_bar_offset_from_top
        skill_button_offset_from_each_other_width = (action_screen_width - skill_bar_offset_from_left) // (num_skill_buttons + 1)// (num_skill_buttons + 1)

        views_num_buttons_height = 3
        views_num_buttons_width = 2
        views_width = (self.screen_width - action_screen_width)
        views_height = (self.screen_height - map_offset_from_top - map_height)
        views_offset_from_left = action_screen_width
        views_offset_from_top = map_offset_from_top + map_height
        views_button_width = (self.screen_width - action_screen_width) // (views_num_buttons_width + 1)
        views_button_height = (self.screen_height - map_offset_from_top - map_height) // (views_num_buttons_height + 1)
        views_button_offset_from_each_other_height = (self.screen_height - map_offset_from_top - map_height) // (
                    views_num_buttons_height + 1) // (views_num_buttons_height + 1)
        views_button_offset_from_each_other_width = (self.screen_width -action_screen_width) // (
                views_num_buttons_width + 1) // (views_num_buttons_width + 1)


       #Making all the tiles
        for x in range(self.x_start, self.x_end):
            for y in range(self.y_start, self.y_end):
                self.draw_single_tile(x, y, floormap, tileDict)

        for key in item_ID.subjects:
            item = item_ID.get_subject(key)
            if (item.x >= self.x_start and item.x < self.x_end and item.y >= self.y_start and item.y < self.y_end):
                if floormap.track_map[item.x][item.y].visible:
                    item_tile = tileDict.tile_string(item.render_tag)
                    self.win.blit(item_tile, (self.textSize * (item.x - self.x_start), self.textSize * (item.y - self.y_start)))

        for key in npc_ID.subjects:
            npc = npc_ID.get_subject(key)
            if (npc.x >= self.x_start and npc.x < self.x_end and npc.y >= self.y_start and npc.y < self.y_end):
                if floormap.track_map[npc.x][npc.y].visible:
                    npc_tile = tileDict.tile_string(npc.render_tag)
                    self.win.blit(npc_tile, (self.textSize * (npc.x - self.x_start), self.textSize * (npc.y - self.y_start)))
                    if npc.has_stuff_to_say:
                        speech_tile = tileDict.tile_string(122) # render tag of speech bubble, check mapping.py if you need to change
                        self.win.blit(speech_tile, (self.textSize * (npc.x - self.x_start), self.textSize * (npc.y - self.y_start)))

        for key in monsterID.subjects:
            monster = monsterID.get_subject(key)
            if (monster.x >= self.x_start and monster.x < self.x_end and monster.y >= self.y_start and monster.y < self.y_end):
                if floormap.track_map[monster.x][monster.y].visible:
                    monster_tile = tileDict.tile_string(monster.render_tag)
                    self.win.blit(monster_tile, (self.textSize*(monster.x - self.x_start), self.textSize*(monster.y - self.y_start)))

        #Draw base character depending on armor state
        if (player.character.equipment_slots["body_armor_slot"][0] == None):
            self.win.blit(tileDict.tile_string(200), (self.r_x * self.textSize, self.r_y * self.textSize)) # DONG MODE ENGAGED
        else:
            self.win.blit(tileDict.tile_string(-200), (self.r_x * self.textSize, self.r_y * self.textSize))

        #Draw items on top
        if player.character.equipment_slots["boots_slot"][0] != None:
            self.win.blit(tileDict.tile_string(201), (self.r_x * self.textSize, self.r_y * self.textSize))
        if player.character.equipment_slots["gloves_slot"][0] != None:
            self.win.blit(tileDict.tile_string(202), (self.r_x * self.textSize, self.r_y * self.textSize))
        if player.character.equipment_slots["helmet_slot"][0] != None:
            self.win.blit(tileDict.tile_string(203), (self.r_x * self.textSize, self.r_y * self.textSize))
        self.uiManager.draw_ui(self.win)

        #Making all map tiles
        item_map = loop.generator.item_map
        for x in range(x_map_start, x_map_end):
            for y in range(y_map_start, y_map_end):
                if (x < 0 or x >= floormap.width or y < 0 or y >= floormap.height):
                    pass
                elif floormap.track_map[x][y].seen == False:
                    pass
                else:
                    if floormap.track_map[x][y].passable:
                        if floormap.track_map[x][y].visible and not monster_map.get_passable(x,y):
                            pygame.draw.rect(self.win, (207, 207, 207),
                                             pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                         map_offset_from_top + map_tile_size * (y - y_map_start),
                                                         map_tile_size, map_tile_size))
                        elif not item_map.get_passable(x,y):
                            pygame.draw.rect(self.win, (0, 200, 0),
                                             pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                         map_offset_from_top + map_tile_size * (y - y_map_start),
                                                         map_tile_size, map_tile_size))
                        elif floormap.track_map[x][y].has_trait("stairs"):
                            pygame.draw.rect(self.win, (0, 0, 200),
                                                 pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                             map_offset_from_top + map_tile_size * (y - y_map_start),
                                                             map_tile_size, map_tile_size))
                        elif floormap.track_map[x][y].has_trait("gateway"):
                            pygame.draw.rect(self.win, (0, 75, 100),
                                                 pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                             map_offset_from_top + map_tile_size * (y - y_map_start),
                                                             map_tile_size, map_tile_size))
                        else:
                            pygame.draw.rect(self.win, (131, 131, 131),
                                             pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                         map_offset_from_top + map_tile_size * (y - y_map_start),
                                                         map_tile_size, map_tile_size))
                            for key in npc_ID.subjects:
                                npc = npc_ID.get_subject(key)
                                if floormap.track_map[npc.x][npc.y].seen:
                                    pygame.draw.rect(self.win, (200, 100, 0),
                                                     pygame.Rect(map_offset_from_left + map_tile_size * (npc.x - x_map_start),
                                                                 map_offset_from_top + map_tile_size * (npc.y - y_map_start),
                                                                 map_tile_size, map_tile_size))
                    else:
                        pygame.draw.rect(self.win, (100, 100, 100),
                                         pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                     map_offset_from_top + map_tile_size * (y - y_map_start),
                                                     map_tile_size, map_tile_size))
        pygame.draw.rect(self.win, (150, 100, 50),
                         pygame.Rect(map_offset_from_left + r_map_x * map_tile_size,
                                     map_offset_from_top + r_map_y * map_tile_size,
                                     map_tile_size, map_tile_size))
        pygame.draw.rect(self.win, (150, 100, 50),
                         pygame.Rect(map_offset_from_left + (num_map_tiles_wide - num_tiles_wide)* map_tile_size // 2,
                                     map_offset_from_top + (num_map_tiles_height - num_tiles_height)* map_tile_size //2,
                                     num_tiles_wide * map_tile_size, num_tiles_height* map_tile_size), 1)

    #HORRIBLE HACK - THIS IS ALSO DEFINED IN UI.PY - KEEP THEM SYNCED!
    def get_status_text(self, entity):
        status = "Healthy"
        if entity.character.health < entity.character.max_health // 3 * 2:
            status = "Wounded"
        effects = entity.character.status_effects
        for effect in effects:
            status += ", " + effect.description()
        return status

    def write_messages(self, messages):
        font = pygame.font.Font('freesansbold.ttf', 12)
        for i, message in enumerate(messages):
            text = font.render(message, True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 100 * 12, self.screen_height // 100 * (85 + i * 3)))

    def draw_examine_window(self, target, loop):
        tileDict = loop.tileDict
        floormap = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        monster_dict = monster_map.dict
        item_dict = loop.generator.item_map.dict
        player = loop.player
        examine_offset_from_left = self.screen_width // 30
        examine_offset_from_top = self.screen_height // 20
        try:
            x, y = target

        except:
            return False 
        if (not loop.generator.in_map(x, y)) or not floormap.track_map[x][y].visible:
            return False
        black_screen = pygame.transform.scale(pygame.image.load("assets/ui/black_screen.png"), (self.screen_width // 5, self.screen_height // 5))
        self.win.blit(black_screen, (0, 0))
        
        any_item_found = False
        
        nothing_at_target = True

        # find monster at target
        if not monster_map.get_passable(x,y):
            monster = monster_map.locate(x,y)
            if monster == None:
                return

            # draw monster
            to_draw = monster.render_tag
            tag = tileDict.tile_string(to_draw)
            self.win.blit(tag, (examine_offset_from_left, examine_offset_from_top))
            font = pygame.font.Font('freesansbold.ttf', 12)

            # name
            text = font.render(monster.name, True, (255, 255, 255))
            self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 50))

            # level
            text = font.render("Level: " + str(monster.character.level), True, (255, 255, 255))
            self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 65))
            
            # health
            text = font.render("Health: " + str(monster.character.health) + "/" + str(monster.character.max_health), True, (255, 255, 255))
            self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 80))
                
            # status
            status = self.get_status_text(monster)
            text = font.render("Status: " + status, True, (255, 255, 255))
            self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 95))

            # description
            description = monster.description
            text = font.render(description, True, (255, 255, 255))
            self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 110))
            nothing_at_target = False
        else:
            # find item at target
            for key in item_dict.subjects:
                item = item_dict.get_subject(key)
                count = 0
                if item.x == x and item.y == y:
                    # draw item
                    to_draw = item.render_tag
                    tag = tileDict.tile_string(to_draw)
                    self.win.blit(tag, (examine_offset_from_left, examine_offset_from_top))
                    font = pygame.font.Font('freesansbold.ttf', 12)

                    # name
                    text = font.render(item.name, True, (255, 255, 255))
                    self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 50))

                    # description item descriptions are too long
                    # text = font.render(item.description, True, (255, 255, 255))
                    # self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 65))
                    # nothing_at_target = False

                    text = font.render(item.equipment_type, True, (255, 255, 255))
                    self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 65))

                    nothing_at_target = False

                    # stats (if present)
                    next_text = 80
                    if hasattr(item, "damage_min"):
                        text = font.render("Damage: " + str(item.damage_min) + " - " + str(item.damage_max), True, (255, 255, 255))
                        self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + next_text))
                        next_text += 15
                    if hasattr(item, "defense"):
                        text = font.render("Defense: " + str(item.defense), True, (255, 255, 255))
                        self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + next_text))
                        next_text += 15
                    if hasattr(item, "consumable"):
                        text = font.render("Consumable", True, (255, 255, 255))
                        self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + next_text))
                        next_text += 15
                    examine_offset_from_top = examine_offset_from_top + next_text + 30
                    count += 1
                    if count > 6:
                        break
        # find player at target
        if nothing_at_target:
            if player.x == x and player.y == y:
                nothing_at_target = False

                to_draw = player.render_tag
                tag = tileDict.tile_string(to_draw)
                self.win.blit(tag, (self.screen_width  // 10, examine_offset_from_top))
                font = pygame.font.Font('freesansbold.ttf', 12)

                # random flavor text since detailed player info is elsewhere
                text = font.render("You", True, (255, 255, 255))
                self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 50))
                text = font.render("You are here", True, (255, 255, 255))
                self.win.blit(text, (examine_offset_from_left, examine_offset_from_top + 65))
        return nothing_at_target

    def draw_on_button(self, button, img, letter="", button_size=None, shrink=False, offset_factor = 10, text_offset = (15, 0.8)):
        offset = (0, 0)
        if shrink:# shrink weapon image a bit
            img = pygame.transform.scale(img, (button_size[0] // 5 * 4, button_size[1] // 5 * 4))
            offset = (button_size[0] // offset_factor, button_size[1] // offset_factor)
        button.drawable_shape.states['normal'].surface.blit(img, offset)
        button.drawable_shape.states['hovered'].surface.blit(img, offset)
        button.drawable_shape.states['disabled'].surface.blit(img, offset)
        button.drawable_shape.states['selected'].surface.blit(img, offset)
        button.drawable_shape.states['active'].surface.blit(img, offset)
        if button_size:
            font_size = 20
            font = pygame.font.Font('freesansbold.ttf', font_size)
            text = font.render(letter, True, (255, 255, 255))
            button.drawable_shape.states['normal'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['hovered'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['disabled'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['selected'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['active'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
        button.drawable_shape.active_state.has_fresh_surface = True
        # button.drawable_shape.redraw_all_states()


    def refresh_screen(self):
        self.uiManager.clear_and_reset()

    def stat_text(self, entity, stat):
        return str(stat)

    def stat_modifier(self, entity, stat):
        if stat >= 0:
            return "+" + str(stat)
        else:
            return str(stat)


    def draw_character_stats(self, player, margin_from_left, margin_from_top, width, height):
        if player.character.strength >= 0:
            strength_modifier = "+" + str(player.character.strength)
        else:
            strength_modifier = str(player.character.strength)
        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((margin_from_left, margin_from_top), (width, height)),
            
            html_text = "Player<br><br>"
                        "Stats<br>"
                        "Strength: " + self.stat_text(player, player.character.strength) + "<br>"
                        "Dexterity: " + self.stat_text(player, player.character.dexterity) + "<br>"
                        "Endurance: " + self.stat_text(player, player.character.endurance) + "<br>"
                        "Intelligence: " + self.stat_text(player, player.character.intelligence) + "<br>" +
                        "Health: " + str(player.character.health) + " / " + str(player.character.max_health) + "<br>"
                        "Mana: " + str(player.character.mana) + " / " + str(player.character.max_mana) + "<br>"
                        "<br>"
                        "Damage: " + str(player.character.get_damage_min()) + " - " + str(player.character.get_damage_max()) + " (" + strength_modifier + ") <br>"
                        "Defense: " + str(player.character.armor) + " (+" + str(player.character.endurance // 3) + ") <br>"
                        "Movement Delay: " + str(player.character.action_costs["move"]) + "<br>"
                        "Skill Damage Bonus: " + str(player.character.skill_damage_increase()) + "<br>"
                        "Effect Duration Bonus: " + str(player.character.skill_duration_increase()) + "<br>"
                        "<br>Known Skills:<br>"
                        + "<br>".join([str(i + 1) + ". " + skill.description() for i, skill in enumerate(player.character.skills)])
                        ,
            manager=self.uiManager
        )

    def draw_empty_box(self, margin_from_left, margin_from_top, width, height):
        box = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((margin_from_left, margin_from_top), (width, height)),
            manager=self.uiManager
        )

    def draw_escape_button(self, windowX, windowY, window_width, window_height):
        buttonWidth = 40
        buttonHeight = 40

        buttonX = windowX + window_width - buttonWidth
        buttonY = windowY

        esc_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((buttonX, buttonY), (buttonWidth, buttonHeight)),
            text="X",
            manager=self.uiManager,
            starting_height=1000)
        esc_button.action = "esc"


    def update_entity(self, loop, item_screen = True, create = False):
        entity = loop.screen_focus
        tileDict = loop.tileDict
        player = loop.player
        if create == True:
            self.uiManager.clear_and_reset()
        self.win.fill((0,0,0))
        entity_screen_width = self.screen_width // 2
        entity_screen_height = self.screen_height // 2
        entity_offset_from_left = self.screen_width // 4
        entity_offset_from_top = self.screen_height // 4

        entity_message_width = self.screen_width // 2
        entity_message_height = self.screen_height // 10
        entity_message_offset_from_left = self.screen_width // 4
        entity_message_offset_from_top = self.screen_height  // 4

        entity_image_width = self.screen_width // 20
        entity_image_height = self.screen_width // 20
        entity_image_offset_from_left = self.screen_width // 4 + self.screen_width // 50
        entity_image_offset_from_top = self.screen_height // 4

        entity_button_width = self.screen_width // 10
        entity_button_height = self.screen_height // 30
        entity_button_offset_from_left = (self.screen_width) // 2 - entity_button_width * 3 //2
        entity_button_offset_from_top = entity_screen_height + entity_offset_from_top - entity_button_height - self.screen_height // 50
        entity_button_offset_from_each_other =  entity_button_width // 2

        entity_text_offset_from_left = entity_offset_from_left + entity_screen_width // 20
        entity_text_offset_from_top = entity_image_offset_from_top + entity_message_height
        entity_text_width = entity_screen_width * 11 // 12
        entity_text_height = entity_screen_height * 3 // 5

        buttons_drawn = 0

        entity_image = pygame.transform.scale(tileDict.tiles[entity.render_tag],
                                     (entity_image_width, entity_image_height))

        pygame.draw.rect(self.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))

        self.win.blit(entity_image, (entity_image_offset_from_left, entity_image_offset_from_top))

        if (create == True):
            self.draw_escape_button(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height)

        entity_name = entity.name
        if create == True:
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                          (entity_message_width, entity_message_height)),
                text=entity_name,
                manager=self.uiManager,
                object_id='#title_small')

        if item_screen:
            item = entity
            show = False
            if item.can_be_levelled:
                item_level = item.level
                if item_level > 1:
                    addition = " (+" + str(item_level - 1) + ")"
                    #
                    if create == True:
                        pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect((entity_message_offset_from_left + entity_message_width * 4// 5, entity_message_offset_from_top),
                                                (entity_message_width // 4, entity_message_height)),
                        text=addition,
                        manager=self.uiManager,
                        object_id='#title_addition')
            pretext = ""
            action = ""
            if item.equipable:
                if item.equipped:
                    pretext = "Unequip"
                    action = "u"
                    show = True
                    if item.cursed:
                        show = False
                else:
                    pretext = "Equip"
                    action = "e"
                    show = True
            elif item.consumeable and item.equipment_type == "Potiorb":
                pretext = "Quaff"
                action = "q"
                show = True
            elif item.consumeable and item.equipment_type == "Scrorb" or item.equipment_type == "Book":
                pretext = "Read"
                action = "r"
                show = True
            if create == True:
                if show:
                    button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((entity_button_offset_from_left, entity_button_offset_from_top),
                                                  (entity_button_width, entity_button_height)),
                        text=pretext,
                        manager=self.uiManager)
                    button.action = action

                buttons_drawn += 1

                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((entity_button_offset_from_left + (entity_button_width + entity_button_offset_from_each_other) * buttons_drawn, entity_button_offset_from_top),
                                              (entity_button_width, entity_button_height)),
                    text='Drop',
                    manager=self.uiManager)
                button.action = "d"

                buttons_drawn += 1


        entity_text = ""
        entity_text += entity.description  + "<br><br>"

        if entity.has_trait("item"):
            item = entity
            if entity.has_trait("equipment"):
                if item.equipped:
                    entity_text += "Currently equipped<br>"
                if item.cursed:
                    entity_text += "<shadow size=1 offset=0,0 color=#901010><font color=#E0F0FF>" + "Once equipped, it cannot be taken off" +  "</font></shadow><br>"
                entity_text += "Equipment type: " + item.equipment_type + "<br>"
                if item.required_strength >= 0:
                    if player.character.strength < item.required_strength:
                        req_str_text = "<shadow size=1 offset=0,0 color=#901010><font color=#E0F0FF>Required Strength: " + str(item.required_strength) + "(Unequippable) </font></shadow><br>"
                    else:
                        req_str_text = "Required Strength: " + str(item.required_strength) + "<br>"
                    entity_text += req_str_text
                if item.has_trait("weapon"):
                    entity_text += "Damage: " + str(item.damage_min + player.character.base_damage) + " - " + str(item.damage_max + player.character.base_damage) + "<br>"
                    if item.on_hit:
                        entity_text += "On hit: " + item.on_hit_description + "<br>"

                stats = item.stats.GetStatsForLevel(item.level)
                if stats[2]> 0:
                    entity_text += "Intelligence: +" + str(stats[2]) + "<br>"
                elif stats[2]<0:
                    entity_text += "Intelligence: " + str(stats[2]) + "<br>"
                if stats[0] > 0:
                    entity_text += "Strength: +" + str(stats[0]) + "<br>"
                elif stats[0]<0:
                    entity_text += "Strength: " + str(stats[0]) + "<br>"
                if stats[1] > 0:
                    entity_text += "Dexterity: +" + str(stats[1]) + "<br>"
                elif stats[1]<0:
                    entity_text += "Dexterity: " + str(stats[1]) + "<br>"
                if stats[3] > 0:
                    entity_text += "Endurance: +" + str(stats[3]) + "<br>"
                elif stats[3]<0:
                    entity_text += "Endurance: " + str(stats[3]) + "<br>"
                if stats[4] > 0:
                    entity_text += "Armor: +" + str(stats[4]) + "<br>"
                elif stats[4]<0:
                    entity_text += "Armor: " + str(stats[4]) + "<br>"
            elif entity.has_trait("potion") or entity.has_trait("ring"):
                entity_text += "Effect: " + str(entity.action_description) + "<br>"
            if item.attached_skill_exists:
                entity_text += "Grants skill: " + item.get_attached_skill_description() + "<br>"

        if entity.has_trait("monster"):
            entity_text += "Health: " + str(entity.character.health) + " / " + str(entity.character.max_health) + "<br>"
            entity_text += "Attack: " + str(entity.character.get_damage_min()) + " - " + str(entity.character.get_damage_max()) + "<br>"
            entity_text += "Armor: " + str(entity.character.armor) + "<br>"
            for skill in entity.character.skills:
                entity_text += "Has skill: " + str(skill.name)+ "<br>"
            if entity.orb:
                entity_text += "It's very round.<br>"
                for i, skill in enumerate(entity.character.skills):
                    if i == 0:
                        entity_text += "Skills: "
                    entity_text += skill.description()
                    if i < len(entity.character.skills) - 1:
                        entity_text += ", "
        if create == True:
            text_box = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((entity_text_offset_from_left, entity_text_offset_from_top), (entity_text_width, entity_text_height)),
                html_text = entity_text,
                manager=self.uiManager)

        self.uiManager.draw_ui(self.win)

    def update_questpopup_screen(self, loop, message):
        pygame.draw.rect(self.win, (0, 0, 0),
                         pygame.Rect(0, 0, 300,
                                     100))
        font = pygame.font.SysFont("Ariel", 25)
        text = font.render(message, True, (255, 255, 255))
        self.win.blit(text, (25, 25))

    def draw_single_tile(self, x, y, floormap, tileDict):
        if (x < 0 or x >= floormap.width or y < 0 or y >= floormap.height):
            pass
        elif floormap.track_map[x][y].seen == False:
            pass
        elif floormap.track_map[x][y].visible == True:
            tag = tileDict.tile_string(floormap.get_tag(x, y))
            self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))
            if floormap.track_map[x][y].on_fire:
                self.win.blit(tileDict.tile_string(20), (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))
        else:
            tag = tileDict.tile_string(floormap.track_map[x][y].shaded_render_tag)
            self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))

    def update_examine(self, target, loop):
        x, y = target
        tag = loop.tileDict.tile_string(901)
        self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))

    def update_ui(self):
        deltaTime = self.clock.tick() / 1000
        self.uiManager.update(deltaTime)

    def update_screen(self, loop):
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)

    def update_screen_without_fill(self, loop):
        self.uiManager.draw_ui(self.win)


