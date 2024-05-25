from collections import namedtuple
class MapData():
    def __init__(self, width, height, numRooms, roomSize, circularity, squarelike):
        self.width = width
        self.height = height
        self.numRooms = numRooms
        self.roomSize = roomSize
        self.circularity = circularity
        self.squarelike = squarelike

# Config data!
def get_map_data(depth, branch = "Dungeon"):
    MapOptions = {}
    MapOptions[1]  = MapData(20, 30, 4, 5, 1.0, 1)
    MapOptions[2]  = MapData(60, 60, 15, 10, .05, 1)
    MapOptions[3]  = MapData(60, 60, 15, 10, .1, 0)
    MapOptions[4]  = MapData(30, 30, 6, 5, 0.0 , 0)   #Square floor!
    MapOptions[5]  = MapData(35, 35, 7, 6, 0.2, 0 )
    MapOptions[6]  = MapData(35, 35, 8, 7, 0.3, 0 )
    MapOptions[7]  = MapData(40, 40, 9, 7, 0.5, 0 )
    MapOptions[8]  = MapData(40, 40, 10, 8, .6 , 0 )
    MapOptions[9]  = MapData(45, 45, 11, 9, 0.0, 0 ) #Square floor!
    MapOptions[10] = MapData(50, 50, 12, 10, 1.0, 0 )
    return MapOptions[depth]

class DungeonData():
    def __init__(self, branches, depth):
        self.branches = branches
        self.depth = depth

        self.master_map_data = {}
        self.master_map_data["dungeon"] = {
            1: MapData(20, 30, 4, 5, 1.0, 1),
            2: MapData(60, 60, 15, 10, .05, 1),
            3: MapData(60, 60, 15, 10, .1, 0),
            4: MapData(30, 30, 6, 5, 0.0, 0),  # Square floor!
            5: MapData(35, 35, 7, 6, 0.2, 0),
            6: MapData(35, 35, 8, 7, 0.3, 0),
            7: MapData(40, 40, 9, 7, 0.5, 0),
            8: MapData(40, 40, 10, 8, .6, 0),
            9: MapData(45, 45, 11, 9, 0.0, 0),  # Square floor!
            10: MapData(50, 50, 12, 10, 1.0, 0)
            }
        self.master_map_data["forest"] = {
            1: MapData(20, 30, 4, 5, 1.0, 1),
            2: MapData(60, 60, 15, 10, .05, 1),
            3: MapData(60, 60, 15, 10, .1, 0),
            4: MapData(30, 30, 6, 5, 0.0, 0),  # Square floor!
            5: MapData(35, 35, 7, 6, 0.2, 0),
            6: MapData(35, 35, 8, 7, 0.3, 0),
            7: MapData(40, 40, 9, 7, 0.5, 0),
            8: MapData(40, 40, 10, 8, .6, 0),
            9: MapData(45, 45, 11, 9, 0.0, 0),  # Square floor!
            10: MapData(50, 50, 12, 10, 1.0, 0)
            }

        self.gateway_data = GatewayData()

class GatewayData():
    def __init__(self):
        Lair = namedtuple("Lair", ["branch", "depth"])
        self.gateway_mapping = {
            Lair("Dungeon", 1): Lair("Forest", 1),
            Lair("Forest", 1): Lair("Dungeon", 1)
        }

    def has_gateway(self, branch, depth):
        Lair = namedtuple("Lair", ["branch", "depth"])
        if Lair(branch, depth) in self.gateway_mapping:
            return True
        return False

    def all_gateways(self):
        return self.gateway_mapping.keys()

    def paired_gateway(self, old_lair):
        return self.gateway_mapping[old_lair]
