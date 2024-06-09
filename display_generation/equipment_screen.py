import pygame_gui, pygame

def create_equipment(display, loop):
    player = loop.player
    tileMap = loop.tileDict
    display.uiManager.clear_and_reset()
    display.win.fill((0, 0, 0))

    equipment_screen_width = display.screen_width // 3 * 2
    equipment_screen_height = display.screen_height
    equipment_offset_from_left = display.screen_width // 3
    equipment_offset_from_top = 0

    equipment_message_width = display.screen_width // 2
    equipment_message_height = display.screen_height // 10
    equipment_message_offset_from_left = display.screen_width // 4
    equipment_message_offset_from_top = display.screen_height // 30

    # 8 buttons, for helmet, armor, gloves, boots, ring 1, ring 2, weapon, shield
    # equipment is across three columns
    medium_button_width = display.screen_width // 8
    medium_button_height = display.screen_height // 5
    first_col_offset_from_left = display.screen_width // 4
    outer_cols_offset_from_top = display.screen_height // 5
    middle_col_offset_from_top = display.screen_height // 5
    small_button_width = display.screen_width // 16 - display.screen_width // 120
    small_button_height = display.screen_height // 8
    margin_between_buttons_height = display.screen_height // 30
    small_margin_between_buttons_width = display.screen_width // 60
    margin_between_buttons_width = display.screen_width // 30

    display.uiManager.clear_and_reset()
    pygame.draw.rect(display.win, (0, 0, 0),
                     pygame.Rect(equipment_offset_from_left, equipment_offset_from_top, equipment_screen_width,
                                 equipment_screen_height))

    display.draw_escape_button(equipment_message_offset_from_left, equipment_message_offset_from_top,
                            equipment_screen_width, equipment_screen_height)

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((equipment_message_offset_from_left, equipment_message_offset_from_top),
                                  (equipment_message_width, equipment_message_height)),
        text="Equipment",
        manager=display.uiManager,
        object_id='#title_label')

    # equipment_slots = ["shield", "ring", "ring", "helmet", "armor", "boots", "weapon", "gloves"]:
    if player.character.free_equipment_slots("hand_slot") != 0:
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
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("hand_slot", 0).render_tag],
                                     (medium_button_width, medium_button_height))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((first_col_offset_from_left,
                                   outer_cols_offset_from_top),
                                  (medium_button_width, medium_button_height)),
        text=pre_text + "shield",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "q", (medium_button_width, medium_button_height))
    button.action = 'q'

    if player.character.free_equipment_slots("ring_slot") != 0:
        available_slot = False
        for item in player.character.inventory:
            if item.equipment_type == "Ring" and (not item.equipped):
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
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("ring_slot", 0).render_tag],
                                     (small_button_width, small_button_height))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((first_col_offset_from_left,
                                   outer_cols_offset_from_top + (medium_button_height + margin_between_buttons_height)),
                                  (small_button_width, small_button_height)),
        text="ring 1",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "r", (small_button_width, small_button_height))
    button.action = 'r'

    if player.character.free_equipment_slots("ring_slot") != 0:
        available_slot = False
        for item in player.character.inventory:
            if item.equipment_type == "Ring" and (not item.equipped):
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
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("hand_slot", 1).render_tag],
                                     (small_button_width, small_button_height))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((first_col_offset_from_left + small_button_width + small_margin_between_buttons_width,
                                   outer_cols_offset_from_top + (medium_button_height + margin_between_buttons_height)),
                                  (small_button_width, small_button_height)),
        text="ring 2",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "z", (small_button_width, small_button_height))
    button.action = 'z'

    if player.character.free_equipment_slots("amulet_slot") != 0:
        available_slot = False
        for item in player.character.inventory:
            if item.equipment_type == "Amulet":
                available_slot = True
                break
        if available_slot == True:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[820],
                                         (medium_button_width, medium_button_height))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[821], (medium_button_width, medium_button_height))

    else:
        pre_text = "change "
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("amulet_slot", 0).render_tag],
                                     (medium_button_width, medium_button_height))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((first_col_offset_from_left,
                                   outer_cols_offset_from_top + 2 * (
                                               medium_button_height + margin_between_buttons_height)),
                                  (medium_button_width, medium_button_height)),
        text=pre_text + "amulet",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "a", (medium_button_width, medium_button_height))
    button.action = 'a'

    if player.character.free_equipment_slots("helmet_slot") != 0:
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
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("helmet_slot", 0).render_tag],
                                     (medium_button_width, medium_button_height))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((first_col_offset_from_left + medium_button_width + margin_between_buttons_width,
                                   middle_col_offset_from_top),
                                  (medium_button_width, medium_button_height)),
        text=pre_text + "helmet",
        manager=display.uiManager,
        object_id='#equipment_button')
    display.draw_on_button(button, img, "w", (medium_button_width, medium_button_height))
    button.action = 'w'

    if player.character.free_equipment_slots("body_armor_slot") != 0:
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
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("body_armor_slot", 0).render_tag],
                                     (medium_button_width, medium_button_height))
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((first_col_offset_from_left + medium_button_width + margin_between_buttons_width,
                                   middle_col_offset_from_top + (medium_button_height + margin_between_buttons_height)),
                                  (medium_button_width, medium_button_height)),
        text=pre_text + "armor",
        manager=display.uiManager,
        object_id='#equipment_button')

    display.draw_on_button(button, img, "s", (medium_button_width, medium_button_height))
    button.action = 's'

    if player.character.free_equipment_slots("boots_slot") != 0:
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
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("boots_slot", 0).render_tag],
                                     (medium_button_width, medium_button_height))

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((first_col_offset_from_left + medium_button_width + margin_between_buttons_width,
                                   middle_col_offset_from_top + 2 * (
                                               medium_button_height + margin_between_buttons_height)),
                                  (medium_button_width, medium_button_height)),
        text=pre_text + "boots",
        manager=display.uiManager,
        object_id='#equipment_button')

    display.draw_on_button(button, img, "x", (medium_button_width, medium_button_height))
    button.action = 'x'

    if player.character.free_equipment_slots("hand_slot") != 0:
        available_slot = False
        for item in player.character.inventory:
            if item.equipment_type == "Weapon":
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
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("hand_slot", 1).render_tag],
                                     (medium_button_width, medium_button_height))

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_offset_from_left + 2 * (medium_button_width + margin_between_buttons_width),
             outer_cols_offset_from_top),
            (medium_button_width, medium_button_height)),
        text=pre_text + "weapon",
        manager=display.uiManager,
        object_id='#equipment_button')

    display.draw_on_button(button, img, "d", (medium_button_width, medium_button_height), shrink=True)
    button.action = 'd'

    if player.character.free_equipment_slots("gloves_slot") != 0:
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
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("gloves_slot", 0).render_tag],
                                     (medium_button_width, medium_button_height))

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_offset_from_left + 2 * (medium_button_width + margin_between_buttons_width),
             outer_cols_offset_from_top + (medium_button_height + margin_between_buttons_height)),
            (medium_button_width, medium_button_height)),
        text=pre_text + "gloves",
        manager=display.uiManager,
        object_id='#equipment_button')

    display.draw_on_button(button, img, "c", (medium_button_width, medium_button_height))
    button.action = 'c'

    if player.character.free_equipment_slots("pants_slot") != 0:
        available_slot = False
        for item in player.character.inventory:
            if item.equipment_type == "Pants":
                available_slot = True
                break
        if available_slot == True:
            pre_text = "change "
            img = pygame.transform.scale(tileMap.tiles[818],
                                         (medium_button_width, medium_button_height))
        else:
            pre_text = "no options "
            img = pygame.transform.scale(tileMap.tiles[819], (medium_button_width, medium_button_height))

    else:
        pre_text = "change "
        img = pygame.transform.scale(tileMap.tiles[player.character.get_nth_item_in_equipment_slot("pants_slot", 0).render_tag],
                                     (medium_button_width, medium_button_height))

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (first_col_offset_from_left + 2 * (medium_button_width + margin_between_buttons_width),
             outer_cols_offset_from_top + 2 * (medium_button_height + margin_between_buttons_height)),
            (medium_button_width, medium_button_height)),
        text=pre_text + "pants",
        manager=display.uiManager,
        object_id='#equipment_button')

    display.draw_on_button(button, img, "p", (medium_button_width, medium_button_height))
    button.action = 'p'

    display.draw_character_stats(player,
                              margin_from_left=first_col_offset_from_left + 3 * (
                                          medium_button_width + margin_between_buttons_width),
                              margin_from_top=middle_col_offset_from_top,
                              width=medium_button_width * 2,
                              height=medium_button_height * 3 + margin_between_buttons_height * 2)
    display.uiManager.draw_ui(display.win)