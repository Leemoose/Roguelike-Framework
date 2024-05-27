class Mage():
    def __init__(self, parent):
        self.parent = parent
        self.known_spells = []

    def add_spell(self, spell):
        self.known_spells.append(spell)

    def cast_spell(self, skill_num, target, loop):
        spell = self.known_spells[skill_num]
        self.parent.character.energy -= spell.action_cost
        return spell.try_to_activate(target, loop)

    def tick_cooldowns(self):
        for skill in self.parent.mage.known_spells:
            skill.tick_cooldown()