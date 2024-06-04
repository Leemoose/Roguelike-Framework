class Mage():
    def __init__(self, parent):
        self.parent = parent
        self.known_spells = []
        self.quick_cast_spells = [None] * 7

    def add_spell(self, spell):
        self.known_spells.append(spell)
        for i in range(7): # cap quick cast skills at 7, for ease of skill bar
            if self.quick_cast_spells[i] == None:
                self.quick_cast_spells[i] = spell
                break

    def cast_spell(self, skill_num, target, loop, quick_cast=False):
        if quick_cast:
            spell = self.quick_cast_spells[skill_num]
        else:
            spell = self.known_spells[skill_num]
        self.parent.character.energy -= spell.action_cost
        return spell.try_to_activate(target, loop)

    def tick_cooldowns(self):
        for skill in self.parent.mage.known_spells:
            skill.tick_cooldown()

    def set_quick_cast(self, spell, slot):
        if spell in self.quick_cast_spells: # swap with existing slot if already in quickcast
            old_idx = self.quick_cast_spells.index(spell)
            self.quick_cast_spells[old_idx] = self.quick_cast_spells[slot]
        self.quick_cast_spells[slot] = spell
        