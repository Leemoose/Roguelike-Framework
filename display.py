import pygame
import pygame_gui
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
        self.buttons = []

    def update_display(self, colorDict, floormap, tileDict, monsterID, item_ID, monster_map, player, messages, target_to_display):
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
            text = font.render(monster.description(), True, (255, 255, 255))
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
            

    def update_inventory(self, player):
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

        buttons = Buttons()
        for i, item in enumerate(player.character.inventory):
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
            buttons.add(button, chr(ord("a") + i))

        self.uiManager.draw_ui(self.win)
        return buttons

    def update_main(self):
    #Main Screen
        self.win.fill((0,0,0))
        self.uiManager.draw_ui(self.win)

    def update_race(self):
    #Race Screen
        race_background = pygame.image.load("assets/race_screen.png")
        race_background = pygame.transform.scale(race_background, (self.screen_width, self.screen_height))
        self.win.blit(race_background, (0,0))

    def update_class(self):
    #Class Screen
        class_background = pygame.image.load("assets/class_screen.png")
        class_background = pygame.transform.scale(class_background, (self.screen_width, self.screen_height))
        self.win.blit(class_background, (0,0))

    def update_item(self, item, tileDict):
        font2 = pygame.font.SysFont('didot.ttc', 32)
        item_background = pygame.transform.scale(pygame.image.load("assets/item_background.png"),
                                     (self.screen_width * 2 // 3, self.screen_height * 4 // 5))
        self.win.blit(item_background, (self.screen_width // 6, self.screen_height // 10))
        item_tile = tileDict.tile_string(item.render_tag)
        self.win.blit(item_tile, (self.screen_width * 17 // 100 , self.screen_height * 11 // 100))
        text = font2.render(item.name, True, (255, 255, 255))
        self.win.blit(text, ((self.screen_width * 22 // 100 , self.screen_height * 12 // 100)))

        message = ""
        if item.equipped:
            message = "u: Unequip"
        elif item.equipable:
            message = "e: Equip"
        elif item.consumeable:
            message = "q: Quaff"

        text = font2.render(message, True, (255, 255, 255))
        self.win.blit(text, ((self.screen_width * 22 // 100, self.screen_height * 15 // 100)))

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

    def open_pause_screen(self):
        #self.pauseWindow = pygame_gui.core.UIContainer(pygame.Rect((0, 0), (self.screen_width, self.screen_height)),
        #                                  manager=self.uiManager, starting_height=1)
        #self.uiManager.get_window_stack().add_new_window(self.pauseWindow)\
        print("Pause screen opens here!")
    
    def close_pause_screen(self):
        #self.uiManager.get_window_stack().remove_window(self.pauseWindow)
        print("Pause screen closes here!")

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


"""
def create_race_screen(scr):
    background = pygame.image.load("assets/class_background.png")
    background = pygame.transform.scale(background, (scr.screen_width, scr.screen_height))
    scr.win.blit(background, (0,0))
    buttons = Buttons()
    button = Button(scr.screen_width, scr.screen_height, "assets/button.png", 15/100, 11/100, "1", scr.screen_width / 2, scr.screen_height * 80/100)
    buttons.add(button, "Human")
    scr.win.blit(button.img, (button.get_position()))

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Human', True, (255, 255, 255))
    text_width, text_height = font.size("Human")
    scr.win.blit(text, (scr.screen_width / 2 - text_width / 2, scr.screen_height * 85/100 + button.height / 2 - text_height / 2))

    #pygame.image.save(scr.win, "assets/race_screen.png")
    return buttons

def create_class_screen(scr):
    background = pygame.image.load("assets/class_background.png")
    background = pygame.transform.scale(background, (scr.screen_width, scr.screen_height))
    scr.win.blit(background, (0,0))
    buttons = Buttons()
    button = Button(scr.screen_width, scr.screen_height, "assets/button.png", 15/100, 11/100, "1", scr.screen_width // 2, scr.screen_height * 80/100)
    buttons.add(button, "Warrior")
    scr.win.blit(button.img, (button.get_position()))

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Warrior', True, (255, 255, 255))
    text_width, text_height = font.size("Warrior")
    scr.win.blit(text, (scr.screen_width / 2 - text_width / 2, scr.screen_height * 85/100 + button.height / 2 - text_height / 2))

    # pygame.image.save(scr.win, "assets/class_screen.png")
    return buttons
"""