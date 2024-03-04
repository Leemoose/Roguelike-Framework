import pygame
import pygame_gui


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
        self.clock = pygame.time.Clock()
        self.buttons = []

    def update_display(self, colorDict, floormap, tileDict, monsterID, item_ID, monster_map, player, messages, target_to_display):
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

        dead_monsters = []
        for key in monsterID.subjects:
            monster = monsterID.get_subject(key)
            if monster.character.is_alive():
                if (monster.x >= self.x_start and monster.x < self.x_end and monster.y >= self.y_start and monster.y < self.y_end):
                    if floormap.track_map[monster.x][monster.y].visible:
                        monster_tile = tileDict.tile_string(monster.render_tag)
                        self.win.blit(monster_tile, (self.textSize*(monster.x - self.x_start), self.textSize*(monster.y - self.y_start)))
            else:
                dead_monsters.append(key)
                monster_map.clear_location(monster.x, monster.y)
        for key in dead_monsters:
            monsterID.subjects.pop(key)

        self.win.blit(tileDict.tile_string(200), (r_x * self.textSize, r_y * self.textSize))

        black_screen = pygame.transform.scale(pygame.image.load("assets/black_screen.png"), (self.screen_width // 5, self.screen_height // 5))
        self.win.blit(black_screen, (0, self.screen_height // 5 * 4))
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render("Health: " + str(player.character.health), True, (255, 255, 255))
        self.win.blit(text, (0, self.screen_height // 100 * 85))
        text = font.render("Experience: " + str(player.experience) + " / " + str(player.experience_to_next_level), True, (255, 255, 255))
        self.win.blit(text, (0, self.screen_height // 100 * 90))
        text = font.render("Level: " + str(player.level), True, (255, 255, 255))
        self.win.blit(text, (0, self.screen_height // 100 * 95))

        self.write_messages(messages)

        if target_to_display != None:
            defeated = self.draw_examine_window(target_to_display, tileDict, monster_map, monsterID)
        

    def write_messages(self, messages):
        font = pygame.font.Font('freesansbold.ttf', 12)
        for i, message in enumerate(messages):
            text = font.render(message, True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 100 * 10, self.screen_height // 100 * (85 + i *3)))

    def draw_examine_window(self, target, tileDict, monster_map, monster_dict):
        x, y = target
        black_screen = pygame.transform.scale(pygame.image.load("assets/black_screen.png"), (self.screen_width // 5, self.screen_height // 5))
        self.win.blit(black_screen, (0, 0))
        monster_defeated = False
        # find monster at target
        if not monster_map.get_passable(x,y):
            monster = monster_dict.get_subject(monster_map.locate(x,y))
            to_draw = monster.render_tag
            tag = tileDict.tile_string(to_draw)
            self.win.blit(tag, (self.screen_width  // 10, self.screen_height // 10))
            font = pygame.font.Font('freesansbold.ttf', 12)
            text = font.render(monster.name, True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 50))
            if monster.character.is_alive():
                text = font.render("Health: " + str(monster.character.health) + "/" + str(monster.character.max_health), True, (255, 255, 255))
                monster_status = "Healthy"
                if monster.character.health < monster.character.max_health // 2:
                    monster_status = "Wounded"
                monster_effects = monster.character.status_effects
                for effect in monster_effects:
                    monster_status += ", " + effect.message
                text2 = font.render("Status: " + monster_status, True, (255, 255, 255))
            else:
                text = font.render(f"Exp gained: {monster.experience_given} exp", True, (255, 255, 255))
                monster_status = "Dead"
                text2 = font.render("Status: " + monster_status, True, (255, 255, 255))
                monster_defeated = True
            
            self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 65))
            self.win.blit(text2, (self.screen_width // 10, self.screen_height // 10 + 80))
            text = font.render(monster.description(), True, (255, 255, 255))
            self.win.blit(text, (self.screen_width // 10, self.screen_height // 10 + 95))
        return monster_defeated
            

    def update_inventory(self, player):
        font2 = pygame.font.SysFont('didot.ttc', 32)
        inv = pygame.transform.scale(pygame.image.load("assets/inventory.png"), (self.screen_width * 2//3, self.screen_height * 4 //5))
        self.win.blit(inv, (self.screen_width // 6, self.screen_height // 10))
        for i, item in enumerate(player.character.inventory):
        #Need to create list of buttons for items
            text = font2.render(item.name, True, (0,255,0))
            num = font2.render(chr(i + ord("a")) + ".", True, (0,255,0))
            self.win.blit(num, (self.screen_width // 6 + 15, self.screen_height // 5 +10+ 20 * i))
            self.win.blit(text, (self.screen_width // 6 + 35, self.screen_height // 5+10+ 20* i))

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

def create_main_screen(scr):
    buttons = Buttons()
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 600), (400, 100)),
                                             text='Play',
                                             manager=scr.uiManager)
    button.action = "return"
    buttons.add(button, "play")
    

    
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((440, 600), (400, 100)),
                                             text='Load',
                                             manager=scr.uiManager)
    button.action = "l"
    buttons.add(button, "load")

    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((860, 600), (400, 100)),
                                             text='Quit',
                                             manager=scr.uiManager)
    button.action = "esc"
    buttons.add(button, "quit")

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, 20), (1240, 580)),
                                text="Orbworld: The Orb of Destiny",
                                manager=scr.uiManager,
                                object_id='#title_label')
    
    return buttons


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