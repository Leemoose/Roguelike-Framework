class Mage():
    def __init__(self, parent):
        self.parent = parent
        self.known_spells = []
        self.quick_cast_spells = []

    def add_spell(self, spell):
        self.known_spells.append(spell)
        if len(self.quick_cast_spells) < 8: # cap quick cast skills at 8, for ease of skill bar
            self.quick_cast_spells.append(spell)

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