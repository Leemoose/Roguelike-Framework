from objects import Objects

class Interactable(Objects):
    def __init__(self, render_tag = 0, x=-1, y=-1, name="Interactable"):
        super().__init__(x=x, y=y,id_tag=-1, render_tag= render_tag, name = name)
        self.name = name

    def interact(self, loop):
        pass

class Campfire(Interactable):
    def __init__(self, render_tag = 3000,x=-1, y = -1, name="Campfire"):
        super().__init__(render_tag, x, y, name=name)
        self.used = False

    def interact(self, entity, loop):
        if not self.used and loop.get_daytime() == "Nighttime":
            loop.change_daytime()
            self.used = True
            loop.add_message("You rested at the campfire")
            entity.character.change_health(entity.character.get_max_health()-entity.character.get_health())
            self.render_tag = 3001

class OrbPedastool(Interactable):
    def __init__(self, render_tag=0, x=-1, y=-1, name="Orb Pedastool"):
        super().__init__(x=x, y=y, render_tag= render_tag, name = name)
        self.name = name

    def interact(self, loop):
        pass

class ForestOrbPedastool(OrbPedastool):
    def __init__(self, render_tag = 3900, x=-1, y=-1, name="Forest Orb Pedastool"):
        super().__init__(x, y, 0, render_tag= render_tag, name = name)
        self.name = name

    def interact(self, loop):
        self.render_tag = 3901