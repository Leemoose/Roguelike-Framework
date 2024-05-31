import pygame, pygame_gui

def create_class_screen(display, loop):
    display.uiManager.clear_and_reset()

    class_screen_width = display.screen_width * 2 // 3
    class_screen_height = display.screen_height * 2 // 3
    class_offset_from_left = (display.screen_width - class_screen_width) // 2
    class_offset_from_top = (display.screen_height - class_screen_height) // 2

    class_title_width = class_screen_width
    class_title_height = class_screen_height // 6
    class_title_offset_from_left = class_offset_from_left
    class_title_offset_from_top = class_offset_from_top

    num_option_buttons = 3
    option_button_offset_from_left = class_offset_from_left
    option_button_offset_from_top = class_title_offset_from_top + class_title_height
    option_button_width = min((class_screen_width) // (num_option_buttons + 1), 300)
    option_button_height =((class_screen_height - class_title_height) // 8)
    option_margin_between_buttons_width = (option_button_width) // (num_option_buttons + 1)

    message_width = class_screen_width
    message_offset_from_left = class_offset_from_left
    message_offset_from_top = option_button_offset_from_top + option_button_height + 10
    message_height = display.screen_height - message_offset_from_top - class_offset_from_top

    pygame.draw.rect(display.win, (50, 50, 50),
                     pygame.Rect(class_offset_from_left - 10, class_offset_from_top - 10, class_screen_width + 20,
                                 class_screen_height + 20))
    pygame.draw.rect(display.win, (0, 0, 0),
                     pygame.Rect(class_offset_from_left, class_offset_from_top, class_screen_width,
                                 class_screen_height))

    display.draw_escape_button(class_offset_from_left, class_offset_from_top, class_screen_width,
                            class_screen_height)
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((class_title_offset_from_left, class_title_offset_from_top),
                                  (class_title_width, class_title_height)),
        text="Classes",
        manager=display.uiManager,
        object_id='#title_label')

    if loop.class_selection == None:
        text = "Choose a class above."
    else:
        chosen_class = loop.class_selection
        text = ""
        text += chosen_class.name + ":\n"
        text += "Description: " + chosen_class.get_description() + "\n"
        text += "Spells: "
        for spell in chosen_class.get_spell_names():
            text += spell
        text += "\n"
        text += "Items: "
        for item in chosen_class.get_items():
            text += item.name
        text += "\n"


    text_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((message_offset_from_left, message_offset_from_top), (message_width, message_height)),

        html_text=text
        ,
        manager=display.uiManager
    )

    options = loop.get_available_classes()
    for i in range(len(options)):
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((option_button_offset_from_left + option_margin_between_buttons_width + i * (
                        option_margin_between_buttons_width + option_button_width),
                                       option_button_offset_from_top),
                                      (option_button_width, option_button_height)),
            text=chr(ord("1") + i) + ". " + "{}".format(options[i].name),
            manager=display.uiManager)
        button.action = chr(ord("1") + i)
