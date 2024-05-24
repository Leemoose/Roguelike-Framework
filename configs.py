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
