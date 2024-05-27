import pygame, pygame_gui

def create_pause_screen(display, loop):
    display.uiManager.clear_and_reset()
    pause_screen_width = display.screen_width // 3
    pause_screen_height = display.screen_height // 2
    pause_offset_from_left = (display.screen_width - pause_screen_width) // 2
    pause_offset_from_top = display.screen_height // 4

    pause_num_buttons_height = 5
    pause_button_width = pause_screen_width * 9 // 10
    pause_button_height = (pause_screen_height) // (pause_num_buttons_height + 1)
    pause_button_offset_from_each_other_height = (pause_screen_height) // (
            pause_num_buttons_height + 1) // (pause_num_buttons_height + 1)
    pause_button_offset_from_top = pause_offset_from_top
    pause_button_offset_from_left = pause_offset_from_left + (pause_screen_width - pause_button_width) // 2

    display.draw_empty_box(pause_offset_from_left, pause_offset_from_top, pause_screen_width,
                        pause_screen_height)

    button_num = 0
    unpause = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height +
             (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
             pause_button_width, pause_button_height)),
        text="Unpause",
        manager=display.uiManager,
        starting_height=1000)  # Important! Need this to be high so it's above the panel.
    unpause.action = "esc"

    button_num += 1
    menu = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height +
             (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
             pause_button_width, pause_button_height)),
        text="Return to (m)enu",
        manager=display.uiManager,
        starting_height=1000)  # Important! Need this to be high so it's above the panel.
    menu.action = 'm'

    button_num += 1
    quit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height +
             (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
             pause_button_width, pause_button_height)),
        text="(B)indings",
        manager=display.uiManager,
        starting_height=1000)
    quit.action = 'b'

    button_num += 1
    save = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height +
             (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
             pause_button_width, pause_button_height)),
        text="(S)ave",
        manager=display.uiManager,
        starting_height=1000)
    save.action = 's'

    button_num += 1
    quit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (pause_button_offset_from_left, pause_button_offset_from_top + pause_button_offset_from_each_other_height +
             (pause_button_height + pause_button_offset_from_each_other_height) * button_num,
             pause_button_width, pause_button_height)),
        text="(Q)uit",
        manager=display.uiManager,
        starting_height=1000)
    quit.action = 'q'