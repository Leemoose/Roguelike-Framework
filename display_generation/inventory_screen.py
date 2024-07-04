import pygame, pygame_gui

def create_inventory(display, loop):
    player = loop.player
    equipment_type = loop.limit_inventory
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

    if equipment_type == "Enchantable":
        enchantable = player.character.get_enchantable()

    # This needs to be fixed
    for i, item in enumerate(player.get_inventory()):
        item_name = item.name
        if (equipment_type == None 
            or (equipment_type == "Enchantable" and item in enchantable) 
            or item.equipment_type == equipment_type):
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

    display.uiManager.draw_ui(display.win)
