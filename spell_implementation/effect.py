class StatusEffect():
    def __init__(self, id_tag, name, message, duration, cumulative = False):
        self.id_tag = id_tag
        self.name = name
        self.duration = duration
        self.active = True
        self.message = message
        self.positive = False
        self.traits = {"status_effect": True}
        self.cumulative = cumulative

    def get_duration(self):
        return self.duration

    def is_cumulative(self):
        return self.cumulative
    def apply_effect(self, target):
        pass

    def description(self):
        if self.duration == -100:
            return self.name + " (permanent)"
        return self.name + " (" + str(self.duration) + ")"

    def tick(self, target):
        if self.duration == -100: # -100 is a special value that means the effect lasts forever, -1 probably works too but made it larger just in case
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False

    def has_trait(self, trait):
        if trait in self.traits:
            return self.traits[trait]
        else:
            return False

    def remove(self, target):
        pass

    def change_duration(self, change):
        self.duration += change


class Burn(StatusEffect):
    def __init__(self, duration, damage, inflictor):
        super().__init__(801, "Burn", "is burning for " + str(damage) + "damage", duration)
        self.damage = damage
        self.inflictor = inflictor

    def apply_effect(self, target):
        pass

    def tick(self, target):
        if self.duration == -100: # -100 is a special value that means the effect lasts forever, -1 probably works too but made it larger just in case
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.inflictor, self.damage)

    def remove(self, target):
        pass

class Petrify(StatusEffect):
    def __init__(self, duration):
        super().__init__(802, "Petrify", "is Petrified", duration)

    def apply_effect(self, target):
        target.can_take_actions = False
    
    def remove(self, target):
        target.can_take_actions = True

class Might(StatusEffect):
    def __init__(self, duration, strength):
        super().__init__(803, "Might", "feels strong", duration)
        self.strength = strength
        self.positive = True

    def apply_effect(self, target):
        target.strength += self.strength

    def remove(self, target):
        target.strength -= self.strength

class Weak(StatusEffect):
    def __init__(self, duration, strength):
        super().__init__(803, "Weak", "feels weak", duration)
        self.strength = strength
        self.positive = False

    def apply_effect(self, target):
        target.strength -= self.strength

    def remove(self, target):
        target.strength += self.strength

class Dumb(StatusEffect):
    def __init__(self, duration, intelligence):
        super().__init__(803, "Dumb", "feels dumb", duration)
        self.intelligence = intelligence
        self.positive = False

    def apply_effect(self, target):
        target.intelligence -= self.intelligence

    def remove(self, target):
        target.intelligence += self.intelligence

class Haste(StatusEffect):
    def __init__(self, duration, dexterity):
        super().__init__(804, "Dexterity", "feels fast", duration)
        self.dexterity = dexterity
        self.positive = True

    def apply_effect(self, target):
        target.dexterity += self.dexterity
    
    def remove(self, target):
        target.dexterity -= self.dexterity

class Slow(StatusEffect):
    def __init__(self, inflictor, duration = 5, dexterity = 5, cumulative = False):
        super().__init__(805, "Slow", "feels slow", duration, cumulative = cumulative)
        self.dexterity = dexterity

    def apply_effect(self, target):
        target.dexterity -= self.dexterity
    
    def remove(self, target):
        target.dexterity += self.dexterity

class Escaping(StatusEffect):
    def __init__(self, duration, dex_buff, str_debuff, int_debuff):
        super().__init__(806, "Escaping", "is trying to escape", duration)
        self.dex_buff = dex_buff
        self.str_debuff = str_debuff
        self.int_debuff = int_debuff
    
    def apply_effect(self, target):
        target.dexterity += self.dex_buff
        target.strength -= self.str_debuff
        target.intelligence -= self.int_debuff
    
    def remove(self, target):
        target.dexterity -= self.dex_buff
        target.strength += self.str_debuff
        target.intelligence += self.int_debuff

class Fear(StatusEffect):
    def __init__(self, duration, inflictor):
        super().__init__(806, "Fear", "is scared", duration)
        self.inflictor = inflictor
        self.old_values = ()
    
    def apply_effect(self, target):
        print("When trying to apply fear effect, {} is the target".format(target))
        if target.parent.has_trait("monster"):
            self.old_values = target.parent.brain.get_tendency("flee")
            target.parent.brain.change_tendency("flee", (1000,0))
            target.parent.flee = True
            print("The {} is inflicted with fear".format(target))
    
    def remove(self, target):
        if target.parent.has_trait("monster"):
            target.parent.brain.change_tendency("flee", self.old_values)
            target.parent.flee = False


class Charm(StatusEffect):
    def __init__(self, duration, inflictor):
        super().__init__(806, "Charmed", "is charmed", duration)
        self.inflictor = inflictor
        self.old_brain = None

    def apply_effect(self, target):
        if target.parent.has_trait("monster"):
            self.old_brain = target.parent.brain
            target.parent.make_friendly()

    def remove(self, target):
        if target.parent.has_trait("monster"):
            target.parent.brain = self.old_brain

class Invincible(StatusEffect):
    def __init__(self, duration, inflictor = None):
        super().__init__(806, "Invincible", "can't be killed", duration)
        self.positive = True

    def apply_effect(self, target):
        target.invincible = True

    def remove(self, target):
        target.invincible = False
        target.health = max(1, target.health)

class Asleep(StatusEffect):
    def __init__(self, duration, inflictor = None):
        super().__init__(806, "Asleep", "...", duration)
        self.traits["asleep"] = True

    def apply_effect(self, target):
        actual = target.parent
        actual.asleep = True

    def remove(self, target):
        actual = target.parent
        actual.asleep = False
class Tormented(StatusEffect):
    def __init__(self, duration, inflictor = None):
        super().__init__(806, "Tormented", "is tormented", duration)
    def apply_effect(self, target):
        target.health //= 2

    def remove(self, target):
        pass

class ArmorShredding(StatusEffect):
    def __init__(self, duration, inflictor = None):
        super().__init__(806, "Shredded", "armor is shredded", duration)
        self.armor_shredded = 0
    def apply_effect(self, target):
        target.armor -= 5
        self.armor_shredded += 5

    def remove(self, target):
        target.armor += self.armor_shredded
        self.armor_shredded = 0

class ArmorBuff(StatusEffect):
    def __init__(self, duration, inflictor = None):
        super().__init__(806, "Fortified", "armor is buffed", duration)
        self.armor_buffed = 0
    def apply_effect(self, target):
        target.armor += 5
        self.armor_buffed += 5

    def remove(self, target):
        target.armor -= self.armor_buffed
        self.armor_buffed = 0

class Bleed(StatusEffect):
    def __init__(self, duration, damage, inflictor):
        super().__init__(801, "Bleed", "is Bleeding", duration)
        self.damage = damage
        self.inflictor = inflictor

    def apply_effect(self, target):
        pass

    def tick(self, target):
        if self.duration == -100: # -100 is a special value that means the effect lasts forever, -1 probably works too but made it larger just in case
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.inflictor, self.damage)
            self.duration -= 1

    def remove(self, target):
        pass

class Poison(StatusEffect):
    def __init__(self, inflictor, duration = 2, damage = 3):
        super().__init__(801, "Poison", "is being poisoned for " + str(damage) + "damage", duration)
        self.damage = damage
        self.inflictor = inflictor
        self.cumulative = True

    def tick(self, target):
        if self.duration == -100: # -100 is a special value that means the effect lasts forever, -1 probably works too but made it larger just in case
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False
        else:
            target.take_damage(self.inflictor, self.damage)

class Rooted(StatusEffect):
    def __init__(self, inflictor, duration = 5):
        super().__init__(801, "Root", "is rooted for ", duration)
        self.inflictor = inflictor

    def apply_effect(self, target):
        target.can_move = False

    def tick(self, target):
        if self.duration == -100: # -100 is a special value that means the effect lasts forever, -1 probably works too but made it larger just in case
            return
        self.duration -= 1
        if self.duration <= 0:
            self.active = False

    def remove(self, target):
        target.moveable = True