import pygame, pygame_gui

class HealthBar(pygame_gui.elements.UIProgressBar):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager)
        self.player = player

    def update(self, time_delta: float):
        self.maximum_progress = max(1.0, self.player.character.max_health)
        self.current_progress = self.player.character.health
        self.percent_full = 100 * self.current_progress / self.maximum_progress

        return super().update(time_delta)
    
class ManaBar(pygame_gui.elements.UIProgressBar):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager)
        self.player = player

    def update(self, time_delta: float):
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
        self.best = 1 / lowest
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

    def update(self, time_delta: float):
        
        self.set_text(html_text="".join([message + "<br>" for message in (self.loop.messages)]))

        return super().update(time_delta)
    
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
            return "You feel the dungeon enhancing your well-rounded stats.<br><br>"
        else:
            return "<br>"

    def update(self, time_delta: float):
        self.set_text(html_text="Player:<br>" +
                        "Strength: " + self.stat_text(self.player, self.player.character.strength) + "<br>"
                        "Dexterity: " + self.stat_text(self.player, self.player.character.dexterity) + "<br>"
                        "Endurance: " + self.stat_text(self.player, self.player.character.endurance) + "<br>"
                        "Intelligence: " + self.stat_text(self.player, self.player.character.intelligence) + "<br>" + \
                        self.round_text(self.player) + \
                        "Status: " + self.get_status_text(self.player) + "<br>" + \
                        self.get_level_text(self.player) + "<br>")

        return super().update(time_delta)
    
class DepthDisplay(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, loop):
        super().__init__(relative_rect=rect, manager=manager, text="Error")
        self.loop = loop

    def update(self, time_delta: float):
        self.set_text("Depth " + str(self.loop.generator.depth))

        return super().update(time_delta)