import items as I

class Quest():
    def __init__(self, experience_given = 10, name = "Quest"):
        self.level = 1
        self.experience_given = experience_given
        self.descriptions = {}
        self.active = True
        self.name = name

    def get_description(self):
        if self.level in self.descriptions:
            return self.descriptions[self.level]
        else:
            return "This quest has been completed."

    def check_for_completion(self, player):
        return self.level > len(self.descriptions)

    def give_reward(self, player):
        player.gain_experience(self.experience_given)

    def increase_level(self, loop):
        self.level += 1

class GoblinQuest(Quest):
    def __init__(self, experience_given = 10, number = 3, name = "Goblin Quest"):
        super().__init__(experience_given = experience_given, name = name)
        self.number_goblins = number
        self.descriptions[1] = "Kill those pesky goblins and show the evidence to the questgiver in order to be rewarded!"

    def check_for_completion(self, loop):
        if self.active:
            player = loop.player
            count = 0
            for item in player.character.inventory:
                if isinstance(item, I.Corpse) and item.monster_type == "Goblin":
                    count += 1
            if count >= self.number_goblins:
                self.level += 1
                self.give_reward(loop)
                return True
            else:
                return False

    def give_reward(self, loop):
        item = I.PermanentDexterityPotion(405, dexterity=3)
        if loop.player.character.get_item(loop, item):
            self.active = False

class TempleQuest(Quest):
    def __init__(self, experience_given = 10, number = 3, name = "Temple Quest"):
        super().__init__(experience_given = experience_given, name = name)
        self.number_goblins = number
        self.descriptions[1] = "The book mentions tore pages scattered throughout the dungeon. Perhaps if you found them, you could understand more."
        self.descriptions[2] = "The fragment seems to be covered in dried blood, but from what you can make out, it seems to be a ritual for power."
        self.descriptions[3] = "Yep, definitely a ritual for power. Looks to require a sacrifice. Perhaps it may make sense to stop this quest..."
        self.descriptions[4] = "Find an unsuspecting npc and murder them. True power will flow through your veins!"

    def check_for_completion(self, loop):
        if self.active:
            pass

    def increase_level(self, loop):
        super().increase_level(loop)
        if self.level == 4:
            loop.can_attack_npcs = True

    def give_reward(self, loop):
        items = []
        items.append(I.PermanentDexterityPotion(405, dexterity=5))
        items.append(I.PermanentStrengthPotion(405, strength=5))
        items.append(I.PermanentEndurancePotion(405, endurance=5))
        items.append(I.PermanentIntelligencePotion(405, intelligence=5))
        for item in items:
            if loop.player.character.get_item(loop, item):
                pass
            else:
                pass
                #drop item on their space

