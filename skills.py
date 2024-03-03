import random
import monster as M

class Skills():
    def __init__(self, parent):
        self.parent = parent
        self.can_teleport = True

    def teleport(self, generator):
        if self.can_teleport ==True:
            tile_map = generator.tile_map
            width = generator.width
            height = generator.height
            startx = random.randint(0, width - 1)
            starty = random.randint(0, height - 1)

            while (tile_map.get_passable(startx, starty) == False):
                startx = random.randint(0, width - 1)
                starty = random.randint(0, height - 1)

            if isinstance(self.parent, M.Monster):
                monster_map = generator.monster_map
                x, y = self.parent.x, self.parent.y
                monster_map.clear_location(x, y)
                self.parent.x = startx
                self.parent.y = starty
                monster_map.place_thing(self.parent)
            else:
                self.parent.x = startx
                self.parent.y = starty
