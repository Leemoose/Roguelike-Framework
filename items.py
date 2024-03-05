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
        self.description = "Its a " + name + "."
        self.stackable = False

    def activate(self, entity):
        pass

    def deactivate(self, entity):
        pass

class Weapon(Equipment):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.damage_min = 0
        self.damage_max = 0
        self.equipment_type = "Weapon"

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

class Armor(Equipment):
    def __init__(self, x,y, id_tag, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, "Armor")
        self.name = "Armor"
        self.armor = 0

    def activate(self, entity):
        if entity.armor :
            entity.armor = 0
        entity.armor += self.armor

    def deactivate(self, entity):
        entity.armor -= self.armor

class Shield(Armor):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Shield")
        self.equipment_type = "Shield"
        self.name = "Shield"
        self.shield = True
        self.armor = 5
        self.description = "A shield that you can use to block things."

    def equip(self, entity):
        if entity.main_shield != None:
            entity.unequip(entity.main_shield)
        entity.main_shield = self
        self.activate(entity)

    def unequip(self, entity):
        entity.main_shield = None
        self.deactivate(entity)

class Ring(Equipment):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Ring")
        self.equipment_type = "Ring"
        self.name = "Ring"
        self.description = "The most circulr thing you own"

    def equip(self, entity):
        if len(entity.main_rings) >= 2 :
            entity.unequip(entity.main_rings[0])
        entity.main_rings.append(self)
        entity.move_cost -= 20

    def unequip(self, entity):
        entity.main_rings.pop(0)
        entity.move_cost += 20

class Chestarmor(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Armor")
        self.equipment_type = "Armor"
        self.name = "Armor"
        self.armor = 5

    def equip(self, entity):
        if entity.main_armor != None:
            entity.unequip(entity.armor)
        entity.main_armor = self
        entity.armor = self.armor
        self.activate(entity)

    def unequip(self, entity):
        entity.armor = None
        self.deactivate(entity)

class Boots(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Boots")
        self.equipment_type = "Boots"
        self.name = "Boots"
        self.armor = 1


    def equip(self, entity):
        if entity.boots != None:
            entity.unequip(entity.boots)
        entity.boots = self
        self.activate(entity)

    def unequip(self, entity):
        entity.boots = None
        self.deactivate(entity)

class Gloves(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Gloves")
        self.equipment_type = "Gloves"
        self.description = "Gloves to keep your hands toasty warm."
        self.name = "Gloves"
        self.armor = 1

    def equip(self, entity):
        if entity.gloves != None:
            entity.unequip(entity.gloves)
        entity.gloves = self
        self.activate(entity)

    def unequip(self, entity):
        entity.gloves = None
        self.deactivate(entity)

class Helmet(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Helmet")
        self.equipment_type = "Helmet"
        self.name = "Helmet"
        self.armor = 1


    def equip(self, entity):
        if entity.helmet != None:
            entity.unequip(entity.helmet)
        entity.helmet = self
        self.activate(entity)

    def unequip(self, entity):
        entity.helmet = None
        self.deactivate(entity)

class Potion(O.Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Potiorb"
        self.consumeable = True
        self.stackable = True
        self.stacks = 1
        self.description = "A potiorb that does something."

    def activate_once(self, entity):
        pass

    def activate(self, entity):
        self.activate_once(entity)
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True

        

class HealthPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Health Potiorb")
        self.description = "A potiorb that heals you."

    def activate_once(self, entity):
        entity.gain_health(20)

class MightPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Might Potiorb")
        self.description = "A potiorb that makes you stronger for a few turns."

    def activate_once(self, entity):
        effect = E.Might(5, 5)
        entity.add_status_effect(effect)

class DexterityPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Dexterity Potiorb")
        self.description = "A potiorb that makes you more dexterous for a few turns."

    def activate_once(self, entity):
        effect = E.Haste(5, 5)
        entity.add_status_effect(effect)

class CurePotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Cure Potiorb")
        self.description = "A potiorb that cures you of all status effects."

    def activate_once(self, entity):
        for effect in entity.status_effects:
            effect.remove(entity)
        entity.status_effects = []

class ManaPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mana Potiorb")
        self.description = "A potiorb that restores your mana."

    def activate_once(self, entity):
        entity.gain_mana(20)

