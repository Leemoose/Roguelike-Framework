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
ItemSpawns.append(ItemSpawnParams( I.EnchantScrorb(450),     1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.BurningAttackScrorb(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.TeleportScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.MassTormentScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.InvincibilityScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.CallingScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.SleepScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.ExperienceScroll(450),      1,               10,          5,              5))
ItemSpawns.append(ItemSpawnParams( I.BlinkScrorb(450),      1,               10,          1,              5))

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

        # useful for debugging specific items, separate from generator
        self.forceSpawn = None
        # self.forceSpawn = ("Enchant Scrorb", 3)
        # self.forceSpawn = ("Blink Scrorb", 5)
        
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
        if depth > 10:
            depth = 10
        items = []
        commonAtDepth = [i for i in self.commonItems if i.AllowedAtDepth(depth)]
        if depth == 1:
            commonWeapons = [i for i in commonAtDepth if i.item.equipment_type == "Weapon"]
            items.append(random.choice(commonWeapons).GetFreshCopy())

        if self.forceSpawn:
            for _ in range(self.forceSpawn[1]):
                item_spawn = [i for i in self.ItemSpawns if i.item.name == self.forceSpawn[0]][0]
                item = item_spawn.GetFreshCopy()
                items.append(item)
        
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

        # level = depth + random.randint(-self.levelVariance, self.levelVariance)

        for _ in range(depth):
            copied.character.level_up()

        return copied
    
MonsterSpawns = []


MonsterSpawns.append(MonsterSpawnParams(M.Goblin(-1, -1), 1, 3, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Gorblin(-1, -1), 2, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Hobgoblin(-1, -1), 1, 3, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Hobgorblin(-1, -1), 2, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Kobold(-1, -1), 1, 3, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Korbold(-1, -1), 2, 5, 0, 0))

MonsterSpawns.append(MonsterSpawnParams(M.Gargoyle(-1, -1), 4, 6, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Gorbgoyle(-1, -1), 6, 8, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Minotaur(-1, -1), 4, 6, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Minotaurb(-1, -1), 6, 8, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Orc(-1, -1), 4, 6, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Orbc(-1, -1), 6, 8, 0, 0))

MonsterSpawns.append(MonsterSpawnParams(M.Raptor(-1, -1), 7, 9, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Raptorb(-1, -1), 8, 9, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Tormentorb(-1, -1), 8, 9, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Golem(-1, -1), 7, 9, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Gorblem(-1, -1), 8, 9, 0, 0))

Monster_Distributions = [(1.0, 0.0), # floor 1
                         (0.8, 0.2), # floor 2
                         (0.2, 0.8), # floor 3
                         (0.7, 0.3), # floor 4
                         (0.5, 0.5), # floor 5
                         (0.2, 0.8), # floor 6
                         (0.7, 0.3), # floor 7
                         (0.3, 0.7), # floor 8
                         (0.0, 1.0), # floor 9
                         (0.0, 1.0)] # floor 10

class MonsterSpawner():
    def __init__(self, MonsterSpawns):
        self.MonsterSpawns = MonsterSpawns
        self.normalMonsters = [i for i in self.MonsterSpawns if i.monster.orb == False]
        self.orbMonsters = [i for i in self.MonsterSpawns if i.monster.orb == True]

        # useful for debugging specific items, separate from generator
        self.forceSpawn = None
        # self.forceSpawn = ("Hobgorblin", 5) 

    def countSpawn(self, depth):
        return random.randint(int(2 + 0.5 * (depth)), int(4 + 1.0 * (depth)))
    
    def random_level(self, depth):
        if depth < 4:
            return random.randint(0, 3)
        elif depth < 7:
            return random.randint(3, 6)
        else:
            return random.randint(6, 9)
    
    def spawnMonsters(self, depth):
        if depth > 9:
            depth = 9
        monsters = []
        normalAtDepth = [i for i in self.normalMonsters if i.AllowedAtDepth(depth)]
        orbAtDepth = [i for i in self.orbMonsters if i.AllowedAtDepth(depth)]
        if orbAtDepth == []:
            orbAtDepth = normalAtDepth

        if self.forceSpawn:
            for _ in range(self.forceSpawn[1]):
                monster_spawn = [i for i in self.MonsterSpawns if i.monster.name == self.forceSpawn[0]][0]
                monster = monster_spawn.GetLeveledCopy(self.random_level(depth))
                monsters.append(monster)
        
        for i in range(self.countSpawn(depth)):
            rarity = random.random()
            if rarity < Monster_Distributions[depth-1][0]:
                monster_spawn = random.choice(normalAtDepth)
                monster = monster_spawn.GetLeveledCopy(self.random_level(depth))
                monsters.append(monster)
            else:
                monster_spawn = random.choice(orbAtDepth)
                monster = monster_spawn.GetLeveledCopy(self.random_level(depth))
                monsters.append(monster)
        return monsters
    
monster_spawner = MonsterSpawner(MonsterSpawns)