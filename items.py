import random

import objects as O
import effect as E
import skills as S
import loops as L
import spell

class statUpgrades():
    def __init__(self, base_str=0, max_str=0, base_dex=0, max_dex = 0, base_int = 0, max_int = 0, base_end = 0, max_end = 0, base_arm=0, max_arm=0):
        self.base_str = base_str
        self.max_str = max_str
        self.base_dex = base_dex
        self.max_dex = max_dex
        self.base_int = base_int
        self.max_int = max_int
        self.base_end = base_end
        self.max_end = max_end
        self.base_arm = base_arm
        self.max_arm = max_arm

    def intLerp(self, a, b, level):
        return (((b-a) * (level-1)) // 5) + a
    
    def GetStatsForLevel(self, level):
        return (self.intLerp(self.base_str, self.max_str, level),
                      self.intLerp(self.base_dex, self.max_dex, level),
                      self.intLerp(self.base_int, self.max_int, level),
                      self.intLerp(self.base_end, self.max_end, level),
                      self.intLerp(self.base_arm, self.max_arm, level))
    
    
    def GetStatsForLevelUp(self, level):
        prev_level = self.GetStatsForLevel(level-1)
        
        this_level = self.GetStatsForLevel(level)
        
        return tuple(map(lambda i, j: i - j, this_level, prev_level))


# not equippable or consumable
class Corpse(O.Item):
    def __init__(self, x, y, id_tag = -1, render_tag = 199, name = "Unknown Corpse"):
        super().__init__(x,y, id_tag = id_tag, render_tag = render_tag, name = name)
        self.monster_type = None

class BobCorpse(Corpse):
    def __init__(self, x, y, id_tag = -1, render_tag = 199, name = "Bob's Corpse"):
        super().__init__(x = x,y = y, id_tag = id_tag, render_tag =render_tag, name = name)
        self.monster_type = "Human"

class Gold(O.Item):
    def __init__(self, amount, x=-1, y=-1, id_tag = -1, render_tag = 210, name = "Gold"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.amount = amount

class DestroyedDummy(O.Item):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 125, name = "Destroyed Dummy"):
        super().__init__(x,y, id_tag, render_tag, name)

"""
All detailed items are initialized here.
"""
class Equipment(O.Item):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.equipable = True
        self.equipped = False
        self.wearer = None
        self.cursed = False
        self.rarity = "Common"
        self.required_strength = 0
        self.stats = statUpgrades()
        self.traits["equipment"] = True

    def activate(self, entity):
        self.wearer = entity
        self.add_stats(entity)

    def deactivate(self, entity):
        self.wearer = None
        self.remove_stats(entity)

    def enchant(self):
        self.level += 1
        if (self.wearer):
            self.update_stats_level_up(self.wearer)

    def add_stats(self, entity):
        (str, dex, intl, end, arm) = self.stats.GetStatsForLevel(self.level)
        entity.strength += str
        entity.dexterity += dex
        entity.intelligence += intl
        entity.endurance += end
        entity.armor += arm

    #Called after level up has completed to get stats to match!
    def update_stats_level_up(self, entity):
        (str, dex, intl, end, arm) = self.stats.GetStatsForLevelUp(self.level)
        entity.strength += str
        entity.dexterity += dex
        entity.intelligence += intl
        entity.endurance += end
        entity.armor += arm

    def remove_stats(self, entity):
        (str, dex, intl, end, arm) = self.stats.GetStatsForLevel(self.level)
        entity.strength -= str
        entity.dexterity -= dex
        entity.intelligence -= intl
        entity.endurance -= end
        entity.armor -= arm

    def can_be_equipped(self, entity):
        return self.equipable and entity.strength >= self.required_strength

    def can_be_unequipped(self, entity):
        return (self.equipped and not self.cursed)

    def get_attached_skill_description(self):
        if self.attached_skill_exists:
            return self.attached_skill(None).description() # temporarily attach skill to nothing to get name
        else:
            return None

"""
WEAPONS
"""

class Weapon(Equipment):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = -1, name = "Unknown weapon", damage_min = 0, damage_max=0, armor_piercing = 0, attack_cost = 80):
        super().__init__(x=x,y=y, id_tag = id_tag, render_tag=render_tag, name = name)
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.armor_piercing = armor_piercing
        self.equipment_type = "Weapon"
        self.slots_taken = 1
        self.on_hit = None
        self.effective = []
        self.attack_cost = attack_cost
        self.diff_action_cost = 0
        self.traits["weapon"] = True

    def can_be_equipped(self, entity):
        return super().can_be_equipped(entity) and entity.free_equipment_slots("hand_slot") >= self.slots_taken

    def equip(self, entity):
        if entity.strength >= self.required_strength and entity.free_equipment_slots("hand_slot") >= self.slots_taken:
            if entity.equipment_slots["hand_slot"][0] != None:
                entity.unequip(entity.equipment_slots["hand_slot"][0])
            entity.add_item_to_equipment_slot(self, "hand_slot", self.slots_taken)
            if self.attached_skill_exists:
                entity.add_skill(self.attached_skill(entity.parent))
            self.activate(entity)

    def unequip(self, entity):
        entity.remove_item_from_equipment_slot(self, "hand_slot", self.slots_taken)
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)
        self.deactivate(entity)

    def attack(self):
        damage = random.randint(self.damage_min, self.damage_max)
        return damage

class Ax(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Axe")
        self.melee = True
        self.name = "Axe"
        self.description = "An axe with a round edge (could be rounder). A solid weapon for a solid warrior."
        self.damage_min = 4
        self.damage_max = 7
        self.effective.append("wood")
    
    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more effective."
        if self.level == 6:
            self.description = "An axe with the roundest edge ever seen. It's been enchanted as much as possible."
        self.damage_min += 1
        self.damage_max += 3


class SlicingAx(Ax):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.melee = True
        self.name = "Slicing Ax"
        self.description = "Like cutting paper "
        self.can_be_levelled = True

        self.on_hit = (lambda inflictor: E.Bleed(3, 4, inflictor))
        self.on_hit_description = f"The target starts to bleed."

        self.wearer = None  # items with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Rare"

    def attack(self):
        return (super().attack(), self.on_hit)

class Hammer(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Hammer")
        self.melee = True
        self.name = "Hammer"
        self.description = "A hammer that you wish was more spherical. High damage potential but hard to get a solid hit in."
        self.damage_min = 2
        self.damage_max = 4
        self.effective.append("stone")

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to hit harder"
        if self.level == 6:
            self.description = "A hammer with incredible damage potential. Still not the easiest to get a clean hit in. It's been enchanted as much as possible."
        self.damage_min += 3
        self.damage_max += 3

""""
DAGGERS
+ Specialize in fast attack speed (works well with on hit effects and attack move combinations).
- Low damage (does poorly against armor)
- No armor piercing
"""
class Dagger(Weapon):
    def __init__(self, render_tag = 321, attack_cost = 20):
        super().__init__(-1, -1, 0, render_tag, "Dagger", attack_cost)
        self.melee = True
        self.name = "Dagger"
        self.description = "I swear that tip is getting rounder... Larry!. Enchanting it might make it more pointy and precise."
        self.damage_min = 1
        self.damage_max = 3


    def activate(self, entity):
        self.wearer = entity
        self.diff_action_cost = max(entity.action_costs["attack"] - self.attack_cost, (entity.action_costs["attack"]) / 2)
        entity.change_action_cost("attack", entity.action_costs["attack"] - self.diff_action_cost)

    def deactivate(self, entity):
        self.wearer = None
        entity.change_action_cost("attack", entity.action_costs["attack"] + self.diff_action_cost)
        self.diff_action_cost = 0

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more precise."
        if self.level == 6:
            self.description = "A dagger that always strikes accurately, never dealing less than full damage. It's been enchanted as much as possible."
        self.damage_min += 0
        self.damage_max += 5
        if self.damage_min > self.damage_max:
            self.damage_min = self.damage_max

class ScreamingDagger(Dagger):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.melee = True
        self.name = "Screaming Dagger"
        self.description = "The sound of thousands dead souls. "
        self.damage_min = 1
        self.damage_max = 1
        self.can_be_levelled = False

        self.on_hit = (lambda inflictor: E.Tormented(5))
        self.on_hit_description = f"Torments the target for half health damage over."

        self.wearer = None  # items with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Legendary"

    def attack(self):
        return (super().attack(), self.on_hit)

"""
SWORDS
 + Specialness lies with armor piercing
 * Average damage
 * Average attack speed
"""
class Sword(Weapon):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 340, name = "Sword", damage_min = 4, damage_max=12, armor_piercing = 4, attack_cost = 80):
        super().__init__(x=x, y=y, id_tag = id_tag, render_tag =render_tag, name = name, damage_min = damage_min, damage_max=damage_max, armor_piercing = armor_piercing, attack_cost = attack_cost)
        self.melee = True
        self.description = "Could be rounder honestly."

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more damaging."
        if self.level == 6:
            self.description = "A sword that has been enchanted as much as possible."
        self.damage_min += 1
        self.damage_max += 2

class BroadSword(Sword):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 340, name = "Broadsword", damage_min = 4, damage_max=12, armor_piercing = 6, attack_cost = 80):
        super().__init__(x=x, y=y, id_tag = id_tag, render_tag =render_tag, name = name, damage_min = damage_min, damage_max=damage_max, armor_piercing = armor_piercing, attack_cost = attack_cost)
        self.required = 1
class LongSword(Sword):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 340, name = "Longsword", damage_min = 4, damage_max=12, armor_piercing = 8, attack_cost = 80):
        super().__init__(x=x, y=y, id_tag = id_tag, render_tag =render_tag, name = name, damage_min = damage_min, damage_max=damage_max, armor_piercing = armor_piercing, attack_cost = attack_cost)
        self.required_strength = 3

class Claymore(Sword):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 340, name = "Claymore", damage_min = 8, damage_max=20, armor_piercing = 8, attack_cost = 80):
        super().__init__(x=x, y=y, id_tag = id_tag, render_tag =render_tag, name = name, damage_min = damage_min, damage_max=damage_max, armor_piercing = armor_piercing, attack_cost = attack_cost)
        self.required_strength = 5

class TwoHandedSword(Sword):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 340, name = "Two Handed Sword", damage_min = 4, damage_max=12, armor_piercing = 10, attack_cost = 80):
        super().__init__(x=x, y=y, id_tag = id_tag, render_tag =render_tag, name = name, damage_min = damage_min, damage_max=damage_max, armor_piercing = armor_piercing, attack_cost = attack_cost)
        self.slots_taken = 2
        self.required_strength = 5

class GreatSword(TwoHandedSword):
    def __init__(self, x=-1, y=-1, id_tag = -1, render_tag = 340, name = "Greatsword", damage_min = 8, damage_max=20, armor_piercing = 15, attack_cost = 80):
        super().__init__(x=x, y=y, id_tag = id_tag, render_tag =render_tag, name = name, damage_min = damage_min, damage_max=damage_max, armor_piercing = armor_piercing, attack_cost = attack_cost)
        self.required_strength = 8

################################################
class SleepingSword(Sword):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.melee = True
        self.name = "Sleeping Sword"
        self.description = "...on the treetops. When the wind blows"
        self.can_be_levelled = False

        self.on_hit = (lambda inflictor: E.Asleep(8))
        self.change_to_hit = 25
        self.on_hit_description = f"The target is sleeping."

        self.wearer = None  # items with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Legendary"

    def attack(self):
        hit = random.randint(1,100)
        if hit < self.change_to_hit:
            return (super().attack(), self.on_hit)
        else:
            return (super().attack(), None)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " the cradle will rock."
        if self.level == 6:
            self.description = "Death is the greatest sleep of all."
            self.damage_min = 1
            self.damage_max = 100
        self.damage_min += 2
        self.damage_max += 3
        if self.damage_min > self.damage_max:
            self.damage_min = self.damage_max


class FlamingSword(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Flaming Sword")
        self.melee = True
        self.name = "Flaming Sword"
        self.description = "A sword that is on fire. You can channel its fire to cast a Burning Attack at a distant foe. "
        self.damage_min = 5
        self.damage_max = 8

        self.on_hit_burn = 4
        self.on_hit_burn_duration = 3
        self.on_hit = (lambda inflictor: E.Burn(self.on_hit_burn, self.on_hit_burn_duration, inflictor))
        self.on_hit_description = f"Burns the target for {self.on_hit_burn} damage over {self.on_hit_burn_duration} turns."

        self.skill_cooldown = 8
        self.skill_cost = 20
        self.skill_damage = 3
        self.skill_burn_damage = 4
        self.skill_burn_duration = 3
        self.skill_range = 4
        self.attached_skill_exists = True

        self.wearer = None  # items with stat buffs or skills need to keep track of owner for level ups
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
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to hit harder and burn stronger."
        if self.level == 6:
            self.description = "A sword that burns intensely. It's burning strike has reached its maximum potency. It's been enchanted as much as possible."
        self.damage_min += 2
        self.damage_max += 3

        self.skill_damage += 2
        self.skill_cooldown -= 1
        if self.skill_cooldown < 5:
            self.skill_cooldown = 5

        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))


"""
HAMMERS
+ Specializes in high damage
+ Solid armor piercing
- High required strength
- Low attack speed
"""
class CrushingHammer(Hammer):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.melee = True
        self.name = "Crushing Hammer"
        self.description = "Player smash. "
        self.can_be_levelled = True

        self.on_hit = (lambda inflictor: E.ArmorShredding(5))
        self.on_hit_description = f"Shreds the targets armor."

        self.wearer = None  # items with stat buffs or skills need to keep track of owner for level ups
        self.rarity = "Rare"

    def attack(self):
        return (super().attack(), self.on_hit)

class MagicWand(Weapon):
    def __init__(self, render_tag):
        super().__init__(-1, -1, 0, render_tag, "Magic Wand")
        self.melee = True
        self.name = "Magic Wand"
        self.description = "A wand that you can use to cast magic missile. You can also use it in melee but why would you?"
        self.damage_min = 1
        self.damage_max = 5
        self.magic_missile_damage = 6
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
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted cast a stronger magic missile"
        if self.level == 6:
            self.description = "A wand that you can use to cast an immensely powerful magic missile. It's been enchanted as much as possible."

        # level up improves magic missile
        self.magic_missile_damage += 2
        self.magic_missile_range += 1
        self.magic_missile_cooldown -= 1
        if self.magic_missile_cooldown < 0:
            self.magic_missile_cooldown = 0
        
        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

        

"""
ARMORS
SHIELDS
"""

class Armor(Equipment):
    def __init__(self, x,y, id_tag, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, "Armor")
        self.name = "Armor"

    def can_be_equipped(self, entity):
        return (entity.strength) >= self.required_strength and self.equipable

class Shield(Armor):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Shield"
        self.name = name
        self.shield = True
        self.offhand = True
        self.description = "A shield that you can use to block things."

    def equip(self, entity):
        if entity.strength >= self.required_strength:
            if entity.equipment_slots["hand_slot"][1] != None:
                entity.unequip(entity.equipment_slots["hand_slot"][1])
            entity.equipment_slots["hand_slot"][1] = self
            self.activate(entity)
            if self.attached_skill_exists:
                entity.add_skill(self.attached_skill(entity.parent))

    def unequip(self, entity):
        entity.equipment_slots["hand_slot"][1] = None
        self.deactivate(entity)
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)
        

class BasicShield(Shield):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Shield")
        self.armor = 3
        self.description = "A shield that you can use to block things."
        self.stats = statUpgrades(base_end=1, max_end=3, base_arm=1, max_arm=6)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A shield that you can use to block nearly anything. It's been enchanted as much as possible."

class Aegis(Shield):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Aegis")
        self.description = "A shield with the face of a horrifying monster on it. It can turn your enemies to stone"
        self.required_strength = 2

        self.skill_cooldown = 12
        self.skill_cost = 20
        self.skill_duration = 3
        self.skill_activation_chance = 0.3
        self.skill_range = 3

        self.attached_skill_exists = True

        self.rarity = "Legendary"
        self.stats = statUpgrades(base_str=1, max_str=2, base_end=2, max_end=3, base_arm=2, max_arm=7)


    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Petrify(owner, self.skill_cooldown, 
                                self.skill_cost, 
                                self.skill_duration, 
                                self.skill_activation_chance, 
                                self.skill_range)

    def level_up(self):
        self.enchant()

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
        self.description = "A massive shield that can block nearly anything but is unwieldy to use"
        self.required_strength = 3
        self.stats = statUpgrades(base_str=1, max_str=2, base_dex=-2, max_dex=0, base_end=2, max_end=4, base_arm=5, max_arm=10)

    def level_up(self):
        self.enchant()
        # if self.wearer != None:
        #     self.wearer.dexterity += 1
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
        self.stats = statUpgrades(base_int=2, max_int=6)

    def level_up(self):
        self.enchant()

        if self.level == 2:
            self.description += " It's been enchanted to be more effective."
        if self.level == 6:
            self.description = "An orb that takes your offhand but lets you cast the most powerful spells. It's been enchanted as much as possible."

"""
BODY ARMORS
"""

class BodyArmor(Armor):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Body Armor"
        self.name = name
        self.description = "A piece of armor that covers your chest."
        self.stats = statUpgrades(base_str=1, max_str=1, base_end=1, max_end=4, base_arm=1, max_arm=4)

    def equip(self, entity):
        if entity.equipment_slots["body_armor_slot"][0] != None:
            entity.unequip(entity.equipment_slots["body_armor_slot"][0])
        entity.equipment_slots["body_armor_slot"][0] = self
        self.activate(entity)
        if self.attached_skill_exists:
            entity.add_skill(self.attached_skill(entity.parent).name)
    
    def unequip(self, entity):
        entity.equipment_slots["body_armor_slot"][0] = None
        self.deactivate(entity)
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)

class Chestarmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Chest Plate")
        self.description = "A reliable piece of armor that covers your chest."
        self.required_strength = 3
        self.wearer = None
        self.stats = statUpgrades(base_int=-2, max_int=0, base_arm=2, max_arm=8)


    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A chest plate that absorbs most hits for you. It's been enchanted as much as possible."

class LeatherArmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Leather Armor")
        self.description = "A comfortable piece of armor, that helps you feel lighter on your feet. "
        self.wearer = None # items with stat buffs need to keep track of owner for level ups
        self.stats = statUpgrades(base_dex=1, max_dex=4, base_arm=1, max_arm=4)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to make you more nimble."
        if self.level == 6:
            self.description = "Comfortable armor that makes you feel incredibly fast on your feet while offering decent protection. It's been enchanted as much as possible."

class GildedArmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Gilded Armor")
        self.description = "A piece of golden armor studded with gems. Just wearing it makes you feel like you can ignore trivial things like status effects."
        self.required_strength = 1
        
        self.skill_cooldown = 5
        self.skill_cost = 15
        self.activation_chance = 0.5

        self.attached_skill_exists = True
        
        self.rarity = "Rare"

        self.stats = statUpgrades(base_str = 1, max_str = 3,
                                  base_dex = 1, max_dex = 1,
                                  base_int = 1, max_int = 3,
                                  base_end = 1, max_end = 1,
                                  base_arm = 1, max_arm = 3)

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.ShrugOff(owner, self.skill_cooldown, self.skill_cost, self.activation_chance, action_cost=100)

    def level_up(self):
        self.enchant()

        self.skill_cooldown -= 1
        if self.skill_cooldown < 3:
            self.skill_cooldown = 3
        self.skill_cost -= 2
        if self.skill_cost < 8:
            self.skill_cost = 8
        self.activation_chance += 0.1
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
        self.description = "Frightening armor that belonged to a famous warrior. Wearing it makes you stronger and your enemies more terrified."
        self.armor = 3
        self.required_strength = 1
        self.strength_buff = 2

        self.wearer = None # items with stat buffs need to keep track of owner for level ups

        self.skill_cooldown = 12
        self.skill_cost = 10
        self.skill_duration = 3
        self.skill_activation_chance = 0.5
        self.skill_range = 2

        self.attached_skill_exists = True
        
        self.rarity = "Legendary"

        self.stats = statUpgrades(base_str = 2, max_str = 5,
                                  base_dex = -3, max_dex = -1,
                                  base_end = 1, max_end = 4,
                                  base_arm = 2, max_arm = 5)

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Terrify(owner, self.skill_cooldown, 
                                self.skill_cost, 
                                self.skill_duration, 
                                self.skill_activation_chance, 
                                self.skill_range)


    def activate(self, entity):
        self.wearer = entity
        return super().activate(entity)

    def deactivate(self, entity):
        self.wearer = None
        return super().deactivate(entity)

    def level_up(self):
        self.enchant()

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
            self.description = "Frightening armor that marks you as a famous warrior who fought in many battles. Your enemies are terrified even from a distance. It's been enchanted as much as possible."

class BloodstainedArmor(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Bloodstained Armor")
        self.description = "A maligment aura surronds this armor."
        self.required_strength = 3
        self.cursed = True
        self.wearer = None  # items with stat buffs need to keep track of owner for level ups
        self.rarity = "Legendary"
        self.stats = statUpgrades(base_str = 2, max_str = 6,
                                  base_dex = -2, max_dex = 0,
                                  base_end = 1, max_end = 4,
                                  base_arm = 2, max_arm = 5)

    def activate(self, entity):
        self.wearer = entity
        return super().activate(entity)

    def deactivate(self, entity):
        self.wearer = None
        return super().deactivate(entity)

    def level_up(self):
        self.enchant()
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
        self.mana_regen_buff = 3
        self.intelligence_buff = 5

        self.wearer = None # items with stat buffs need to keep track of owner for level ups

        self.rarity = "Rare"
        self.stats = statUpgrades(base_str = -2, max_str = 0,
                                  base_int = 2, max_int = 5)

    def activate(self, entity):
        entity.max_mana += self.mana_buff
        entity.mana_regen += self.mana_regen_buff
        return super().activate(entity)

    def deactivate(self, entity):
        entity.max_mana -= self.mana_buff
        entity.mana_regen -= self.mana_regen_buff
        return super().deactivate(entity)

    def level_up(self):
        self.enchant()
        self.mana_buff += 10
        self.mana_regen_buff += 5

        if self.wearer != None:
            self.wearer.max_mana += 10
            self.wearer.mana_regen += 5

        if self.level == 2:
            self.description += " It's been enchanted to make you more magical"
        if self.level == 6:
            self.description = "A robe that makes you feel like you can cast spells for all eternity. It's been enchanted as much as possible."

class KarateGi(BodyArmor):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Karate Gi")
        self.description = "A gi that makes your unarmed combat stronger."
        self.damage_boost_min = 2
        self.damage_boost_max = 4

        self.wearer = None # items with stat buffs need to keep track of owner for level ups

        self.rarity = "Rare"

        self.stats = statUpgrades(base_str = 1, max_str = 1,
                                  base_dex = 3, max_dex = 6,
                                  base_int = 0, max_int = 0,
                                  base_end = 2, max_end = 6,
                                  base_arm = 1, max_arm = 3)

    def activate(self, entity):
        entity.unarmed_damage_min += self.damage_boost_min
        entity.unarmed_damage_max += self.damage_boost_max
        return super().activate(entity)

    def deactivate(self, entity):
        entity.unarmed_damage_min -= self.damage_boost_min
        entity.unarmed_damage_max -= self.damage_boost_max
        return super().deactivate(entity)

    def level_up(self):
        self.enchant()
        self.damage_boost_min += 1
        self.damage_boost_max += 1
        if self.wearer != None:
            self.wearer.unarmed_damage_min += 1
            self.wearer.unarmed_damage_max += 1
        if self.level == 2:
            self.description += " It's been enchanted to make your fists stronger"
        if self.level == 6:
            self.description = "A gi that lets you punch through anything. It's been enchanted as much as possible."

"""
BOOTS
"""

class Boots(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Boots")
        self.equipment_type = "Boots"
        self.name = "Boots"
        self.description = "Boots that are incredibly comfortable but only offer a little protection"
        self.stats = statUpgrades(base_dex=1, max_dex=2, base_arm=1, max_arm=4)


    def equip(self, entity):
        if entity.equipment_slots["boots_slot"][0] != None:
            entity.unequip(entity.equipment_slots["boots_slot"][0])
        entity.equipment_slots["boots_slot"][0] = self
        self.activate(entity)
        if self.attached_skill_exists:
            entity.add_skill(self.attached_skill(entity.parent))

    def unequip(self, entity):
        entity.equipment_slots["boots_slot"][0] = None
        self.deactivate(entity)
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)
            # print("Remove boot skill")

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "Boots that are somehow incredibly comfy and tough at the same time. It's been enchanted as much as possible."

class BlackenedBoots(Boots):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.equipment_type = "Boots"
        self.name = "Blackened Boots"
        self.cursed = True
        self.description = "A dark spirit dwells in these boots."
        self.rarity = "Legendary"
        self.stats = statUpgrades(base_str = -2, max_str = 1,
                                  base_dex = 4, max_dex = 7,
                                  base_int = -2, max_int = 1,
                                  base_end = -2, max_end = 0,
                                  base_arm = 1, max_arm = 4)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " You see the quickest path in a sea of blood."
        if self.level == 6:
            self.description = "You ride on screaming winds."

class BootsOfEscape(Boots):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.equipment_type = "Boots"
        self.name = "Boots of Escape"
        self.armor = 0
        self.description = "Boots that let you cast the skill flee"

        self.skill_cooldown = 40
        self.skill_cost = 25
        self.dex_buff = 10
        self.str_debuff = 5
        self.int_debuff = 5
        self.duration = 4
        self.rarity = "Rare"

        self.attached_skill_exists = True
        self.stats = statUpgrades(base_dex = 3, max_dex = 8,
                                  base_arm = 1, max_arm = 3)
    
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

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to let you flee on a shorter cooldown."
        if self.level == 6:
            self.description = "Boots that let you flee at the drop of a hat. It's been enchanted as much as possible."
        self.skill_cooldown -= 5
        if self.skill_cooldown < 5:
            self.skill_cooldown = 5
        self.skill_cost -= 2
        if self.skill_cost < 10:
            self.skill_cost = 10
        self.duration += 1
        if self.duration > 6:
            self.duration = 6
        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

class AssassinBoots(Boots):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.equipment_type = "Boots"
        self.name = "Assassin Boots"
        self.description = "Boots to help you move in the shadows."
        self.rarity = "Rare"
        self.stats = statUpgrades(base_dex = 2, max_dex = 5,
                                  base_str = -2, max_str = 0,
                                  base_int = 1, max_int = 3,
                                  base_end = -2, max_end = 0,
                                  base_arm = 1, max_arm = 3)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to make you feel more nimble."
        if self.level == 6:
            self.description = "Boots to help you move in the shadows. It's been enchanted as much as possible."

"""
GLOVES
"""

class Gloves(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Gloves")
        self.equipment_type = "Gloves"
        self.description = "Gloves to keep your hands toasty warm. Enchanting is especially effective on these."
        self.name = "Gloves"
        self.armor = 1
        self.stats = statUpgrades(base_end = 1, max_end = 8,
                                  base_arm = 0, max_arm = 10)

    def equip(self, entity):
        if entity.equipment_slots["gloves_slot"][0] != None:
            entity.unequip(entity.equipment_slots["gloves_slot"][0])
        entity.equipment_slots["gloves_slot"][0] = self
        self.activate(entity)
        if self.attached_skill_exists:
            entity.add_skill(self.attached_skill(entity.parent))

    def unequip(self, entity):
        entity.equipment_slots["body_armor_slot"][0] = None
        self.deactivate(entity)
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "Gloves that are incredibly warm and tough at the same time. It's been enchanted as much as possible."

class Gauntlets(Gloves):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.equipment_type = "Gloves"
        self.description = "Iron gauntlets that protect your hands. It's hard to enchant for some reason"
        self.name = "Gauntlets"
        self.stats = statUpgrades(base_dex = -1, max_dex = 0,
                                  base_end = 4, max_end = 10,
                                  base_arm = 4, max_arm = 6)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been slightly enchanted to be more protective."
        if self.level == 6:
            self.description = "Iron gauntlets that feel stronger than adamantium. It's been enchanted as much as possible."

class BoxingGloves(Gloves):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.equipment_type = "Gloves"
        self.description = "Gloves that make your unarmed combat stronger."
        self.name = "Boxing Gloves"
        self.damage_boost_min = 1
        self.damage_boost_max = 3
        self.stats = statUpgrades(base_str = 1, max_str = 5,
                                  base_dex = 1, max_dex = 5,
                                  base_arm = 0, max_arm = 2)

    def activate(self, entity):
        entity.unarmed_damage_min += self.damage_boost_min
        entity.unarmed_damage_max += self.damage_boost_max


    def deactivate(self, entity):
        entity.unarmed_damage_min -= self.damage_boost_min
        entity.unarmed_damage_max -= self.damage_boost_max

    def level_up(self):
        self.enchant()
        self.damage_boost_min += 1
        self.damage_boost_max += 3
        if self.wearer != None:
            self.wearer.unarmed_damage_min += 1
            self.wearer.unarmed_damage_max += 3
        if self.level == 2:
            self.description += " It's been enchanted to make your fists stronger"
        if self.level == 6:
            self.description = "Gloves that let you punch through anything. It's been enchanted as much as possible."

class HealingGloves(Gloves):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.equipment_type = "Gloves"
        self.description = "Gloves that let you heal yourself."
        self.name = "Healing Gloves"
        self.armor = 0

        # self, parent, cooldown, cost, heal_amount, activation_threshold, action_cost):
        self.skill_cooldown = 15
        self.skill_cost = 25
        self.heal_amount = 35
        self.activation_threshold = 1.1
        self.action_cost = 100
        self.rarity = "Rare"

        self.attached_skill_exists = True

        self.stats = statUpgrades(base_int = 1, max_int = 3,
                                  base_end = 1, max_end = 1,
                                  base_arm = 2, max_arm = 5)

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Heal(owner, self.skill_cooldown, 
                        self.skill_cost, 
                        self.heal_amount,
                        self.activation_threshold,
                        self.action_cost)

    def level_up(self):
        self.enchant()
        self.skill_cooldown -= 1
        if self.skill_cooldown < 10:
            self.skill_cooldown = 10
        self.skill_cost -= 5
        if self.skill_cost < 10:
            self.skill_cost = 10
        self.heal_amount += 15
        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))
        if self.level == 2:
            self.description += " It's been enchanted to heal more."
        if self.level == 6:
            self.description = "Gloves that lets life surge through you. It's been enchanted as much as possible."

class LichHand(Gloves):
    def __init__(self, render_tag):
        super().__init__(render_tag)
        self.equipment_type = "Gloves"
        self.description = "Immense power is sworn to whoever if brave enough to sacrifice their hand and some of their max life to the hand. If you dare, it enhances all your stats and allows you to embrace the lich's immortality briefly."
        self.name = "Lich Hand"
        self.armor = 0
        self.cursed = True

        self.skill_cooldown = 20
        self.skill_cost = 30
        self.skill_duration = 4

        self.health_cost = 2 # 1 / health cost is how much is removed


        self.rarity = "Legendary"

        self.attached_skill_exists = True
        self.health_removed = 0

        self.stats = statUpgrades(base_str = 2, max_str = 3,
                                  base_dex = 3, max_dex = 4,
                                  base_int = 3, max_int = 4,
                                  base_end = 1, max_end = 2,
                                  base_arm = 0, max_arm = 2)

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Invinciblity(owner, self.skill_cost, self.skill_cooldown, self.skill_duration, activation_threshold=1.1, by_scroll=False)

    def activate(self, entity):
        self.health_removed = entity.max_health // self.health_cost
        entity.max_health -= self.health_removed
        if entity.health > entity.max_health:
            entity.health = entity.max_health

    def deactivate(self, entity):
        entity.max_health += self.health_removed

    def level_up(self):
        self.enchant()
        self.skill_cooldown -= 2
        if self.skill_cooldown < 10:
            self.skill_cooldown = 10
        self.skill_cost -= 2
        if self.skill_cost < 10:
            self.skill_cost = 10

        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))
        if self.level == 2:
            self.description += " Your power grows."
        if self.level == 6:
            self.description = "A hand that lets you embrace the lich's immortality. It's been enchanted as much as possible."

"""
HELMETS
"""

class Helmet(Armor):
    def __init__(self, render_tag, name = "Helmet"):
        super().__init__(-1,-1, 0, render_tag, name)
        self.equipment_type = "Helmet"
        self.name = "Helmet"
        self.description = "A helmet that protects your head. You like how round it is."
        self.attached_skill_exists = False
        self.attached_skill = None
        self.stats = statUpgrades(base_str = 0, max_str = 2,
                                  base_end = 1, max_end = 1,
                                  base_arm = 1, max_arm = 3)


    def equip(self, entity):
        if entity.equipment_slots["helmet_slot"][0] != None:
            entity.unequip(entity.equipment_slots["helmet_slot"][0])
        entity.equipment_slots["helmet_slot"][0] = self
        self.activate(entity)
        if self.attached_skill_exists:
            entity.add_skill(self.attached_skill(entity.parent))

    def unequip(self, entity):
        entity.equipment_slots["helmet_slot"][0] = None
        self.deactivate(entity)
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A round helmet that protects your head from nearly anything. It's been enchanted as much as possible."


class VikingHelmet(Helmet):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Viking Helmet")
        self.equipment_type = "Helmet"
        self.name = "Viking Helmet"
        self.description = "A helmet that lets you go berserk below a quarter health."
        
        self.skill_cooldown = 0
        self.skill_cost = 0
        self.skill_duration = 10
        self.skill_threshold = 0.25
        self.strength_increase = 5

        self.rarity = "Legendary"
        self.str_buff = 3

        self.attached_skill_exists = True
        self.stats = statUpgrades(base_str = 3, max_str = 6,
                                  base_dex = 1, max_dex = 3,
                                  base_int = -1, max_int = -3,
                                  base_end = -1, max_end = -3,
                                  base_arm = 1, max_arm = 3)

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Berserk(owner, self.skill_cooldown, self.skill_cost, self.skill_duration, self.skill_threshold, self.strength_increase, action_cost=1)

    def level_up(self):
        self.enchant()
        if self.description == 2:
            self.description += " It's been enchanted to lower the damage you need to take before going berserk"
        if self.level == 6:
            self.description = "A helmet that lets you go berserk below three quarters. It's been enchanted as much as possible"
        self.skill_threshold += 0.2
        if self.skill_threshold > 0.75:
            self.skill_threshold = 0.75
        if self.wearer != None:
            self.wearer.remove_skill(self.attached_skill(self.wearer.parent).name)
            self.wearer.add_skill(self.attached_skill(self.wearer.parent))

class SpartanHelmet(Helmet):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Spartan Helmet")
        self.equipment_type = "Helmet"
        self.name = "Spartan Helmet"
        self.description = "A helmet for a mighty warrior who doesn't need things like magic to help him"

        self.required_strength = 2

        self.str_buff = 2
        self.end_buff = 4
        self.int_debuff = 5

        self.rarity = "Rare"
        self.stats = statUpgrades(base_str = 1, max_str = 3,
                                  base_int = -5, max_int = 0,
                                  base_end = 3, max_end = 4,
                                  base_arm = 1, max_arm = 3)
    def level_up(self):
        self.enchant()

        if self.level == 2:
            self.description += " It's been enchanted to make you even tougher"
        if self.level == 6:
            self.description = "A helmet for the greatest of warriors who shuns magic. It's been enchanted as much as possible."

class GreatHelm(Helmet):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Great Helm")
        self.equipment_type = "Helmet"
        self.name = "Great Helm"
        self.armor = 4
        self.required_strength = 3
        self.description = "A helmet that fully covers your face for maximum protection although it restricts your movement a bit."
        self.dex_debuff = 4

        self.rarity = "Rare"

        self.stats = statUpgrades(base_dex = -4, max_dex = 0,
                                  base_arm = 4, max_arm = 8)

    def level_up(self):
        self.enchant()

        if self.level == 2:
            self.description += " It's been enchanted to be less restrictive."
        if self.level == 6:
            self.description = "A helmet that fully covers your face for maximum protection without restricting you at all. It's been enchanted as much as possible."

class ThiefHood(Helmet):
    def __init__(self, render_tag):
        super().__init__( render_tag, "Thief Hood")
        self.equipment_type = "Helmet"
        self.name = "Thief Hood"
        self.description = "A hood that helps you move faster and think more cleverly."

        self.dex_buff = 3
        self.int_buff = 2

        self.rarity = "Rare"

        self.stats = statUpgrades(base_dex = 3, max_dex = 5,
                                  base_int = 1, max_int = 4)


    def level_up(self):
        self.enchant()

        if self.level == 2:
            self.description += " It's been enchanted to be more effective."
        if self.level == 6:
            self.description = "A hood that gives you the physical and mental speed of a master thief. It's been enchanted as much as possible."

class WizardHat(Helmet):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Wizard Hat")
        self.equipment_type = "Helmet"
        self.name = "Wizard Hat"
        self.description = "A hat that makes you feel more magical."
        self.mana_buff = 20

        self.rarity = "Rare"

        self.stats = statUpgrades(base_int = 3, max_int = 6)

    def activate(self, entity):
        entity.max_mana += self.mana_buff

    def deactivate(self, entity):
        entity.max_mana -= self.mana_buff
        if entity.mana >= entity.max_mana:
            entity.mana = entity.max_mana

    def level_up(self):
        self.enchant()
        self.mana_buff += 10

        if self.wearer != None:
            self.wearer.max_mana += self.mana_buff

        if self.level == 2:
            self.description += " It's been enchanted to be more effective."
        if self.level == 6:
            self.description = "A hat that makes you feel like you can cast spells for all eternity. It's been enchanted as much as possible."

"""
PANTS
"""

class Pants(Armor):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Pants")
        self.equipment_type = "Pants"
        self.name = "Pants"
        self.description = "A pair of pants. Why would you ever take them off?"

        self.stats = statUpgrades(base_str = 0, max_str = 2,
                                  base_end = 1, max_end = 1,
                                  base_arm = 1, max_arm = 3)


    def equip(self, entity):
        if entity.equipment_slots["pants_slot"][0] != None:
            entity.unequip(entity.equipment_slots["pants_slot"][0])
        entity.equipment_slots["pants_slot"][0] = self
        self.activate(entity)
        if self.attached_skill_exists:
            entity.add_skill(self.attached_skill(entity.parent))

    def unequip(self, entity):
        entity.equipment_slots["pants_slot"][0] = None
        self.deactivate(entity)
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A round pair of pants that protects your head from nearly anything. It's been enchanted as much as possible."


"""
RINGS
"""

class Ring(Equipment):
    def __init__(self, render_tag, name):
        super().__init__(-1, -1, 0, render_tag, name)
        self.equipment_type = "Ring"
        self.name = name
        self.description = "A ring that does something."
        self.can_be_levelled = False
        self.required_strength = -100
        self.action_description = "Power courses through your hands"
        self.traits["ring"] = True

    def equip(self, entity):
        if self.equipped:
            return
        equipped = False
        for ring, i in enumerate(entity.equipment_slots["ring_slot"]):
            if ring == None:
                entity.equipment_slots["ring_slot"][i] = self
                self.activate(entity)
                if self.attached_skill_exists:
                    entity.add_skill(self.attached_skill(entity.parent))
                self.equipped = True
                break
        if equipped == False:
            entity.unequip(entity.equipment_slots["ring_slot"][0])
            for ring,i in enumerate(entity.equipment_slots["ring_slot"]):
                if ring == None:
                    entity.equipment_slots["ring_slot"][i] = self
                    self.activate(entity)
                    if self.attached_skill_exists:
                        entity.add_skill(self.attached_skill(entity.parent))
                    self.equipped = True

    def unequip(self, entity):
        for i, ring in enumerate(entity.equipment_slots["ring_slot"]):
            if entity.equipment_slots["ring_slot"][ring] == self:
                entity.equipment_slots["ring_slot"][ring] = None
                self.deactivate(entity)
                if self.attached_skill_exists:
                    skill_still_exists = False
                    for ring_2 in entity.equipment_slots["ring_slot"]:
                        if ring_2.name == self.name:
                            skill_still_exists = True
                    if not skill_still_exists:
                        entity.remove_skill(self.attached_skill(entity.parent).name)
                self.equipped = False


class RingOfSwiftness(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Swiftness")
        self.description = "The most circular thing you own, it makes you feel spry on your feet"
        self.rarity = "Rare"
        self.action_description = "You move a fifth faster"

    def activate(self, entity):
        entity.move_cost -= 20

    def deactivate(self, entity):
        entity.move_cost += 20


class BloodRing(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Blood Ring")
        self.description = "Pricking your finger on the spikes of this ring makes you feel alive."
        self.action_description = "Gain the Blood Pact skill."

        # skill doesn't have an owner until equipped to an entity, so need a lambda expression here
        self.rarity = "Rare"
        self.attached_skill_exists = True

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.BloodPact(owner, cooldown=10, cost=25, strength_increase=5, duration=5, action_cost=100)


class RingOfMight(Ring):
    def __init__(self, render_tag = 503):
        super().__init__(render_tag, "Ring of Might")
        self.equipment_type = "Ring"
        self.name = "Ring of Might"
        self.description = "A ring that makes you feel stronger."
        self.action_description = "Gain 4 strength"
        self.rarity = "Rare"

    def activate(self, entity):
        entity.strength += 4

    def deactivate(self, entity):
        entity.strength -= 4


class RingOfMana(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Mana")
        self.description = "A ring that every spellcaster is given on their 10th birthday"
        self.action_description = "Gain 20 mana, 3 intelligence and extra mana regen."
        self.rarity = "Rare"

    def activate(self, entity):
        entity.mana += 20
        entity.max_mana += 20
        entity.mana_regen += 4
        entity.intelligence += 3

    def deactivate(self, entity):
        entity.mana -= 20
        entity.max_mana -= 20
        entity.mana_regen -= 4
        entity.intelligence -= 3


class BoneRing(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Bone Ring")
        self.description = "An eerie ring that makes you much stronger and faster while wearing it but rapidly drains your health and mana"
        self.action_description = "Gain 4 strength and 4 dexterity but lose health and mana over time."
        self.rarity = "Legendary"

    def activate(self, entity):
        self.entity.safe_rest = False
        entity.strength += 4
        entity.dexterity += 4
        entity.mana_regen -= 10
        entity.health_regen -= 10  # intended to kill you if you don't take it off after a few turns

    def deactivate(self, entity):
        self.entity.safe_rest = True
        entity.strength -= 4
        entity.dexterity -= 4
        entity.mana_regen += 10
        entity.health_regen += 10


class RingOfTeleportation(Ring):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Ring of Teleportation")
        self.description = "The most circular thing you own, it makes you feel spry on your feet"
        self.rarity = "Rare"
        self.name = "Ring of Teleportation"
        self.action_description = "Gain the teleport skill."

        self.wearer = None  # items with stat buffs need to keep track of owner for level ups

        self.skill_cooldown = 40
        self.skill_cost = 30

        self.attached_skill_exists = True

        self.rarity = "Legendary"

    def attached_skill(self, owner):
        self.attached_skill_exists = True
        return S.Teleport(owner, self.skill_cooldown, self.skill_cost)

    def activate(self, entity):
        # entity.add_skill(self.attached_skill(entity.parent))
        self.wearer = entity
        return super().activate(entity)

    def deactivate(self, entity):
        #if entity.ring_1 != None and entity.ring_1.name == "Ring of Teleportation":
        #    return  # don't remove skill if other ring was a teleportation ring
        # entity.remove_skill(self.attached_skill(entity.parent).name)
        self.wearer = None
        return super().deactivate(entity)


"""
    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It seems to be growing stronger?"
        if self.level == 6:
            self.skill_cooldown = 0
            self.description = "Unlimited power."
            """

"""
AMULETS
"""

class Amulet(Equipment):
    def __init__(self, render_tag):
        super().__init__(-1,-1, 0, render_tag, "Amulet")
        self.equipment_type = "Amulet"
        self.name = "Amulet"
        self.can_be_levelled = False
        self.description = "A heavy amulet in heavy iron?"

    def equip(self, entity):
        if entity.equipment_slots["amulet_slot"][0] != None:
            entity.unequip(entity.equipment_slots["amulet_slot"][0])
        entity.equipment_slots["amulet_slot"][0] = self
        self.activate(entity)

    def unequip(self, entity):
        entity.equipment_slots["amulet_slot"][0] = None
        self.deactivate(entity)
        if self.attached_skill_exists:
            entity.remove_skill(self.attached_skill(entity.parent).name)




"""
POTIONS
"""

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
        self.action_description = "Something flows through your body"
        self.rarity = "Common"
        self.yendorb = False
        self.traits["potion"] = True

    def can_be_equipped(self, entity):
        return False
    
    def can_be_unequipped(self, entity):
        return False

    def activate_once(self, entity):
        pass

    def activate(self, entity):
        self.activate_once(entity)
        self.stacks -= 1
        if self.stacks <= 0:
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

    def can_be_equipped(self, entity):
        return False
    
    def can_be_unequipped(self, entity):
        return False

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
        self.rarity = "Rare"
        self.skill = S.MassTorment(None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class InvincibilityScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Invincibility Scrorb")
        self.description = "Death cannot hold me back."
        self.rarity = "Legendary"
        self.skill = S.Invinciblity(self, 0, 5, 0)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class CallingScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "The Scrorb of Calling")
        self.description = "Read at your own peril."
        self.rarity = "Rare"
        self.skill = S.Awaken_Monsters(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class SleepScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Sleeping Scrorb")
        self.description = "A guide to monster lullabies."
        self.rarity = "Rare"
        self.skill = S.Monster_Lullaby(None, None, None)

    def activate_once(self, entity, loop):
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class ExperienceScroll(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Experience Scrorb")
        self.description = "Orb you glad you picked this up."
        self.rarity = "Legendary"
        self.experience = 50

    def activate_once(self, entity, loop):
        entity.parent.experience += entity.parent.experience_to_next_level
        entity.parent.check_for_levelup()
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)

class HealthPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Health Potiorb")
        self.description = "A potiorb that heals you."
        self.action_description = "Heal by 20 + 10% max health."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.gain_health(20 + (entity.max_health // 10))

class MightPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Might Potiorb")
        self.description = "A potiorb that makes you stronger for a few turns."
        self.rarity = "Rare"
        self.action_description = "Gain 5 strength temporarily."

    def activate_once(self, entity):
        effect = E.Might(5, 5)
        entity.add_status_effect(effect)

class DexterityPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Dexterity Potiorb")
        self.description = "A potiorb that makes you more dexterous for a few turns."
        self.action_description = "Gain 5 dexterity temporarily."
        self.rarity = "Rare"

    def activate_once(self, entity):
        effect = E.Haste(5, 5)
        entity.add_status_effect(effect)

class PermanentDexterityPotion(Potion):
    def __init__(self, render_tag, dexterity = 1):
        super().__init__(render_tag, "Permanent Dex Potiorb")
        self.description = "Speed in a bottle"
        self.action_description = "Gain 1 dexterity."
        self.rarity = "Rare"
        self.dexterity_addition = dexterity

    def activate_once(self, entity):
        entity.dexterity += self.dexterity_addition

class PermanentStrengthPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Permanent Str Potiorb")
        self.description = "Strength in a bottle"
        self.action_description = "Gain 1 strength."
        self.rarity = "Rare"

    def activate_once(self, entity):
        entity.strength += 1

class CurePotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Cure Potiorb")
        self.description = "A potiorb that cures you of all status effects."
        self.action_description = "Remove all status effects."
        self.rarity = "Rare"

    def activate_once(self, entity):
        for effect in entity.status_effects:
            if not effect.positive:
                effect.remove(entity)
        entity.status_effects = []

class ManaPotion(Potion):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mana Potiorb")
        self.description = "A potiorb that restores your mana."
        self.action_description = "Gain 20 + 10% max mana."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.gain_mana(20 + (entity.max_mana // 10))

class EnchantScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Enchant Scrorb")
        self.description = "A scrorb that enchants an item."
        self.rarity = "Extra Common"

    def activate_once(self, entity, loop):
        loop.limit_inventory = "Enchantable"
        loop.change_loop(L.LoopType.enchant)
        # print("read enchant")

class BurningAttackScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Flame Scrorb")
        self.description = "A scrorb that lets you cast burning attack once."
        self.rarity = "Common"

    def activate_once(self, entity, loop):
        entity.ready_skill = S.BurningAttack(entity.parent, 0, 0, 5, 4, 6, 7)
        loop.start_targetting()
        loop.targets.store_skill(0, entity.ready_skill, entity.parent, temp_cast=True)

class BlinkScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Blink Scrorb")
        self.description = "A scrorb that lets you cast blink once."
        self.rarity = "Rare"

    def activate_once(self, entity, loop):
        entity.ready_skill = S.BlinkToEmpty(entity.parent, 0, 0, 10, 1)
        loop.start_targetting(start_on_player=True)
        loop.targets.store_skill(0, entity.ready_skill, entity.parent, temp_cast=True)

class MassHealScrorb(Scroll):
    def __init__(self, render_tag):
        super().__init__(render_tag, "Mass Heal Scrorb")
        self.description = "A scrorb that lets you cast mass heal once."
        self.rarity = "Rare"
        self.skill = S.MassHeal(None)

    def activate_once(self, entity, loop):
        self.skill.parent = entity
        self.skill.activate(loop, bypass = True)
        self.consume_scroll(entity)
        loop.change_loop(L.LoopType.inventory)


class Book(O.Item):
    def __init__(self, render_tag, skill, name = "Book"):
        super().__init__(-1, -1, 0, render_tag, name = name)
        self.name = "Book"
        self.equipment_type = "Book"
        self.consumeable = True
        self.stackable = False
        self.equipable = False
        self.can_be_levelled = False
        self.stacks = 1
        self.attached_skill_exists = True
        self.description = "A book that does something."
        self.yendorb = False
        self.rarity = "Rare"

        self.skill = skill
        self.attached_skill = None

    def can_be_equipped(self, entity):
        return False

    def can_be_unequipped(self, entity):
        return False

    def mark_owner(self, entity):
        self.attached_skill = self.skill(entity.parent)

    def activate(self, entity, loop):
        if self.attached_skill.can_learn():
            new_skill = self.skill(entity.parent)
            entity.add_skill(new_skill)
            self.destroy = True
            entity.inventory.remove(self)
            loop.change_loop(L.LoopType.inventory)
        else:
            loop.add_message("You do not have enough intelligence to learn this spell.")

    def get_attached_skill_description(self):
        if self.attached_skill_exists:
            return self.attached_skill.description() # temporarily attach skill to nothing to get name
        else:
            return None

class BookofSummoning(Book):
    def __init__(self, render_tag = 480):
        self.school = spell.SummonSchool()
        self.skill = self.school.random_spell()
        super().__init__(render_tag, skill = self.skill, name = "Book of Summoning")
        self.name = "Book of Summoning"

class BookofSpace(Book):
    def __init__(self, render_tag = 480):
        self.school = spell.SpaceSchool()
        self.skill = self.school.random_spell()
        super().__init__(render_tag, skill = self.skill, name = "Book of Space")
        self.name = "Book of Space"

class BookofFire(Book):
    def __init__(self, render_tag = 480):
        self.school = spell.FireSchool()
        self.skill = self.school.random_spell()
        super().__init__(render_tag, skill = self.skill, name = "Book of Fire")
        self.name = "Book of Fire"

class BookofHypnosis(Book):
    def __init__(self, render_tag = 480):
        self.school = spell.HypnosisSchool()
        self.skill = self.school.random_spell()
        super().__init__(render_tag, skill = self.skill, name = "Book of Hypnosis")
        self.name = "Book of Hypnosis"

class OrbOfYendorb(O.Item):
    def __init__(self):
        super().__init__(-1, -1, 0, 161, "Orb of Yendorb")
        self.equipable = False
        self.equipment_type = "Orb of Yendorb"
        self.description = "Its the all-powerful orb of yendorb. The magic animating it has deactivated"
        self.stackable = False
        self.level = 1
        self.can_be_levelled = False
        self.equipped = False
        self.wearer = None
        self.rarity = "YENDORB"
        self.required_strength = 0
        self.attached_skill_exists = False
        self.yendorb = True