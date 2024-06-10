import pygame, pygame_gui
from .action_screen import *

def create_quickcast_select(display, loop):
    player = loop.player
    entity = player.mage.known_spells[loop.current_spell]
    tileDict = loop.tileDict
    player = loop.player    
    spell = entity
    
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
    

    # pygame.draw.rect(self.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))
    pygame.draw.rect(display.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))

    display.win.blit(entity_image, (entity_image_offset_from_left, entity_image_offset_from_top))

    display.draw_escape_button(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height)

    entity_name = entity.name
    pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((entity_message_offset_from_left, entity_message_offset_from_top),
                                        (entity_message_width, entity_message_height)),
            text=entity_name,
            manager=display.uiManager,
            object_id='#title_small')

    entity_text = ""
    entity_text += entity.full_description()  + "<br><br>"

    entity_text += f"Select 1-7 to assign {spell.name} a quickcast slot"    

    create_skill_bar(display, loop, display_empty=True)


    text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((entity_text_offset_from_left, entity_text_offset_from_top), (entity_text_width, entity_text_height)),
            html_text = entity_text,
            manager=display.uiManager)

    display.uiManager.draw_ui(display.win)

def update_quickcast_select(loop):
    display = loop.display
    tileDict = loop.tileDict
    player = loop.player
    entity = player.mage.known_spells[loop.current_spell]

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

    display.update_screen(loop)

    entity_image = pygame.transform.scale(tileDict.tiles[entity.render_tag],
                                    (entity_image_width, entity_image_height))

    pygame.draw.rect(display.win, (112,128,144), pygame.Rect(entity_offset_from_left, entity_offset_from_top, entity_screen_width, entity_screen_height))

    display.win.blit(entity_image, (entity_image_offset_from_left, entity_image_offset_from_top))

    display.uiManager.draw_ui(display.win)