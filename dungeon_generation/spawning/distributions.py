import random

# can overwrite distributions for individual branches
class BranchDistributions:
    def __init__(self):
        self.branch_name = None
        self.difficulty_base = 3 # min sum of tiers of encounters
        self.difficulty_growth = 1 # how much sum of tiers of encounters grow with depth
        self.difficulty_variance = 1 # how much sum of tiers of encounters can vary

        # relative weights for equipment types, this lets us adjust equipment types as we generate to bias towards equipment slots not generated yet
        #                      weapon,  shield, body armor, boots,  helmets, gloves,    pants,  rings,  amulets 
        self.equipment_type = [4,       1,      1,          0.5,    0.5,     0.5,       1,      1,      0.5]

        # chance that tier 2 monster spawn is lone rare monster or a pack of common monsters
        self.monster_pack_chance = 0.5

        # common, rare, legendary
        self.equipment = [(0.9, 0.1, 0.0), # floor 1
                          (0.7, 0.3, 0.0), # floor 2
                          (0.5, 0.4, 0.1), # floor 3
                          (0.3, 0.6, 0.1), # floor 4
                          (0.3, 0.5, 0.2), # floor 5
                          (0.3, 0.5, 0.2), # floor 6
                          (0.3, 0.4, 0.3), # floor 7
                          (0.3, 0.4, 0.3), # floor 8
                          (0.3, 0.3, 0.4), # floor 9
                          (0.3, 0.3, 0.4)] # floor 10
        
        # common, rare
        # no legendary potiorbs exist
        self.potiorbs = [(0.7, 0.3), # floor 1
                         (0.7, 0.3), # floor 2
                         (0.7, 0.3), # floor 3
                         (0.7, 0.3), # floor 4
                         (0.7, 0.3), # floor 5
                         (0.7, 0.3), # floor 6
                         (0.7, 0.3), # floor 7
                         (0.7, 0.3), # floor 8
                         (0.7, 0.3), # floor 9
                         (0.7, 0.3)] # floor 10
        
        # common, rare, legendary
        self.scrorbs = [(0.7, 0.3, 0.0), # floor 1
                        (0.7, 0.3, 0.0), # floor 2
                        (0.5, 0.4, 0.1), # floor 3
                        (0.5, 0.4, 0.2), # floor 4
                        (0.4, 0.4, 0.2), # floor 5
                        (0.4, 0.4, 0.2), # floor 6
                        (0.4, 0.4, 0.2), # floor 7
                        (0.4, 0.4, 0.2), # floor 8
                        (0.4, 0.4, 0.2), # floor 9
                        (0.4, 0.4, 0.2)] # floor 10
    
        # tier 0 is roll monster distribution from previous floors (unlikely to show up)
        # tier 1 is normal monsters from current floors (most common to show up)
        # tier 2 is either pack of normal monsters or rare monster (less common to show up)
        # tier 3 is pack of rare monster + normal monsters (less common to show up)
        # tier 0, tier 1, tier 2, tier 3
        # orb (and any other minibosses we incldue) does not fit into thie tier system and needs to be manually spawned in (this is so we can have random monsters on orb floor as well)
        self.monsters = [(0.0, 1.0, 0.0, 0.0), # floor 1
                         (0.0, 0.7, 0.3, 0.0), # floor 2
                         (0.0, 0.5, 0.3, 0.2), # floor 3
                         (0.0, 0.3, 0.4, 0.3), # floor 4
                         (0.1, 0.7, 0.2, 0.0), # floor 5
                         (0.1, 0.5, 0.2, 0.2), # floor 6
                         (0.1, 0.3, 0.3, 0.3), # floor 7
                         (0.1, 0.7, 0.2, 0.0), # floor 8
                         (0.1, 0.5, 0.2, 0.2), # floor 9
                         (0.1, 0.3, 0.3, 0.3)] # floor 10
    
    # since monsters exist in groups across every 3 floors, have a slight chance of easy monsters appearing later so dungeon doesn't feel totally different across floors
    # exists in this function in case other branches want to overwrite the grouping of every 3 floors that exists in dungeon
    def prev_monster_dist(self, depth):
        # this equation maps 2-4 to 1, 5-7 to 4 and 8-10 to 7
        # doesn't work properly for 1 so don't set tier 0 prob of floor 1 > 0
        return (depth - 2 // 3) * 3 + 1

    def depth_difficulty(self, depth):
        min_difficulty = self.difficulty_base + self.difficulty_growth * depth - self.difficulty_variance
        max_difficulty = self.difficulty_base + self.difficulty_growth * depth + self.difficulty_variance
        return random.randint(min_difficulty, max_difficulty)
    
    # maybe define these by branch but for now its just here
    def monster_pack_size(self, depth, base_size=3, growth=0.5, variance=2):
        min_size = base_size + int(growth * depth)
        max_size = min_size + variance
        return random.randint(min_size, max_size)

    def countEquipment(self, depth):
        return random.randint(int(2 + 0.2 * (depth)), int(3 + 0.3 * (depth)))
    
    def countPotiorbs(self, depth):
        return random.randint(int(2 + 0.1 * (depth)), int(3 + 0.2 * (depth)))
    
    def countExtraCommon(self, depth):
        return random.randint(int(1.5 - 0.1 * (depth - 1)), int(2 + 0.1 * (depth - 1)))
    
    def countScrorbs(self, depth):
        return random.randint(int(2 + 0.1 * (depth)), int(3 + 0.2 * (depth)))

class DungeonDistributions(BranchDistributions):
    def __init__(self):
        super().__init__()
        self.branch_name = "Dungeon"

class ForestDistributions(BranchDistributions):
    def __init__(self):
        super().__init__()
        self.branch_name = "Forest"

        # forest has rarer potions but fewer of them
        # no real reason for this, just to test spawning so can be changed

        self.potiorbs = [(0.4, 0.6), # floor 1
                         (0.4, 0.6), # floor 2
                         (0.4, 0.6), # floor 3
                         (0.4, 0.6), # floor 4
                         (0.4, 0.6), # floor 5
                         (0.4, 0.6), # floor 6
                         (0.4, 0.6), # floor 7
                         (0.4, 0.6), # floor 8
                         (0.4, 0.6), # floor 9
                         (0.4, 0.6)] # floor 10
    
        # forest starts with more encounters than dungeon but no growth
        self.difficulty_base = 6
        self.difficulty_growth = 0
    
    def countPotiorbs(self, depth):
        return random.randint(int(1 + 0.5 * (depth)), int(2 + 0.5 * (depth)))
    
class OceanDistributions(BranchDistributions):
    def __init__(self):
        super().__init__()
        self.branch_name = "Ocean"

dists_list = [DungeonDistributions(),
              ForestDistributions(),
              OceanDistributions()]

# make distributions into dictionary keyed on branch names for ease of use
dists = {d.branch_name : d for d in dists_list}