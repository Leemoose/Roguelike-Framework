import dice as R

class StatusEffect():
    def __init__(self, id_tag, name, message, duration):
        self.id_tag = id_tag
        self.name = name
        self.duration = duration
        self.active = True
        self.message = message
        self.positive = False

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

class Burn(StatusEffect):
    def __init__(self, duration, damage, inflictor):
        super().__init__(801, "Burn", "is Burning", duration)
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

class Petrify(StatusEffect):
    def __init__(self, duration):
        super().__init__(802, "Petrify", "is Petrified", duration)

    def apply_effect(self, target):
        target.movable = False
    
    def remove(self, target):
        target.movable = True

class Might(StatusEffect):
    def __init__(self, duration, strength):
        super().__init__(803, "Might", "feels strong", duration)
        self.strength = strength
        self.positive = True

    def apply_effect(self, target):
        target.base_damage += self.strength

    def remove(self, target):
        target.base_damage -= self.strength

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
    def __init__(self, duration, dexterity):
        super().__init__(805, "Slow", "feels slow", duration)
        self.dexterity = dexterity

    def apply_effect(self, target):
        target.dexterity -= self.dexterity
    
    def remove(self, target):
        target.dexterity += self.dexterity