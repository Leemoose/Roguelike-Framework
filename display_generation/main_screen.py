import pygame, pygame_gui

def create_main_screen(display, loop):
    num_buttons = 5
    button_width = display.screen_width // (num_buttons + 1)
    button_height = display.screen_height // 8
    button_offset_from_bottom = display.screen_height * 95 // 100 - button_height
    button_offset_from_each_other = display.screen_width // (num_buttons + 1) // (num_buttons + 1)
    button_offset_from_left = display.screen_width // (num_buttons + 1) // \
                (num_buttons + 1)  # Should be (1 - 3* button_width - 2 * button_offset from each other) / 2

    message_width = display.screen_width * 5 // 6
    message_height = display.screen_height * 2 // 3
    message_offset_from_left = display.screen_width // 12
    message_offset_from_top = display.screen_height // 12

    display.uiManager.clear_and_reset()

    imp = pygame.image.load('assets/title_screen.jpg')
    display.win.blit(imp, (0, 0))

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_offset_from_left, button_offset_from_bottom), (button_width, button_height)),
        text='Play',
        manager=display.uiManager)
    button.action = "return"

    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (button_offset_from_left + button_width + button_offset_from_each_other, button_offset_from_bottom),
        (button_width, button_height)),
                                          text='Load',
                                          manager=display.uiManager)
    button.action = "l"

    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (button_offset_from_left + button_width * 2 + button_offset_from_each_other * 2, button_offset_from_bottom),
        (button_width, button_height)),
        text='The Story So Far',
        manager=display.uiManager)
    button.action = "s"

    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (button_offset_from_left + button_width * 3 + button_offset_from_each_other * 3, button_offset_from_bottom),
        (button_width, button_height)),
        text='Help',
        manager=display.uiManager)
    button.action = "h"

    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
        (button_offset_from_left + button_width * 4 + button_offset_from_each_other * 4, button_offset_from_bottom),
        (button_width, button_height)),
                                          text='Quit',
                                          manager=display.uiManager)
    button.action = "esc"

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((message_offset_from_left, message_offset_from_top), (message_width, message_height)),
        text="Orbworld: The Orb of Destiny",
        manager=display.uiManager,
        object_id='#title_label')
