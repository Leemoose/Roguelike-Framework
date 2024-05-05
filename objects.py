
class Objects():
    def __init__(self, x = -1, y = -1, id_tag = -1, render_tag = -1, name = "Unknown object"):
        self.id_tag = id_tag
        self.render_tag = render_tag
        self.shaded_render_tag = -render_tag
        self.name = name
        self.description = ""
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
    def __init__(self, x, y, render_tag = 0, passable = False, blocks_vision = True, id_tag = 0):
        super().__init__(x, y, id_tag, render_tag, "Tile")
        self.passable = passable
        self.blocks_vision = blocks_vision
        self.seen = False
        self.visible = False
        self.on_fire = False

    def is_visible(self):
        return self.visible

    def is_blocking_vision(self):
        return self.blocks_vision

    def __str__(self):
        if self.passable:
            return(".")
        else:
            return("#")

class Item(Objects):
    def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name=-1):
        super().__init__(x, y, id_tag, render_tag, name)
        self.equipable = False
        self.dropable = True
        self.consumeable = False
        self.equipped = False
        self.destroy = False
        self.description = "Its a " + name + "."
        self.stackable = False
        self.yendorb = False
        self.can_be_levelled = True
        self.level = 1
        self.attached_skill_exists = False
        self.equipment_type = None
