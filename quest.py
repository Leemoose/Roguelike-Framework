import items as I
import monster as M

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

    def check_for_progress(self, loop):
        pass

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

class KingdomQuest(Quest):
    def __init__(self, experience_given = 10, name = "Kingdom Quest"):
        super().__init__(experience_given = experience_given, name = name)
        self.descriptions[1] = "The king has asked you to push back the darkness, and push back the darkness you will."
        self.descriptions[2] = "You find killing in the kings name an easy thing to do..."
        self.descriptions[3] = "Monsters fall like wheat being reaped by the farmer. Like leaves falling from the tree. You revel in the blood..."

    def check_for_completion(self, loop):
        if self.active:
            return False

    def check_for_progress(self, loop):
        if self.active:
            level_up = False
            if loop.player.statistics.total_monsters_killed() > 10 and self.level < 2:
                self.level += 1
                level_up = True
            elif loop.player.statistics.total_monsters_killed() > 30 and self.level < 3:
                self.level += 1
                level_up = True

            if level_up:
                for i in range(self.level):
                    self.give_reward(loop.player)


class BrothersQuest(Quest):
    def __init__(self, experience_given=20, name="Missing Brother"):
        super().__init__(experience_given=experience_given, name=name)
        self.descriptions[1] = "Someone's brother is missing in the deep depths of the pit. Find them"
        self.descriptions[2] = "You sense that the brother is close by."
        self.descriptions[3] = "The brother is dead. Bring back a relic to provide closure to their relative"

    def check_for_completion(self, loop):
        if self.active:
            player = loop.player
            for item in player.character.inventory:
                if isinstance(item, I.BobCorpse):
                    self.level += 1
                    self.give_reward(loop)
                    return True
        return False

    def check_for_progress(self, loop):
        if self.active:
            if self.level < 2 and loop.generator.depth >= 5:
                self.level += 1
            elif self.level < 3:
                for item in loop.generator.item_map.all_entities():
                    if isinstance(item, I.BobCorpse) and loop.generator.tile_map.locate(item.x, item.y).is_seen():
                        self.level += 1
                        break

    def give_reward(self, loop):
        item = I.RingOfMight()
        if loop.player.character.get_item(loop, item):
            self.active = False

class DojoQuest(Quest):
    def __init__(self, experience_given=20, name="Dojo Quest"):
        super().__init__(experience_given=experience_given, name=name)
        self.descriptions[1] = "Destroy the training dummy to prove your might to this weird guy calling himself your teacher."
    
    def check_for_completion(self, loop):
        if self.active:
            for monster in loop.generator.monster_map.all_entities():           
                if isinstance(monster, M.Dummy):
                    return False
            print("Quest Complete")
            return True
        return False 
    
    def give_reward(self, loop):
        item = I.PermanentStrengthPotion(401)
        if loop.player.character.get_item(loop, item):
            self.active = False
