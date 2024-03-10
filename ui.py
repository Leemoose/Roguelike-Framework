import pygame, pygame_gui
import character

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
        text = "".join([message + "<br>" for message in (self.loop.messages)])
        text = text[:-3] #Remove last <br>
        self.set_text(html_text=text)
        self.loop.dirty_messages = False
    
class LevelUpHeader(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager, text="Allocate " + str(player.stat_points) + " Stat Points")
        self.player = player

    def update(self, time_delta: float):
        self.set_text("Allocate " + str(self.player.stat_points - sum(self.player.stat_decisions)) + " Stat Points")
        return super().update(time_delta)
    
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
                self.rounded == entity.character.rounded() and
                self.strength == entity.character.strength and
                self.dexterity ==entity.character.dexterity and
                self.endurance == entity.character.endurance and
                self.intelligence == entity.character.intelligence)

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
        self.rounded = entity.character.rounded()
        self.strength = entity.character.strength
        self.dexterity = entity.character.dexterity
        self.endurance = entity.character.endurance
        self.intelligence = entity.character.intelligence

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

    def stat_text(self, entity, stat):
        if entity.character.rounded():
            return str(stat) + " (+" + str(int(stat * entity.character.round_bonus()) - stat) + ")"
        else:
            return str(stat)
        
    def round_text(self, entity):
        if entity.character.rounded():
            return "Your stats are well rounded.<br><br>"
        else:
            return "Your stats are not well rounded.<br><br>"

    def update(self, time_delta: float):
        if (self.NeedsUpdate(self.player)):
            self.set_text(html_text=
                            "Health: " + "<br>" +
                            "Mana: " + "<br>" +
                            "Strength: " + self.stat_text(self.player, self.player.character.strength) + " "
                            "Dexterity: " + self.stat_text(self.player, self.player.character.dexterity) + "<br>"
                            "Endurance: " + self.stat_text(self.player, self.player.character.endurance) + " "
                            "Intelligence: " + self.stat_text(self.player, self.player.character.intelligence) + "<br>" + \
                            self.round_text(self.player) + \
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
        self.ready = 0
        self.draw_on_button(self, self.img2, chr(ord("1") + index), self.relative_rect.size, True)

    def needs_change(self):
        skill = self.player.character.skills[self.index]
        closest_monster = self.player.character.get_closest_monster(self.player, self.loop.monster_dict, self.loop.generator.tile_map)
        if closest_monster == self.player and skill.range != -1:
            castable = False  # no monster to caste ranged skill on
        else:
            castable = skill.castable(closest_monster)
        if castable != self.castable or skill.ready != self.ready:
            self.castable = castable
            self.ready = skill.ready
            return True
        return False

    def draw_on_button(self, button, img, letter="", button_size=None, shrink=False, offset_factor = 10, text_offset = (15, 0.8)):
        offset = (0, 0)
        if shrink:# shrink weapon image a bit
            img = pygame.transform.scale(img, (button_size[0] // 5 * 4, button_size[1] // 5 * 4))
            offset = (button_size[0] // offset_factor, button_size[1] // offset_factor)
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
            skill = self.player.character.skills[self.index]
            closest_monster = self.player.character.get_closest_monster(self.player, self.loop.monster_dict, self.loop.generator.tile_map)
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

    def update(self, time_delta: float):
        if (self.last_depth != self.loop.generator.depth):
            self.set_text("Depth " + str(self.loop.generator.depth))
            self.last_depth = self.loop.generator.depth

        return super().update(time_delta)