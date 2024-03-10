import pygame
import pygame_gui
import items as I
import ui
import objects as O
import monster as M

class Buttons:
    def __init__(self):
        self.buttons = {}

    def add(self, button, name):
        self.buttons[name] = button
"""
    def render_button(self, key):
        font = pygame.font.Font('freesansbold.ttf', 32)

        button = self.buttons[key]
        text = font.render(key, True, (255, 255, 255))
        text_width, text_height = font.size("Enter: Play!")
        scr.win.blit(text, (scr.screen_width / 2 - text_width / 2, scr.screen_height * 85 / 100 + button.height / 2 - text_height / 2))
        """


class Button:
    # A button is anything in game that you could click
    def __init__(self, screen_width, screen_height, asset, modx, mody, action, positionx, positiony):
        self.width = screen_width * modx
        self.height = screen_height * mody
        self.modx = modx  #How large in fraction relative to the screen
        self.mody = mody  #How tall in fraction relative to the screen
        self.img = pygame.transform.scale(pygame.image.load("assets/button.png"), (self.width, self.height))
        self.action = action  #See keyboard for list of actions
        self.positionx = positionx  #center of button
        self.positiony = positiony  #center of button

    def scale(self, screen_width, screen_height):
        #rescaling the button size
        self.img = pygame.transform.scale(self.img, (screen_width * self.modx, screen_height * self.mody))

    def clicked(self, x, y):
        #x,y is position clicked
        cornerx, cornery = self.get_position()
        return (cornerx < x and x < cornerx + self.width) and (cornery < y and y < cornery + self.height)

    def get_position(self):
        return self.positionx - self.width // 2, self.positiony + self.height // 2


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
        self.uiManager = pygame_gui.UIManager((width, height), "theme.json")
        self.windows = []
        self.clock = pygame.time.Clock()
        self.buttons = Buttons()
        self.colorDict = None
        

    def screen_to_tile(self, player, x, y):
        xplayerscreen, yplayerscreen = self.r_x * self.textSize + self.textSize // 2, self.r_y * self.textSize + self.textSize // 2
        xdiff = x - xplayerscreen + 10
        ydiff = y - yplayerscreen + 10
        return (player.x + xdiff // self.textSize, player.y + ydiff//self.textSize)
    def update_sizes(self):
        self.screen_width, self.screen_height = self.win.get_size()

    def create_display(self, loop):
        self.uiManager.clear_and_reset()
        #FPS counter
        #fps_counter = ui.FPSCounter(
        #   pygame.Rect((0,0),(400,40)),
        #    self.uiManager
        #)

        tileDict = loop.tileDict
        monsterID = loop.monster_dict
        player = loop.player
        messages = loop.messages

        action_screen_width = self.screen_width * 3 // 4
        action_screen_height = self.screen_height * 5 // 6
        num_tiles_wide = action_screen_width // self.textSize
        num_tiles_height = action_screen_height // self.textSize

        r_x = num_tiles_wide // 2
        r_y = num_tiles_height // 2

        self.x_start = player.x - r_x
        self.x_end = player.x + r_x
        self.y_start = player.y - r_y
        self.y_end = player.y + r_y

        stats_offset_from_left = action_screen_width
        stats_offset_from_top = 0
        stats_width = self.screen_width - stats_offset_from_left
        stats_height = self.screen_height // 3

        map_tile_size = 8
        map_offset_from_left = action_screen_width
        map_offset_from_top = stats_height
        map_width = self.screen_width - action_screen_width
        map_message_width = 80
        map_height = self.screen_height // 4
        map_message_height = 30
        num_map_tiles_wide = map_width // map_tile_size
        num_map_tiles_height = map_height // map_tile_size
        r_map_x = num_map_tiles_wide // 2
        r_map_y = num_map_tiles_height // 2

        message_offset_from_left = 0
        message_offset_from_top = action_screen_height
        message_width = action_screen_width *5 // 12 - 2 * message_offset_from_left
        message_height = self.screen_height - action_screen_height

        skill_bar_height = self.screen_height - action_screen_height
        skill_bar_offset_from_left = message_offset_from_left + message_width
        skill_bar_width = stats_offset_from_left - skill_bar_offset_from_left
        skill_bar_offset_from_top = action_screen_height

        num_skill_buttons = 8
        skill_button_width = (action_screen_width - skill_bar_offset_from_left) // (num_skill_buttons + 1)
        skill_button_height = (self.screen_height - action_screen_height) * 3 // 4
        skill_button_offset_from_top = (self.screen_height - action_screen_height) // 8 + skill_bar_offset_from_top
        skill_button_offset_from_each_other_width = (action_screen_width - skill_bar_offset_from_left) // (num_skill_buttons + 1)// (num_skill_buttons + 1)

        views_num_buttons_height = 3
        views_num_buttons_width = 3
        views_offset_from_left = action_screen_width
        views_offset_from_top = map_offset_from_top + map_height
        views_width = (self.screen_width - action_screen_width)
        views_height = (self.screen_height - map_offset_from_top - map_height)
        views_button_width = (self.screen_width - action_screen_width) // (views_num_buttons_width + 1)
        views_button_height = (self.screen_height - map_offset_from_top - map_height) // (views_num_buttons_height + 1)
        views_button_offset_from_each_other_height = (self.screen_height - map_offset_from_top - map_height) // (
                    views_num_buttons_height + 1) // (views_num_buttons_height + 1)
        views_button_offset_from_each_other_width = (self.screen_width -action_screen_width) // (
                views_num_buttons_width + 1) // (views_num_buttons_width + 1)

        # Writing messages
        text_box = ui.MessageBox(
            pygame.Rect((message_offset_from_left, message_offset_from_top),
                                      (message_width, message_height)),
            manager=self.uiManager,
            loop=loop)

        #Map box
        self.draw_empty_box(map_offset_from_left,
                            map_offset_from_top,
                            map_width, map_height)
        
        #Depth
        depth_label = ui.DepthDisplay(pygame.Rect((map_offset_from_left, map_offset_from_top),
                                                                (map_message_width, map_message_height)),
                                    manager=self.uiManager,
                                    loop=loop)
        
        stat_box = ui.StatBox(
            pygame.Rect((stats_offset_from_left, stats_offset_from_top), (stats_width, stats_height)),
            self.uiManager,
            player
        )

        button_num_height = 0
        button_num_width = 0
        self.draw_empty_box(views_offset_from_left,
                               views_offset_from_top,
                              views_width, views_height)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="(I)nventory",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "i"
        self.buttons.add(button, "i")

        button_num_height += 1
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="(E)quip",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "e"
        self.buttons.add(button, "e")

        button_num_height += 1
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="Rest(z)",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "z"
        self.buttons.add(button, "z")

        button_num_height = 0
        button_num_width += 1
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="(Q)uaff",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "q"
        self.buttons.add(button, "q")

        button_num_height += 1
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="(R)ead",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "r"
        self.buttons.add(button, "r")

        button_num_height += 1
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="Aut(o)explore",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "o"
        self.buttons.add(button, "o")

        button_num_height = 0
        button_num_width += 1
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="Pause(esc)",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "esc"
        self.buttons.add(button, "esc")

        button_num_height += 1
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="(S)tairs",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "s"
        self.buttons.add(button, "s")

        button_num_height += 1
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((
                                        views_offset_from_left + views_button_offset_from_each_other_width+ (views_button_offset_from_each_other_width + views_button_width) * button_num_width,
                                        views_offset_from_top + views_button_offset_from_each_other_height+ (views_button_offset_from_each_other_height + views_button_height) * button_num_height),
                                        (views_button_width, views_button_height)),
            text="(G)rab",
            manager=self.uiManager,
                    starting_height=800)
        button.action = "g"
        self.buttons.add(button, "g")

    #if target_to_display != None:
    #    clear_target = self.draw_examine_window(target_to_display, tileDict, floormap, monster_map, monsterID, item_ID, player)
    #    if clear_target:
    #        target_to_display = None

        num_skill = len(player.character.skills)
        if num_skill == 0:
            self.draw_empty_box(skill_bar_offset_from_left,
                                skill_bar_offset_from_top,
                                skill_bar_width, skill_bar_height)
        else:
            self.draw_empty_box(skill_bar_offset_from_left,
                                skill_bar_offset_from_top,
                                skill_bar_width, skill_bar_height)
            for i, skill in enumerate(player.character.skills):
                img1 = pygame.transform.scale(tileDict.tiles[skill.render_tag],
                                                    (skill_button_width, skill_button_height))
                img2 = pygame.transform.scale(tileDict.tiles[-skill.render_tag],
                                                    (skill_button_width, skill_button_height))
                button = ui.SkillButton(
                    rect=pygame.Rect((
                                                skill_bar_offset_from_left + skill_button_offset_from_each_other_width +(skill_button_offset_from_each_other_width + skill_button_width) * i,
                                                skill_button_offset_from_top),
                                                (skill_button_width, skill_button_height)),
                    manager=self.uiManager,
                    player=player,
                    index=i,
                    img1=img1,
                    img2=img2,
                    loop=loop,
                    object_id='#skill_button')
                button.action = chr(ord("1") + i)
                # self.draw_on_button(button, img, chr(ord("1") + i), (skill_button_width, skill_button_height), shrink=True,
                #                     offset_factor=10, text_offset=(12, (0.6)))
                self.buttons.add(button, chr(ord("1") + i))
        

        healthBar = ui.HealthBar(pygame.Rect((stats_offset_from_left + 70, stats_offset_from_top + 12), (stats_width//3, stats_height//12)), self.uiManager, player)
        manaBar = ui.ManaBar(pygame.Rect((stats_offset_from_left + 70, stats_offset_from_top + 38), (stats_width//3, stats_height//12)), self.uiManager, player)

    def update_display(self, loop):
        self.win.fill((0,0,0))

        floormap = loop.generator.tile_map
        tileDict = loop.tileDict
        monsterID = loop.monster_dict
        item_ID = loop.item_dict
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

        for key in monsterID.subjects:
            monster = monsterID.get_subject(key)
            if (monster.x >= self.x_start and monster.x < self.x_end and monster.y >= self.y_start and monster.y < self.y_end):
                if floormap.track_map[monster.x][monster.y].visible:
                    monster_tile = tileDict.tile_string(monster.render_tag)
                    self.win.blit(monster_tile, (self.textSize*(monster.x - self.x_start), self.textSize*(monster.y - self.y_start)))

        #Draw base character depending on armor state
        if (player.character.main_armor == None):
            self.win.blit(tileDict.tile_string(200), (self.r_x * self.textSize, self.r_y * self.textSize)) # DONG MODE ENGAGED
        else:
            self.win.blit(tileDict.tile_string(-200), (self.r_x * self.textSize, self.r_y * self.textSize))

        #Draw items on top
        if player.character.boots != None:
            self.win.blit(tileDict.tile_string(201), (self.r_x * self.textSize, self.r_y * self.textSize))
        if player.character.gloves != None:
            self.win.blit(tileDict.tile_string(202), (self.r_x * self.textSize, self.r_y * self.textSize))
        if player.character.helmet != None:
            self.win.blit(tileDict.tile_string(203), (self.r_x * self.textSize, self.r_y * self.textSize))
        if player.character.main_armor != None:
            self.win.blit(tileDict.tile_string(204), (self.r_x * self.textSize, self.r_y * self.textSize))

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
                            pygame.draw.rect(self.win, (200, 0, 0),
                                             pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                         map_offset_from_top + map_tile_size * (y - y_map_start),
                                                         map_tile_size, map_tile_size))
                        elif not item_map.get_passable(x,y):
                            pygame.draw.rect(self.win, (0, 200, 0),
                                             pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                         map_offset_from_top + map_tile_size * (y - y_map_start),
                                                         map_tile_size, map_tile_size))
                        elif isinstance(floormap.track_map[x][y], O.Stairs):
                            pygame.draw.rect(self.win, (0, 0, 200),
                                                 pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                             map_offset_from_top + map_tile_size * (y - y_map_start),
                                                             map_tile_size, map_tile_size))
                        else:
                            pygame.draw.rect(self.win, (200, 200, 200),
                                             pygame.Rect(map_offset_from_left + map_tile_size * (x - x_map_start),
                                                         map_offset_from_top + map_tile_size * (y - y_map_start),
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

    def draw_examine_window(self, target, tileDict, floormap, monster_map, monster_dict, item_dict, player):
        examine_offset_from_left = self.screen_width // 30
        examine_offset_from_top = self.screen_height // 20
        try:
            x, y = target
        except:
            return False
        if not floormap.track_map[x][y].visible:
            return
        black_screen = pygame.transform.scale(pygame.image.load("assets/black_screen.png"), (self.screen_width // 5, self.screen_height // 5))
        self.win.blit(black_screen, (0, 0))
        
        any_item_found = False
        
        nothing_at_target = True

        # find monster at target
        if not monster_map.get_passable(x,y):
            monster = monster_dict.get_subject(monster_map.locate(x,y))
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

    def create_inventory(self, player, equipment_type=None):   
        self.uiManager.clear_and_reset()
        self.win.fill((0,0,0))
        inventory_screen_width = self.screen_width // 2
        inventory_screen_height = self.screen_height
        inventory_offset_from_left = self.screen_width // 4
        inventory_offset_from_top = 0

        inventory_message_width = self.screen_width // 2
        inventory_message_height = self.screen_height // 10
        inventory_message_offset_from_left = self.screen_width // 4
        inventory_message_offset_from_top = self.screen_height // 30

        inventory_button_width = self.screen_width // 5
        inventory_button_height = self.screen_height // 30
        inventory_button_offset_from_left = self.screen_width *2 //5
        inventory_button_offset_from_top = self.screen_height // 10 + self.screen_height // 30+ self.screen_height // 30
        inventory_button_offset_from_each_other = self.screen_height // 100

        self.uiManager.clear_and_reset()
        pygame.draw.rect(self.win, (0,0,0), pygame.Rect(inventory_offset_from_left, inventory_offset_from_top, inventory_screen_width, inventory_screen_height))

        self.draw_escape_button(inventory_button_offset_from_left, inventory_button_offset_from_top, inventory_screen_width, inventory_screen_height)

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((inventory_message_offset_from_left, inventory_message_offset_from_top),
                                                              (inventory_message_width, inventory_message_height)),
                                    text="Inventory",
                                    manager=self.uiManager,
                                    object_id='#title_label')
        
        if equipment_type == "Enchantable":
            enchantable = player.character.get_enchantable()

        for i, item in enumerate(player.character.inventory):
            if equipment_type == "Enchantable" and item not in enchantable:
                continue
            elif equipment_type != None and equipment_type != "Enchantable" and item.equipment_type != equipment_type:
                continue
            if item.stackable:
                item_name = item.name + " (x" + str(item.stacks) + ")"
            else:
                item_name = item.name
            if item.can_be_levelled:
                item_level = item.level
                if item_level > 1:
                    item_name = item_name + " (+" + str(item_level - 1) + ")"
            if item.equipped:
                item_name = item_name + " (equipped)"
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((inventory_button_offset_from_left, inventory_button_offset_from_top + inventory_button_offset_from_each_other * i + inventory_button_height * i),
                                                              (inventory_button_width, inventory_button_height)),
                text= chr(ord("a") + i) + ". " + item_name,
                manager=self.uiManager)
            button.action = chr(ord("a") + i)
            self.buttons.add(button, chr(ord("a") + i))

        self.uiManager.draw_ui(self.win)
        return self.buttons     

    def update_inventory(self, player, equipment_type=None):
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)
    
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

    def create_equipment(self, player, tileMap):
        self.uiManager.clear_and_reset()
        self.win.fill((0,0,0))

        equipment_screen_width = self.screen_width // 3 * 2
        equipment_screen_height = self.screen_height
        equipment_offset_from_left = self.screen_width // 3
        equipment_offset_from_top = 0

        equipment_message_width = self.screen_width // 2
        equipment_message_height = self.screen_height // 10
        equipment_message_offset_from_left = self.screen_width // 4
        equipment_message_offset_from_top = self.screen_height // 30

        # 8 buttons, for helmet, armor, gloves, boots, ring 1, ring 2, weapon, shield
        # equipment is across three columns
        medium_button_width = self.screen_width // 8
        medium_button_height = self.screen_height // 5
        first_col_offset_from_left = self.screen_width // 4
        outer_cols_offset_from_top = self.screen_height // 5 * 2
        middle_col_offset_from_top = self.screen_height // 5
        small_button_width = self.screen_width // 16 - self.screen_width // 120
        small_button_height = self.screen_height // 8
        margin_between_buttons_height = self.screen_height // 30
        small_margin_between_buttons_width = self.screen_width // 60
        margin_between_buttons_width = self.screen_width // 30

        self.uiManager.clear_and_reset()
        pygame.draw.rect(self.win, (0,0,0), pygame.Rect(equipment_offset_from_left, equipment_offset_from_top, equipment_screen_width, equipment_screen_height))

        self.draw_escape_button(equipment_message_offset_from_left, equipment_message_offset_from_top, equipment_screen_width, equipment_screen_height)


        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((equipment_message_offset_from_left, equipment_message_offset_from_top),
                                                              (equipment_message_width, equipment_message_height)),
                                    text="Equipment",
                                    manager=self.uiManager,
                                    object_id='#title_label')

        # equipment_slots = ["shield", "ring", "ring", "helmet", "armor", "boots", "weapon", "gloves"]:
        if player.character.main_shield == None:
            available_slot = False
            for item in player.character.inventory:
                if item.equipment_type == "Shield":
                    available_slot = True
                    break
            if available_slot == True:
                pre_text = "change "
                img = pygame.transform.scale(tileMap.tiles[816],
                                             (medium_button_width, medium_button_height))
            else:
                pre_text = "no options "
                img = pygame.transform.scale(tileMap.tiles[806], (medium_button_width, medium_button_height))

        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.main_shield.render_tag], (medium_button_width, medium_button_height))
        button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((first_col_offset_from_left, 
                                                   outer_cols_offset_from_top),
                                                  (medium_button_width, medium_button_height)),
                        text = pre_text + "shield",
                        manager=self.uiManager,
                        object_id='#equipment_button')
        self.draw_on_button(button, img, "q", (medium_button_width, medium_button_height))
        button.action = 'q'

        if player.character.ring_1 == None:
            available_slot = False
            for item in player.character.inventory:
                if item.equipment_type == "Ring":
                    available_slot = True
                    break
            if available_slot == True:
                pre_text = "change "
                img = pygame.transform.scale(tileMap.tiles[817],
                                             (small_button_width, small_button_height))
            else:
                pre_text = "no options "
                img = pygame.transform.scale(tileMap.tiles[807], (small_button_width, small_button_height))

        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.ring_1.render_tag], (small_button_width, small_button_height))
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((first_col_offset_from_left, 
                                               outer_cols_offset_from_top + (medium_button_height + margin_between_buttons_height)),
                                               (small_button_width, small_button_height)),
                    text = "ring 1",
                    manager=self.uiManager,
                    object_id='#equipment_button')
        self.draw_on_button(button, img, "a", (small_button_width, small_button_height))
        button.action = 'a'

        if player.character.ring_2 == None:
            available_slot = False
            for item in player.character.inventory:
                if item.equipment_type == "Ring":
                    available_slot = True
                    break
            if available_slot == True:
                pre_text = "change "
                img = pygame.transform.scale(tileMap.tiles[817],
                                             (small_button_width, small_button_height))
            else:
                pre_text = "no options "
                img = pygame.transform.scale(tileMap.tiles[807], (small_button_width, small_button_height))
        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.ring_2.render_tag], (small_button_width, small_button_height))
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((first_col_offset_from_left + small_button_width + small_margin_between_buttons_width, 
                                               outer_cols_offset_from_top + (medium_button_height + margin_between_buttons_height)),
                                              (small_button_width, small_button_height)),
                    text = "ring 2",
                    manager=self.uiManager,
                    object_id='#equipment_button')
        self.draw_on_button(button, img, "z", (small_button_width, small_button_height))
        button.action = 'z'

        if player.character.helmet == None:
            available_slot = False
            for item in player.character.inventory:
                if item.equipment_type == "Helmet":
                    available_slot = True
                    break
            if available_slot == True:
                pre_text = "change "
                img = pygame.transform.scale(tileMap.tiles[814],
                                             (medium_button_width, medium_button_height))
            else:
                pre_text = "no options "
                img = pygame.transform.scale(tileMap.tiles[804], (medium_button_width, medium_button_height))

        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.helmet.render_tag], (medium_button_width, medium_button_height))
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((first_col_offset_from_left + medium_button_width + margin_between_buttons_width, 
                                               middle_col_offset_from_top),
                                               (medium_button_width, medium_button_height)),
                    text = pre_text + "helmet",
                    manager=self.uiManager,
                    object_id='#equipment_button')
        self.draw_on_button(button, img, "w", (medium_button_width, medium_button_height))
        button.action = 'w'

        if player.character.main_armor == None:
            available_slot = False
            for item in player.character.inventory:
                if item.equipment_type == "Body Armor":
                    available_slot = True
                    break
            if available_slot == True:
                pre_text = "change "
                img = pygame.transform.scale(tileMap.tiles[811],
                                             (medium_button_width, medium_button_height))
            else:
                pre_text = "no options "
                img = pygame.transform.scale(tileMap.tiles[801], (medium_button_width, medium_button_height))

        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.main_armor.render_tag], (medium_button_width, medium_button_height))
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((first_col_offset_from_left + medium_button_width + margin_between_buttons_width, 
                                               middle_col_offset_from_top + (medium_button_height + margin_between_buttons_height)),
                                               (medium_button_width, medium_button_height)),
                    text = pre_text + "armor",
                    manager=self.uiManager,
                    object_id='#equipment_button')
        
        self.draw_on_button(button, img, "s", (medium_button_width, medium_button_height))
        button.action = 's'

        if player.character.boots == None:
            available_slot = False
            for item in player.character.inventory:
                if item.equipment_type == "Boots":
                    available_slot = True
                    break
            if available_slot == True:
                pre_text = "change "
                img = pygame.transform.scale(tileMap.tiles[812],
                                             (medium_button_width, medium_button_height))
            else:
                pre_text = "no options "
                img = pygame.transform.scale(tileMap.tiles[802], (medium_button_width, medium_button_height))

        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.boots.render_tag], (medium_button_width, medium_button_height))
        
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((first_col_offset_from_left + medium_button_width + margin_between_buttons_width, 
                                               middle_col_offset_from_top + 2 * (medium_button_height + margin_between_buttons_height)),
                                               (medium_button_width, medium_button_height)),
                    text = pre_text + "boots",
                    manager=self.uiManager,
                    object_id='#equipment_button')

        self.draw_on_button(button, img, "x", (medium_button_width, medium_button_height))
        button.action = 'x'

        if player.character.main_weapon == None:
            available_slot = False
            for item in player.character.inventory:
                if item.equipment_type== "Weapon":
                    available_slot = True
                    break
            if available_slot == True:
                pre_text = "change "
                img = pygame.transform.scale(tileMap.tiles[815],
                                             (medium_button_width, medium_button_height))
            else:
                pre_text = "no options "
                img = pygame.transform.scale(tileMap.tiles[805], (medium_button_width, medium_button_height))

        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.main_weapon.render_tag], (medium_button_width, medium_button_height))
        
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((first_col_offset_from_left + 2 * (medium_button_width + margin_between_buttons_width), 
                                               outer_cols_offset_from_top),
                                               (medium_button_width, medium_button_height)),
                    text = pre_text + "weapon",
                    manager=self.uiManager,
                    object_id='#equipment_button')
        
        self.draw_on_button(button, img, "d", (medium_button_width, medium_button_height), shrink=True)
        button.action = 'd'

        if player.character.gloves == None:
            available_slot = False
            for item in player.character.inventory:
                if item.equipment_type == "Gloves":
                    available_slot = True
                    break
            if available_slot == True:
                pre_text = "change "
                img = pygame.transform.scale(tileMap.tiles[813],
                                             (medium_button_width, medium_button_height))
            else:
                pre_text = "no options "
                img = pygame.transform.scale(tileMap.tiles[803], (medium_button_width, medium_button_height))

        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.gloves.render_tag], (medium_button_width, medium_button_height))
        
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((first_col_offset_from_left + 2 * (medium_button_width + margin_between_buttons_width), 
                                               outer_cols_offset_from_top + (medium_button_height + margin_between_buttons_height)),
                                               (medium_button_width, medium_button_height)),
                    text = pre_text + "gloves",
                    manager=self.uiManager,
                    object_id='#equipment_button')
        
        self.draw_on_button(button, img, "c", (medium_button_width, medium_button_height))
        button.action = 'c'

        self.draw_character_stats(player, 
                                  margin_from_left = first_col_offset_from_left + 3 * (medium_button_width + margin_between_buttons_width),
                                  margin_from_top = middle_col_offset_from_top,
                                  width = medium_button_width * 2,
                                  height = medium_button_height * 3 + margin_between_buttons_height * 2)       
        self.uiManager.draw_ui(self.win)

    def update_equipment(self, player, tileMap):       
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)

    def update_victory_screen(self):       
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)

    def refresh_screen(self):
        self.uiManager.clear_and_reset()

    def create_pause_screen(self):
        self.uiManager.clear_and_reset()
        pause_screen_width = self.screen_width // 3
        pause_screen_height = self.screen_height // 2
        pause_offset_from_left = (self.screen_width - pause_screen_width) // 2
        pause_offset_from_top = self.screen_height // 4

        pause_num_buttons_height = 4
        pause_button_width = pause_screen_width * 9 // 10
        pause_button_height = (pause_screen_height) // (pause_num_buttons_height + 1)
        pause_button_offset_from_each_other_height = (pause_screen_height) // (
                pause_num_buttons_height + 1) // (pause_num_buttons_height + 1)
        pause_button_offset_from_top = pause_offset_from_top
        pause_button_offset_from_left = pause_offset_from_left + (pause_screen_width- pause_button_width) //2

        self.draw_empty_box(pause_offset_from_left, pause_offset_from_top, pause_screen_width,
                            pause_screen_height)

        button_num = 0
        unpause = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height+
                                               (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
                                               pause_button_width, pause_button_height)),
                    text = "Unpause",
                    manager=self.uiManager,
                    starting_height=1000) #Important! Need this to be high so it's above the panel.
        unpause.action = "esc"

        button_num += 1
        menu = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height+
                                               (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
                                               pause_button_width, pause_button_height)),
                    text = "Return to (m)enu",
                    manager=self.uiManager,
                    starting_height=1000) #Important! Need this to be high so it's above the panel.
        menu.action = 'm'

        button_num += 1
        save = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height+
                                               (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
                                               pause_button_width, pause_button_height)),
                    text = "(S)ave",
                    manager=self.uiManager,
                    starting_height=1000)
        save.action = 's'

        button_num += 1
        quit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height+
                                       (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
                                       pause_button_width, pause_button_height)),
            text="(Q)uit",
            manager=self.uiManager,
            starting_height=1000)
        quit.action = 'q'


    def update_pause_screen(self):
        self.uiManager.draw_ui(self.win)

    def stat_text(self, entity, stat):
        if entity.character.rounded():
            return str(stat) + " (+" + str(int(stat * entity.character.round_bonus()) - stat) + ")"
        else:
            return str(stat)
        
    def round_text(self, entity):
        if entity.character.rounded():
            return "You feel the dungeon enhancing your well-rounded stats.<br><br>"
        else:
            return "<br>"

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
                        "Intelligence: " + self.stat_text(player, player.character.intelligence) + "<br>" + \
                        self.round_text(player) + "<br>"
                        "Health: " + str(player.character.health) + " / " + str(player.character.max_health) + "<br>"
                        "Mana: " + str(player.character.mana) + " / " + str(player.character.max_mana) + "<br>"
                        "<br>"
                        "Damage: " + str(player.character.get_damage_min()) + " - " + str(player.character.get_damage_max()) + " (" + strength_modifier + ") <br>"
                        "Defense: " + str(player.character.armor) + " (+" + str(player.character.endurance // 3) + ") <br>"
                        "Movement Delay: " + str(player.character.move_cost) + "<br>"
                        "Skill Damage Bonus: " + str(player.character.skill_damage_increase()) + "<br>"
                        "Effect Duration Bonus: " + str(player.character.skill_duration_increase()) + "<br>"
                        "<br>Known Skills:<br>"
                        + "<br>".join([str(i + 1) + ". " + skill.name for i, skill in enumerate(player.character.skills)])
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


    def update_main(self):
    #Main Screen
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)
        image_size = 100
        image_offset_from_left = (self.screen_width - image_size) // 2
        image_offset_from_top = self.screen_height // 2
        self.win.blit(pygame.transform.scale(pygame.image.load('assets/yendorb_deactivated.png'),(image_size,image_size)), (image_offset_from_left, image_offset_from_top))
        font = pygame.font.Font('freesansbold.ttf', 12)

    def update_entity(self, entity, tileDict, player, item_screen = True, create = False):
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

        buttons = Buttons()
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
            show = True
            if item.equipable:
                if item.equipped:
                    pretext = "Unequip"
                    action = "u"
                    if item.cursed:
                        show = False
                else:
                    pretext = "Equip"
                    action = "e"
            elif item.consumeable and item.equipment_type == "Potiorb":
                pretext = "Quaff"
                action = "q"
            elif item.consumeable and item.equipment_type == "Scrorb":
                pretext = "Read"
                action = "r"
            if create == True:
                if show:
                    button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((entity_button_offset_from_left, entity_button_offset_from_top),
                                                  (entity_button_width, entity_button_height)),
                        text=pretext,
                        manager=self.uiManager)
                    button.action = action
                    buttons.add(button, pretext)
                buttons_drawn += 1

                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((entity_button_offset_from_left + (entity_button_width + entity_button_offset_from_each_other) * buttons_drawn, entity_button_offset_from_top),
                                              (entity_button_width, entity_button_height)),
                    text='Drop',
                    manager=self.uiManager)
                button.action = "d"
                buttons.add(button, "Drop")
                buttons_drawn += 1


        entity_text = ""
        entity_text += entity.description  + "<br><br>"

        if isinstance(entity,O.Item):
            item = entity
            if isinstance(entity, I.Equipment):
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
                #if isinstance(item, I.Armor):
                    #entity_text += "Armor: " + str(item.armor) + "<br>"
                if isinstance(item, I.Weapon):
                    entity_text += "Damage: " + str(item.damage_min + player.character.base_damage) + " - " + str(item.damage_max + player.character.base_damage) + "<br>"
                    if item.on_hit:
                        entity_text += "On hit: " + item.on_hit_description + "<br>"

                stats = item.stats.GetStatsForLevel(item.level)
                if stats[2]> 0:
                    entity_text += "Intelligence: +" + str(stats[2]) + "<br>"
                elif stats[2]<0:
                    entity_text += "Intelligence: -" + str(stats[2]) + "<br>"
                if stats[0] > 0:
                    entity_text += "Strength: +" + str(stats[0]) + "<br>"
                elif stats[0]<0:
                    entity_text += "Strength: +" + str(stats[0]) + "<br>"
                if stats[1] > 0:
                    entity_text += "Dexterity: +" + str(stats[1]) + "<br>"
                elif stats[1]<0:
                    entity_text += "Dexterity: +" + str(stats[1]) + "<br>"
                if stats[3] > 0:
                    entity_text += "Endurance: +" + str(stats[3]) + "<br>"
                elif stats[3]<0:
                    entity_text += "Endurance: +" + str(stats[3]) + "<br>"
                if stats[4] > 0:
                    entity_text += "Armor: +" + str(stats[4]) + "<br>"
                elif stats[4]<0:
                    entity_text += "Armor: -" + str(stats[4]) + "<br>"
            elif isinstance(entity, I.Potion) or isinstance(entity, I.Ring):
                entity_text += "Effect: " + str(entity.action_description) + "<br>"
            if item.attached_skill_exists:
                entity_text += "Grants skill: " + item.get_attached_skill_description() + "<br>"

        if isinstance(entity, M.Monster):
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
        return self.buttons
    
    def draw_single_tile(self, x, y, floormap, tileDict):
        if (x < 0 or x >= floormap.width or y < 0 or y >= floormap.height):
            pass
        elif floormap.track_map[x][y].seen == False:
            pass
        elif floormap.track_map[x][y].visible == True:
            tag = tileDict.tile_string(floormap.get_tag(x, y))
            self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))
        else:
            tag = tileDict.tile_string(floormap.track_map[x][y].shaded_render_tag)
            self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))

    def update_examine(self, target, loop):
        x, y = target
        tag = loop.tileDict.tile_string(901)
        self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))

    def update_level_up(self, loop):
        line_to_outline = loop.current_stat
        player = loop.player
        entity_screen_width = self.screen_width // 2
        entity_screen_height = self.screen_height // 2
        entity_offset_from_left = self.screen_width // 4
        entity_offset_from_top = self.screen_height // 4

        entity_message_width = entity_screen_width // 2
        entity_message_height = entity_screen_height // 10
        entity_message_offset_from_left = entity_offset_from_left + entity_screen_width // 4
        entity_message_offset_from_top = entity_offset_from_top + entity_screen_height // 30

        border_width = 8
        border_height = 8

        pygame.draw.rect(self.win, (0, 0, 0), pygame.Rect(entity_offset_from_left - border_width // 2, entity_offset_from_top - border_height // 2, entity_screen_width + border_width, entity_screen_height+border_height))
        pygame.draw.rect(self.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))
        pygame.draw.rect(self.win, (0, 0, 0), pygame.Rect((0,0),(self.screen_width // 2,40)))

        stat_line_offset_from_left = entity_offset_from_left + entity_screen_width // 6
        stat_line_offset_from_top = entity_offset_from_top + entity_screen_height // 4
        stat_line_width = entity_screen_width // 3 * 2
        stat_line_height = entity_screen_height // 10
        stat_line_offset_from_each_other = entity_screen_height // 30

        stat_change_button_width = entity_screen_width // 30
        stat_change_button_height = entity_screen_height // 20
        stat_change_button_offset_from_left = entity_offset_from_left + entity_screen_width // 24
        stat_change_button_offset_from_top = stat_line_offset_from_top + (stat_change_button_height // 2)
        stat_change_button_offset_from_each_other_height = stat_line_offset_from_each_other
        stat_change_offset_from_each_other_width = stat_change_button_width
        stat_change_text_offset_left = stat_change_button_offset_from_left + stat_change_button_width + (stat_change_button_width // 8)
        
        stat_outline_offset_from_left = stat_change_button_offset_from_left - (stat_change_button_width // 2)
        stat_outline_offset_from_top = stat_line_offset_from_top - entity_screen_height // 30
        stat_outline_width = stat_line_width + entity_screen_width // 5
        stat_outline_height = stat_line_height + entity_screen_height // 20

        for i in range(0, 4):
            if i == loop.current_stat:
                color = (0, 0, 0)
            else:
                color = (112, 128, 144)
            pygame.draw.rect(self.win, color, pygame.Rect(stat_outline_offset_from_left, 
                                                          stat_outline_offset_from_top + i * (stat_line_height + stat_line_offset_from_each_other), 
                                                          stat_outline_width, 
                                                          stat_outline_height))

        self.uiManager.draw_ui(self.win)

    def create_victory_screen(self, loop):
        self.uiManager.clear_and_reset()
        player = loop.player
        tileDict = loop.tileDict
        entity_screen_width = self.screen_width // 2
        entity_screen_height = self.screen_height // 2
        entity_offset_from_left = self.screen_width // 4
        entity_offset_from_top = self.screen_height // 4

        entity_message_width = entity_screen_width // 2
        entity_message_height = entity_screen_height // 5
        entity_message_offset_from_left = entity_offset_from_left + entity_screen_width // 4
        entity_message_offset_from_top = entity_offset_from_top + entity_screen_height // 30

        border_width = 8
        border_height = 8
        pygame.draw.rect(self.win, (0, 0, 0), pygame.Rect(entity_offset_from_left - border_width // 2, entity_offset_from_top - border_height // 2, entity_screen_width + border_width, entity_screen_height+border_height))
        pygame.draw.rect(self.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))
        
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                        (entity_message_width, entity_message_height)),
            text="Victory!",
            manager=self.uiManager,
            object_id='#title_label')
        
        html_text = "You have defeated the dungeon and achieved maximum orb-iness!<br><br>"
        html_text += "You reached level " + str(player.level) + ".<br>"
        html_text += "You killed " + str(player.kill_count) + " monsters along the way.<br>"


        pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((entity_offset_from_left + entity_screen_width // 20, entity_offset_from_top + entity_screen_height // 4),
                                    (entity_screen_width * 9 // 10, entity_screen_height * 3 // 5)),
            html_text = html_text,
            manager=self.uiManager)

    def create_level_up(self, loop):
        player = loop.player
        tileDict = loop.tileDict
        entity_screen_width = self.screen_width // 2
        entity_screen_height = self.screen_height // 2
        entity_offset_from_left = self.screen_width // 4
        entity_offset_from_top = self.screen_height // 4

        entity_message_width = entity_screen_width // 2
        entity_message_height = entity_screen_height // 10
        entity_message_offset_from_left = entity_offset_from_left + entity_screen_width // 4
        entity_message_offset_from_top = entity_offset_from_top + entity_screen_height // 30

        border_width = 8
        border_height = 8
        pygame.draw.rect(self.win, (0, 0, 0), pygame.Rect(entity_offset_from_left - border_width // 2, entity_offset_from_top - border_height // 2, entity_screen_width + border_width, entity_screen_height+border_height))
        pygame.draw.rect(self.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))
        
        stat_line_offset_from_left = entity_offset_from_left + entity_screen_width // 6
        stat_line_offset_from_top = entity_offset_from_top + entity_screen_height // 4
        stat_line_width = entity_screen_width // 3 * 2
        stat_line_height = entity_screen_height // 10
        stat_line_offset_from_each_other = entity_screen_height // 30

        stat_change_button_width = entity_screen_width // 30
        stat_change_button_height = entity_screen_height // 20
        stat_change_button_offset_from_left = entity_offset_from_left + entity_screen_width // 24
        stat_change_button_offset_from_top = stat_line_offset_from_top + (stat_change_button_height // 2)
        stat_change_button_offset_from_each_other_height = stat_line_offset_from_each_other
        stat_change_offset_from_each_other_width = stat_change_button_width
        stat_change_text_offset_left = stat_change_button_offset_from_left + stat_change_button_width + (stat_change_button_width // 8)

        stat_outline_offset_from_left = stat_change_button_offset_from_left - (stat_change_button_width // 2)
        stat_outline_offset_from_top = stat_line_offset_from_top - entity_screen_height // 30
        stat_outline_width = stat_line_width + entity_screen_width // 5
        stat_outline_height = stat_line_height + entity_screen_height // 20

        for i in range(4):
            stat_change_left = pygame.transform.scale(tileDict.tiles[51],
                                        (stat_change_button_width, stat_change_button_height))
            stat_change_left_dark = pygame.transform.scale(tileDict.tiles[-51],
                                        (stat_change_button_width, stat_change_button_height))
            stat_change_right = pygame.transform.scale(tileDict.tiles[50],
                                        (stat_change_button_width, stat_change_button_height))
            stat_change_right_dark = pygame.transform.scale(tileDict.tiles[-50],
                                        (stat_change_button_width, stat_change_button_height))
            
            button = ui.StatDownButton(
                rect=pygame.Rect((stat_change_button_offset_from_left, 
                                  stat_change_button_offset_from_top + i * (stat_line_height + stat_change_button_offset_from_each_other_height)),
                                 (stat_change_button_width, stat_change_button_height)),
                manager=self.uiManager,
                player=player,
                img1=stat_change_left,
                img2=stat_change_left_dark,
                index=i)
            
            button.action = "left"
            button.row = i
            
            # self.draw_on_button(button, stat_change_left, letter = "", button_size=(stat_change_button_width, stat_change_button_height), shrink=False, offset_factor=12, text_offset=(15, 0.8))

            ui.StatChangeText(
                rect=pygame.Rect(
                    (stat_change_text_offset_left, 
                    stat_change_button_offset_from_top + i * (stat_line_height + stat_change_button_offset_from_each_other_height)),
                    (stat_change_button_width, stat_change_button_height)),
                manager=self.uiManager,
                player=player,
                index=i)
            
            button_2 = ui.StatUpButton(
                rect=pygame.Rect((stat_change_button_offset_from_left + stat_change_button_width + stat_change_offset_from_each_other_width, 
                                           stat_change_button_offset_from_top + i * (stat_line_height + stat_change_button_offset_from_each_other_height)),
                                          (stat_change_button_width, stat_change_button_height)),
                manager=self.uiManager,
                player=player,
                img1=stat_change_right,
                img2=stat_change_right_dark,
                index=i)
            
            # self.draw_on_button(button_2, stat_change_right, letter = "", button_size=(stat_change_button_width, stat_change_button_height), shrink=False, offset_factor=12, text_offset=(15, 0.8))
            
            button_2.action = "right"
            button_2.row = i

        self.draw_escape_button(entity_message_offset_from_left, entity_message_offset_from_top, stat_line_width + stat_change_offset_from_each_other_width, entity_screen_height)


        #stat_line_outline_offset_from_left = stat_change_button_offset_from_left - entity_screen_width // 24
        #stat_line_outline = pygame.Rect((stat_change_button_offset_from_left, stat_line_offset_from_top), (stat_line_width, stat_line_height * 4 + stat_line_offset_from_each_other * 3))
        ui.LevelUpHeader(
            rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top), (entity_message_width, entity_message_height)),
            manager=self.uiManager,
            player=player)

        # strength
        description = "Str (currently " + str(player.character.strength) + ") - increase your damage and wear heavier armor"
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((stat_line_offset_from_left, stat_line_offset_from_top), 
                                      (stat_line_width, stat_line_height)),
            text=description,
            manager=self.uiManager,
            object_id='#stat_label')
        
        # dexterity
        description = "Dex (currently " + str(player.character.dexterity) + ") - increase your dodge chance and action speed"
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((stat_line_offset_from_left, stat_line_offset_from_top + stat_line_height + stat_line_offset_from_each_other), 
                                      (stat_line_width, stat_line_height)),
            text=description,
            manager=self.uiManager,
            object_id='#stat_label')
        
        # endurance
        description = "En (currently " + str(player.character.endurance) + ") - increase your defense and your health growth"
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((stat_line_offset_from_left, stat_line_offset_from_top + 2 * (stat_line_height + stat_line_offset_from_each_other)), 
                                      (stat_line_width, stat_line_height)),
            text=description,
            manager=self.uiManager,
            object_id='#stat_label')
        
        # intelligence
        description = "Int (currently " + str(player.character.intelligence) + ") - increase your mana growth and skill damage"
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((stat_line_offset_from_left, stat_line_offset_from_top + 3 * (stat_line_height + stat_line_offset_from_each_other)), 
                                      (stat_line_width, stat_line_height)),
            text=description,
            manager=self.uiManager,
            object_id='#stat_label')
        
        ui.RoundedText(
            rect=pygame.Rect((stat_change_button_offset_from_left, stat_line_offset_from_top + 4 * (stat_line_height + stat_line_offset_from_each_other)), 
                                      (stat_outline_width, stat_line_height)),
            manager=self.uiManager,
            player=player)
        
        # confirmation_button
        confirmation_button_width = entity_message_width // 3
        confirmation_button_height = stat_change_button_height * 2
        confirmation_button_offset_from_left = stat_outline_width + stat_outline_offset_from_left - confirmation_button_width
        confirmation_button_offset_from_top = stat_line_offset_from_top + 4 * (stat_line_height + stat_line_offset_from_each_other) + stat_line_height + (stat_line_offset_from_each_other // 4 * 3)

        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((confirmation_button_offset_from_left, confirmation_button_offset_from_top),
                                      (confirmation_button_width, confirmation_button_height)),
            text="Confirm",
            manager=self.uiManager)
        button.action = "return"
        button.row = None


    def update_ui(self):
        deltaTime = self.clock.tick() / 1000
        self.uiManager.update(deltaTime)


    def create_main_screen(self):
        num_buttons = 4
        button_width = self.screen_width // (num_buttons + 1)
        button_height = self.screen_height // 8
        button_offset_from_bottom = self.screen_height * 95 // 100 - button_height
        button_offset_from_each_other = self.screen_width // (num_buttons + 1) // (num_buttons + 1)
        button_offset_from_left = self.screen_width // (num_buttons + 1) // (num_buttons + 1) #Should be (1 - 3* button_width - 2 * button_offset from each other) / 2

        message_width = self.screen_width * 5//6
        message_height = self.screen_height * 2//3
        message_offset_from_left = self.screen_width // 12
        message_offset_from_top = self.screen_height // 12


        self.uiManager.clear_and_reset()
        buttons = Buttons()
        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_offset_from_left, button_offset_from_bottom), (button_width, button_height)),
                                                 text='Play',
                                                 manager=self.uiManager)
        button.action = "return"
        buttons.add(button, "play")



        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_offset_from_left + button_width+ button_offset_from_each_other, button_offset_from_bottom), (button_width, button_height)),
                                                 text='Load',
                                                 manager=self.uiManager)
        button.action = "l"
        buttons.add(button, "load")

        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (button_offset_from_left + button_width * 2 + button_offset_from_each_other * 2, button_offset_from_bottom),
            (button_width, button_height)),
                                              text='Help',
                                              manager=self.uiManager)
        button.action = "h"
        buttons.add(button, "help")

        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_offset_from_left+ button_width * 3 + button_offset_from_each_other * 3, button_offset_from_bottom), (button_width, button_height)),
                                                 text='Quit',
                                                 manager=self.uiManager)
        button.action = "esc"
        buttons.add(button, "quit")

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((message_offset_from_left, message_offset_from_top), (message_width, message_height)),
                                    text="Orbworld: The Orb of Destiny",
                                    manager=self.uiManager,
                                    object_id='#title_label')

        return buttons

    def create_help_screen(self):
        button_width = self.screen_width // 4
        button_height = self.screen_height // 8
        button_offset_from_bottom = self.screen_height * 95 // 100 - button_height
        button_offset_from_left = (self.screen_width -button_width) // 2

        message_width = self.screen_width // 2
        message_height = self.screen_height // 2
        message_offset_from_left = self.screen_width // 4
        message_offset_from_top = self.screen_height // 4

        title_width = self.screen_width // 2
        title_height = self.screen_height // 10
        title_offset_from_left = self.screen_width // 4
        title_offset_from_top = self.screen_height // 10


        self.uiManager.clear_and_reset()
        buttons = Buttons()

        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_offset_from_left, button_offset_from_bottom), (button_width, button_height)),
                                                 text='Return to Main Menu',
                                                 manager=self.uiManager)
        button.action = "esc"
        buttons.add(button, "Return to Main Menu")

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((title_offset_from_left, title_offset_from_top), (title_width, title_height)),
                                    text="Action Shortcuts",
                                   manager=self.uiManager,
                                    object_id='#title_label')

        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((message_offset_from_left,message_offset_from_top), (message_width, message_height)),
            html_text = "Action Screen: <br>" +
            "Inventory: i || Equipments: e || Potions: q || Scrolls: r <br>" +
            "Autoexplore: o || Find Stairs: s || Wait: . || Rest: z <br>" +
            "Examine: x || Save: / || Pause: esc <br>" +
            "Grab: g || Allocate stats: l <br>" +
            "Downstairs: > || Upstairs: < <br>" +
            "Skills: 1-8 <br>" +
            "Up / Down / Left / Right --> Arrow keys <br>" +
            "Up - Left / Up - Right / Down - Left / Down - Right --> y / u / n / b <br>"
            ,
            manager=self.uiManager
        )

        return buttons

    def update_help(self):
    #Main Screen
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)

    def create_death_screen(self):
        self.uiManager.clear_and_reset()

        message_width = self.screen_width // 4
        message_height = self.screen_height // 5
        message_offset_from_left = (self.screen_width - message_width) // 2
        message_offset_from_top = (self.screen_height - message_height) // 2

        button_width = self.screen_width // 8
        button_height = self.screen_height // 12
        button_offset_from_top = message_offset_from_top + message_height - button_height - 10
        button_offset_from_left = (self.screen_width -button_width) // 2

        #self.draw_empty_box(message_offset_from_left, message_offset_from_top, message_width, message_height)

        button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_offset_from_left, button_offset_from_top), (button_width, button_height)),
                                                 text='Return to Main Menu',
                                                 manager=self.uiManager,
                                                 starting_height=10000)
        button.action = "esc"

        text_box = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((button_offset_from_left, message_offset_from_top), (button_width, button_height)),
            text = "You have died.",
            manager=self.uiManager
        )

    def update_death_screen(self):
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)