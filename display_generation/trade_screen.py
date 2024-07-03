import pygame, pygame_gui

from .ui import MessageBox, DialogueInteraction
def create_trade_screen(display, loop):
    display.uiManager.clear_and_reset()

    trading_screen_width = display.screen_width // 9 * 4
    trading_screen_height = display.screen_height // 9 * 4
    trading_offset_from_left = (display.screen_width - trading_screen_width) // 2
    trading_offset_from_top = (display.screen_height - trading_screen_height) // 2

    trading_title_width = trading_screen_width
    trading_title_height = trading_screen_height // 5
    trading_title_offset_from_left = trading_offset_from_left
    trading_title_offset_from_top = trading_offset_from_top

    num_buttons_height = 4
    num_buttons_width = 8
    button_offset_from_left = trading_offset_from_left + trading_screen_width // 2
    button_offset_from_top = trading_title_offset_from_top + trading_title_height
    button_width = (trading_screen_width // 2) // (num_buttons_width + 1)
    button_height =((trading_screen_height - trading_title_height) * 2 // 3) // (num_buttons_height + 1)
    margin_between_buttons_height = ((trading_screen_height - trading_title_height) * 2 // 3) // (
                num_buttons_height + 1) // (num_buttons_height + 1)
    margin_between_buttons_width = (trading_screen_width // 2) // (num_buttons_width + 1) // (num_buttons_width + 1)

    num_option_buttons = len(loop.npc_focus.options)
    option_button_offset_from_left = trading_offset_from_left
    option_button_offset_from_top = trading_title_offset_from_top + trading_title_height
    option_button_width = (trading_screen_width // 4)
    option_button_height = min(((trading_screen_height - trading_title_height) * 2 // 3) // (num_option_buttons + 1),
                               100)
    option_margin_between_buttons_height = ((trading_screen_height - trading_title_height) * 2 // 3) // (
            num_option_buttons + 1) // (num_option_buttons + 1)

    message_width = trading_screen_width
    message_offset_from_left = trading_offset_from_left
    message_offset_from_top = button_offset_from_top + (trading_screen_height - trading_title_height) * 2 // 3
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
        text=loop.npc_focus.name,
        manager=display.uiManager,
        object_id='#title_label')
        
    # text_box = MessageBox(
    #     pygame.Rect((message_offset_from_left, message_offset_from_top),
    #                 (message_width, message_height)),
    #     manager=display.uiManager,
    #     loop=loop)

    # options = loop.npc_focus.options
    # for i in range(num_option_buttons):
    #     button = pygame_gui.elements.UIButton(
    #         relative_rect=pygame.Rect((option_button_offset_from_left,
    #                                    option_button_offset_from_top + option_margin_between_buttons_height + i * (
    #                                                option_margin_between_buttons_height + option_button_height)),
    #                                   (option_button_width, option_button_height)),
    #         text=chr(ord("1") + i) + ". " + options[i],
    #         manager=display.uiManager)
    #     button.action = chr(ord("1") + i)

    if loop.npc_focus.purpose == "trade":
        for i, weapon in enumerate(loop.npc_focus.items):
            img = pygame.transform.scale(loop.tileDict.tiles[weapon.render_tag], (button_width, button_height))
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_offset_from_left + margin_between_buttons_width + (
                            i // num_buttons_height) * (margin_between_buttons_width + button_width),
                                           button_offset_from_top + margin_between_buttons_height + (
                                                       i % num_buttons_height) * (
                                                       margin_between_buttons_height + button_height)),
                                          (button_width, button_height)),
                text=str(weapon.name),
                manager=display.uiManager,
                object_id='#equipment_button')
            display.draw_on_button(button, img, chr(ord("a") + i), (button_width, button_height))
            button.action = chr(ord("a") + i)

    else:
        player_offset_left = trading_offset_from_left + trading_screen_width // 15
        player_offset_top = trading_offset_from_top + trading_screen_height // 5 * 4
        player_size = trading_screen_width // 10
        display.draw_player(loop, player_offset_left, player_offset_top, player_size)

        npc = loop.npc_focus
        npc_tile = loop.tileDict.tile_string(npc.render_tag)
        npc_offset_left = trading_offset_from_left + trading_screen_width // 11 * 9
        display.win.blit(pygame.transform.scale(npc_tile, (player_size, player_size)), (npc_offset_left, player_offset_top))

        dialogue_window_width = trading_screen_width // 5 * 3
        dialogue_window_height = trading_screen_height // 5 * 4
        dialogue_window_offset_left = trading_offset_from_left + trading_screen_width // 5
        dialogue_window_offset_top = trading_offset_from_top + trading_screen_height // 6

        dialogue_panel = DialogueInteraction(
                            rect=pygame.Rect((dialogue_window_offset_left, dialogue_window_offset_top), 
                                                    (dialogue_window_width, dialogue_window_height)),
                            manager=display.uiManager,
                            loop=loop,
                            npc=loop.npc_focus,
                            max_messages=4,
                            bubble_gap=dialogue_window_height // 20)

        display.uiManager.draw_ui(display.win)
