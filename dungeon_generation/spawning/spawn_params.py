import copy
import random

class ItemSpawnParams:
    def __init__(self, item, minFloor=1, maxFloor=10, branch=None):
        self.item = item
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.branch = branch

    def AllowedAtDepth(self, depth, branch=None):
        return (depth >= self.minFloor and depth <= self.maxFloor and branch == self.branch)

    def GetFreshCopy(self):
        return copy.deepcopy(self.item)
    
class MonsterSpawnParams:
    def __init__(self, monster, minFloor, maxFloor, branch, rarity, group = None):
        self.monster = monster
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.rarity = rarity
        self.branch = branch
        self.group = group

    def AllowedAtDepth(self, depth, branch=None):
        return (depth >= self.minFloor and depth <= self.maxFloor and self.branch == branch)

    def GetLeveledCopy(self, depth):
        copied = copy.deepcopy(self.monster)

        # level = depth + random.randint(-self.levelVariance, self.levelVariance)

        for _ in range(depth):
            if (depth % 2 == 1):
                copied.character.level_up(1,0,1,0)
                copied.character.health = copied.character.max_health
                copied.character.mana = copied.character.max_mana
            else:
                copied.character.level_up(0,1,0,1)
                copied.character.health = copied.character.max_health
                copied.character.mana = copied.character.max_mana
                

        return copied