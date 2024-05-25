import pygame, pygame_gui

def create_story_screen(display, loop):
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
        text="The Story So Far",
        manager=display.uiManager,
        object_id='#title_label')

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((message_offset_from_left, message_offset_from_top), (message_width, message_height)),
        html_text=
        "Awakened by recent excavations, a terrible evil has descened up on the land. <br><br>" +
        "The ORB of YENDORB - an ancient, malignant artifact designed to bring orbiness<br>" +
        "into the world. The device has grown a dungeon around itdisplay, and filled it<br>" +
        "with unspeakable horrors to defend it. While it waits, it expands its magical power - <br>" +
        "should it finish charging, all of existence will be made round.<br><br>" +
        "As a Cornerian knight, you cannot let this evil continue! Delve deep into this<br>" +
        "incomprehensible place, where roundess is power. Slay the aberrations that defend it, and<br>" +
        "retrieve the orb before it completes its task. The fate of the world depends on you!<br>"
        ,
        manager=display.uiManager
    )