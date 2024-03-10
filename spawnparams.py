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
ItemSpawns.append(ItemSpawnParams( I.Dagger(321),             1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.MagicWand(332),          2,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.Sword(340),           1,               5,          1,              5))

ItemSpawns.append(ItemSpawnParams( I.ScreamingDagger(322),           1,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.SleepingSword(341),           3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.FlamingSword(331),       3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.CrushingHammer(302),       2,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.SlicingAx(303),       2,               10,          1,              1))

ItemSpawns.append(ItemSpawnParams( I.BasicShield(311),             1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.Aegis(312),              3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.TowerShield(313),        2,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.MagicFocus(314),         3,               10,          1,              1))

ItemSpawns.append(ItemSpawnParams( I.Chestarmor(600),              1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.LeatherArmor(601),         1,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.GildedArmor(602),         3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.WarlordArmor(603),        3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.WizardRobe(604),          2,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.KarateGi(605),            2,               8,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.BloodstainedArmor(606),        3,               10,          1,              1))

ItemSpawns.append(ItemSpawnParams( I.Boots(700),              1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.BootsOfEscape(701),      3,               7,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.BlackenedBoots(702),              5,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.AssassinBoots(703),              2,               10,          1,              1))

ItemSpawns.append(ItemSpawnParams( I.Helmet(770),              1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.VikingHelmet(771),       2,               8,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.SpartanHelmet(772),       3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.GreatHelm(773),       3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.ThiefHood(774),       3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.WizardHat(775),       3,               10,          1,              1))


ItemSpawns.append(ItemSpawnParams( I.Gloves(750),              1,               5,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.Gauntlets(751),           2,               5,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.BoxingGloves(752),        1,               8,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.HealingGloves(753),       3,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.LichHand(754),            5,               10,          1,              1))

ItemSpawns.append(ItemSpawnParams( I.RingOfSwiftness(500),               1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.RingOfTeleportation(505),              5,               10,          1,              1))
ItemSpawns.append(ItemSpawnParams( I.BloodRing(501),          3,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.RingOfMana(502),          1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.RingOfMight(503),          1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.BoneRing(504),          3,               10,          0,              0))

ItemSpawns.append(ItemSpawnParams( I.HealthPotion(401),       1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.ManaPotion(402),         1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.CurePotion(403),         1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.MightPotion(404),        1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.DexterityPotion(405),    1,               10,          0,              0))
ItemSpawns.append(ItemSpawnParams( I.PermanentStrengthPotion(404),      1,               10,          0,              1))
ItemSpawns.append(ItemSpawnParams( I.PermanentDexterityPotion(405),      1,               10,          0,              1))

ItemSpawns.append(ItemSpawnParams( I.EnchantScrorb(450),     1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.BurningAttackScrorb(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.TeleportScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.MassTormentScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.InvincibilityScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.CallingScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.SleepScroll(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.ExperienceScroll(450),      1,               10,          5,              5))
ItemSpawns.append(ItemSpawnParams( I.BlinkScrorb(450),      1,               10,          1,              5))
ItemSpawns.append(ItemSpawnParams( I.MassHealScrorb(450),      1,               10,          1,              5))


Item_Equipment_Distributions = [(0.9, 0.1, 0.0), # floor 1
                                (0.7, 0.3, 0.0), # floor 2
                                (0.5, 0.4, 0.1), # floor 3
                                (0.3, 0.6, 0.1), # floor 4
                                (0.3, 0.5, 0.2), # floor 5
                                (0.3, 0.5, 0.2), # floor 6
                                (0.3, 0.4, 0.3), # floor 7
                                (0.3, 0.4, 0.3), # floor 8
                                (0.3, 0.3, 0.4), # floor 9
                                (0.3, 0.3, 0.4)] # floor 10

# no legendary potiorbs exist
Item_Potiorb_Distributions = [(0.7, 0.3), # floor 1
                              (0.7, 0.3), # floor 2
                              (0.7, 0.3), # floor 3
                              (0.7, 0.3), # floor 4
                              (0.7, 0.3), # floor 5
                              (0.7, 0.3), # floor 6
                              (0.7, 0.3), # floor 7
                              (0.7, 0.3), # floor 8
                              (0.7, 0.3), # floor 9
                              (0.7, 0.3)] # floor 10

Item_Scrorb_Distributions = [(0.7, 0.3, 0.0), # floor 1
                             (0.7, 0.3, 0.0), # floor 2
                             (0.5, 0.4, 0.1), # floor 3
                             (0.5, 0.4, 0.2), # floor 4
                             (0.4, 0.4, 0.2), # floor 5
                             (0.4, 0.4, 0.2), # floor 6
                             (0.4, 0.4, 0.2), # floor 7
                             (0.4, 0.4, 0.2), # floor 8
                             (0.4, 0.4, 0.2), # floor 9
                             (0.4, 0.4, 0.2)] # floor 10


class ItemSpawner():
    def __init__(self, ItemSpawns):
        self.ItemSpawns = ItemSpawns
        self.commonEquip = [i for i in self.ItemSpawns if i.item.rarity == "Common" and i.item.equipable]
        self.commonPotiorbs = [i for i in self.ItemSpawns if i.item.rarity == "Common" and i.item.equipment_type == "Potiorb"]
        self.commonScrorbs = [i for i in self.ItemSpawns if i.item.rarity == "Common" and i.item.equipment_type == "Scrorb"]   
        self.rareEquip = [i for i in self.ItemSpawns if i.item.rarity == "Rare" and i.item.equipable]
        self.rarePotiorbs = [i for i in self.ItemSpawns if i.item.rarity == "Rare" and i.item.equipment_type == "Potiorb"]
        self.rareScrorbs = [i for i in self.ItemSpawns if i.item.rarity == "Rare" and i.item.equipment_type == "Scrorb"]
        self.legendaryEquip = [i for i in self.ItemSpawns if i.item.rarity == "Legendary" and i.item.equipable]
        self.legendaryScrorbs = [i for i in self.ItemSpawns if i.item.rarity == "Legendary" and i.item.equipment_type == "Scrorb"]
        self.ExtraCommon = [i for i in self.ItemSpawns if i.item.rarity == "Extra Common"]

        # useful for debugging specific items, separate from generator
        self.forceSpawn = []

        # self.forceSpawn.append(("Magic Wand", 3))
        # self.forceSpawn.append(("Invincibility Scrorb", 3))
        # self.forceSpawn.append(("Permanent Dex Potiorb", 3))
        # self.forceSpawn.append(("Health Potiorb", 3))
        # self.forceSpawn.append(("Chest Plate", 3))
        # self.forceSpawn.append(("Ring of Might", 4))
        # self.forceSpawn.append(("Gilded Armor", 3))
        # self.forceSpawn.append(("Leather Armor", 3))
        # self.forceSpawn.append(("Bloodstained Armor", 3))
        # self.forceSpawn.append(("Boxing Gloves", 3))
        # self.forceSpawn.append(("Blackened Boots", 5))
        # self.forceSpawn.append(("Ring of Teleportation", 3))
        # self.forceSpawn.append(("Flaming Sword", 5))
        
    def countEquipment(self, depth):
        return random.randint(int(1 + 0.25 * (depth)), int(2 + 0.5 * (depth)))
    
    def countPotiorbs(self, depth):
        return random.randint(int(1 + 0.25 * (depth)), int(3 + 0.5 * (depth)))
    
    def countExtraCommon(self, depth):
        return random.randint(int(1 + 0.25 * (depth - 1)), int(1 + 0.5 * (depth - 1)))
    
    def countScrorbs(self, depth):
        return random.randint(int(1 + 0.25 * (depth)), int(2 + 0.5 * (depth)))
    
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

        for itemToSpawn in self.forceSpawn:
            for _ in range(itemToSpawn[1]):
                item_spawn = [i for i in self.ItemSpawns if i.item.name == itemToSpawn[0]][0]
                item = item_spawn.GetFreshCopy()
                items.append(item)

        commonEquipAtDepth = [i for i in self.commonEquip if i.AllowedAtDepth(depth)]
        commonPotiorbsAtDepth = [i for i in self.commonPotiorbs if i.AllowedAtDepth(depth)]
        commonScrorbsAtDepth = [i for i in self.commonScrorbs if i.AllowedAtDepth(depth)]
        if depth == 1:
            commonWeapons = [i for i in commonEquipAtDepth if i.item.equipment_type == "Weapon"]
            items.append(random.choice(commonWeapons).GetFreshCopy())
        
        rareEquipAtDepth = [i for i in self.rareEquip if i.AllowedAtDepth(depth)]
        rarePotiorbsAtDepth = [i for i in self.rarePotiorbs if i.AllowedAtDepth(depth)]
        rareScrorbsAtDepth = [i for i in self.rareScrorbs if i.AllowedAtDepth(depth)]
        if rareEquipAtDepth == []:
            rareEquipAtDepth = commonEquipAtDepth
        legendaryEquipAtDepth = [i for i in self.legendaryEquip if i.AllowedAtDepth(depth)]
        legendaryScrorbsAtDepth = [i for i in self.legendaryScrorbs if i.AllowedAtDepth(depth)]
        if legendaryEquipAtDepth == []: # downgrade if no legendary items available
            if rareEquipAtDepth == []:
                legendaryEquipAtDepth = commonEquipAtDepth
            else:
                legendaryEquipAtDepth = rareEquipAtDepth

        for i in range(self.countEquipment(depth)):
            rarity = random.random()
            if rarity < Item_Equipment_Distributions[depth-1][0]:
                item_spawn = random.choice(commonEquipAtDepth)
                item = item_spawn.GetFreshCopy()
                if item.can_be_levelled:
                    for _ in range(self.random_level(depth)):
                        item.level_up()
                items.append(item)
            elif rarity < Item_Equipment_Distributions[depth-1][0] + Item_Equipment_Distributions[depth-1][1]:
                item_spawn = random.choice(rareEquipAtDepth)
                item = item_spawn.GetFreshCopy()
                if item.can_be_levelled:
                    for _ in range(self.random_level(depth)):
                        item.level_up()
                items.append(item)     
            else:
                item_spawn = random.choice(legendaryEquipAtDepth)
                item = item_spawn.GetFreshCopy()
                if item.can_be_levelled:
                    for _ in range(self.random_level(depth)):
                        item.level_up()
                items.append(item)
        for i in range(self.countPotiorbs(depth)):
            rarity = random.random()
            if rarity < Item_Potiorb_Distributions[depth-1][0]:
                item_spawn = random.choice(commonPotiorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
            else:
                item_spawn = random.choice(rarePotiorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
        for i in range(self.countScrorbs(depth)):
            rarity = random.random()
            if rarity < Item_Scrorb_Distributions[depth-1][0]:
                item_spawn = random.choice(commonScrorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
            elif rarity < Item_Scrorb_Distributions[depth-1][0] + Item_Scrorb_Distributions[depth-1][1]:
                item_spawn = random.choice(rareScrorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
            else:
                item_spawn = random.choice(legendaryScrorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
        for i in range(self.countExtraCommon(depth)):
            item_spawn = random.choice(self.ExtraCommon)
            item = item_spawn.GetFreshCopy()
            items.append(item)


        # for i in range(self.countSpawn(depth)):
        #     rarity = random.random()
        #     if rarity < Floor_Distributions[depth-1][0]:
        #         item_spawn = random.choice(commonAtDepth)
        #         item = item_spawn.GetFreshCopy()
        #         if item.can_be_levelled:
        #             for _ in range(self.random_level(depth)):
        #                 item.level_up()
        #         items.append(item)
        #     elif rarity < Floor_Distributions[depth-1][0] + Floor_Distributions[depth-1][1]:
        #         item_spawn = random.choice(rareAtDepth)
        #         item = item_spawn.GetFreshCopy()
        #         if item.can_be_levelled:
        #             for _ in range(self.random_level(depth)):
        #                 item.level_up()
        #         items.append(item)
        #     else:
        #         item_spawn = random.choice(legendaryAtDepth)
        #         item = item_spawn.GetFreshCopy()
        #         if item.can_be_levelled:
        #             for _ in range(self.random_level(depth)):
        #                 item.level_up()
        #         items.append(item)
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
            if (depth % 2 == 1):
                copied.character.level_up(1,0,1,0)
                copied.character.health = copied.character.max_health
                copied.character.mana = copied.character.max_mana
            else:
                copied.character.level_up(0,1,0,1)
                copied.character.health = copied.character.max_health
                copied.character.mana = copied.character.max_mana
                

        return copied
    
MonsterSpawns = []


MonsterSpawns.append(MonsterSpawnParams(M.Goblin(-1, -1), 1, 3, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Gorblin(-1, -1), 2, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Hobgoblin(-1, -1), 1, 3, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Hobgorblin(-1, -1), 2, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Kobold(-1, -1), 1, 3, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.Korbold(-1, -1), 2, 5, 0, 0))
MonsterSpawns.append(MonsterSpawnParams(M.GorblinShaman(-1, -1), 3, 5, 0, 0))

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
MonsterSpawns.append(MonsterSpawnParams(M.BossOrb(-1, -1), 10, 10, 1, 1))


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
        #self.forceSpawn = ("Gorblin Shaman", 1)
        # self.forceSpawn = ("Hobgorblin", 5) 

    def countSpawn(self, depth):
        if depth == 10:
            return 1
        return random.randint(int(2 + 0.5 * (depth)), int(4 + 1.0 * (depth)))
    
    def random_level(self, depth):
        if depth < 4:
            return random.randint(0, 1)
        elif depth < 7:
            return random.randint(2, 5)
        else:
            return random.randint(6, 9)
    
    def spawnMonsters(self, depth):
        if depth > 10:
            depth = 10
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