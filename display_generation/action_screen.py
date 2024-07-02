import pygame_gui, pygame

from .ui import FPSCounter, MessageBox, DepthDisplay, StatBox, SkillButton, HealthBar, ManaBar

def create_skill_bar(display, loop, display_empty=False):
    player = loop.player
    tileDict = loop.tileDict

    action_screen_width = display.screen_width * 3 // 4
    action_screen_height = display.screen_height * 5 // 6

    message_offset_from_left = 0
    message_width = action_screen_width * 5 // 12 - 2 * message_offset_from_left

    stats_offset_from_left = action_screen_width

    skill_bar_height = display.screen_height - action_screen_height
    skill_bar_offset_from_left = message_offset_from_left + message_width
    skill_bar_width = stats_offset_from_left - skill_bar_offset_from_left
    skill_bar_offset_from_top = action_screen_height

    num_skill_buttons = len(player.mage.quick_cast_spells) + 1
    skill_button_width = (action_screen_width - skill_bar_offset_from_left) // (num_skill_buttons + 1)
    skill_button_height = (display.screen_height - action_screen_height) * 3 // 4
    skill_button_offset_from_top = (display.screen_height - action_screen_height) // 8 + skill_bar_offset_from_top
    skill_button_offset_from_each_other_width = (action_screen_width - skill_bar_offset_from_left) // (
                num_skill_buttons + 1) // (num_skill_buttons + 1)
    
    num_skill = len(player.mage.quick_cast_spells) + 1
    if player.mage.quick_cast_spells.count(None) == len(player.mage.quick_cast_spells):
        display.draw_empty_box(skill_bar_offset_from_left,
                            skill_bar_offset_from_top,
                            skill_bar_width, skill_bar_height)
    else:
        display.draw_empty_box(skill_bar_offset_from_left,
                            skill_bar_offset_from_top,
                            skill_bar_width, skill_bar_height)
        for i, skill in enumerate(player.mage.quick_cast_spells):
            if skill == None:
                if display_empty:
                    img1 = None
                    img2 = None
                else:
                    continue
            else:
                img1 = pygame.transform.scale(tileDict.tiles[skill.render_tag],
                                            (skill_button_width, skill_button_height))
                img2 = pygame.transform.scale(tileDict.tiles[-skill.render_tag],
                                            (skill_button_width, skill_button_height))
            button = SkillButton(
                rect=pygame.Rect((
                    skill_bar_offset_from_left + skill_button_offset_from_each_other_width + (
                                skill_button_offset_from_each_other_width + skill_button_width) * i,
                    skill_button_offset_from_top),
                    (skill_button_width, skill_button_height)),
                manager=display.uiManager,
                player=player,
                index=i,
                img1=img1,
                img2=img2,
                loop=loop,
                object_id='#skill_button')
            button.action = chr(ord("1") + i)
            # display.draw_on_button(button, img, chr(ord("1") + i), (skill_button_width, skill_button_height), shrink=True,
            #                     offset_factor=10, text_offset=(12, (0.6)))
        button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((
                        skill_bar_offset_from_left + skill_button_offset_from_each_other_width + (
                                    skill_button_offset_from_each_other_width + skill_button_width) * (num_skill - 1),
                        skill_button_offset_from_top),
                        (skill_button_width, skill_button_height)),
                text="All S(p)ells",
                manager=display.uiManager,
                starting_height=800)
        button.action = "p"

def create_display(display, loop):
    display.uiManager.clear_and_reset()
    fps_counter = FPSCounter(
        pygame.Rect((0, 0), (400, 40)),
        display.uiManager
    )

    tileDict = loop.tileDict
    player = loop.player
    messages = loop.messages

    action_screen_width = display.screen_width * 3 // 4
    action_screen_height = display.screen_height * 5 // 6
    num_tiles_wide = action_screen_width // display.textSize
    num_tiles_height = action_screen_height // display.textSize

    r_x = num_tiles_wide // 2
    r_y = num_tiles_height // 2

    display.x_start = player.x - r_x
    display.x_end = player.x + r_x
    display.y_start = player.y - r_y
    display.y_end = player.y + r_y

    stats_offset_from_left = action_screen_width
    stats_offset_from_top = 0
    stats_width = display.screen_width - stats_offset_from_left
    stats_height = display.screen_height // 3

    map_tile_size = 8
    map_offset_from_left = action_screen_width
    map_offset_from_top = stats_height
    map_width = display.screen_width - action_screen_width
    map_message_width = stats_width
    map_height = display.screen_height // 3
    map_message_height = 30
    num_map_tiles_wide = map_width // map_tile_size
    num_map_tiles_height = map_height // map_tile_size
    r_map_x = num_map_tiles_wide // 2
    r_map_y = num_map_tiles_height // 2

    message_offset_from_left = 0
    message_offset_from_top = action_screen_height
    message_width = action_screen_width * 5 // 12 - 2 * message_offset_from_left
    message_height = display.screen_height - action_screen_height

    views_num_buttons_height = 2
    views_num_buttons_width = 3
    views_offset_from_left = action_screen_width
    views_offset_from_top = map_offset_from_top + map_height
    views_width = (display.screen_width - action_screen_width)
    views_height = (display.screen_height - map_offset_from_top - map_height)
    views_button_width = (display.screen_width - action_screen_width) // (views_num_buttons_width + 1)
    views_button_height = (display.screen_height - map_offset_from_top - map_height) // (views_num_buttons_height + 1)
    views_button_offset_from_each_other_height = (display.screen_height - map_offset_from_top - map_height) // (
            views_num_buttons_height + 1) // (views_num_buttons_height + 1)
    views_button_offset_from_each_other_width = (display.screen_width - action_screen_width) // (
            views_num_buttons_width + 1) // (views_num_buttons_width + 1)

    # Writing messages
    text_box = MessageBox(
        pygame.Rect((message_offset_from_left, message_offset_from_top),
                    (message_width, message_height)),
        manager=display.uiManager,
        loop=loop)

    # Map box
    display.draw_empty_box(map_offset_from_left,
                        map_offset_from_top,
                        map_width, map_height)

    # Depth
    display.depth_label = DepthDisplay(pygame.Rect((map_offset_from_left, map_offset_from_top),
                                           (map_message_width, map_message_height)),
                               manager=display.uiManager,
                               loop=loop)

    stat_box = StatBox(
        pygame.Rect((stats_offset_from_left, stats_offset_from_top), (stats_width, stats_height)),
        display.uiManager,
        player
    )

    button_num_height = 0
    button_num_width = 0
    display.draw_empty_box(views_offset_from_left,
                        views_offset_from_top,
                        views_width, views_height)
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((
            views_offset_from_left + views_button_offset_from_each_other_width + (
                        views_button_offset_from_each_other_width + views_button_width) * button_num_width,
            views_offset_from_top + views_button_offset_from_each_other_height + (
                        views_button_offset_from_each_other_height + views_button_height) * button_num_height),
            (views_button_width, views_button_height)),
        text="(I)nventory",
        manager=display.uiManager,
        starting_height=800)
    button.action = "i"

    button_num_height += 1
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((
            views_offset_from_left + views_button_offset_from_each_other_width + (
                        views_button_offset_from_each_other_width + views_button_width) * button_num_width,
            views_offset_from_top + views_button_offset_from_each_other_height + (
                        views_button_offset_from_each_other_height + views_button_height) * button_num_height),
            (views_button_width, views_button_height)),
        text="(E)quip",
        manager=display.uiManager,
        starting_height=800)
    button.action = "e"

    button_num_height = 0
    button_num_width += 1
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((
            views_offset_from_left + views_button_offset_from_each_other_width + (
                        views_button_offset_from_each_other_width + views_button_width) * button_num_width,
            views_offset_from_top + views_button_offset_from_each_other_height + (
                        views_button_offset_from_each_other_height + views_button_height) * button_num_height),
            (views_button_width, views_button_height)),
        text="Rest(z)",
        manager=display.uiManager,
        starting_height=800)
    button.action = "z"

    button_num_height += 1

    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((
            views_offset_from_left + views_button_offset_from_each_other_width + (
                        views_button_offset_from_each_other_width + views_button_width) * button_num_width,
            views_offset_from_top + views_button_offset_from_each_other_height + (
                        views_button_offset_from_each_other_height + views_button_height) * button_num_height),
            (views_button_width, views_button_height)),
        text="Aut(o)explore",
        manager=display.uiManager,
        starting_height=800)
    button.action = "o"

    button_num_height = 0
    button_num_width += 1
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((
            views_offset_from_left + views_button_offset_from_each_other_width + (
                        views_button_offset_from_each_other_width + views_button_width) * button_num_width,
            views_offset_from_top + views_button_offset_from_each_other_height + (
                        views_button_offset_from_each_other_height + views_button_height) * button_num_height),
            (views_button_width, views_button_height)),
        text="Pause(esc)",
        manager=display.uiManager,
        starting_height=800)
    button.action = "esc"



    # if target_to_display != None:
    #    clear_target = display.draw_examine_window(target_to_display, tileDict, floormap, monster_map, monsterID, item_ID, player)
    #    if clear_target:
    #        target_to_display = None

    create_skill_bar(display, loop)

    healthBar = HealthBar(
        pygame.Rect((stats_offset_from_left + 70, stats_offset_from_top + 12), (stats_width // 3, stats_height // 12)),
        display.uiManager, player)
    manaBar = ManaBar(
        pygame.Rect((stats_offset_from_left + 70, stats_offset_from_top + 38), (stats_width // 3, stats_height // 12)),
        display.uiManager, player)
