import pygame
import pygame_gui
import items as I
import ui

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
        self.win = pygame.display.set_mode((width, height))
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

    def update_display(self, colorDict, floormap, tileDict, monsterID, item_ID, monster_map, player, messages, target_to_display):
        if self.colorDict == None:
            self.colorDict = colorDict
        self.uiManager.clear_and_reset()
        self.win.fill(colorDict.getColor("black"))
        r_x = self.textWidth // 2
        r_y = self.textHeight // 2

        self.x_start = player.x - r_x
        self.x_end = player.x + r_x
        self.y_start = player.y - r_y
        self.y_end = player.y + r_y

        for x in range(self.x_start, self.x_end):
            for y in range(self.y_start, self.y_end):
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

        self.win.blit(tileDict.tile_string(200), (r_x * self.textSize, r_y * self.textSize))

        black_screen = pygame.transform.scale(pygame.image.load("assets/black_screen.png"), (self.screen_width // 5, self.screen_height // 5))
        self.win.blit(black_screen, (0, self.screen_height // 5 * 4))
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render("Health: " + str(player.character.health) + "/" + str(player.character.max_health), True, (255, 255, 255))
        self.win.blit(text, (0, self.screen_height // 100 * 80))
        text = font.render("Mana: " + str(player.character.mana) + "/" + str(player.character.max_mana), True, (255, 255, 255))
        self.win.blit(text, (0, self.screen_height // 100 * 83))
        status = self.get_status_text(player)
        text = font.render("Status: " + status, True, (255, 255, 255))
        self.win.blit(text, (0, self.screen_height // 100 * 86))
        text = font.render("Experience: " + str(player.experience) + " / " + str(player.experience_to_next_level), True, (255, 255, 255))
        self.win.blit(text, (0, self.screen_height // 100 * 89))
        text = font.render("Level: " + str(player.level), True, (255, 255, 255))
        self.win.blit(text, (0, self.screen_height // 100 * 92))

        self.write_messages(messages)

        if target_to_display != None:
            clear_target = self.draw_examine_window(target_to_display, tileDict, floormap, monster_map, monsterID, item_ID, player)
            if clear_target:
                target_to_display = None
        self.uiManager.draw_ui(self.win)

    def write_messages(self, messages):
        font = pygame.font.Font('freesansbold.ttf', 12)
        for i, message in enumerate(messages):
            text = font.render(message, True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 100 * 12, self.screen_height // 100 * (85 + i * 3)))

    def get_status_text(self, entity):
        status = "Healthy"
        if entity.character.health < entity.character.max_health // 3 * 2:
            status = "Wounded"
        effects = entity.character.status_effects
        for effect in effects:
            status += ", " + effect.description()
        return status

    def draw_examine_window(self, target, tileDict, floormap, monster_map, monster_dict, item_dict, player):
        x, y = target
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
            self.win.blit(tag, (self.screen_width  // 10, self.screen_height // 10))
            font = pygame.font.Font('freesansbold.ttf', 12)

            # name
            text = font.render(monster.name, True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 50))
            
            # health
            text = font.render("Health: " + str(monster.character.health) + "/" + str(monster.character.max_health), True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 65))
                
            # status
            status = self.get_status_text(monster)
            text = font.render("Status: " + status, True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 80))

            # description
            description = monster.description
            text = font.render(description, True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 95))
            nothing_at_target = False
        else:
            # find item at target
            for key in item_dict.subjects:
                item = item_dict.get_subject(key)
                if item.x == x and item.y == y:
                    # draw item
                    to_draw = item.render_tag
                    tag = tileDict.tile_string(to_draw)
                    self.win.blit(tag, (self.screen_width // 10, self.screen_height // 10))
                    font = pygame.font.Font('freesansbold.ttf', 12)

                    # name
                    text = font.render(item.name, True, (255, 255, 255))
                    self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 50))

                    # description 
                    text = font.render(item.description, True, (255, 255, 255))
                    self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 65))
                    nothing_at_target = False

                    # stats (if present)
                    next_text = 80
                    if hasattr(item, "damage_min"):
                        text = font.render("Damage: " + str(item.damage_min) + " - " + str(item.damage_max), True, (255, 255, 255))
                        self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + next_text))
                        next_text += 15
                    if hasattr(item, "defense"):
                        text = font.render("Defense: " + str(item.defense), True, (255, 255, 255))
                        self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + next_text))
                        next_text += 15
                    if hasattr(item, "consumable"):
                        text = font.render("Consumable", True, (255, 255, 255))
                        self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + next_text))
                        next_text += 15
        # find player at target
        if nothing_at_target:
            if player.x == x and player.y == y:
                nothing_at_target = False

                to_draw = player.render_tag
                tag = tileDict.tile_string(to_draw)
                self.win.blit(tag, (self.screen_width  // 10, self.screen_height // 10))
                font = pygame.font.Font('freesansbold.ttf', 12)

                # random flavor text since detailed player info is elsewhere
                text = font.render("You", True, (255, 255, 255))
                self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 50))
                text = font.render("You are here", True, (255, 255, 255))
                self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 65))
        return nothing_at_target

    def create_inventory(self, player, equipment_type=None):   
        self.uiManager.clear_and_reset()
        self.win.fill(self.colorDict.getColor("black"))
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


        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((inventory_message_offset_from_left, inventory_message_offset_from_top),
                                                              (inventory_message_width, inventory_message_height)),
                                    text="Inventory",
                                    manager=self.uiManager,
                                    object_id='#title_label')

        for i, item in enumerate(player.character.inventory):
            if equipment_type != None and item.equipment_type != equipment_type:
                continue
            if item.stackable:
                item_name = item.name + " (x" + str(item.stacks) + ")"
            else:
                item_name = item.name
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
        self.win.fill(self.colorDict.getColor("black"))
        self.uiManager.draw_ui(self.win)
    
    def draw_on_button(self, button, img, letter="", button_size=None):
        offset = (0, 0)
        if letter == "d": # shrink weapon image a bit
            img = pygame.transform.scale(img, (button_size[0] // 5 * 4, button_size[1] // 5 * 4))
            offset = (button_size[0] // 10, button_size[1] // 10)
        button.drawable_shape.states['normal'].surface.blit(img, offset)
        if button_size:
            font_size = 20
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(letter, True, (255, 255, 255))
            button.drawable_shape.states['normal'].surface.blit(text, (button_size[0] // 15, button_size[1] // 5 * 4))
        button.drawable_shape.active_state.has_fresh_surface = True
        # button.drawable_shape.redraw_all_states()

    def create_equipment(self, player, tileMap):
        self.uiManager.clear_and_reset()
        self.win.fill(self.colorDict.getColor("black"))

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


        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((equipment_message_offset_from_left, equipment_message_offset_from_top),
                                                              (equipment_message_width, equipment_message_height)),
                                    text="Equipment",
                                    manager=self.uiManager,
                                    object_id='#title_label')

        # equipment_slots = ["shield", "ring", "ring", "helmet", "armor", "boots", "weapon", "gloves"]:
        if player.character.main_shield == None:
            pre_text = "equip "
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

        if len(player.character.main_rings) == 0:
            pre_text = "equip "
            img = pygame.transform.scale(tileMap.tiles[807], (small_button_width, small_button_height))
        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.main_rings[0].render_tag], (small_button_width, small_button_height))
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((first_col_offset_from_left, 
                                               outer_cols_offset_from_top + (medium_button_height + margin_between_buttons_height)),
                                               (small_button_width, small_button_height)),
                    text = "ring 1",
                    manager=self.uiManager,
                    object_id='#equipment_button')
        self.draw_on_button(button, img, "a", (small_button_width, small_button_height))
        button.action = 'a'
        
        if len(player.character.main_rings) != 2:
            pre_text = "equip "
            img = pygame.transform.scale(tileMap.tiles[807], (small_button_width, small_button_height))
        else:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[player.character.main_rings[1].render_tag], (small_button_width, small_button_height))
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
            pre_text = "equip "
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
            pre_text = "equip "
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
            pre_text = "equip "
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
            pre_text = "equip "
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
        
        self.draw_on_button(button, img, "d", (medium_button_width, medium_button_height))
        button.action = 'd'

        if player.character.gloves == None:
            pre_text = "equip "
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
        self.win.fill(self.colorDict.getColor("black"))
        self.uiManager.draw_ui(self.win)

    def create_pause_screen(self):
        self.uiManager.clear_and_reset()

        width = 700
        height = 300
        startX = (self.screen_width - width) / 2
        startY = (self.screen_height - height) / 2

        numButtons = 3

        offset = 10
        self.draw_empty_box(startX, startY, width, height)

        startX += offset
        startY += offset
        width -= 2 * offset
        buttonHeight = ((height - offset) / numButtons) - offset
        
        unpause = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((startX, startY, width, buttonHeight)),
                    text = "Unpause",
                    manager=self.uiManager,
                    starting_height=1000) #Important! Need this to be high so it's above the panel.
        unpause.action = "esc"

        startY += buttonHeight + offset
        menu = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((startX, startY, width, buttonHeight)),
                    text = "Return to (m)enu",
                    manager=self.uiManager,
                    starting_height=1000) #Important! Need this to be high so it's above the panel.
        menu.action = 'm'

        startY += buttonHeight + offset
        quit = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((startX, startY, width, buttonHeight)),
                    text = "(Q)uit",
                    manager=self.uiManager,
                    starting_height=1000)
        quit.action = 'q'

    def update_pause_screen(self):
        self.uiManager.draw_ui(self.win)


    def draw_character_stats(self, player, margin_from_left, margin_from_top, width, height):
        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((margin_from_left, margin_from_top), (width, height)),
            html_text = "Player<br><br>"
                        "Stats<br>"
                        "Strength: " + str(player.character.strength) + "<br>"
                        "Dexterity: " + str(player.character.dexterity) + "<br>"
                        "Endurance: " + str(player.character.endurance) + "<br>"
                        "Intelligence: " + str(player.character.intelligence) + "<br>"
                        "<br>"
                        "Health: " + str(player.character.health) + " / " + str(player.character.max_health) + "<br>"
                        "Mana: " + str(player.character.mana) + " / " + str(player.character.max_mana) + "<br>"
                        "<br>"
                        "Damage: " + str(player.character.get_damage_min()) + " - " + str(player.character.get_damage_max()) + " (+" + str(player.character.strength) + ") <br>"
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

    def update_main(self):
    #Main Screen
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)

    def update_item(self, item, tileDict):
        self.uiManager.clear_and_reset()
        self.win.fill(self.colorDict.getColor("black"))
        item_screen_width = self.screen_width // 2
        item_screen_height = self.screen_height // 2
        item_offset_from_left = self.screen_width // 4
        item_offset_from_top = self.screen_height // 4

        item_message_width = self.screen_width // 2
        item_message_height = self.screen_height // 10
        item_message_offset_from_left = self.screen_width // 4
        item_message_offset_from_top = self.screen_height // 4

        item_image_width = self.screen_width // 20
        item_image_height = self.screen_width // 20
        item_image_offset_from_left = self.screen_width // 4 + self.screen_width // 50
        item_image_offset_from_top = self.screen_height // 4 + self.screen_width // 50

        item_button_width = self.screen_width // 10
        item_button_height = self.screen_height // 30
        item_button_offset_from_left = item_offset_from_left+ self.screen_width // 20
        item_button_offset_from_top = item_screen_height + item_offset_from_top - item_button_height - self.screen_height // 50
        item_button_offset_from_each_other = self.screen_width // 20

        item_text_offset_from_left = item_offset_from_left + item_screen_width // 20
        item_text_offset_from_top = item_image_offset_from_top + item_message_height
        item_text_width = item_screen_width * 9 // 10
        item_text_height = item_screen_height // 2

        buttons = Buttons()
        buttons_drawn = 0

        item_image = pygame.transform.scale(tileDict.tiles[item.render_tag],
                                     (item_image_width, item_image_height))

        self.uiManager.clear_and_reset()
        pygame.draw.rect(self.win, (112,128,144), pygame.Rect(item_offset_from_left, item_offset_from_top, item_screen_width, item_screen_height))

        self.win.blit(item_image, (item_image_offset_from_left, item_image_offset_from_top))
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((item_message_offset_from_left, item_message_offset_from_top),
                                      (item_message_width, item_message_height)),
            text=item.name,
            manager=self.uiManager,
            object_id='#title_label')

        pretext = ""
        action = ""
        if item.equipable:
            if item.equipped:
                pretext = "Unequip"
                action = "u"
            else:
                pretext = "Equip"
                action = "e"
        elif item.consumeable:
            pretext = "Quaff"
            action = "q"
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((item_button_offset_from_left, item_button_offset_from_top),
                                      (item_button_width, item_button_height)),
            text=pretext,
            manager=self.uiManager)
        button.action = action
        buttons.add(button, pretext)
        buttons_drawn += 1

        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((item_button_offset_from_left + (item_button_width + item_button_offset_from_each_other) * buttons_drawn, item_button_offset_from_top),
                                      (item_button_width, item_button_height)),
            text='Drop',
            manager=self.uiManager)
        button.action = "d"
        buttons.add(button, "Drop")
        buttons_drawn += 1

        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((item_button_offset_from_left + (item_button_width + item_button_offset_from_each_other) * buttons_drawn, item_button_offset_from_top),
                                      (item_button_width, item_button_height)),
            text='Destroy',
            manager=self.uiManager)
        button.action = "b"
        buttons.add(button, "Destroy")
        buttons_drawn += 1

        item_text = ""
        item_text += item.description  + "<br>"
        if item.equipped:
            item_text += "Currently equipped<br>"
        item_text += "Equipment type: " + item.equipment_type + "<br>"
        if isinstance(item, I.Armor):
            item_text += "Armor: " + str(item.armor) + "<br>"
        if isinstance(item, I.Weapon):
            item_text += "Damage: " + str(item.damage_min) + " - " + str(item.damage_max) + "<br>"
            if item.on_hit:
                item_text += "On hit: " + item.on_hit_description + "<br>"
        if item.attached_skill != None:
            item_text += "Grants skill: " + item.get_attached_skill_name() + "<br>"
      #  item_text += item.attached_skill.name + "<br>"
        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((item_text_offset_from_left, item_text_offset_from_top), (item_text_width, item_text_height)),
            html_text = item_text,
            manager=self.uiManager
        )

        self.uiManager.draw_ui(self.win)
        return self.buttons

    def update_examine(self, target, tileDict, messages):
        x, y = target
        tag = tileDict.tile_string(901)
        self.win.blit(tag, (self.textSize * (x - self.x_start), self.textSize * (y - self.y_start)))
        self.write_messages(messages)

    def update_ui(self):
        deltaTime = self.clock.tick() / 1000
        self.uiManager.update(deltaTime)

    def create_game_ui(self, player):
        self.uiManager.clear_and_reset()

        healthBar = ui.HealthBar(pygame.Rect((20,400), (120,40)), self.uiManager, player)
        manaBar = ui.ManaBar(pygame.Rect((20,450), (120,40)), self.uiManager, player)

def create_main_screen(scr, width, height):
    button_width = width // 6
    button_height = height // 8
    button_offset_from_bottom = height * 95 // 100 - button_height
    button_offset_from_each_other = width // 12
    button_offset_from_left = width * 1/6 #Should be (1 - 3* button_width - 2 * button_offset from each other) / 2

    message_width = width * 5//6
    message_height = height * 2//3
    message_offset_from_left = width // 12
    message_offset_from_top = height // 12


    scr.uiManager.clear_and_reset()
    buttons = Buttons()
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_offset_from_left, button_offset_from_bottom), (button_width, button_height)),
                                             text='Play',
                                             manager=scr.uiManager)
    button.action = "return"
    buttons.add(button, "play")
    

    
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_offset_from_left + button_width+ button_offset_from_each_other, button_offset_from_bottom), (button_width, button_height)),
                                             text='Load',
                                             manager=scr.uiManager)
    button.action = "l"
    buttons.add(button, "load")

    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_offset_from_left+ button_width * 2 + button_offset_from_each_other * 2, button_offset_from_bottom), (button_width, button_height)),
                                             text='Quit',
                                             manager=scr.uiManager)
    button.action = "esc"
    buttons.add(button, "quit")

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((message_offset_from_left, message_offset_from_top), (message_width, message_height)),
                                text="Orbworld: The Orb of Destiny",
                                manager=scr.uiManager,
                                object_id='#title_label')
    
    return buttons
