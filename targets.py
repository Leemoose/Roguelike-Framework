
class Target:
    def __init__(self):
        self.target_list= ()
        self.index_to_cast = None
        self.skill_to_cast = None
        self.caster = None

    def start_target(self, starting_target):
        self.target_list = (starting_target)

    def adjust(self, xdelta, ydelta):
        x, y = self.target_list
        self.target_list = (x+xdelta, y + ydelta)

    def store_skill(self, index_to_cast, skill_to_cast, caster):
        self.index_to_cast = index_to_cast
        self.skill_to_cast = skill_to_cast
        self.caster = caster

    def void_skill(self):
        self.index_to_cast = None
        self.skill_to_cast = None
        self.caster = None

    def cast_on_target(self, loop):
        x, y = self.target_list
        monster_map = loop.generator.monster_map
        monster_dict = loop.generator.monster_dict
        if not monster_map.get_passable(x,y):
            monster = monster_dict.get_subject(monster_map.locate(x,y))
            if self.skill_to_cast.castable(monster):
                self.caster.cast_skill(self.index_to_cast, monster, loop)
                loop.add_message("You cast " + str(self.skill_to_cast.name) + " on " + monster.name)
                self.void_skill()
            else:
                loop.add_message("You can't cast " + self.skill_to_cast.name + " on " + monster.name + " right now")
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
        if not tile_map[x][y].visible:
            loop.add_message("You can't see that location")
            return
        loop.add_message("That is a " + tile_map[x][y].name + " my friend")
        if not monster_map.get_passable(x,y):
            monster = monster_dict.get_subject(monster_map.locate(x,y))
            loop.add_message("And there is a " + monster.name + " inhabiting it" )
        if not item_map.get_passable(x,y):
            item = item_dict.get_subject(item_map.locate(x, y))
            loop.add_message("There is a " + item.name + " there as well")

