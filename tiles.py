import objects as O
import npc
import copy
import monster as M

class Floor(O.Tile):
    def __init__(self, x, y, render_tag = 2, passable = True, blocks_vision = False, id_tag = 0):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, blocks_vision=blocks_vision)

class Door(Floor):
    def __init__(self, x, y, render_tag = 30, passable = True, blocks_vision = True, id_tag = 0):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, blocks_vision=blocks_vision)

    def open(self):
        self.render_tag = 31
        self.shaded_render_tag = -31
        self.blocks_vision = False



class NPCSpawn(Floor):
    def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = None):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.entity = entity(x, y)

    #Not currently supported
    def spawn_entity(self):
        return self.entity
    
class MonsterSpawn(Floor):
    def __init__(self, x, y, render_tag, passable = False, id_tag = 0, entity = None):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.entity = copy.deepcopy(entity(x, y))
    
    def spawn_entity(self):
        return self.entity

class DummyTile(MonsterSpawn):
    def __init__(self, x, y, render_tag = 6, passable = False, id_tag = 0, entity = M.Dummy):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)

class KingTile(NPCSpawn):
    def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.King):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)

class GuardTile(NPCSpawn):
    def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.Guard):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)

class BobBrotherTile(GuardTile):
    def __init__(self, x, y, render_tag = 2, passable = True, id_tag = 0, entity = npc.BobBrother):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)

class Wall(O.Tile):
    def __init__(self, x, y, render_tag = 1, passable = False, blocks_vision = True, id_tag = 0):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, blocks_vision = blocks_vision, id_tag = id_tag)

class SenseiTile(NPCSpawn):
    def __init__(self, x, y, render_tag = 6, passable = True, id_tag = 0, entity = npc.Sensei):
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, entity=entity)

class Stairs(O.Tile):
    def __init__(self, x, y, render_tag = 0, passable = True, id_tag = 0, downward = False):
        super().__init__(x, y, render_tag, passable, id_tag)
        self.stairs = True
        self.pair = None

class DownStairs(Stairs):
    def __init__(self, x, y, render_tag = 91, passable = True, id_tag = 0):
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.downward = True

class UpStairs(Stairs):
    def __init__(self, x, y, render_tag = 90, passable = True, id_tag = 0):
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.downward = False

class Gateway(O.Tile):
    def __init__(self, x, y, level, branch, render_tag = 91, passable = True, id_tag = 0):
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.branch = branch
        self.level = level
        self.pair = None

    def get_branch(self):
        return self.branch

    def get_depth(self):
        return self.level

    def pair_gateway(self, other_gateway):
        self.pair = other_gateway
        other_gateway.pair = self


class ForestGateway(Gateway):
    def __init__(self, x, y, level = 10, branch = "Dungeon", render_tag = 91, passable = True, id_tag = 0):
        super().__init__(x, y, level, branch, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.branch = branch
        self.level = level
class DungeonGateway(Gateway):
    def __init__(self, x, y, level = 1, branch = "Forest", render_tag = 91, passable = True, id_tag = 0):
        super().__init__(x, y,level, branch, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.branch = branch
        self.level = level

