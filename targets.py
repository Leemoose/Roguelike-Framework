
class Target:
    def __init__(self):
        self.target_list= ()
        self.skill = None

    def start_target(self, starting_target):
        self.target_list = (starting_target)

    def adjust(self, xdelta, ydelta):
        x, y = self.target_list
        self.target_list = (x+xdelta, y + ydelta)

    def store_skill(self, skill):
        self.skill = skill

    def void_skill(self):
        self.skill = None

    def cast_on_target(self, loop):
        x, y = self.target_list
        monster_map = loop.generator.monster_map
        monster_dict = loop.generator.monster_dict
        if not monster_map.get_passable(x,y):
            monster = monster_dict.get_subject(monster_map.locate(x,y))
            self.skill(monster, loop)
            self.void_skill()
        else:
            loop.add_message("Not a valid target there")

    def explain_target(self, loop):
        x, y = self.target_list
        monster_map = loop.generator.monster_map
        monster_dict = loop.generator.monster_dict
        item_dict = loop.generator.item_dict
        item_map = loop.generator.item_map
        tile_map = loop.generator.tile_map.track_map
        loop.add_message("That is a " + tile_map[x][y].name + " my friend")
        if not monster_map.get_passable(x,y):
            monster = monster_dict.get_subject(monster_map.locate(x,y))
            loop.add_message("And there is a " + monster.name + " inhabiting it" )
        if not item_map.get_passable(x,y):
            item = item_dict.get_subject(item_map.locate(x, y))
            loop.add_message("There is a " + item.name + " there as well")

