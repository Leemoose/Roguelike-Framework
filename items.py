import dice as R
import objects as O
import effect as E

"""
All detailed items are initialized here.
"""
class Weapon(O.Item):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.equipable = True

class Ax(Weapon):
    def __init__(self, render_tag, x, y):
        super().__init__(x, y, 0, render_tag, "Ax")
        self.melee = True
        self.name = "Ax"

    def attack(self):
        damage = R.roll_dice(20, 40)[0]
        return damage

class Hammer(Weapon):
    def __init__(self, render_tag, x, y):
        super().__init__(x, y, 0, render_tag, "Hammer")
        self.melee = True
        self.name = "Hammer"

    def attack(self):
        damage = R.roll_dice(5, 60)[0]
        return damage

class HealthPotion(O.Item):
    def __init__(self, render_tag, x, y):
        super().__init__(x, y, 0, render_tag, "Health Potion")
        self.consumeable = True

    def activate(self, entity):
        entity.gain_health(20)
        self.destroy = True
<<<<<<< HEAD

class MightPotion(O.Item):
    def __init__(self, render_tag, x, y):
        super().__init__(x, y, 0, render_tag, "Might Potion")
        self.consumeable = True

    def activate(self, entity):
        effect = E.Might(5, 50)
        entity.add_status_effect(effect)
        self.destroy = True

class HastePotion(O.Item):
    def __init__(self, render_tag, x, y):
        super().__init__(x, y, 0, render_tag, "Haste Potion")
        self.consumeable = True

    def activate(self, entity):
        effect = E.Haste(5, 50)
        entity.add_status_effect(effect)
        self.destroy = True
