import items as I
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
        return copy.copy(self.item)
    
#Spawn lists!
ItemSpawns = []                                              # minFloor    maxFloor(incl)  minAmount   maxAmount(incl)
ItemSpawns.append(ItemSpawnParams( I.Ax(300, -1, -1),                 1,               5,          0,              3))
ItemSpawns.append(ItemSpawnParams( I.Hammer(301, -1, -1),             1,               5,          0,              3))
ItemSpawns.append(ItemSpawnParams( I.HealthPotion(401, -1, -1),       1,               5,          0,              3))