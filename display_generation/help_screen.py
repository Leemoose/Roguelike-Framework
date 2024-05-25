import pygame, pygame_gui

def create_help_screen(display, loop):
    button_width = display.screen_width // 4
    button_height = display.screen_height // 8
    button_offset_from_bottom = display.screen_height * 95 // 100 - button_height
    button_offset_from_left = (display.screen_width -button_width) // 2

    message_width = display.screen_width // 2
    message_height = display.screen_height // 2
    message_offset_from_left = display.screen_width // 4
    message_offset_from_top = display.screen_height // 4

    title_width = display.screen_width // 2
    title_height = display.screen_height // 10
    title_offset_from_left = display.screen_width // 4
    title_offset_from_top = display.screen_height // 10

    display.uiManager.clear_and_reset()

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((button_offset_from_left, button_offset_from_bottom), (button_width, button_height)),
        text='Return to Main Menu',
        manager=display.uiManager)
    button.action = "esc"

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((title_offset_from_left, title_offset_from_top), (title_width, title_height)),
        text="Action Shortcuts",
        manager=display.uiManager,
        object_id='#title_label')

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((message_offset_from_left, message_offset_from_top), (message_width, message_height)),
        html_text="Action Screen: <br>" +
                  "Inventory: i || Equipments: e || Potions: q || Scrolls: r <br>" +
                  "Autoexplore: o || Find Stairs: s || Wait: . || Rest: z <br>" +
                  "Examine: x || Save: / || Pause: esc <br>" +
                  "Grab: g || Allocate stats: l <br>" +
                  "Downstairs: > || Upstairs: < <br>" +
                  "Skills: 1-8 <br>" +
                  "Up / Down / Left / Right --> Arrow keys <br>" +
                  "Up - Left / Up - Right / Down - Left / Down - Right --> y / u / n / b <br>"
        ,
        manager=display.uiManager
    )
