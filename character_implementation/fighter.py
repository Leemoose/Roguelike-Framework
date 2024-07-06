import random

class Fighter():
    def __init__(self, parent, min_damage = 2, max_damage = 3):
        self.parent = parent
        self.min_unarmed = 3
        self.max_unarmed = 6
        self.on_hit = None

        self.base_damage = 0
        self.armor = 0

        self.unarmed_damage_min = min_damage
        self.unarmed_damage_max = max_damage

    def get_armor(self):
        return self.armor

    def get_base_damage(self):
        return self.base_damage

    def get_attribute(self, attribute):
        if attribute == "armor":
            return self.get_armor()

    def change_attribute(self, attribute, change):
        if attribute == "armor":
            self.armor += change

    def do_defend(self):
        defense = self.armor + (self.parent.character.get_attribute("Endurance") // 3)
        return defense

    """
    1. Damage: Calculate how much damage opponent you would deal
    2. Chance to hit: dexterity vs dexterity affected by how heavy the armor is for both sides (% shave off damage?)
    2. On hit effects
    3. Armor: Armor flat damage decrease vs armor piercing 
    4. Take damage

    Armor piercing <=> Armor
    Magic penetration <=> MR
    Mental power <=> Will power
    Attribute (either suceptible or resistent)
    Accuracy <=> Dodge
    True damage
    On hit modifiers
    
    """

    def do_attack(self, defender, loop):
        #self.energy -= self.action_costs["attack"] move to player

        damage, effect = self.get_damage()

        dodge_damage = defender.fighter.get_dodge_chance() - self.get_accuracy()
        damage_shave = 1 - ((min(dodge_damage, 0) // 10) / 10)

        if effect is not None and damage_shave == 0:
            effect = effect(self.parent)  # some effects need an inflictor
            defender.character.add_status_effect(effect)

        defense = defender.fighter.do_defend() - self.get_armor_piercing()

        effectiveness = 0
        weapon = self.parent.body.get_weapon()
        if weapon is not None:
            for types in weapon.effective:
                if types in defender.attributes:
                    if defender.attributes[types] == True:
                        effectiveness += 1
                        loop.add_message(
                            "The attack is effective against {} as it is a {} type.".format(defender.name, types))

        finalDamage = max(0, int((damage + self.base_damage) * damage_shave * (max(1, 1.5 * effectiveness)) - defense))
        defender.character.take_damage(self.parent, finalDamage)
        return finalDamage

    def get_accuracy(self):
        strike_chance = random.randint(1,100) + self.parent.character.get_attribute("Dexterity") * 2
        return min(100, strike_chance)

    def get_damage_min(self):
        return self.get_damage()[0]

    def get_damage_max(self):
        return self.get_damage()[1]

    def get_dodge_chance(self):
        dodge_chance = random.randint(1, 100) + self.parent.character.get_attribute("Dexterity") * 2
        return (min(100, dodge_chance))

    def get_damage(self):
        effect = None
        weapon = self.parent.body.get_weapon()

        if weapon is None:
            damage = random.randint(self.base_damage + self.unarmed_damage_min,
                                    self.base_damage + self.unarmed_damage_max)  # Should make object for unarmed damage
        else:
            if weapon.on_hit == None:
                damage = weapon.attack()
            else:
                damage, effect = weapon.attack()

        return damage, effect


    def get_armor_piercing(self):
        weapon = self.parent.body.get_weapon()
        if weapon is None:
            ap = 0
        else:
            ap = weapon.get_armor_piercing()
        return ap


