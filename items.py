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
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Ax")
        self.melee = True
        self.name = "Ax"

    def attack(self):
        damage = R.roll_dice(20, 40)[0]
        return damage

class Hammer(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Hammer")
        self.melee = True
        self.name = "Hammer"

    def attack(self):
        damage = R.roll_dice(5, 60)[0]
        return damage

class HealthPotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Health Potion")
        self.consumeable = True

    def activate(self, entity):
        entity.gain_health(20)
        self.destroy = True

class MightPotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Might Potion")
        self.consumeable = True

    def activate(self, entity):
        effect = E.Might(5, 50)
        entity.add_status_effect(effect)
        self.destroy = True

class HastePotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Haste Potion")
        self.consumeable = True

    def activate(self, entity):
        effect = E.Haste(5, 50)
        entity.add_status_effect(effect)
        self.destroy = True

class CurePotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Cure Potion")
        self.consumeable = True

    def activate(self, entity):
        for effect in entity.status_effects:
            effect.remove(entity)
        entity.status_effects = []
        self.destroy = True

class ManaPotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Mana Potion")
        self.consumeable = True

    def activate(self, entity):
        entity.gain_mana(20)
        self.destroy = True