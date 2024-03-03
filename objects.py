
class Objects():
    def __init__(self, x, y, id_tag, render_tag, name):
        self.id_tag = id_tag
        self.render_tag = render_tag
        self.shaded_render_tag = -render_tag
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return self.name

    def gain_ID(self, ID):
        self.id_tag = ID

    def get_location(self):
        return (self.x,self.y)

    def get_distance(self, x, y):
        return ((self.x - x)**2 + (self.y - y)**2)**(1/2)

class Tile(Objects):
    def __init__(self, x, y, render_tag = 0, passable = False, id_tag = 0):
        super().__init__(x, y, id_tag, render_tag, "Tile")
        self.passable = passable
        self.seen = False
        self.visible = False

    def __str__(self):
        if self.passable:
            print(".")
        else:
            print("#")

class Stairs(Tile):
    def __init__(self, x, y, render_tag = 0, passable = True, id_tag = 0, downward = False):
        super().__init__(x, y, render_tag, passable, id_tag)
        self.stairs = True
        self.pair = None
        self.downward = downward

class Item(Objects):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x, y, id_tag, render_tag, name)
        self.equipable = False
        self.dropable = True
        self.consumeable = False
        self.equipped = False
        self.destroy = False
