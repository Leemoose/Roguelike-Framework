from objects import Objects

class Interactable(Objects):
    def __init__(self, render_tag, x, y, name="Interactable"):
        super().__init__(x, y, 0, render_tag= render_tag, name = name)
        self.name = name

    def interact(self, loop):
        pass

class Campfire(Interactable):
    def __init__(self, render_tag = 0,x=-1, y = -1, name="Campfire"):
        super().__init__(render_tag, x, y, name=name)
        self.used = False

    def interact(self, loop):
        if not self.used and loop.get_daytime() == "Nighttime":
            loop.change_daytime()
            self.used = True