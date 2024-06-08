import random
from .distributions import dists
from .monster_initializations import MonsterSpawns
import items as I

class MonsterSpawner():
    def __init__(self, MonsterSpawns):
        self.MonsterSpawns = MonsterSpawns
        self.commonMonsters = [i for i in self.MonsterSpawns if i.rarity == "Common"]
        self.rareMonsters = [i for i in self.MonsterSpawns if i.rarity == "Rare"]
        self.bossMonsters = [i for i in self.MonsterSpawns if i.boss == True]

        # useful for debugging specific monsters, separate from generator
        self.forceSpawn = None
        # self.forceSpawn = ("Slime", 1)
        # self.forceSpawn = ("Hobgorblin", 5) 

    def countSpawn(self, depth):
        if depth == 10:
            return 1
        return random.randint(int(5 + 0.5 * (depth)), int(8 + 1.0 * (depth)))
    
    def random_level(self, depth):
        if depth < 5:
            return random.randint(0, 1)
        elif depth < 8:
            return random.randint(2, 5)
        else:
            return random.randint(6, 9)
        
    def generate_encounter_numbers(self, target_difficulty, distribution):
        possible_tiers = [0, 1, 2, 3]
        encounter_nums = [0, 0, 0, 0]

        current_difficulty = 0

        while current_difficulty < target_difficulty:
            encounter = random.choices(possible_tiers, weights=distribution, k=1)[0] # choose an encounter tier, weighted by the distribution defined for floor and branch in distributions.py
            # if we would go over target_difficulty just add the highest difficulty that we can without going over, which is target_difficulty - current_difficulty
            if current_difficulty + encounter > target_difficulty:
                encounter_nums[target_difficulty - current_difficulty] += 1
                break
            encounter_nums[encounter] += 1
            current_difficulty += encounter

        return encounter_nums
    
    def make_monster_pack(self, depth, branch, tier):
        if tier < 2 or tier > 3:
            print("invalid tier for monster pack")
            return []
        
        commonAtDepth = [i for i in self.commonMonsters if i.AllowedAtDepth(depth, branch)]
        rareAtDepth = [i for i in self.rareMonsters if i.AllowedAtDepth(depth, branch)]

        monsterGroups = {}
        for common in commonAtDepth:
            if common.group != None:
                if not common.group in monsterGroups.keys():
                    monsterGroups[common.group] = []
                monsterGroups[common.group].append(common)

        # every key in rare groups must exist in common groups as well
        monsterGroupsRare = {}
        for rare in rareAtDepth:
            if rare.group != None and rare.group in monsterGroups.keys():
                if not rare.group in monsterGroupsRare.keys():
                    monsterGroupsRare[rare.group] = []
                monsterGroupsRare[rare.group].append(rare)
        
        if monsterGroups == {}:
            return []
        
        if monsterGroupsRare == {} and tier == 3:
            tier -= 1

        pack_size = dists[branch].monster_pack_size(depth)

        monsters = []

        if tier == 2:
            group = random.choice(list(monsterGroups.keys()))
        if tier == 3:
            # if tier 3, we spawn a rare so need to make sure key is in rare monsters groups
            group = random.choice(list(monsterGroupsRare.keys()))
        
        for _ in range(pack_size):
            monster_spawn = random.choice(monsterGroups[group])
            monsters.append(monster_spawn.GetLeveledCopy(self.random_level(depth)))
        
        # maybe change this so packs can have multiple rares but for now just 1 rare in tier 3 packs
        if tier == 3:
            monster_spawn = random.choice(monsterGroupsRare[group])
            monsters.append(monster_spawn.GetLeveledCopy(self.random_level(depth)))

        return monsters
    
    def get_tier_zero_possibs(self, depth, branch, dist):
        if depth == 1:
            return []
        prev_depth = dist.prev_monster_dist(depth)
        monsters = self.make_monster_pack(prev_depth, branch, random.randint(2, 3))
        return monsters
    
    def get_tier_one_possibs(self, depth, branch, _):
        commonAtDepth = [i for i in self.commonMonsters if i.AllowedAtDepth(depth, branch)]
        if commonAtDepth == []:
            return None
        monster_spawn = random.choice(commonAtDepth)
        monster = monster_spawn.GetLeveledCopy(self.random_level(depth))
        return monster

    def get_tier_two_possibs(self, depth, branch, dist):
        pack_prob = random.random()
        rareAtDepth = [i for i in self.rareMonsters if i.AllowedAtDepth(depth, branch)]
        if pack_prob < dist.monster_pack_chance or rareAtDepth == []:
            return self.make_monster_pack(depth, branch, 2)
        
        monster_spawn = random.choice(rareAtDepth)
        monster = monster_spawn.GetLeveledCopy(self.random_level(depth))
        return monster

    def get_tier_three_possibs(self, depth, branch, _):
        return self.make_monster_pack(depth, branch, 3)

    def spawnMonsters(self, depth, branch):
        if depth > 10:
            depth = 10
        distribution = dists[branch]

        monsters = []

        bossAtDepth = [i for i in self.bossMonsters if i.AllowedAtDepth(depth, branch)]

        if self.forceSpawn:
            for _ in range(self.forceSpawn[1]):
                monster_spawn = [i for i in self.MonsterSpawns if i.monster.name == self.forceSpawn[0]][0]
                monster = monster_spawn.GetLeveledCopy(self.random_level(depth))
                monsters.append(monster)

        for boss in bossAtDepth:
            print("Boss monster: " + boss.monster.name)
            # maybe can change this so bosses aren't leveled if we want to just manually buff bosses so they are less random
            monster = boss.GetLeveledCopy(self.random_level(depth))
            monsters.append(monster)
        
        # monster spawning now works on tiers
        # tier 0 is roll monster distribution from previous floors (unlikely to show up)
        # tier 1 is normal monsters from current floors (most common to show up)
        # tier 2 is either pack of normal monsters or rare monster (less common to show up)
        # tier 3 is pack of rare monster + normal monsters (less common to show up)
        # sum of tier levels equals a difficulty calculated based on depth and branch
        difficulty = distribution.depth_difficulty(depth)

        encounters = self.generate_encounter_numbers(difficulty, distribution.monsters[depth - 1])
        tier_possibs = [self.get_tier_zero_possibs, self.get_tier_one_possibs, self.get_tier_two_possibs, self.get_tier_three_possibs]

        for tier, tier_count in enumerate(encounters):
            for _ in range(tier_count):
                monster = tier_possibs[tier](depth, branch, distribution)
                if monster != None and monster != []:
                    monsters.append(monster)
        
        return monsters
    
monster_spawner = MonsterSpawner(MonsterSpawns)