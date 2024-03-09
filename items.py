import dice as R
import objects as O
import effect as E
import skills as S
import loops as L

"""
All detailed items are initialized here.
"""
class Equipment(O.Item):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.equipable = True
        self.description = "Its a " + name + "."
        self.stackable = False
        self.level = 1
        self.can_be_levelled = True
        self.equipped = False
        self.wearer = None
        self.cursed = False
        self.rarity = "Common"
        self.required_strength = 0
        self.attached_skill_exists = False
        self.yendorb = False

    def activate(self, entity):
        self.wearer = entity

    def deactivate(self, entity):
        self.wearer = None

    def enchant(self):
        self.level += 1

    def can_be_equipped(self, entity):
        return self.equipable

    def can_be_unequipped(self, entity):
        return (self.equipped and not self.cursed)

    def get_attached_skill_description(self):
        if self.attached_skill_exists:
            return self.attached_skill(None).description() # temporarily attach skill to nothing to get name
        else:
            return None

class Weapon(Equipment):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.damage_min = 0
        self.damage_max = 0
        self.equipment_type = "Weapon"
        self.on_hit = None

    def equip(self, entity):
        if entity.strength >= self.required_strength:
            if entity.main_weapon != None:
                entity.unequip(entity.main_weapon)
            if self.attached_skill_exists:
                entity.add_skill(self.attached_skill(entity.parent))
            entity.main_weapon = self
            self.activate(entity)

    def unequip(self, entity):
        entity.main_weapon = None
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)
        self.deactivate(entity)

    def attack(self):
        damage = R.roll_dice(self.damage_min, self.damage_max)[0]
        return damage

class Ax(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Axe")
        self.melee = True
        self.name = "Axe"
        self.description = "An axe with a round edge (could be rounder). A solid weapon for a solid warrior."
        self.damage_min = 20
        self.damage_max = 40
    
    def level_up(self):
        self.level += 1
        if self.level == 2:
            self.description += " It's been enchanted to be more effective."
        if self.level == 6:
            self.description = "An axe with the roundest edge ever seen. It's been enchanted as much as possible."
        self.damage_min += 10
        self.damage_max += 10

class Hammer(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Hammer")
        self.melee = True
        self.name = "Hammer"
        self.description = "A hammer that you wish was more spherical. High damage potential but hard to get a solid hit in."
        self.damage_min = 5
        self.damage_max = 60

    def level_up(self):
        self.level += 1
        if self.level == 2:
            self.description += " It's been enchanted to hit harder"
        if self.level == 6:
            self.description = "A hammer with incredible damage potential. Still not the easiest to get a clean hit in. It's been enchanted as much as possible."
        self.damage_min += 5
        self.damage_max += 15

class Dagger(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Dagger")
        self.melee = True
        self.name = "Dagger"
        self.description = "I swear that tip is getting rounder... Larry!. Enchanting it might make it more pointy and precise."
        self.damage_min = 3
        self.damage_max = 20

    def level_up(self):
        self.level += 1
        if self.level == 2:
            self.description += " It's been enchanted to be more precise."
        if self.level == 6:
            self.description = "A dagger that always strikes accurately, never dealing less than full damage. It's been enchanted as much as possible."
        self.damage_min += 10
        self.damage_max += 5
        if self.damage_min > self.damage_max:
            self.damage_min = self.damage_max


class MagicWand(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Magic Wand")
        self.melee = True
        self.name = "Magic Wand"
        self.description = "A wand that you can use to cast magic missile. You can also use it in melee but why would you?"
        self.damage_min = 1
        self.damage_max = 5
        self.magic_missile_damage = 25
        self.magic_missile_range = 6
        self.magic_missile_cost = 10
        self.magic_missile_cooldown = 3
        self.attached_skill_exists = True
        
        self.wearer = None # items with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Common"

        self.attached_skill_exists = True

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.MagicMissile(owner, self.magic_missile_cooldown, 
                                     self.magic_missile_cost, 
                                     self.magic_missile_damage, 
                                     self.magic_missile_range, 
                                     action_cost=100)

    def level_up(self):
        self.level += 1
        if self.level == 2:
            self.description += " It's been enchanted cast a stronger magic missile"
        if self.level == 6:
            self.description = "A wand that you can use to cast an immensely powerful magic missile. It's been enchanted as much as possible."

        # level up improves magic missile
        self.magic_missile_damage += 5
        self.magic_missile_range += 1
        self.magic_missile_cooldown -= 1
        if self.magic_missile_cooldown < 0:
            self.magic_missile_cooldown = 0
        
        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

        
class FlamingSword(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Flaming Sword")
        self.melee = True
        self.name = "Flaming Sword"
        self.description = "A sword that is on fire. You can channel its fire to cast a Burning Attack at a distant foe. "
        self.damage_min = 15
        self.damage_max = 20

        self.on_hit_burn = 5
        self.on_hit_burn_duration = 3
        self.on_hit = (lambda inflictor : E.Burn(self.on_hit_burn, self.on_hit_burn_duration, inflictor))
        self.on_hit_description = f"Burns the target for {self.on_hit_burn} damage over {self.on_hit_burn_duration} turns."

        self.skill_cooldown = 5
        self.skill_cost = 10
        self.skill_damage = 10
        self.skill_burn_damage = 5
        self.skill_burn_duration = 10
        self.skill_range = 5
        self.attached_skill_exists = True

        self.wearer = None # items with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Legendary"

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.BurningAttack(owner, self.skill_cooldown, 
                                self.skill_cost, 
                                self.skill_damage, 
                                self.skill_burn_damage, 
                                self.skill_burn_duration, 
                                self.skill_range)

    def attack(self):
        return (super().attack(), self.on_hit)
    
    def level_up(self):
        self.level += 1
        if self.level == 2:
            self.description += " It's been enchanted to hit harder and burn stronger."
        if self.level == 6:
            self.description = "A sword that burns intensely. It's burning strike has reached its maximum potency. It's been enchanted as much as possible."
        self.damage_min += 5
        self.damage_max += 5
        self.on_hit_burn += 5
        self.skill_damage += 5
        self.skill_burn_damage += 5
        self.skill_cooldown -= 1
        if self.skill_cooldown < 2:
            self.skill_cooldown = 2
        
        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

class Armor(Equipment):
    def __init__(self, x,y, id_tag, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, "Armor")
        self.name = "Armor"
        self.armor = 0

    def activate(self, entity):
        if entity.armor == None:
            entity.armor = 0
        entity.armor += self.armor
        super().activate(entity)

    def deactivate(self, entity):
        entity.armor -= self.armor
        super().deactivate(entity)

    def can_be_equipped(self, entity):
        return (entity.strength * entity.round_bonus()) >= self.required_strength and self.equipable

class Shield(Armor):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Shield"
        self.name = name
        self.shield = True
        self.description = "A shield that you can use to block things."

    def equip(self, entity):
        if entity.strength >= self.required_strength:
            if entity.main_shield != None:
                entity.unequip(entity.main_shield)
            entity.main_shield = self
            self.activate(entity)

    def unequip(self, entity):
        entity.main_shield = None
        self.deactivate(entity)

class BasicShield(Shield):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Shield")
        self.armor = 3
        self.description = "A shield that you can use to block things."

    def level_up(self):
        self.level += 1
        self.armor += 3
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A shield that you can use to block nearly anything. It's been enchanted as much as possible."

class Aegis(Shield):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Aegis")
        self.armor = 5
        self.description = "A shield with the face of a horrifying monster on it. It can turn your enemies to stone"
        self.required_strength = 2

        self.skill_cooldown = 10
        self.skill_cost = 20
        self.skill_duration = 3
        self.skill_activation_chance = 0.3
        self.skill_range = 3

        self.attached_skill_exists = True

        self.rarity = "Rare"

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Petrify(owner, self.skill_cooldown, 
                                self.skill_cost, 
                                self.skill_duration, 
                                self.skill_activation_chance, 
                                self.skill_range)

    def activate(self, entity):
        entity.add_skill(self.attached_skill(entity.parent))
        return super().activate(entity)

    def deactivate(self, entity):
        entity.remove_skill(self.attached_skill(entity.parent).name)
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 2

        self.skill_activation_chance += 0.2
        if self.skill_activation_chance > 1.0:
            self.skill_activation_chance = 1.0
        
        self.skill_range += 1
        if self.skill_range > 6:
            self.skill_range = 6

        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))
        
        if self.level == 2:
            self.description += " It's been enchanted to be even uglier."
        if self.level == 6:
            self.description = "A shield with the face of a horrifying monster on it. It can turn your enemies to stone for longer. It's been enchanted as much as possible."

class TowerShield(Shield):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Tower Shield")
        self.armor = 10
        self.description = "A massive shield that can block nearly anything but is unwieldy to use"
        self.dex_debuff = 5
        self.required_strength = 3


    def activate(self, entity):
        entity.dexterity -= self.dex_debuff
        return super().activate(entity)
    
    def deactivate(self, entity):
        entity.dexterity += self.dex_debuff
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 1
        self.dex_debuff -= 1
        if self.dex_debuff < 0:
            self.dex_debuff = 0
        if self.wearer != None:
            self.wearer.dexterity += 1
        if self.level == 2:
            self.description += " It's been enchanted to be less unwieldy."
        if self.level == 6:
            self.description = "A massive shield that can block nearly anything. It's been enchanted as much as possible."

class MagicFocus(Shield):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Magic Focus")
        self.armor = 0
        self.description = "An orb that takes your offhand but lets you cast even more powerful spells."
        self.intelligence_buff = 6

        self.rarity = "Rare"
        
    def activate(self, entity):
        entity.intelligence += self.intelligence_buff
        return super().activate(entity)

    def deactivate(self, entity):
        entity.intelligence -= self.intelligence_buff
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        
        self.intelligence_buff += 2
        if self.wearer != None:
            self.wearer.intelligence += 2

        if self.level == 2:
            self.description += " It's been enchanted to be more effective."
        if self.level == 6:
            self.description = "An orb that takes your offhand but lets you cast the most powerful spells. It's been enchanted as much as possible."

class Ring(Equipment):
    def __init__(self, render_tag, name):
        super().__init__(-1,-1, 0, render_tag, name)
        self.equipment_type = "Ring"
        self.name = name
        self.description = "A ring that does something."
        self.can_be_levelled = False

    def equip(self, entity):
        if self.equipped:
            return
        if entity.force_ring_2:
            entity.ring_2 = self
            entity.force_ring_2 = False
        elif entity.ring_1 == None:
            entity.ring_1 = self
        elif entity.ring_2 == None: # and ring_1 is not
            entity.ring_2 = self
        else: # both rings are equipped
            entity.ring_1.deactivate(entity)
            entity.ring_1 = entity.ring_2
            entity.ring_2 = self
        self.activate(entity)

    def unequip(self, entity):
        if entity.ring_1 == self:
            entity.ring_1 = entity.ring_2
            entity.ring_2 = None
        elif entity.ring_2 == self:
            entity.ring_2 = None
        self.deactivate(entity)

class RingOfSwiftness(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Swiftness")
        self.description = "The most circular thing you own, it makes you feel spry on your feet"
        self.rarity = "Rare"

    def activate(self, entity):
        entity.move_cost -= 20

    def deactivate(self, entity):
        entity.move_cost += 20

class BloodRing(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Blood Ring")
        self.description = "Pricking your finger on the spikes of this ring makes you feel alive."
        
        # skill doesn't have an owner until equipped to an entity, so need a lambda expression here
        self.rarity = "Rare"
        self.attached_skill_exists = True

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.BloodPact(owner, cooldown=10, cost=10, strength_increase=10, duration=4, action_cost=100)
        

    def activate(self, entity):
        entity.add_skill(self.attached_skill(entity.parent))

    def deactivate(self, entity):
        if entity.ring_1 != None and entity.ring_1.name == "Blood Ring":
            return # don't remove skill if other ring was a blood ring
        entity.remove_skill(self.attached_skill(entity.parent).name)
        

class RingOfMight(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Might")
        self.equipment_type = "Ring"
        self.name = "Ring of Might"
        self.description = "A ring that makes you feel stronger."

        self.rarity = "Rare"

    def activate(self, entity):
        entity.strength += 10

    def deactivate(self, entity):
        entity.strength -= 10

class RingOfMana(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Mana")
        self.description = "A ring that every spellcaster is given on their 10th birthday"

        self.rarity = "Rare"

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

        self.rarity = "Legendary"

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

class RingOfTeleportation(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Teleportation")
        self.description = "The most circular thing you own, it makes you feel spry on your feet"
        self.rarity = "Rare"
        self.name = "Ring of Teleportation"

        self.wearer = None  # items with stat buffs need to keep track of owner for level ups

        self.skill_cooldown =100
        self.skill_cost = 0

        self.attached_skill_exists = True

        self.rarity = "Legendary"

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Teleport(owner, self.skill_cooldown, self.skill_cost)

    def activate(self, entity):
        entity.add_skill(self.attached_skill(entity.parent))
        self.wearer = entity
        return super().activate(entity)

    def deactivate(self, entity):
        entity.remove_skill(self.attached_skill(entity.parent).name)
        self.wearer = None
        return super().deactivate(entity)
"""
    def level_up(self):
        self.level += 1
        if self.level == 2:
            self.description += " It seems to be growing stronger?"
        if self.level == 6:
            self.skill_cooldown = 0
            self.description = "Unlimited power."
            """


class BodyArmor(Armor):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Body Armor"
        self.name = name
        self.description = "A piece of armor that covers your chest."
        self.armor = 0

    def equip(self, entity):
        if entity.main_armor != None:
            entity.unequip(entity.main_armor)
        entity.main_armor = self
        self.activate(entity)
    
    def unequip(self, entity):
        entity.main_armor = None
        self.deactivate(entity)

class Chestarmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Chest Plate")
        self.description = "A reliable piece of armor that covers your chest."
        self.armor = 8
        self.required_strength = 3

    def level_up(self):
        self.level += 1
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A chest plate that absorbs most hits for you. It's been enchanted as much as possible."
        self.armor += 5

class LeatherArmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Leather Armor")
        self.description = "A comfortable piece of armor, that helps you feel lighter on your feet. "
        self.armor = 2
        self.dex_buff = 2
        self.wearer = None # items with stat buffs need to keep track of owner for level ups

    def activate(self, entity):
        entity.dexterity += self.dex_buff
        return super().activate(entity)

    def deactivate(self, entity):
        entity.dexterity -= self.dex_buff
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 1
        self.dex_buff += 1
        if self.wearer != None:
            self.wearer.dexterity += 1
        if self.level == 2:
            self.description += " It's been enchanted to make you more nimble."
        if self.level == 6:
            self.description = "Comfortable armor that makes you feel incredibly fast on your feet while offering decent protection. It's been enchanted as much as possible."

class GildedArmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Gilded Armor")
        self.description = "A piece of golden armor studded with gems. Just wearing it makes you feel like you can ignore trivial things like status effects."
        self.armor = 3
        self.required_strength = 1
        
        self.skill_cooldown = 15
        self.skill_cost = 20
        self.activation_chance = 0.5

        self.attached_skill_exists = True
        
        self.rarity = "Rare"

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.ShrugOff(owner, self.skill_cooldown, self.skill_cost, self.activation_chance, action_cost=100)

    def activate(self, entity):
        entity.add_skill(self.attached_skill(entity.parent))
        return super().activate(entity)

    def deactivate(self, entity):
        entity.remove_skill(self.attached_skill(entity.parent).name)
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 3

        self.skill_cooldown -= 1
        if self.skill_cooldown < 5:
            self.skill_cooldown = 5
        self.skill_cost -= 2
        if self.skill_cost < 10:
            self.skill_cost = 10
        self.activation_chance += 0.2
        if self.activation_chance > 1.0:
            self.activation_chance = 1.0

        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

        if self.level == 2:
            self.description += " It's been enchanted to make you feel more invincible."
        if self.level == 6:
            self.description = "A work of art covered in gold and studded in gemstones. Let's you always ignore a status condition. It's been enchanted as much as possible."

class WarlordArmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Warlord Armor")
        self.description = "Bloodstained armor that belonged to a famous warrior. Wearing it makes you stronger and your enemies more terrified."
        self.armor = 3
        self.required_strength = 1
        self.strength_buff = 2

        self.wearer = None # items with stat buffs need to keep track of owner for level ups

        self.skill_cooldown = 10
        self.skill_cost = 10
        self.skill_duration = 3
        self.skill_activation_chance = 0.5
        self.skill_range = 2

        self.attached_skill_exists = True
        
        self.rarity = "Legendary"

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Terrify(owner, self.skill_cooldown, 
                                self.skill_cost, 
                                self.skill_duration, 
                                self.skill_activation_chance, 
                                self.skill_range)


    def activate(self, entity):
        entity.add_skill(self.attached_skill(entity.parent))
        self.wearer = entity
        return super().activate(entity)

    def deactivate(self, entity):
        entity.remove_skill(self.attached_skill(entity.parent).name)
        self.wearer = None
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 3
        self.strength_buff += 1
        if self.wearer != None:
            self.wearer.strength += 1

        self.skill_activation_chance += 0.1
        if self.skill_activation_chance > 1.0:
            self.skill_activation_chance = 1.0
        self.skill_range += 1
        if self.skill_range > 5:
            self.skill_range = 5

        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

        if self.level == 2:
            self.description += " It's been enchanted to make you more strong and frightening"
        if self.level == 6:
            self.description = "Bloodstained armor that marks you as a famous warrior who fought in many battles. Your enemies are terrified even from a distance. It's been enchanted as much as possible."


class BloodstainedArmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Bloodstained Armor")
        self.description = "A maligment aura surronds this armor."
        self.armor = 8
        self.required_strength = 3
        self.strength_buff = 10
        self.cursed = True
        self.wearer = None  # items with stat buffs need to keep track of owner for level ups
        self.rarity = "Legendary"

    def activate(self, entity):
        self.wearer = entity
        self.wearer.strength += self.strength_buff
        return super().activate(entity)

    def deactivate(self, entity):
        self.wearer.strength -= self.strength_buff
        self.wearer = None
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 3
        self.strength_buff += 1
        if self.wearer != None:
            self.wearer.strength += 1
        if self.level == 2:
            self.description += " It's been enchanted to make its aura stronger"
        if self.level == 6:
            self.description = "An immensely menacing aura surround you and this armor bounds to your soul. It's been enchanted as much as possible."


class WizardRobe(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Wizard Robe")
        self.description = "A robe that makes you feel like you can cast spells all day long."
        self.armor = 1
        self.mana_buff = 20
        self.mana_regen_buff = 5
        self.intelligence_buff = 5

        self.wearer = None # items with stat buffs need to keep track of owner for level ups

        self.rarity = "Rare"

    def activate(self, entity):
        entity.mana += self.mana_buff
        entity.mana_regen += self.mana_regen_buff
        entity.intelligence += self.intelligence_buff
        return super().activate(entity)

    def deactivate(self, entity):
        entity.mana -= self.mana_buff
        entity.mana_regen -= self.mana_regen_buff
        entity.intelligence -= self.intelligence_buff
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.mana_buff += 10
        self.mana_regen_buff += 5
        self.intelligence_buff += 2

        if self.wearer != None:
            self.wearer.mana += 10
            self.wearer.mana_regen += 5
            self.wearer.intelligence += 2

        if self.level == 2:
            self.description += " It's been enchanted to make you more magical"
        if self.level == 6:
            self.description = "A robe that makes you feel like you can cast spells for all eternity. It's been enchanted as much as possible."

class KarateGi(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Karate Gi")
        self.description = "A gi that makes your unarmed combat stronger."
        self.damage_boost = 30

        self.armor = 1

        self.wearer = None # items with stat buffs need to keep track of owner for level ups

        self.rarity = "Rare"

    def activate(self, entity):
        entity.unarmed_damage_min += self.damage_boost
        entity.unarmed_damage_max += self.damage_boost
        return super().activate(entity)

    def deactivate(self, entity):
        entity.unarmed_damage_min -= self.damage_boost
        entity.unarmed_damage_max -= self.damage_boost
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 1
        self.damage_boost += 4
        if self.wearer != None:
            self.wearer.unarmed_damage_min += 4
            self.wearer.unarmed_damage_max += 4
        if self.level == 2:
            self.description += " It's been enchanted to make your fists stronger"
        if self.level == 6:
            self.description = "A gi that lets you punch through anything. It's been enchanted as much as possible."

class Boots(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Boots")
        self.equipment_type = "Boots"
        self.name = "Boots"
        self.armor = 1
        self.description = "Boots that are incredibly comfortable but only offer a little protection"


    def equip(self, entity):
        if entity.boots != None:
            entity.unequip(entity.boots)
        entity.boots = self
        self.activate(entity)

    def unequip(self, entity):
        entity.boots = None
        self.deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 1
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "Boots that are somehow incredibly comfy and tough at the same time. It's been enchanted as much as possible."

class BlackenedBoots(Boots):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.equipment_type = "Boots"
        self.name = "Blackened Boots"
        self.armor = 3
        self.dexterity_buff = 2
        self.cursed = True
        self.description = "A dark spirit dwells in these boots."

    def activate(self, entity):
        self.wearer = entity
        self.wearer.dexterity += self.dexterity_buff
        return super().activate(entity)

    def deactivate(self, entity):
        self.wearer.dexterity -= self.dexterity_buff
        self.wearer = None
        return super().deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 1
        self.dexterity_buff += 1
        if self.wearer != None:
            self.wearer.dexterity += 1
        if self.level == 2:
            self.description += " You see the quickest path in a sea of blood."
        if self.level == 6:
            self.description = "You ride on screaming winds."

class BootsOfEscape(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Boots of Escape")
        self.equipment_type = "Boots"
        self.name = "Boots of Escape"
        self.armor = 0
        self.description = "Boots that let you cast the skill flee"

        self.skill_cooldown = 10
        self.skill_cost = 25
        self.dex_buff = 20
        self.str_debuff = 10
        self.int_debuff = 10
        self.duration = 4
        self.rarity = "Rare"

        self.attached_skill_exists = True
    
    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Escape(owner, self.skill_cooldown, 
                        self.skill_cost, 
                        self_fear=False, 
                        dex_buff=self.dex_buff,
                        str_debuff=self.str_debuff,
                        int_debuff=self.int_debuff,
                        haste_duration=self.duration,
                        activation_threshold=1.1, 
                        action_cost=1)

    def equip(self, entity):
        if entity.boots != None:
            entity.unequip(entity.boots)
        entity.boots = self
        entity.add_skill(self.attached_skill(entity.parent))
        self.activate(entity)

    def unequip(self, entity):
        entity.boots = None
        entity.remove_skill(self.attached_skill(entity.parent).name)
        self.deactivate(entity)

    def level_up(self):
        self.level += 1
        if self.level == 2:
            self.description += " It's been enchanted to let you flee on a shorter cooldown."
        if self.level == 6:
            self.description = "Boots that let you flee at the drop of a hat. It's been enchanted as much as possible."
        self.skill_cooldown -= 1
        if self.skill_cooldown < 5:
            self.skill_cooldown = 5
        self.skill_cost -= 2
        if self.skill_cost < 10:
            self.skill_cost = 10
        self.dex_buff += 2
        self.str_debuff -= 1
        if self.str_debuff < 5:
            self.str_debuff = 5
        self.int_debuff -= 1
        if self.int_debuff < 5:
            self.int_debuff = 5
        self.duration += 1
        if self.duration > 6:
            self.duration = 6
        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

class Gloves(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Gloves")
        self.equipment_type = "Gloves"
        self.description = "Gloves to keep your hands toasty warm. Enchanting is especially effective on these."
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

    def level_up(self):
        self.level += 1
        self.armor += 3
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "Gloves that are incredibly warm and tough at the same time. It's been enchanted as much as possible."

class Gauntlets(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Gauntlets")
        self.equipment_type = "Gloves"
        self.description = "Iron gauntlets that protect your hands. It's hard to enchant for some reason"
        self.name = "Gauntlets"
        self.armor = 4

    def equip(self, entity):
        if entity.gloves != None:
            entity.unequip(entity.gloves)
        entity.gloves = self
        self.activate(entity)

    def unequip(self, entity):
        entity.gloves = None
        self.deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 1
        if self.level == 2:
            self.description += " It's been slightly enchanted to be more protective."
        if self.level == 6:
            self.description = "Iron gauntlets that feel stronger than adamantium. It's been enchanted as much as possible."

class BoxingGloves(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Boxing Gloves")
        self.equipment_type = "Gloves"
        self.description = "Gloves that make your unarmed combat stronger."
        self.name = "Boxing Gloves"
        self.armor = 0
        self.damage_boost = 30 # yeah this needs to be high to compete with basic weapons

    def equip(self, entity):
        if entity.gloves != None:
            entity.unequip(entity.gloves)
        entity.gloves = self
        entity.unarmed_damage_min += self.damage_boost
        entity.unarmed_damage_max += self.damage_boost
        self.activate(entity)

    def unequip(self, entity):
        entity.gloves = None
        entity.unarmed_damage_min -= self.damage_boost
        entity.unarmed_damage_max -= self.damage_boost
        self.deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 1
        self.damage_boost += 4
        if self.wearer != None:
            self.wearer.unarmed_damage_min += 4
            self.wearer.unarmed_damage_max += 4
        if self.level == 2:
            self.description += " It's been enchanted to make your fists stronger"
        if self.level == 6:
            self.description = "Gloves that let you punch through anything. It's been enchanted as much as possible."

class Helmet(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Helmet")
        self.equipment_type = "Helmet"
        self.name = "Helmet"
        self.armor = 1
        self.description = "A helmet that protects your head. You like how round it is."


    def equip(self, entity):
        if entity.helmet != None:
            entity.unequip(entity.helmet)
        entity.helmet = self
        self.activate(entity)

    def unequip(self, entity):
        entity.helmet = None
        self.deactivate(entity)

    def level_up(self):
        self.level += 1
        self.armor += 1
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A round helmet that protects your head from nearly anything. It's been enchanted as much as possible."


class VikingHelmet(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Viking Helmet")
        self.equipment_type = "Helmet"
        self.name = "Viking Helmet"
        self.armor = 0
        self.description = "A helmet that lets you go berserk below a quarter health."
        
        self.skill_cooldown = 0
        self.skill_cost = 10
        self.skill_duration = 10
        self.skill_threshold = 0.25
        self.strength_increase = 10

        self.rarity = "Rare"

        self.attached_skill_exists = True

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Berserk(owner, self.skill_cooldown, self.skill_cost, self.skill_duration, self.skill_threshold, self.strength_increase, action_cost=1)

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

    def level_up(self):
        self.level += 1
        if self.description == 2:
            self.description += " It's been enchanted to raise the damage you need to take before going berserk"
        if self.level == 6:
            self.description = "A helmet that lets you go berserk below half health. It's been enchanted as much as possible"
        self.strength_increase += 2
        self.skill_threshold += 0.1
        if self.skill_threshold > 0.5:
            self.skill_threshold = 0.5
        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

class Potion(O.Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Potiorb"
        self.consumeable = True
        self.stackable = True
        self.stacks = 1
        self.equipable = False
        self.can_be_levelled = False
        self.attached_skill_exists = False
        self.description = "A potiorb that does something."
        self.rarity = "Common"
        self.yendorb = False

    def activate_once(self, entity):
        pass

    def activate(self, entity):
        self.activate_once(entity)
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True

class Scroll(O.Item):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Scrorb"
        self.consumeable = True
        self.stackable = True
        self.equipable = False
        self.can_be_levelled = False
        self.stacks = 1
        self.attached_skill_exists = False
        self.description = "A scrorb that does something."
        self.yendorb = False

        self.rarity = "Common"

    def activate_once(self, entity, loop):
        pass

    def activate(self, entity, loop):
        self.activate_once(entity, loop)
        entity.ready_scroll = self

    def consume_scroll(self, entity):
        self.stacks -= 1
        if self.stacks == 0:
            self.destroy = True
            entity.inventory.remove(self)
        

class TeleportScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Teleport Scrorb")
        self.description = "Let's go for a ride."
        self.rarity = "Common"
        self.skill = S.Teleport(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity.parent
        self.skill.activate(entity, loop.generator, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class MassTormentScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mass Torment Scrorb")
        self.description = "Must kill everything."
        self.rarity = "Common"
        self.skill = S.MassTorment(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class InvincibilityScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Invincibility Scrorb")
        self.description = "Death cannot hold me back."
        self.rarity = "Common"
        self.skill = S.Invinciblity(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class CallingScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "The Scrorb of Calling")
        self.description = "Read at your own peril."
        self.rarity = "Common"
        self.skill = S.Awaken_Monsters(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class SleepScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Sleeping Scrorb")
        self.description = "A guide to monster lullabies."
        self.rarity = "Common"
        self.skill = S.Monster_Lullaby(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class ExperienceScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Experience Scrorb")
        self.description = "Orb you glad you picked this up."
        self.rarity = "Common"
        self.experience = 50

    def activate_once(self, entity, loop):
        entity.parent.experience += 50
        entity.parent.check_for_levelup()
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class HealthPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Health Potiorb")
        self.description = "A potiorb that heals you."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.gain_health(20)

class MightPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Might Potiorb")
        self.description = "A potiorb that makes you stronger for a few turns."
        self.rarity = "Rare"

    def activate_once(self, entity):
        effect = E.Might(5, 5)
        entity.add_status_effect(effect)

class DexterityPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Dexterity Potiorb")
        self.description = "A potiorb that makes you more dexterous for a few turns."
        self.rarity = "Rare"

    def activate_once(self, entity):
        effect = E.Haste(5, 5)
        entity.add_status_effect(effect)

class PermanentDexterityPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Permanent Dex Potiorb")
        self.description = "Speed in a bottle"
        self.rarity = "Rare"

    def activate_once(self, entity):
        entity.dexterity += 1

class PermanentStrengthPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Permanent Str Potiorb")
        self.description = "Strength in a bottle"
        self.rarity = "Rare"

    def activate_once(self, entity):
        entity.strength += 1

class CurePotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Cure Potiorb")
        self.description = "A potiorb that cures you of all status effects."
        self.rarity = "Rare"

    def activate_once(self, entity):
        for effect in entity.status_effects:
            effect.remove(entity)
        entity.status_effects = []

class ManaPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mana Potiorb")
        self.description = "A potiorb that restores your mana."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.gain_mana(20)

class EnchantScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Enchant Scrorb")
        self.description = "A scrorb that enchants an item."
        self.rarity = "Common"

    def activate_once(self, entity, loop):
        loop.limit_inventory = "Enchantable"
        loop.change_loop(L.LoopType.enchant)
        print("read enchant")

class BurningAttackScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Flame Scrorb")
        self.description = "A scrorb that lets you cast burning attack once."
        self.rarity = "Common"

    def activate_once(self, entity, loop):
        entity.ready_skill = S.BurningAttack(entity.parent, 0, 0, 10, 5, 5, 5)
        loop.start_targetting()
        loop.targets.store_skill(0, entity.ready_skill, entity.parent, temp_cast=True)

class BlinkScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Blink Scrorb")
        self.description = "A scrorb that lets you cast blink once."
        self.rarity = "Common"

    def activate_once(self, entity, loop):
        entity.ready_skill = S.BlinkToEmpty(entity.parent, 0, 0, 10, 1)
        loop.start_targetting(start_on_player=True)
        loop.targets.store_skill(0, entity.ready_skill, entity.parent, temp_cast=True)

class MassHealScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mass Heal Scrorb")
        self.description = "A scrorb that lets you cast mass heal once."
        self.rarity = "Common"
        self.skill = S.MassHeal(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class OrbOfYendorb(O.Item):
    def __init__(self):
        super().__init__(-1, -1, 0, 161, "Orb of Yendorb")
        self.equipable = False
        self.description = "Its the all-powerful orb of yendorb. The magic animating it has deactivated"
        self.stackable = False
        self.level = 1
        self.can_be_levelled = False
        self.equipped = False
        self.wearer = None
        self.rarity = "Common"
        self.required_strength = 0
        self.attached_skill_exists = False
        self.yendorb = True