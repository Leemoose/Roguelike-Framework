import pygame
import pygame_gui

def create_death_screen(display, loop):
    display.uiManager.clear_and_reset()

    message_width = display.screen_width // 4
    message_height = display.screen_height // 5
    message_offset_from_left = (display.screen_width - message_width) // 2
    message_offset_from_top = (display.screen_height - message_height) // 2

    button_width = display.screen_width // 8
    button_height = display.screen_height // 12
    button_offset_from_top = message_offset_from_top + message_height - button_height - 10
    button_offset_from_left = (display.screen_width - button_width) // 2

    # display.draw_empty_box(message_offset_from_left, message_offset_from_top, message_width, message_height)

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_offset_from_left, button_offset_from_top), (button_width, button_height)),
        text='Return to Main Menu',
        manager=display.uiManager,
        starting_height=10000)
    button.action = "esc"

    text_box = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((button_offset_from_left, message_offset_from_top), (button_width, button_height)),
        text="You have died.",
        manager=display.uiManager
    )