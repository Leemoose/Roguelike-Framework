import pygame, pygame_gui

def create_spellcasting(display, loop):
    player = loop.player

    display.uiManager.clear_and_reset()
    display.win.fill((0, 0, 0))
    spell_screen_width = display.screen_width // 2
    spell_screen_height = display.screen_height
    spell_offset_from_left = display.screen_width // 4
    spell_offset_from_top = 0

    spell_message_width = display.screen_width // 2
    spell_message_height = display.screen_height // 10
    spell_message_offset_from_left = display.screen_width // 4
    spell_message_offset_from_top = display.screen_height // 30

    spell_button_width = display.screen_width // 5
    spell_button_height = display.screen_height // 30
    spell_button_offset_from_left = display.screen_width * 2 // 5
    spell_button_offset_from_top = display.screen_height // 10 + display.screen_height // 30 + display.screen_height // 30
    spell_button_offset_from_each_other = display.screen_height // 100

    display.uiManager.clear_and_reset()
    pygame.draw.rect(display.win, (0, 0, 0),
                     pygame.Rect(spell_offset_from_left, spell_offset_from_top, spell_screen_width,
                                 spell_screen_height))

    display.draw_escape_button(spell_button_offset_from_left, spell_button_offset_from_top, spell_screen_width,
                            spell_screen_height)

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((spell_message_offset_from_left, spell_message_offset_from_top),
                                  (spell_message_width, spell_message_height)),
        text="Known Spells",
        manager=display.uiManager,
        object_id='#title_label')


    # This needs to be fixed
    for i, spell in enumerate(player.mage.known_spells):
        spell_name = spell.name
        if 1==1:
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((spell_button_offset_from_left,
                                           spell_button_offset_from_top + spell_button_offset_from_each_other * i + spell_button_height * i),
                                          (spell_button_width, spell_button_height)),
                text=chr(ord("a") + i) + ". " + spell_name,
                manager=display.uiManager)
            button.action = chr(ord("a") + i)

    display.uiManager.draw_ui(display.win)
