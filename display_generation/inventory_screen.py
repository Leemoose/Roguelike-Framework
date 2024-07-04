import pygame, pygame_gui

def create_inventory(display, loop):
    player = loop.player
    display.uiManager.clear_and_reset()
    display.win.fill((0, 0, 0))
    inventory_screen_width = display.screen_width // 2
    inventory_screen_height = display.screen_height
    inventory_offset_from_left = display.screen_width // 4
    inventory_offset_from_top = 0

    inventory_message_width = display.screen_width // 2
    inventory_message_height = display.screen_height // 10
    inventory_message_offset_from_left = display.screen_width // 4
    inventory_message_offset_from_top = display.screen_height // 30

    inventory_button_width = display.screen_width // 5
    inventory_button_height = display.screen_height // 30
    inventory_button_offset_from_left = display.screen_width * 2 // 5
    inventory_button_offset_from_top = display.screen_height // 10 + display.screen_height // 30 + display.screen_height // 30
    inventory_button_offset_from_each_other = display.screen_height // 100
    
    num_buttons = 5
    selection_offset_from_left = display.screen_width // 16
    selection_offset_from_top = display.screen_height // 4
    selection_button_height = (display.screen_height - (selection_offset_from_top * 2)) / (num_buttons + 1)
    selection_button_width = display.screen_width // 8
    selection_offset_from_each_other = selection_button_height / (num_buttons+1)


    display.uiManager.clear_and_reset()
    pygame.draw.rect(display.win, (0, 0, 0),
                     pygame.Rect(inventory_offset_from_left, inventory_offset_from_top, inventory_screen_width,
                                 inventory_screen_height))

    display.draw_escape_button(inventory_button_offset_from_left, inventory_button_offset_from_top, inventory_screen_width,
                            inventory_screen_height)

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((inventory_message_offset_from_left, inventory_message_offset_from_top),
                                  (inventory_message_width, inventory_message_height)),
        text="Inventory",
        manager=display.uiManager,
        object_id='#title_label')

    # This needs to be fixed
    for i, item in enumerate(player.inventory.get_limit_inventory()):
        item_name = item.name
        if item.stackable:
            item_name = item.name + " (x" + str(item.stacks) + ")"
        if item.can_be_levelled:
            item_level = item.level
            if item_level > 1:
                item_name = item_name + " (+" + str(item_level - 1) + ")"
        if item.equipped:
            item_name = item_name + " (equipped)"
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((inventory_button_offset_from_left,
                                       inventory_button_offset_from_top + inventory_button_offset_from_each_other * i + inventory_button_height * i),
                                      (inventory_button_width, inventory_button_height)),
            text=chr(ord("a") + i) + ". " + item_name,
            manager=display.uiManager)
        button.action = chr(ord("a") + i)

    button_num = 0
    items = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (selection_offset_from_left,
             selection_offset_from_top + selection_offset_from_each_other +
             (selection_button_height + selection_offset_from_each_other) * button_num,
             selection_button_width, selection_button_height)),
        text="1. All items",
        manager=display.uiManager,
        starting_height=1)  # Important! Need this to be high so it's above the panel.
    items.action = "1"

    button_num += 1
    potion = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (selection_offset_from_left,
             selection_offset_from_top + selection_offset_from_each_other +
             (selection_button_height + selection_offset_from_each_other) * button_num,
             selection_button_width, selection_button_height)),
        text="2. Potions",
        manager=display.uiManager,
        starting_height=1)  # Important! Need this to be high so it's above the panel.
    potion.action = '2'

    button_num += 1
    scroll = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (selection_offset_from_left,
             selection_offset_from_top + selection_offset_from_each_other +
             (selection_button_height + selection_offset_from_each_other) * button_num,
             selection_button_width, selection_button_height)),
        text="3. Scrolls",
        manager=display.uiManager,
        starting_height=1)
    scroll.action = '3'

    button_num += 1
    equipment = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (selection_offset_from_left,
             selection_offset_from_top + selection_offset_from_each_other +
             (selection_button_height + selection_offset_from_each_other) * button_num,
             selection_button_width, selection_button_height)),
        text="4. Equipment",
        manager=display.uiManager,
        starting_height=1)
    equipment.action = '4'

    button_num += 1
    weapons = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (selection_offset_from_left,
             selection_offset_from_top + selection_offset_from_each_other +
             (selection_button_height + selection_offset_from_each_other) * button_num,
             selection_button_width, selection_button_height)),
        text="5. Weapons",
        manager=display.uiManager,
        starting_height=1)
    weapons.action = '5'

    display.uiManager.draw_ui(display.win)
