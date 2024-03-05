import dice as R
import objects as O
import effect as E

"""
All detailed items are initialized here.
"""
class Equipment(O.Item):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.equipable = True

class Weapon(Equipment):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.damage_min = 0
        self.damage_max = 0

    def equip(self, entity):
        if entity.main_weapon != None:
            entity.unequip(entity.main_weapon)
        entity.main_weapon = self

    def unequip(self, entity):
        entity.main_weapon = None

    def attack(self):
        damage = R.roll_dice(self.damage_min, self.damage_max)[0]
        return damage

class Ax(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Ax")
        self.melee = True
        self.name = "Ax"
        self.description = "An ax with a round edge (could be rounder)"
        self.damage_min = 20
        self.damage_max = 40

    def attack(self):
        damage = R.roll_dice(20, 40)[0]
        return damage

class Hammer(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Hammer")
        self.melee = True
        self.name = "Hammer"
        self.description = "A hammer that you wish was more spherical."
        self.damage_min = 5
        self.damage_max = 60

class Dagger(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Dagger")
        self.melee = True
        self.name = "Dagger"
        self.description = "I swear that tip is getting rounder... Larry!"
        self.damage_min = 3
        self.damage_max = 20

class Shield(Equipment):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Shield")
        self.shield = True
        self.defense = 5
        self.description = "A shield that you can use to block things."

    def defend(self):
        return self.defense

    def equip(self, entity):
        if entity.main_shield != None:
            entity.unequip(entity.main_shield)
        entity.main_shield = self

    def unequip(self, entity):
        entity.main_shield = None

class Ring(Equipment):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Ring")
        self.description = "The most circulr thing you own"

    def equip(self, entity):
        if len(entity.main_rings) >= 2 :
            entity.unequip(entity.main_rings[0])
        entity.main_rings.append(self)
        entity.move_cost -= 20

    def unequip(self, entity):
        entity.main_rings.pop(0)
        entity.move_cost += 20


class HealthPotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Health Potiorb")
        self.consumeable = True
        self.description = "A potiorb that heals you."

    def activate(self, entity):
        entity.gain_health(20)
        self.destroy = True

class MightPotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Might Potiorb")
        self.consumeable = True
        self.description = "A potiorb that makes you stronger for a few turns."

    def activate(self, entity):
        effect = E.Might(5, 5)
        entity.add_status_effect(effect)
        self.destroy = True


class DexterityPotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, 1, 0, render_tag, "Dexterity Potiorb")
        self.consumeable = True
        self.description = "A potiorb that makes you more dexterous for a few turns."

    def activate(self, entity):
        effect = E.Haste(5, 5)
        entity.add_status_effect(effect)
        self.destroy = True

class CurePotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Cure Potiorb")
        self.consumeable = True
        self.description = "A potiorb that cures you of all status effects."

    def activate(self, entity):
        for effect in entity.status_effects:
            effect.remove(entity)
        entity.status_effects = []
        self.destroy = True

class ManaPotion(O.Item):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Mana Potiorb")
        self.consumeable = True
        self.description = "A potiorb that restores your mana."

    def activate(self, entity):
        entity.gain_mana(20)
        self.destroy = True

