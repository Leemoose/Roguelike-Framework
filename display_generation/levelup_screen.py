import pygame, pygame_gui
from .ui import StatChangeText, StatDownButton,StatUpButton, LevelUpHeader

def create_level_up(display, loop):
    player = loop.player
    tileDict = loop.tileDict
    entity_screen_width = display.screen_width // 2
    entity_screen_height = display.screen_height // 2
    entity_offset_from_left = display.screen_width // 4
    entity_offset_from_top = display.screen_height // 4

    entity_message_width = entity_screen_width // 2
    entity_message_height = entity_screen_height // 10
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
    stat_change_text_offset_left = stat_change_button_offset_from_left + stat_change_button_width + (
                stat_change_button_width // 8)

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

        button = StatDownButton(
            rect=pygame.Rect((stat_change_button_offset_from_left,
                              stat_change_button_offset_from_top + i * (
                                          stat_line_height + stat_change_button_offset_from_each_other_height)),
                             (stat_change_button_width, stat_change_button_height)),
            manager=display.uiManager,
            player=player,
            img1=stat_change_left,
            img2=stat_change_left_dark,
            index=i)

        button.action = "left"
        button.row = i

        # display.draw_on_button(button, stat_change_left, letter = "", button_size=(stat_change_button_width, stat_change_button_height), shrink=False, offset_factor=12, text_offset=(15, 0.8))

        StatChangeText(
            rect=pygame.Rect(
                (stat_change_text_offset_left,
                 stat_change_button_offset_from_top + i * (
                             stat_line_height + stat_change_button_offset_from_each_other_height)),
                (stat_change_button_width, stat_change_button_height)),
            manager=display.uiManager,
            player=player,
            index=i)

        button_2 = StatUpButton(
            rect=pygame.Rect((
                             stat_change_button_offset_from_left + stat_change_button_width + stat_change_offset_from_each_other_width,
                             stat_change_button_offset_from_top + i * (
                                         stat_line_height + stat_change_button_offset_from_each_other_height)),
                             (stat_change_button_width, stat_change_button_height)),
            manager=display.uiManager,
            player=player,
            img1=stat_change_right,
            img2=stat_change_right_dark,
            index=i)

        # display.draw_on_button(button_2, stat_change_right, letter = "", button_size=(stat_change_button_width, stat_change_button_height), shrink=False, offset_factor=12, text_offset=(15, 0.8))

        button_2.action = "right"
        button_2.row = i

    display.draw_escape_button(entity_message_offset_from_left, entity_message_offset_from_top,
                            stat_line_width + stat_change_offset_from_each_other_width, entity_screen_height)

    # stat_line_outline_offset_from_left = stat_change_button_offset_from_left - entity_screen_width // 24
    # stat_line_outline = pygame.Rect((stat_change_button_offset_from_left, stat_line_offset_from_top), (stat_line_width, stat_line_height * 4 + stat_line_offset_from_each_other * 3))
    LevelUpHeader(
        rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                         (entity_message_width, entity_message_height)),
        manager=display.uiManager,
        player=player)

    # strength
    description = "Str (currently " + str(player.character.strength) + ") - increase your damage and wear heavier armor"
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((stat_line_offset_from_left, stat_line_offset_from_top),
                                  (stat_line_width, stat_line_height)),
        text=description,
        manager=display.uiManager,
        object_id='#stat_label')

    # dexterity
    description = "Dex (currently " + str(
        player.character.dexterity) + ") - increase your dodge chance and action speed"
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((stat_line_offset_from_left,
                                   stat_line_offset_from_top + stat_line_height + stat_line_offset_from_each_other),
                                  (stat_line_width, stat_line_height)),
        text=description,
        manager=display.uiManager,
        object_id='#stat_label')

    # endurance
    description = "En (currently " + str(player.character.endurance) + ") - increase your defense and your max health"
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((stat_line_offset_from_left, stat_line_offset_from_top + 2 * (
                    stat_line_height + stat_line_offset_from_each_other)),
                                  (stat_line_width, stat_line_height)),
        text=description,
        manager=display.uiManager,
        object_id='#stat_label')

    # intelligence
    description = "Int (currently " + str(player.character.intelligence) + ") - increase your max mana and skill damage"
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((stat_line_offset_from_left, stat_line_offset_from_top + 3 * (
                    stat_line_height + stat_line_offset_from_each_other)),
                                  (stat_line_width, stat_line_height)),
        text=description,
        manager=display.uiManager,
        object_id='#stat_label')

    # confirmation_button
    confirmation_button_width = entity_message_width // 3
    confirmation_button_height = stat_change_button_height * 2
    confirmation_button_offset_from_left = stat_outline_width + stat_outline_offset_from_left - confirmation_button_width
    confirmation_button_offset_from_top = stat_line_offset_from_top + 4 * (
                stat_line_height + stat_line_offset_from_each_other) + stat_line_height + (
                                                      stat_line_offset_from_each_other // 4 * 3)

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((confirmation_button_offset_from_left, confirmation_button_offset_from_top),
                                  (confirmation_button_width, confirmation_button_height)),
        text="Confirm",
        manager=display.uiManager)
    button.action = "return"
    button.row = None

def update_level_up(loop):
    line_to_outline = loop.current_stat
    display = loop.display
    player = loop.player
    entity_screen_width = display.screen_width // 2
    entity_screen_height = display.screen_height // 2
    entity_offset_from_left = display.screen_width // 4
    entity_offset_from_top = display.screen_height // 4

    entity_message_width = entity_screen_width // 2
    entity_message_height = entity_screen_height // 10
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
    pygame.draw.rect(display.win, (0, 0, 0), pygame.Rect((0, 0), (display.screen_width // 2, 40)))

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
    stat_change_text_offset_left = stat_change_button_offset_from_left + stat_change_button_width + (
                stat_change_button_width // 8)

    stat_outline_offset_from_left = stat_change_button_offset_from_left - (stat_change_button_width // 2)
    stat_outline_offset_from_top = stat_line_offset_from_top - entity_screen_height // 30
    stat_outline_width = stat_line_width + entity_screen_width // 5
    stat_outline_height = stat_line_height + entity_screen_height // 20

    for i in range(0, 4):
        if i == loop.current_stat:
            color = (0, 0, 0)
        else:
            color = (112, 128, 144)
        pygame.draw.rect(display.win, color, pygame.Rect(stat_outline_offset_from_left,
                                                      stat_outline_offset_from_top + i * (
                                                                  stat_line_height + stat_line_offset_from_each_other),
                                                      stat_outline_width,
                                                      stat_outline_height))

    display.uiManager.draw_ui(display.win)

