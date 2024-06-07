import random

# can overwrite distributions for individual branches
class BranchDistributions:
    def __init__(self):
        self.branch_name = None

        # relative weights for equipment types, this lets us adjust equipment types as we generate to bias towards equipment slots not generated yet
        #                      weapon,  shield, body armor, boots,  helmets, gloves,    pants,  rings,  amulets 
        self.equipment_type = [4,       1,      1,          0.5,    0.5,     0.5,       1,      1,      0.5]

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
    
        # common, rare, orb
        self.monsters = [(1.0, 0.0, 0.0), # floor 1
                         (0.9, 0.1, 0.0), # floor 2
                         (0.8, 0.2, 0.0), # floor 3
                         (0.7, 0.3, 0.0), # floor 4
                         (0.7, 0.3, 0.0), # floor 5
                         (0.6, 0.4, 0.0), # floor 6
                         (0.6, 0.4, 0.0), # floor 7
                         (0.5, 0.5, 0.0), # floor 8
                         (0.5, 0.5, 1.0), # floor 9
                         (0.0, 0.0, 1.0)] # floor 10
    
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
        self.branch_name = "dungeon"

class ForestDistributions(BranchDistributions):
    def __init__(self):
        super().__init__()
        self.branch_name = "forest"

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
    
    def countPotiorbs(self, depth):
        return random.randint(int(1 + 0.5 * (depth)), int(2 + 0.5 * (depth)))
    
class OceanDistributions(BranchDistributions):
    def __init__(self):
        super().__init__()
        self.branch_name = "ocean"

dists_list = [DungeonDistributions(),
              ForestDistributions(),
              OceanDistributions()]

# make distributions into dictionary keyed on branch names for ease of use
dists = {d.branch_name : d for d in dists_list}