import pygame, pygame_gui
import random
from npc import BobBrother
from copy import deepcopy

class HealthBar(pygame_gui.elements.UIProgressBar):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager)
        self.player = player
        self.health = -1
        self.max_health = -1

    def needs_update(self, character):
        if (self.health != character.health or self.max_health != character.max_health):
            self.health = character.health
            self.max_health = character.max_health
            return True
        return False

    def update(self, time_delta: float):
        if (self.needs_update(self.player.character)):
            self.maximum_progress = max(1.0, self.player.character.max_health)
            self.current_progress = self.player.character.health
            self.percent_full = self.current_progress / self.maximum_progress

        return super().update(time_delta)
    
class ManaBar(pygame_gui.elements.UIProgressBar):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager)
        self.player = player
        self.mana = -1
        self.max_mana = -1

    def needs_update(self, character):
        if (self.mana != character.mana or self.max_mana != character.max_mana):
            self.mana = character.mana
            self.max_mana = character.max_mana
            return True
        return False

    def update(self, time_delta: float):
        if (self.needs_update(self.player.character)):
            self.maximum_progress = max(1.0, self.player.character.max_mana)
            self.current_progress = self.player.character.mana
            self.percent_full = 100 * self.current_progress / self.maximum_progress

        return super().update(time_delta)
    
class FPSCounter(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager):
        super().__init__(relative_rect=rect, manager=manager, text="Debug")
        self.times = []
        self.FPS = 0.0
        self.best = 0.0
        self.worst = 1000.0
        
    def compute_values(self):
        average = 0.0
        lowest = 1000
        highest = 0.0
        for val in self.times:
            average += val
            if (val < lowest):
                lowest = val
            if (val > highest):
                highest = val
        self.FPS = 1 / (average / len(self.times))
        self.best = 1 / max(1,lowest)
        self.worst = 1 / highest

    def truncate(self, f, n):
        #Truncates/pads a float f to n decimal places without rounding
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])


    def update(self, time_delta: float):
        self.times.append(time_delta)
        if (len(self.times) > 300):
            self.times.pop(0)

        self.compute_values()

        self.set_text("FPS:   " + self.truncate(self.FPS, 2) + "    " +
                      "Worst: " + self.truncate(self.worst, 2) + "    " +
                      "Best:  " + self.truncate(self.best, 2))

        return super().update(time_delta)
    
class MessageBox(pygame_gui.elements.UITextBox):
    def __init__(self, rect, manager, loop):
        super().__init__(relative_rect=rect, manager=manager, html_text="Error")
        self.loop = loop #Store loop to retrieve messages
        self.set_message()

    def update(self, time_delta: float):
        if (self.loop.dirty_messages):
            self.set_message()

        return super().update(time_delta)
    
    def set_message(self):
        text = "".join([message[0] + "<br>" for message in (self.loop.messages)])
        text = text[:-3] #Remove last <br>
        self.set_text(html_text=text)
        self.loop.dirty_messages = False

class DialogueButton(pygame_gui.elements.UIButton):
    def __init__(self, rect, manager, object_id, container, color=(252, 252, 252), text="...", left=False):
        super().__init__(relative_rect=rect, manager=manager, container=container, text=text, object_id=object_id,
                    starting_height=900)
        self.active_state = self.drawable_shape.active_state
        self.loop = None
        self.text = text
        self.left = left
        self.color = color


    def draw_speech_bubble(self, surface, text, bubble_width, bubble_height, color, left=True):
        bubble_color = color
        border_radius = 50
        padding = 10

        surface.fill((0, 0, 0, 0))

        # Draw the rounded rectangle
        pygame.draw.rect(surface, bubble_color, (0, 0, bubble_width, bubble_height), border_top_left_radius=border_radius, 
                                                                                    border_top_right_radius=border_radius, 
                                                                                    border_bottom_left_radius=border_radius * (not left),
                                                                                    border_bottom_right_radius= border_radius * (left))

        # Blit the text onto the bubble
        font = pygame.font.Font(None, 24)
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + ' ' + word
            if font.size(test_line)[0] <= bubble_width - 2 * padding:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        y_offset = padding
        for line in lines:
            text_surface = font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(padding, y_offset))
            surface.blit(text_surface, text_rect)
            y_offset += font.get_height()

    def draw_on_all_surfaces(self, text, left, color):
        button_surface = self.image
        for state in ["normal", "hovered", "disabled", "selected", "active"]:
            self.draw_speech_bubble(self.drawable_shape.states[state].surface, text, button_surface.get_width(), button_surface.get_height(), color, left)
            self.drawable_shape.active_state.has_fresh_surface = True

    def update(self, time_delta: float):
        if self.active_state != self.drawable_shape.active_state:
            self.draw_on_all_surfaces(self.text, self.left, self.color)

        return super().update(time_delta)

class DialogueInteraction(pygame_gui.elements.UIPanel):
    def __init__(self, rect, manager, loop, npc, max_messages, bubble_gap):
        super().__init__(relative_rect=rect, manager=manager)
        self.loop = loop #Store loop to retrieve messages
        self.npc = npc
        # load dialogue queue from npc object
        self.dialogue_queue = npc.dialogue_queue
        self.next_y_position = bubble_gap
        self.bubble_gap = bubble_gap
        self.bubble_padding = bubble_gap // 2
        self.dialogue_next = False
        self.max_messages = max_messages
        self.text_boxes = []
        self.prev_text_boxes = None
        if self.npc.dialogue_memory == []:
            self.next_dialogue()
        else:
            curr_memory = deepcopy(self.npc.dialogue_memory)
            for mem in curr_memory:
                self.npc.dialogue_memory.pop(0) # need to pop original memory so we don't store duplicates
                self.add_dialogue(*mem) # unpack stored tuple into arguments for function with *
        
        label_width = rect.width * 0.9
        label_height = rect.height * 0.15
        label_x = (rect.width - label_width) / 2
        label_y = rect.height - label_height
        self.continue_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((label_x, label_y), (label_width, label_height)),
            text="(Press Enter or Click to continue)",
            manager=manager,
            container=self
        )

    def clear_last_player_dialogue(self):
        prev_options = [] # keep track of all removed player dialogue so we can readd the selected option
        num_to_delete = self.loop.dialogue_options
        for i in range(len(self.text_boxes)):
            tbox, left = self.text_boxes[-1] # don't iterate cuz that will mess stuff up, just keep popping 0th elem
            if i >= num_to_delete or not left:
                break
            prev_options.append(tbox.text)
            tbox.kill()
            self.text_boxes.pop(-1)
            self.npc.dialogue_memory.pop(-1)
        self.update_textbox_positions()
        prev_options.reverse() # because we remove them from end, we build prev options list in reverse order and need to flip it
        return prev_options


    def update_textbox_positions(self):
        self.next_y_position = self.bubble_gap
        for i, (tb, old_left) in enumerate(self.text_boxes):
            tb_width = tb.get_relative_rect().width
            tb_height = tb.get_relative_rect().height
            x_position = self.bubble_padding if old_left else self.get_relative_rect().width - tb_width - (self.bubble_padding)
            tb.set_relative_position((x_position, self.next_y_position))
            self.next_y_position += tb.get_relative_rect().height + self.bubble_gap

    def next_dialogue(self):
        if not self.npc.dialogue_queue:
            self.continue_label.text = "(Seems like they have nothing else to say to you)"
            return
        curr_dialogue = self.npc.dialogue_queue.pop(0)
        if len(curr_dialogue) == 2:
            text, left = curr_dialogue
            self.add_dialogue(text, left)
        else:
            if curr_dialogue[-1]: # player has multiple options, draw all dialogue boxes
                for i, text in enumerate(curr_dialogue[:-1]):
                    text = str(i + 1) + ". " + text
                    self.add_dialogue(text, curr_dialogue[-1], choice=True, action=str(i + 1))
                self.loop.dialogue_options = len(curr_dialogue) - 1 # to account for the left flag
            else:
                left = curr_dialogue[-1]
                text = random.choice(curr_dialogue[:-1]) # if npc has multiple options, choose a random one
                self.add_dialogue(text, left)


    def add_dialogue(self, text, left, choice=False, action="return"):
        # self.npc.dialogue_memory.append((text, left, choice, action))
        self.npc.add_to_memory(text, left, choice, action, self.loop)

        if choice:
            color = (185, 185, 185)
        else:
            color = (255, 255, 255)

        max_bubble_width = self.get_relative_rect().width // 5 * 4
        padding = self.image.get_height() // 25

        # Create a font and measure the text size
        font = pygame.font.Font(None, 24)
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + ' ' + word
            if font.size(test_line)[0] <= max_bubble_width - 2 * padding:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        text_height = font.get_height()
        bubble_width = min(max_bubble_width, max(font.size(line)[0] for line in lines) + 2 * padding)
        bubble_height = len(lines) * text_height + 2 * padding

        # # Create a surface for the speech bubble
        # bubble_surface = pygame.Surface((bubble_width, bubble_height), pygame.SRCALPHA)
        # draw_speech_bubble(bubble_surface, text, left)
        
        # Determine x position based on alignment
        x_position = self.bubble_padding if left else self.get_relative_rect().width - bubble_width - (self.bubble_padding)

        # Create UIButton to display the speech bubble
        bubble_button = DialogueButton(
            rect=pygame.Rect((x_position, self.next_y_position), (bubble_width, bubble_height)),
            text=text,
            left=left,
            manager=self.ui_manager,
            color=color,
            container=self,
            object_id='#speech_bubble'
        )

        bubble_button.draw_on_all_surfaces(text, left, color)

        # # Manually render the text onto the button surface
        # button_surface = bubble_button.image
        # for state in ["normal", "hovered", "disabled", "selected", "active"]:
        #     draw_speech_bubble(bubble_button.drawable_shape.states[state].surface, text, button_surface.get_width(), button_surface.get_height(), left)
        # bubble_button.drawable_shape.active_state.has_fresh_surface = True

        self.text_boxes.append((bubble_button, left))
        self.next_y_position += bubble_height + self.bubble_gap

        # Remove oldest message if exceeding limit
        if len(self.text_boxes) > self.max_messages:
            self.text_boxes[0][0].kill()
            self.text_boxes.pop(0)
            # Update positions
            self.update_textbox_positions()

        for box, _ in self.text_boxes:
            if hasattr(box, "action") and box.action == action:
                box.action = ""
        self.text_boxes[-1][0].action = action

    def repeat_important_options(self, prev_options, chosen_dialogue):
        # import pdb; pdb.set_trace()
        for option in prev_options:
            option = option.split(" ", 1)[1] # strip option numbers
            if option != chosen_dialogue:
                if option in self.npc.repeat_dict.keys():
                    # import pdb; pdb.set_trace()
                    self.npc.dialogue_dict[option] = self.npc.repeat_dict[option]
                    self.npc.insert_into_dialogue_queue(option, True) # only player options should be allowed to repeat, something has gone wrong if player should be False here

    def update(self, time_delta: float):
        if self.loop.player_choice != -1:
            prev_options = self.clear_last_player_dialogue()
            # import pdb; pdb.set_trace()
            chosen_dialogue = prev_options[self.loop.player_choice - 1]
            chosen_dialogue = chosen_dialogue.split(" ", 1)[1] # removes number from option
            self.add_dialogue(chosen_dialogue, True)
            self.repeat_important_options(prev_options, chosen_dialogue)
            self.loop.player_choice = -1
            self.loop.dialogue_options = 0
            self.next_dialogue()
            
        if self.loop.next_dialogue:
            self.next_dialogue()
            self.loop.next_dialogue = False
        
        super().update(time_delta)
        
    
class LevelUpHeader(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager, text="Allocate " + str(player.stat_points) + " Stat Points")
        self.player = player

    def update(self, time_delta: float):
        self.set_text("Allocate " + str(self.player.stat_points - sum(self.player.stat_decisions)) + " Stat Points")
        return super().update(time_delta)

"""
class RoundedText(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager, text="Round do be rounding")
        self.player = player

    def check_stats(self, player):
        example_strength = player.character.strength + player.stat_decisions[0]
        example_dexterity = player.character.dexterity + player.stat_decisions[1]
        example_endurance = player.character.endurance + player.stat_decisions[2]
        example_intelligence = player.character.intelligence + player.stat_decisions[3]

        if (example_strength == example_dexterity and example_dexterity == example_endurance and example_endurance == example_intelligence):
            return True
        else:
            return False

    def update(self, time_delta: float):
        if self.check_stats(self.player):
            self.set_text("You feel the dungeon would approve of your stats after this change.")
        elif self.player.character.rounded() and (not self.check_stats(self.player)):
            self.set_text("You feel the dungeon would stop enhancing your stats after this change.")
        else:
            self.set_text("You feel the dungeon will continue to not enhance your stats after this change.")
        return super().update(time_delta)
    """
class StatChangeText(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, player, index):
        super().__init__(relative_rect=rect, manager=manager, text="+" + str(player.stat_decisions[index]))
        self.player = player
        self.index = index

    def update(self, time_delta: float):
        self.set_text("+" + str(self.player.stat_decisions[self.index]))

        return super().update(time_delta)

class StatBox(pygame_gui.elements.UITextBox):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager, html_text="Error")
        self.player = player
        self.status = 'N'
        self.status_effects = []
        self.status_effect_durations = []
        self.stat_points = -1
        self.level = -1
        self.experience = -1
        self.experience_to_next_level = -1
        self.rounded = False
        self.strength = -1
        self.dexterity = -1
        self.endurance = -1
        self.intelligence = -1
        self.rounded = 0

    def NeedsUpdate(self, entity):
        if not (self.CompareStats(entity)):
            self.SetCompareStats(entity)
            return True
        return False

    def CompareStats(self, entity):
        curr_status_effect_durations = []
        for effect in entity.character.status_effects:
            curr_status_effect_durations.append(effect.duration)
        return (self.status == self.get_health_status(entity) and
                self.status_effects == entity.character.status_effects and
                self.status_effect_durations == curr_status_effect_durations and
                self.stat_points == entity.stat_points and
                self.level == entity.level and
                self.experience == entity.experience and
                self.experience_to_next_level == entity.experience_to_next_level and
                self.strength == entity.character.strength and
                self.dexterity ==entity.character.dexterity and
                self.endurance == entity.character.endurance and
                self.intelligence == entity.character.intelligence and
                self.armor == entity.character.armor)

    def SetCompareStats(self, entity):
        self.status = self.get_health_status(entity)
        self.status_effects = entity.character.status_effects
        self.status_effect_durations = []
        for effect in self.status_effects:
            self.status_effect_durations.append(effect.duration)
        self.stat_points = entity.stat_points
        self.level = entity.level
        self.experience = entity.experience
        self.experience_to_next_level = entity.experience_to_next_level
        self.strength = entity.character.strength
        self.dexterity = entity.character.dexterity
        self.endurance = entity.character.endurance
        self.intelligence = entity.character.intelligence
        self.armor = entity.character.armor

    def get_health_status(self, entity):
        if entity.character.health < entity.character.max_health // 3 * 2:
            return 'W'
        else:
            return 'H'

    #HORRIBLE HACK - THIS IS ALSO DEFINED IN DISPLAY.PY - KEEP THEM SYNCED!
    def get_status_text(self, entity):
        status = "Healthy"
        if entity.character.health < entity.character.max_health // 3 * 2:
            status = "Wounded"
        effects = entity.character.status_effects
        for effect in effects:
            status += ", " + effect.description()
        return status
    
    def get_level_text(self, entity):
        if entity.stat_points > 0:
            return "<shadow size=1 offset=0,0 color=#306090><font color=#E0F0FF>Level: " \
                    + str(entity.level) + " (Press L to allocate stat points)</font></shadow>"
        else:
            to_next_level = str(format(entity.experience / entity.experience_to_next_level, ".1%"))
            return "Level: " + str(entity.level) + " (" + to_next_level + " there to next level)"

    def stat_text(self, entity, stat, useRounded=False):
        return str(stat)
        
    def round_text(self, entity):
        total_stats = entity.character.strength + entity.character.intelligence + entity.character.dexterity + entity.character.endurance
        if total_stats <= 6:
            return "You are weak.<br><br>"
        elif total_stats <= 10:
            return "You have potential<br><br>"
        elif total_stats <= 20:
            return "You are a strong challenger<br><br>"
        elif total_stats <= 40:
            return "You are one of the strongest foes<br><br>"
        elif total_stats <= 100:
            return "Your strength is unparalleled<br><br>"
        else:
            "You shouldn't be seeing this message"

    def update(self, time_delta: float):
        if (self.NeedsUpdate(self.player)):
            self.set_text(html_text=
                            "Health: " + "<br>" +
                            "Mana: " + "<br>" +
                            "Strength: " + self.stat_text(self.player, self.player.character.strength) + " "
                            "Dexterity: " + self.stat_text(self.player, self.player.character.dexterity) + "<br>"
                            "Endurance: " + self.stat_text(self.player, self.player.character.endurance) + " "
                            "Intelligence: " + self.stat_text(self.player, self.player.character.intelligence) + "<br>" + \
                            "Armor: " + self.stat_text(self.player, self.player.character.armor, False) + "<br>" + \
                            self.round_text(self.player) + \
                            "Gold: " + self.stat_text(self.player, self.player.character.gold, False) + "<br>" + \
                            "Status: " + self.get_status_text(self.player) + "<br>" + \
                            self.get_level_text(self.player) + "<br>")

        return super().update(time_delta)
    
class SkillButton(pygame_gui.elements.UIButton):
    def __init__(self, rect, manager, player, index, img1, img2, loop, object_id):
        super().__init__(relative_rect=rect, manager=manager, text="", object_id=object_id,
                    starting_height=900)
        self.player = player
        self.index = index
        self.img1 = img1
        self.img2 = img2
        self.loop = loop
        self.set_text("")
        self.castable = False
        self.active_state = self.drawable_shape.active_state
        self.ready = 0
        self.draw_on_button(self, self.img2, chr(ord("1") + index), self.relative_rect.size, True)

    def needs_change(self):
        skill = self.player.mage.quick_cast_spells[self.index]
        if skill == None:
            return False
        closest_monster = self.player.character.get_closest_monster(self.loop)
        if closest_monster == self.player and skill.range != -1:
            castable = False  # no monster to caste ranged skill on
        else:
            castable = skill.castable(closest_monster)
        if castable != self.castable or skill.ready != self.ready or self.active_state != self.drawable_shape.active_state:
            self.castable = castable
            self.ready = skill.ready
            self.active_state = self.drawable_shape.active_state
            return True
        return False

    def draw_on_button(self, button, img, letter="", button_size=None, shrink=False, offset_factor = 10, text_offset = (15, 0.8)):
        offset = (0, 0)
        if shrink:# shrink weapon image a bit
            if img != None:
                img = pygame.transform.scale(img, (button_size[0] // 5 * 4, button_size[1] // 5 * 4))
            offset = (button_size[0] // offset_factor, button_size[1] // offset_factor)
        if img != None:
            button.drawable_shape.states['normal'].surface.blit(img, offset)
            button.drawable_shape.states['hovered'].surface.blit(img, offset)
            button.drawable_shape.states['disabled'].surface.blit(img, offset)
            button.drawable_shape.states['selected'].surface.blit(img, offset)
            button.drawable_shape.states['active'].surface.blit(img, offset)
        if button_size:
            font_size = 20
            font = pygame.font.Font('freesansbold.ttf', font_size)
            text = font.render(letter, True, (255, 255, 255))
            button.drawable_shape.states['normal'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['hovered'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['disabled'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['selected'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
            button.drawable_shape.states['active'].surface.blit(text, (button_size[0] // text_offset[0], button_size[1] * text_offset[1]))
        button.drawable_shape.active_state.has_fresh_surface = True

    def draw_text_on_button(self, button, text, button_size):
        # draw text on middle of button
        font_size = 20
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text = font.render(text, True, (255, 255, 255))
        button.drawable_shape.states['normal'].surface.blit(text, (button_size[0] // 2 - 10, button_size[1] // 2 - 10))
        button.drawable_shape.states['hovered'].surface.blit(text, (button_size[0] // 2 - 10, button_size[1] // 2 - 10))
        button.drawable_shape.states['disabled'].surface.blit(text, (button_size[0] // 2 - 10, button_size[1] // 2 - 10))
        button.drawable_shape.states['selected'].surface.blit(text, (button_size[0] // 2 - 10, button_size[1] // 2 - 10))
        button.drawable_shape.states['active'].surface.blit(text, (button_size[0] // 2 - 10, button_size[1] // 2 - 10))
        button.drawable_shape.active_state.has_fresh_surface = True

    def draw_box_over_button(self, button, button_size):
        # draw box over button
        border = 5
        pygame.draw.rect(button.drawable_shape.states['normal'].surface, (69, 73, 78), (border, border, button_size[0] - border * 2, button_size[1] - border * 2))
        pygame.draw.rect(button.drawable_shape.states['hovered'].surface, (69, 73, 78), (border, border, button_size[0] - border * 2, button_size[1] - border * 2))
        pygame.draw.rect(button.drawable_shape.states['disabled'].surface, (69, 73, 78), (border, border, button_size[0] - border * 2, button_size[1] - border * 2))
        pygame.draw.rect(button.drawable_shape.states['selected'].surface, (69, 73, 78), (border, border, button_size[0] - border * 2, button_size[1] - border * 2))
        pygame.draw.rect(button.drawable_shape.states['active'].surface, (69, 73, 78), (border, border, button_size[0] - border * 2, button_size[1] - border * 2))
        button.drawable_shape.active_state.has_fresh_surface = True

    def update(self, time_delta: float):
        if (self.needs_change()):
            skill = self.player.mage.quick_cast_spells[self.index]
            closest_monster = self.player.character.get_closest_monster(self.loop)
            if closest_monster == self.player and skill.range != -1:
                castable = False  # no monster to caste ranged skill on
            else:
                castable = skill.castable(closest_monster)
            if (castable):
                self.draw_on_button(self, self.img1, str(self.index + 1), self.relative_rect.size, True)
            else:
                ready = skill.ready
                if ready != 0:
                    self.draw_box_over_button(self, self.relative_rect.size)
                    self.draw_on_button(self, self.img2, "", self.relative_rect.size, True)
                    self.draw_text_on_button(self, str(ready), self.relative_rect.size)
                else:
                    self.draw_box_over_button(self, self.relative_rect.size)
                    self.draw_on_button(self, self.img2, str(self.index + 1), self.relative_rect.size, True)
                    #self.draw_text_in_corner(self, str(self.index + 1), self.relative_rect.size)

        return super().update(time_delta)
    
class StatDownButton(pygame_gui.elements.UIButton):
    def __init__(self, rect, manager, player, img1, img2, index):
        super().__init__(relative_rect=rect, manager=manager, text="")
        self.player = player
        self.img1 = img1
        self.img2 = img2
        self.index = index
        self.set_text("")
        self.draw_on_button(self, self.img2)

    def draw_on_button(self, button, img):
        offset = (0, 0)
        button.drawable_shape.states['normal'].surface.blit(img, offset)
        button.drawable_shape.states['hovered'].surface.blit(img, offset)
        button.drawable_shape.states['disabled'].surface.blit(img, offset)
        button.drawable_shape.states['selected'].surface.blit(img, offset)
        button.drawable_shape.states['active'].surface.blit(img, offset)
        button.drawable_shape.active_state.has_fresh_surface = True

    def update(self, time_delta: float):
        if (self.player.stat_decisions[self.index] > 0):
            self.draw_on_button(self, self.img1)
        else:
            self.draw_on_button(self, self.img2)

        return super().update(time_delta)
    
class ExamineWindow(pygame_gui.elements.UITextBox):
    def __init__(self, rect, manager, loop):
        super().__init__(relative_rect=rect, manager=manager, html_text="Error")
        self.loop = loop
        self.last_examine = -1

    def update(self, time_delta: float):
        if (self.last_examine != self.loop.examine):
            self.set_text(html_text=self.loop.examine)
            self.last_examine = self.loop.examine

        return super().update(time_delta)
    
class StatUpButton(pygame_gui.elements.UIButton):
    def __init__(self, rect, manager, player, img1, img2, index):
        super().__init__(relative_rect=rect, manager=manager, text="")
        self.player = player
        self.img1 = img1
        self.img2 = img2
        self.index = index
        self.set_text("")
        self.draw_on_button(self, self.img2)

    def draw_on_button(self, button, img):
        offset = (0, 0)
        button.drawable_shape.states['normal'].surface.blit(img, offset)
        button.drawable_shape.states['hovered'].surface.blit(img, offset)
        button.drawable_shape.states['disabled'].surface.blit(img, offset)
        button.drawable_shape.states['selected'].surface.blit(img, offset)
        button.drawable_shape.states['active'].surface.blit(img, offset)
        button.drawable_shape.active_state.has_fresh_surface = True

    def update(self, time_delta: float):
        if self.player.stat_points > sum(self.player.stat_decisions):
            self.draw_on_button(self, self.img1)
        else:
            self.draw_on_button(self, self.img2)

        return super().update(time_delta)
    

    
class DepthDisplay(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, loop):
        super().__init__(relative_rect=rect, manager=manager, text="Error")
        self.loop = loop
        self.last_depth = -1
        self.last_branch = ""

    def update(self, time_delta: float):
        if (self.last_depth != self.loop.generator.depth) or self.last_branch != self.loop.generator.branch or self.last_branch == "Forest":
            if self.loop.branch == "Forest":
                self.set_text(str(self.loop.generator.branch) + " " + str(self.loop.generator.depth) + " " + str(self.loop.day) + " " + str(self.loop.total_time % 100))
            else:
                self.set_text(str(self.loop.generator.branch) + " " + str(self.loop.generator.depth))
            self.last_depth = self.loop.generator.depth
            self.last_branch = self.loop.generator.branch

        return super().update(time_delta)