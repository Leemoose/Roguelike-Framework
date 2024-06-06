import pygame, pygame_gui
from .action_screen import *

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

def update_spell_window(loop, create = False):
    player = loop.player
    entity = player.mage.known_spells[loop.current_spell]
    tileDict = loop.tileDict
    display = loop.display
    player = loop.player
    if create == True:
        display.uiManager.clear_and_reset()
    display.win.fill((0,0,0))
    entity_screen_width = display.screen_width // 2
    entity_screen_height = display.screen_height // 2
    entity_offset_from_left = display.screen_width // 4
    entity_offset_from_top = display.screen_height // 4

    entity_message_width = display.screen_width // 2
    entity_message_height = display.screen_height // 10
    entity_message_offset_from_left = display.screen_width // 4
    entity_message_offset_from_top = display.screen_height  // 4

    entity_image_width = display.screen_width // 20
    entity_image_height = display.screen_width // 20
    entity_image_offset_from_left = display.screen_width // 4 + display.screen_width // 50
    entity_image_offset_from_top = display.screen_height // 4

    entity_button_width = display.screen_width // 10
    entity_button_height = display.screen_height // 30
    entity_button_offset_from_left = (display.screen_width) // 2 - entity_button_width * 3 //2
    entity_button_offset_from_top = entity_screen_height + entity_offset_from_top - entity_button_height - display.screen_height // 50
    entity_button_offset_from_each_other =  entity_button_width // 2

    entity_text_offset_from_left = entity_offset_from_left + entity_screen_width // 20
    entity_text_offset_from_top = entity_image_offset_from_top + entity_message_height
    entity_text_width = entity_screen_width * 11 // 12
    entity_text_height = entity_screen_height * 3 // 5
    entity_image = pygame.transform.scale(tileDict.tiles[entity.render_tag],
                                    (entity_image_width, entity_image_height))

    pygame.draw.rect(display.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))

    display.win.blit(entity_image, (entity_image_offset_from_left, entity_image_offset_from_top))

    if (create == True):
        display.draw_escape_button(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height)

    entity_name = entity.name
    if create == True:
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                        (entity_message_width, entity_message_height)),
            text=entity_name,
            manager=display.uiManager,
            object_id='#title_small')

    entity_text = ""
    entity_text += entity.full_description()  + "<br><br>"

    if create == True:
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((entity_button_offset_from_left, entity_button_offset_from_top),
                                              (entity_button_width, entity_button_height)),
                    text="Cast",
                    manager=display.uiManager)
        button.action = "c"
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((entity_button_offset_from_left + (entity_button_width + entity_button_offset_from_each_other), entity_button_offset_from_top),
                                              (entity_button_width, entity_button_height)),
                    text="Set (q)uickcast",
                    manager=display.uiManager)
        button.action = "q"

    if create == True:
        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((entity_text_offset_from_left, entity_text_offset_from_top), (entity_text_width, entity_text_height)),
            html_text = entity_text,
            manager=display.uiManager)

    display.uiManager.draw_ui(display.win)

def update_quickselect(loop, create=True):
    display = loop.display
    display.uiManager.clear_and_reset()
    display.win.fill((0,0,0))

    player = loop.player
    spell = player.mage.known_spells[loop.current_spell]
    entity = spell
    tileDict = loop.tileDict
    entity_screen_width = display.screen_width // 2
    entity_screen_height = display.screen_height // 4
    entity_offset_from_left = display.screen_width // 4
    entity_offset_from_top = display.screen_height // 4

    entity_message_width = entity_screen_width // 2
    entity_message_height = entity_screen_height // 10
    entity_message_offset_from_left = entity_offset_from_left + entity_screen_width // 4
    entity_message_offset_from_top = entity_offset_from_top + entity_screen_height // 30

    border_width = 8
    border_height = 8
    if create == True:
        display.uiManager.clear_and_reset()
    display.win.fill((0,0,0))
    entity_screen_width = display.screen_width // 2
    entity_screen_height = display.screen_height // 2
    entity_offset_from_left = display.screen_width // 4
    entity_offset_from_top = display.screen_height // 4

    entity_message_width = display.screen_width // 2
    entity_message_height = display.screen_height // 10
    entity_message_offset_from_left = display.screen_width // 4
    entity_message_offset_from_top = display.screen_height  // 4

    entity_image_width = display.screen_width // 20
    entity_image_height = display.screen_width // 20
    entity_image_offset_from_left = display.screen_width // 4 + display.screen_width // 50
    entity_image_offset_from_top = display.screen_height // 4

    entity_button_width = display.screen_width // 10
    entity_button_height = display.screen_height // 30
    entity_button_offset_from_left = (display.screen_width) // 2 - entity_button_width * 3 //2
    entity_button_offset_from_top = entity_screen_height + entity_offset_from_top - entity_button_height - display.screen_height // 50
    entity_button_offset_from_each_other =  entity_button_width // 2

    entity_text_offset_from_left = entity_offset_from_left + entity_screen_width // 20
    entity_text_offset_from_top = entity_image_offset_from_top + entity_message_height
    entity_text_width = entity_screen_width * 11 // 12
    entity_text_height = entity_screen_height * 3 // 5
    entity_image = pygame.transform.scale(tileDict.tiles[entity.render_tag],
                                    (entity_image_width, entity_image_height))

    pygame.draw.rect(display.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))

    display.win.blit(entity_image, (entity_image_offset_from_left, entity_image_offset_from_top))

    if (create == True):
        display.draw_escape_button(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height)

    entity_name = entity.name
    if create == True:
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                        (entity_message_width, entity_message_height)),
            text=entity_name,
            manager=display.uiManager,
            object_id='#title_small')

    entity_name = entity.name
    if create == True:
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                        (entity_message_width, entity_message_height)),
            text=entity_name,
            manager=display.uiManager,
            object_id='#title_small')
        
    entity_text = ""
    entity_text += entity.full_description()  + "<br><br>"

    entity_text += f"Select 1-7 to assign {spell.name} a quickcast slot"    

    if create == True:
        text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((entity_text_offset_from_left, entity_text_offset_from_top), (entity_text_width, entity_text_height)),
            html_text = entity_text,
            manager=display.uiManager)

    create_skill_bar(display, loop)

    display.uiManager.draw_ui(display.win)
    
