import items as I
import monster as M
import copy
import random

class ItemSpawnParams:
    def __init__(self, item, minFloor, maxFloor, minNumber, maxNumber):
        self.item = item
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.minNumber = minNumber
        self.maxNumber = maxNumber

    def AllowedAtDepth(self, depth):
        return (depth >= self.minFloor and depth <= self.maxFloor)
    
    def GetNumberToSpawn(self):
        return random.randint(self.minNumber, self.maxNumber)

    def GetFreshCopy(self):
        return copy.deepcopy(self.item)
    
#Spawn lists!
ItemSpawns = []                                                         # minFloor    maxFloor(incl)  minAmount   maxAmount(incl)

ItemSpawns.append(ItemSpawnParams( I.Ax(300),                 1,               5,          0,              3))
ItemSpawns.append(ItemSpawnParams( I.Hammer(301),             1,               5,          0,              3))
ItemSpawns.append(ItemSpawnParams( I.Shield(311),             1,               5,          1,              3))
ItemSpawns.append(ItemSpawnParams( I.Chestarmor(600),              1,               5,          1,              3))
ItemSpawns.append(ItemSpawnParams( I.Boots(700),              1,               5,          0,              3))
ItemSpawns.append(ItemSpawnParams( I.Helmet(770),              1,               5,          1,              3))
ItemSpawns.append(ItemSpawnParams( I.Gloves(750),              1,               5,          1,              3))
ItemSpawns.append(ItemSpawnParams( I.HealthPotion(401),       1,               10,          0,              5))
ItemSpawns.append(ItemSpawnParams( I.Dagger(321),             1,               10,          0,              5))
ItemSpawns.append(ItemSpawnParams( I.RingOfSwiftness(500),               1,               10,          0,              5))
ItemSpawns.append(ItemSpawnParams( I.FlamingSword(331),       1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.MagicWand(332),          1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.VikingHelmet(771),       1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.BootsOfEscape(701),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.BloodRing(501),          1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.RingOfMana(502),          1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.RingOfMight(503),          1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.BoneRing(504),          1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.ManaPotion(402),         1,               10,          0,              5))
ItemSpawns.append(ItemSpawnParams( I.CurePotion(403),         1,               10,          0,              3))
ItemSpawns.append(ItemSpawnParams( I.MightPotion(404),        1,               10,          0,              2))
ItemSpawns.append(ItemSpawnParams( I.DexterityPotion(405),    1,               10,          0,              2))
ItemSpawns.append(ItemSpawnParams( I.EnchantScrorb(450),     1,               10,          5,              5))

class MonsterSpawnParams:
    def __init__(self, monster, minFloor, maxFloor, minNumber, maxNumber, levelVariance = 0):
        self.monster = monster
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.minNumber = minNumber
        self.maxNumber = maxNumber
        self.levelVariance = levelVariance

    def AllowedAtDepth(self, depth):
        return (depth >= self.minFloor and depth <= self.maxFloor)
    
    def GetNumberToSpawn(self):
        return random.randint(self.minNumber, self.maxNumber)

    def GetLeveledCopy(self, depth):
        copied = copy.deepcopy(self.monster)

        level = depth + random.randint(-self.levelVariance, self.levelVariance)

        for i in range(level):
            copied.character.level_up()

        return copied
    
MonsterSpawns = []


MonsterSpawns.append(MonsterSpawnParams(M.Gargoyle(-1, -1), 1, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Kobold(-1, -1), 1, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Raptor(-1, -1), 1, 5, 1, 1))
MonsterSpawns.append(MonsterSpawnParams(M.Minotaur(-1, -1), 1, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Orc(-1, -1), 1, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Goblin(-1, -1), 1, 5, 1, 1))