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
        
    def compute_average(self):
        average = 0.0
        for val in self.times:
            average += val
        return 1 / (average / len(self.times))


    def update(self, time_delta: float):
        self.times.append(time_delta)
        if (len(self.times) > 10):
            self.times.remove(self.times[0])

        self.set_text(str(self.compute_average()))

        return super().update(time_delta)
    
class MessageBox(pygame_gui.elements.UITextBox):
    def __init__(self, rect, manager, loop):
        super().__init__(relative_rect=rect, manager=manager, html_text="Error")
        self.loop = loop #Store loop to retrieve messages

    def update(self, time_delta: float):
        
        self.set_text(html_text="".join([message + "<br>" for message in (self.loop.messages)]))

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

    def update(self, time_delta: float):
        self.set_text(html_text="Player:<br>" +
                        "Health: " + str(self.player.character.health) + " / " + str(self.player.character.max_health) + "<br>"
                        "Mana: " + str(self.player.character.mana) + " / " + str(self.player.character.max_mana) + "<br>"
                        "Status: " + self.get_status_text(self.player) + "<br><br>"+
                        "Level: " + str(self.player.level)+ "<br>"
                        "Experience: " + str(self.player.experience) + " / " + str(self.player.experience_to_next_level) + "<br>"
                        "<br>")

        return super().update(time_delta)
    
class DepthDisplay(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, loop):
        super().__init__(relative_rect=rect, manager=manager, text="Error")
        self.loop = loop

    def update(self, time_delta: float):
        self.set_text("Depth " + str(self.loop.generator.depth))

        return super().update(time_delta)