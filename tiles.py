import objects as O
import npc
class Floor(O.Tile):
    def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag)

class NPCSpawn(Floor):
    def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = None):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.entity = entity(x, y)

    #Not currently supported
    def spawn_entity(self):
        return self.entity

class KingTile(NPCSpawn):
    def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.King):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)

class Wall(O.Tile):
    def __init__(self, x, y, render_tag = 1, passable = False, id_tag = 0):
        super().__init__(x, y,  render_tag = 1, passable = False, id_tag = id_tag)


class Stairs(O.Tile):
    def __init__(self, x, y, render_tag = 0, passable = True, id_tag = 0, downward = False):
        super().__init__(x, y, render_tag, passable, id_tag)
        self.stairs = True
        self.pair = None
        self.downward = downward

class DownStairs(Stairs):
    def __init__(self, x, y, render_tag = 91, passable = True, id_tag = 0, downward = True):
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag, downward = downward)

class UpStairs(Stairs):
    def __init__(self, x, y, render_tag = 90, passable = True, id_tag = 0, downward = False):
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag, downward = downward)

