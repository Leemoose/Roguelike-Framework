import pygame, pygame_gui
from .ui import MessageBox

def create_binding_screen(display, loop):
    display.uiManager.clear_and_reset()

    binding_screen_width = display.screen_width * 2 // 3
    binding_screen_height = display.screen_height * 2 // 3
    binding_offset_from_left = (display.screen_width - binding_screen_width) // 2
    binding_offset_from_top = (display.screen_height - binding_screen_height) // 2

    binding_title_width = binding_screen_width
    binding_title_height = binding_screen_height // 6
    binding_title_offset_from_left = binding_offset_from_left
    binding_title_offset_from_top = binding_offset_from_top

    message_width = binding_screen_width
    message_offset_from_left = binding_offset_from_left
    message_offset_from_top = (binding_screen_height - binding_title_height) * 2 // 3
    message_height = display.screen_height - message_offset_from_top - binding_offset_from_top

    pygame.draw.rect(display.win, (50, 50, 50),
                     pygame.Rect(binding_offset_from_left - 10, binding_offset_from_top - 10, binding_screen_width + 20,
                                 binding_screen_height + 20))
    pygame.draw.rect(display.win, (0, 0, 0),
                     pygame.Rect(binding_offset_from_left, binding_offset_from_top, binding_screen_width,
                                 binding_screen_height))

    display.draw_escape_button(binding_offset_from_left, binding_offset_from_top, binding_screen_width,
                            binding_screen_height)
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((binding_title_offset_from_left, binding_title_offset_from_top),
                                  (binding_title_width, binding_title_height)),
        text="Bindings",
        manager=display.uiManager,
        object_id='#title_label')
    text_box = MessageBox(
        pygame.Rect((message_offset_from_left, message_offset_from_top),
                    (message_width, message_height)),
        manager=display.uiManager,
        loop=loop)
