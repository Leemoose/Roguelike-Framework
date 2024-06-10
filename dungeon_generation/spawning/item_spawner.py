import random
from .branch_params import branch_params
from .item_initializations import ItemSpawns
import items as I


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
        self.commonCorpse = [i for i in self.ItemSpawns if i.item.has_trait("corpse")]

        # useful for debugging specific items, separate from generator
        self.forceSpawn = []

        # self.forceSpawn.append(("Boots of Escape", 3))
        # self.forceSpawn.append(("Blood Ring", 3))
        # self.forceSpawn.append(("Wizard Hat", 3))
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
    
    def random_level(self, depth):
        if depth < 4:
            return 0
        elif depth < 7:
            return random.randint(0, 2)
        else:
            return random.randint(0, 3)
    
    def spawnItems(self, depth, branch):
        distribution = branch_params[branch]
        if depth > 10:
            depth = 10
        items = []

        for itemToSpawn in self.forceSpawn:
            for _ in range(itemToSpawn[1]):
                item_spawn = [i for i in self.ItemSpawns if i.item.name == itemToSpawn[0]][0]
                item = item_spawn.GetFreshCopy()
                items.append(item)

        items.append(I.BookofHypnosis())



        commonEquipAtDepth = [i for i in self.commonEquip if i.AllowedAtDepth(depth, branch)]
        commonPotiorbsAtDepth = [i for i in self.commonPotiorbs if i.AllowedAtDepth(depth, branch)]
        commonScrorbsAtDepth = [i for i in self.commonScrorbs if i.AllowedAtDepth(depth, branch)]
        commonCorpsesAtDepth = [i for i in self.commonCorpse if i.AllowedAtDepth(depth, branch)]

        rareEquipAtDepth = [i for i in self.rareEquip if i.AllowedAtDepth(depth, branch)]
        rarePotiorbsAtDepth = [i for i in self.rarePotiorbs if i.AllowedAtDepth(depth, branch)]
        rareScrorbsAtDepth = [i for i in self.rareScrorbs if i.AllowedAtDepth(depth, branch)]
        if rareEquipAtDepth == []:
            rareEquipAtDepth = commonEquipAtDepth
        legendaryEquipAtDepth = [i for i in self.legendaryEquip if i.AllowedAtDepth(depth, branch)]
        legendaryScrorbsAtDepth = [i for i in self.legendaryScrorbs if i.AllowedAtDepth(depth, branch)]
        if legendaryEquipAtDepth == []: # downgrade if no legendary items available
            if rareEquipAtDepth == []:
                legendaryEquipAtDepth = commonEquipAtDepth
            else:
                legendaryEquipAtDepth = rareEquipAtDepth

        for i in range(distribution.countEquipment(depth)):
            rarity = random.random()
            if rarity < distribution.equipment[depth-1][0]:
                item_spawn = random.choice(commonEquipAtDepth)
                item = item_spawn.GetFreshCopy()
                if item.can_be_levelled:
                    for _ in range(self.random_level(depth)):
                        item.level_up()
                items.append(item)
            elif rarity < distribution.equipment[depth-1][0] + distribution.equipment[depth-1][1]:
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
        for i in range(distribution.countPotiorbs(depth)):
            rarity = random.random()
            if rarity < distribution.potiorbs[depth-1][0]:
                item_spawn = random.choice(commonPotiorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
            else:
                item_spawn = random.choice(rarePotiorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
        for i in range(distribution.countScrorbs(depth)):
            rarity = random.random()
            if rarity < distribution.scrorbs[depth-1][0]:
                item_spawn = random.choice(commonScrorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
            elif rarity < distribution.scrorbs[depth-1][0] + distribution.scrorbs[depth-1][1]:
                item_spawn = random.choice(rareScrorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
            else:
                item_spawn = random.choice(legendaryScrorbsAtDepth)
                item = item_spawn.GetFreshCopy()
                items.append(item)
        for i in range(distribution.countExtraCommon(depth)):
            item_spawn = random.choice(self.ExtraCommon)
            item = item_spawn.GetFreshCopy()
            items.append(item)

        for i in range(distribution.countCorpses(depth)):
            rarity = random.random()
            item_spawn = random.choice(commonCorpsesAtDepth)
            item = item_spawn.GetFreshCopy()
            items.append(item)


        return items
    
item_spawner = ItemSpawner(ItemSpawns)