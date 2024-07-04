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
    def __init__(self, experience_given = 10, number = 5, name = "Goblin Quest"):
        super().__init__(experience_given = experience_given, name = name)
        self.number_goblins = number
        self.descriptions[1] = "Kill those pesky goblins and show the evidence to the Archmage in order to be rewarded!"

    def check_for_completion(self, loop):
        if self.active:
            player = loop.player
            count = 0
            for item in player.get_inventory():
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
        self.descriptions[1] = "The king has asked you to push back the darkness and though he is an idiot, push back the darkness you will."
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
        self.descriptions[1] = "The desperate guard has asked you to find his brother, who was lost in a rift. Search the area for any signs of his brother."
        self.descriptions[2] = "You found a piece of the guard’s brother’s armor near the entrance of the rift. Continue deeper into the rift and follow any further signs to locate his brother."
        self.descriptions[3] = "You have discovered the body of the guard's brother. Carefully bring his remains back to the desperate guard at the palace."

    def check_for_completion(self, loop):
        if self.active:
            player = loop.player
            for item in player.get_inventory():
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
            self.give_reward(loop)
            return True
        return False 
    
    def give_reward(self, loop):
        loop.player.stat_points += 2
        self.active = False
