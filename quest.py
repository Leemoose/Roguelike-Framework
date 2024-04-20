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

