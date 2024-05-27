import pygame
class Bindings():
    def __init__(self):
        self.key_mapping = {
           # "v":["i"]
        }
        self.key_queue = []

        self.temp_binding = None
        self.temp_binding_map = []
        self.accepting_binding = False

    def save_key_binding(self):
        self.key_mapping[self.temp_binding] = self.temp_binding_map
        self.temp_binding = None
        self.temp_binding_map = []
        self.accepting_binding = False

    def has_queue(self):
        if len(self.key_queue) > 0:
            return True

    def next_key(self):
        return self.key_queue.pop(0)

    def has_binding(self, key):
        return key in self.key_mapping

    def use_keybinding(self, key):
        self.key_queue = self.key_mapping[key]