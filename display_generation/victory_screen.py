import pygame, pygame_gui

def create_victory_screen(display, loop):
    display.uiManager.clear_and_reset()
    player = loop.player
    tileDict = loop.tileDict
    entity_screen_width = display.screen_width // 2
    entity_screen_height = display.screen_height // 2
    entity_offset_from_left = display.screen_width // 4
    entity_offset_from_top = display.screen_height // 4

    entity_message_width = entity_screen_width // 2
    entity_message_height = entity_screen_height // 5
    entity_message_offset_from_left = entity_offset_from_left + entity_screen_width // 4
    entity_message_offset_from_top = entity_offset_from_top + entity_screen_height // 30

    border_width = 8
    border_height = 8
    pygame.draw.rect(display.win, (0, 0, 0), pygame.Rect(entity_offset_from_left - border_width // 2,
                                                      entity_offset_from_top - border_height // 2,
                                                      entity_screen_width + border_width,
                                                      entity_screen_height + border_height))
    pygame.draw.rect(display.win, (112, 128, 144),
                     pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width,
                                 entity_screen_height))

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                  (entity_message_width, entity_message_height)),
        text="Victory!",
        manager=display.uiManager,
        object_id='#title_label')

    html_text = "You have defeated the dungeon and achieved maximum orb-iness!<br><br>"
    html_text += "You reached level " + str(player.level) + ".<br>"
    html_text += "You killed " + str(player.statistics.total_monsters_killed) + " monsters along the way.<br>"

    pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect(
            (entity_offset_from_left + entity_screen_width // 20, entity_offset_from_top + entity_screen_height // 4),
            (entity_screen_width * 9 // 10, entity_screen_height * 3 // 5)),
        html_text=html_text,
        manager=display.uiManager)