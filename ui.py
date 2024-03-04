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