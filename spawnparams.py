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

ItemSpawns.append(ItemSpawnParams( I.Ax(300),                 1,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.Hammer(301),             1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.BasicShield(311),             1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.Aegis(312),              3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.TowerShield(313),        2,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.MagicFocus(314),         3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.Chestarmor(600),              1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.LeatherArmor(601),         1,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.GildedArmor(602),         3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.WarlordArmor(603),        3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.WizardRobe(604),          2,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.Boots(700),              1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.Helmet(770),              1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.Gloves(750),              1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.Gauntlets(751),           2,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.HealthPotion(401),       1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.Dagger(321),             1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.RingOfSwiftness(500),               1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.FlamingSword(331),       3,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.MagicWand(332),          2,               8,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.VikingHelmet(771),       2,               8,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.BootsOfEscape(701),      3,               7,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.BloodRing(501),          3,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.RingOfMana(502),          1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.RingOfMight(503),          1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.BoneRing(504),          3,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.ManaPotion(402),         1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.CurePotion(403),         1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.MightPotion(404),        1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.DexterityPotion(405),    1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.EnchantScrorb(450),     1,               10,          5,              5))

Floor_Distributions = [(0.9, 0.1, 0.0), # floor 1
                       (0.7, 0.3, 0.0), # floor 2
                       (0.5, 0.4, 0.1), # floor 3
                       (0.3, 0.6, 0.1), # floor 4
                       (0.3, 0.5, 0.2), # floor 5
                       (0.3, 0.5, 0.2), # floor 6
                       (0.3, 0.4, 0.3), # floor 7
                       (0.3, 0.4, 0.3), # floor 8
                       (0.3, 0.3, 0.4), # floor 9
                       (0.3, 0.3, 0.4)] # floor 10

class ItemSpawner():
    def __init__(self, ItemSpawns):
        self.ItemSpawns = ItemSpawns
        self.commonItems = [i for i in self.ItemSpawns if i.item.rarity == "Common"]
        self.rareItems = [i for i in self.ItemSpawns if i.item.rarity == "Rare"]
        self.legendaryItems = [i for i in self.ItemSpawns if i.item.rarity == "Legendary"]

    def countSpawn(self, depth):
        return random.randint(int(2 + 0.25 * (10 - depth)), int(4 + 0.5 * (10 - depth)))
    
    def random_level(self, depth):
        if depth < 4:
            return 0
        elif depth < 7:
            return random.randint(0, 2)
        else:
            return random.randint(0, 3)
    
    def spawnItems(self, depth):
        items = []
        commonAtDepth = [i for i in self.commonItems if i.AllowedAtDepth(depth)]
        rareAtDepth = [i for i in self.rareItems if i.AllowedAtDepth(depth)]
        if rareAtDepth == []:
            rareAtDepth = commonAtDepth
        legendaryAtDepth = [i for i in self.legendaryItems if i.AllowedAtDepth(depth)]
        if legendaryAtDepth == []: # downgrade if no legendary items available
            if rareAtDepth == []:
                legendaryAtDepth = commonAtDepth
            else:
                legendaryAtDepth = rareAtDepth
        for i in range(self.countSpawn(depth)):
            rarity = random.random()
            if rarity < Floor_Distributions[depth-1][0]:
                item_spawn = random.choice(commonAtDepth)
                item = item_spawn.GetFreshCopy()
                if item.can_be_levelled:
                    for _ in range(self.random_level(depth)):
                        item.level_up()
                items.append(item)
            elif rarity < Floor_Distributions[depth-1][0] + Floor_Distributions[depth-1][1]:
                item_spawn = random.choice(rareAtDepth)
                item = item_spawn.GetFreshCopy()
                if item.can_be_levelled:
                    for _ in range(self.random_level(depth)):
                        item.level_up()
                items.append(item)
            else:
                item_spawn = random.choice(legendaryAtDepth)
                item = item_spawn.GetFreshCopy()
                if item.can_be_levelled:
                    for _ in range(self.random_level(depth)):
                        item.level_up()
                items.append(item)
        return items
    
item_spawner = ItemSpawner(ItemSpawns)

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