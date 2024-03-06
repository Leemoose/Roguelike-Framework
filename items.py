import dice as R
import objects as O
import effect as E
import skills as S

"""
All detailed items are initialized here.
"""
class Equipment(O.Item):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.equipable = True
        self.description = "Its a " + name + "."
        self.stackable = False
        self.attached_skill = None

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
        self.on_hit = None

    def equip(self, entity):
        if entity.main_weapon != None:
            entity.unequip(entity.main_weapon)
        if self.attached_skill != None:
            entity.add_skill(self.attached_skill(entity.parent))
        entity.main_weapon = self

    def unequip(self, entity):
        entity.main_weapon = None
        if self.attached_skill != None:
            entity.remove_skill(self.attached_skill(entity.parent).name)

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

class MagicWand(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Magic Wand")
        self.melee = True
        self.name = "Magic Wand"
        self.description = "A wand that you can use to cast magic missile. You can also use it in melee but why would you?"
        self.damage_min = 1
        self.damage_max = 5
        self.attached_skill = (lambda owner : S.MagicMissile(owner, cooldown=3, cost=5, damage=25, range=6, action_cost=100))

class FlamingSword(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Flaming Sword")
        self.melee = True
        self.name = "Flaming Sword"
        self.description = "A sword that is on fire. You can channel its fire to cast a Burning Attack at a distant foe. "
        self.damage_min = 15
        self.damage_max = 20

        self.on_hit = (lambda inflictor : E.Burn(5, 3, inflictor))

        self.attached_skill = (lambda owner : S.BurningAttack(owner, cooldown=5, cost=10, damage=10, burn_damage=5, burn_duration=10, range=5))
    
    def attack(self):
        return (super().attack(), self.on_hit)

class Armor(Equipment):
    def __init__(self, x,y, id_tag, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, "Armor")
        self.name = "Armor"
        self.armor = 0

    def activate(self, entity):
        if entity.armor == None:
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
    def __init__(self, render_tag, name):
        super().__init__(-1,-1, 0, render_tag, name)
        self.equipment_type = "Ring"
        self.name = name
        self.description = "A ring that does something."

    def equip(self, entity):
        if len(entity.main_rings) >= 2 :
            entity.unequip(entity.main_rings[0])
        entity.main_rings.append(self)
        self.activate(entity)

    def unequip(self, entity):
        entity.main_rings.pop(0)
        self.deactivate(entity)

class RingOfSwiftness(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Swiftness")
        self.description = "The most circular thing you own, it makes you feel spry on your feet"

    def activate(self, entity):
        entity.move_cost -= 20

    def deactivate(self, entity):
        entity.move_cost += 20

class BloodRing(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Blood Ring")
        self.description = "Pricking your finger on the spikes of this ring makes you feel alive."
        
        # skill doesn't have an owner until equipped to an entity, so need a lambda expression here
        self.attached_skill = (lambda owner : S.BloodPact(owner, cooldown=10, cost=10, strength_increase=10, duration=4, action_cost=100))
        
    def equip(self, entity):
        if len(entity.main_rings) >= 2 :
            entity.unequip(entity.main_rings[0])
        entity.add_skill(self.attached_skill(entity.parent))
        entity.main_rings.append(self)

    def unequip(self, entity):
        entity.main_rings.pop(0)
        # if other ring is a blood ring don't remove skill
        if entity.main_rings[0].name != "Blood Ring":
            entity.remove_skill(self.attached_skill(entity.parent).name)

class RingOfMight(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Might")
        self.equipment_type = "Ring"
        self.name = "Ring of Might"
        self.description = "A ring that makes you feel stronger."

    def activate(self, entity):
        entity.strength += 10

    def deactivate(self, entity):
        entity.strength -= 10

class RingOfMana(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Mana")
        self.description = "A ring that every spellcaster is given on their 10th birthday"

    def activate(self, entity):
        entity.mana += 30
        entity.mana_regen += 5
        entity.intelligence += 5

    def deactivate(self, entity):
        entity.mana -= 30
        entity.mana_regen -= 5
        entity.intelligence -= 5

class BoneRing(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Bone Ring")
        self.description = "An eerie ring that makes you much stronger and faster while wearing it but rapidly drains your health and mana"

    def activate(self, entity):
        entity.strength += 10
        entity.dexterity += 10
        entity.mana_regen -= 10
        entity.health_regen -= 10
        
    def deactivate(self, entity):
        entity.strength -= 10
        entity.dexterity -= 10
        entity.mana_regen += 10
        entity.health_regen += 10

class Chestarmor(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Armor")
        self.equipment_type = "Chestarmor"
        self.name = "Armor"
        self.armor = 5

    def equip(self, entity):
        if entity.main_armor != None:
            entity.unequip(entity.main_armor)
        entity.main_armor = self
        self.activate(entity)

    def unequip(self, entity):
        entity.chestarmor = None
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

class BootsOfEscape(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Boots of Escape")
        self.equipment_type = "Boots"
        self.name = "Boots of Escape"
        self.armor = 0
        self.description = "Boots that let you cast the skill flee"
        self.skill_attached = (lambda owner : S.Escape(owner, cooldown=10, cost=25, self_fear=False, activation_threshold=1.1, action_cost=1))
        

    def equip(self, entity):
        if entity.boots != None:
            entity.unequip(entity.boots)
        entity.boots = self
        entity.add_skill(self.skill_attached(entity.parent))
        self.activate(entity)

    def unequip(self, entity):
        entity.boots = None
        entity.remove_skill(self.skill_attached(entity.parent).name)
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

class VikingHelmet(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Viking Helmet")
        self.equipment_type = "Helmet"
        self.name = "Viking Helmet"
        self.armor = 0
        self.description = "A helmet that lets you go berserk below a quarter health"
        self.attached_skill = (lambda owner : S.Berserk(owner, cooldown=0, cost=10, duration=10, activation_threshold=0.25, strength_increase=10, action_cost=1))

    def equip(self, entity):
        if entity.helmet != None:
            entity.unequip(entity.helmet)
        entity.helmet = self
        entity.add_skill(self.attached_skill(entity.parent))
        self.activate(entity)

    def unequip(self, entity):
        entity.helmet = None
        entity.remove_skill(self.attached_skill(entity.parent).name)
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

