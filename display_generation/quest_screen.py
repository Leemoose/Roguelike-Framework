import pygame, pygame_gui

def create_quest_screen(display, loop):
    display.uiManager.clear_and_reset()

    trading_screen_width = display.screen_width * 2 // 3
    trading_screen_height = display.screen_height * 2 // 3
    trading_offset_from_left = (display.screen_width - trading_screen_width) // 2
    trading_offset_from_top = (display.screen_height - trading_screen_height) // 2

    trading_title_width = trading_screen_width
    trading_title_height = trading_screen_height // 6
    trading_title_offset_from_left = trading_offset_from_left
    trading_title_offset_from_top = trading_offset_from_top

    num_option_buttons = len(loop.player.quests)
    option_button_offset_from_left = trading_offset_from_left
    option_button_offset_from_top = trading_title_offset_from_top + trading_title_height
    option_button_width = min((trading_screen_width) // (num_option_buttons + 1), 300)
    option_button_height =((trading_screen_height - trading_title_height) // 8)
    option_margin_between_buttons_width = (option_button_width) // (num_option_buttons + 1)

    message_width = trading_screen_width
    message_offset_from_left = trading_offset_from_left
    message_offset_from_top = option_button_offset_from_top + option_button_height + 10
    message_height = display.screen_height - message_offset_from_top - trading_offset_from_top

    pygame.draw.rect(display.win, (50, 50, 50),
                     pygame.Rect(trading_offset_from_left - 10, trading_offset_from_top - 10, trading_screen_width + 20,
                                 trading_screen_height + 20))
    pygame.draw.rect(display.win, (0, 0, 0),
                     pygame.Rect(trading_offset_from_left, trading_offset_from_top, trading_screen_width,
                                 trading_screen_height))

    display.draw_escape_button(trading_offset_from_left, trading_offset_from_top, trading_screen_width,
                            trading_screen_height)
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((trading_title_offset_from_left, trading_title_offset_from_top),
                                  (trading_title_width, trading_title_height)),
        text="Active Quests",
        manager=display.uiManager,
        object_id='#title_label')
    text = ""
    if display.quest_number < 1 or display.quest_number > len(loop.player.quests):
        print("The current quest number does not line up with something that can be displayed")
    else:
        text = loop.player.quests[display.quest_number - 1].get_description()

    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((message_offset_from_left, message_offset_from_top), (message_width, message_height)),

        html_text=text
        ,
        manager=display.uiManager
    )

    options = loop.player.quests
    for i in range(len(options)):
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((option_button_offset_from_left + option_margin_between_buttons_width + i * (
                        option_margin_between_buttons_width + option_button_width),
                                       option_button_offset_from_top),
                                      (option_button_width, option_button_height)),
            text=chr(ord("1") + i) + ". " + "{}".format(options[i].name),
            manager=display.uiManager)
        button.action = chr(ord("1") + i)
