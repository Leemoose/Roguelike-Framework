
class Target:
    def __init__(self):
        self.target_current = None
        self.target_previous = None
        self.index_to_cast = None
        self.skill_to_cast = None
        self.caster = None
        self.temp_cast = None
        self.quick_cast = False

    def start_target(self, starting_target):
        self.target_current = starting_target
        self.target_previous = None

    def adjust(self, xdelta, ydelta, tile_map, loop):
        if (tile_map.track_map[self.target_current[0] + xdelta][self.target_current[1] + ydelta].passable and
            tile_map.track_map[self.target_current[0] + xdelta][self.target_current[1] + ydelta].seen):
            x, y = self.target_current
            self.target_current = (x+xdelta, y + ydelta)
            loop.screen_focus = self.target_current


    def store_skill(self, index_to_cast, skill_to_cast, caster, temp_cast = False, quick_cast=False):
        self.index_to_cast = index_to_cast
        self.skill_to_cast = skill_to_cast
        self.caster = caster
        self.temp_cast = temp_cast
        self.quick_cast = quick_cast

    def void_skill(self):
        if self.temp_cast:
            self.caster.inventory.ready_scroll = None
        self.index_to_cast = None
        self.skill_to_cast = None
        self.caster = None
        self.temp_cast = False

    def cast_on_target(self, loop):
        x, y = self.target_current
        monster_map = loop.generator.monster_map
        if loop.generator.tile_map.track_map[x][y].visible == False:
            loop.add_message("You can't see that location")
            return
        if not monster_map.get_passable(x,y):
            if not self.skill_to_cast.targets_monster:
                loop.add_message("You can't cast " + self.skill_to_cast.name + " on a space with a monster")
                self.void_skill()
                return
            monster = monster_map.locate(x,y)
            # print(monster)
            if self.skill_to_cast.castable(monster):
                if self.temp_cast:
                    self.skill_to_cast.try_to_activate(monster, loop)
                    self.caster.inventory.ready_scroll.consume_scroll(self.caster)
                    loop.add_message("You cast " + str(self.skill_to_cast.name) + " on " + monster.name)
                    self.void_skill()
                else:
                    self.caster.cast_skill(self.index_to_cast, monster, loop, self.quick_cast)
                    loop.add_message("You cast " + str(self.skill_to_cast.name) + " on " + monster.name)
                    self.void_skill()
            else:
                loop.add_message("You can't cast " + self.skill_to_cast.name + " on " + monster.name + " right now")
                self.void_skill()
        else:
            if not self.skill_to_cast.targets_monster:
                if self.temp_cast:
                    self.skill_to_cast.try_to_activate((x, y), loop)
                    self.caster.inventory.ready_scroll.consume_scroll(self.caster)
                    loop.add_message("You cast " + str(self.skill_to_cast.name))
                    self.void_skill()
                else:
                    self.caster.cast_skill(self.index_to_cast, (x, y), loop)
                    loop.add_message("You cast " + str(self.skill_to_cast.name))
                    self.void_skill()
            else:
                loop.add_message("Not a valid target there")
            


    def explain_target(self, loop):
        x, y = self.target_current
        monster_map = loop.generator.monster_map
        item_map = loop.generator.item_map
        tile_map = loop.generator.tile_map.track_map
        if not tile_map[x][y].visible:
            loop.add_message("You can't see that location")
            return False
        loop.add_message("That is a " + tile_map[x][y].name + " my friend")
        if not monster_map.get_passable(x,y):
            monster = monster_map.locate(x,y)
            loop.add_message("And there is a " + monster.name + " inhabiting it" )
        if not item_map.get_passable(x,y):
            item = item_map.locate(x, y)
            loop.add_message("There is a " + item.name + " there as well")
        return True

