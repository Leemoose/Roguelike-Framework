from objects import Objects
from items import ForestOrb, OceanOrb

class Interactable(Objects):
    def __init__(self, render_tag = 0, x=-1, y=-1, name="Interactable"):
        super().__init__(x=x, y=y,id_tag=-1, render_tag= render_tag, name = name)
        self.name = name
        self.active = True

    def interact(self, loop):
        pass

class Campfire(Interactable):
    def __init__(self, render_tag = 3000,x=-1, y = -1, name="Campfire"):
        super().__init__(render_tag, x, y, name=name)
        self.used = False

    def interact(self, entity, loop):
        if self.active and loop.get_daytime() == "Nighttime":
            loop.change_daytime()
            self.active = False
            loop.add_message("You rested at the campfire")
            entity.character.change_health(entity.character.get_max_health()-entity.character.get_health())
            self.render_tag = 3001

class OrbPedastool(Interactable):
    def __init__(self, render_tag=0, x=-1, y=-1, name="Orb Pedastool"):
        super().__init__(x=x, y=y, render_tag= render_tag, name = name)
        self.name = name
        self.main_render_tag = 0
        self.deactivated_render_tag = 0
        self.traits["orb_pedastool"] = True
        self.orb_type = "orb"

    def interact(self, loop):
        if self.active:
            loop.player.inventory.get_item(self.orb, loop)
            self.render_tag = self.deactivated_render_tag
            self.active = False
        else:
            for orb in loop.player.inventory.get_orb_inventory():
                if orb.has_trait(self.orb_type):
                    self.orb = orb
                    loop.player.inventory.remove_item(orb)
                    self.active = True
                    self.render_tag = self.main_render_tag
                    break

class ForestOrbPedastool(OrbPedastool):
    def __init__(self, render_tag = 3900, x=-1, y=-1, name="Forest Orb Pedastool"):
        super().__init__( render_tag= render_tag, x=x, y=y, name = name)
        self.name = name
        self.orb = ForestOrb()
        self.deactivated_render_tag = 3901
        self.main_render_tag = 3900
        self.traits["forest_orb_pedastool"] = True
        self.orb_type = "forest_orb"

class OceanOrbPedastool(OrbPedastool):
    def __init__(self, render_tag = 3910, x=-1, y=-1, name="Ocean Orb Pedastool"):
        super().__init__( render_tag= render_tag, x=x, y=y, name = name)
        self.name = name
        self.orb = OceanOrb()
        self.deactivated_render_tag = 3911
        self.main_render_tag = 3910
        self.traits["ocean_orb_pedastool"] = True
        self.orb_type = "ocean_orb"




