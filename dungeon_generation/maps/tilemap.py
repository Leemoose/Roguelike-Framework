import random

from .trackingmap import TrackingMap
from .prefab import *
from .floodmap import FloodMap
from .room import Room

"""
This map is responsible for carving all tiles out.
"""

class TileMap(TrackingMap):
    """
            if mapData.squarelike == 1:
            self.track_map_render = [x[:] for x in [[0] * self.width] * self.height]
            #Add rooms
            for roomNum in range(mapData.numRooms):
                size = random.randint(4, mapData.roomSize)
                self.place_room(size, size, mapData.circularity)

            #Connect Rooms
            for i in range(len(self.rooms) - 1):
                self.connect_rooms(self.rooms[i], self.rooms[i + 1])

        #Apply smoothing
        else:
            self.track_map_render = [x[:] for x in [[0 if random.random() > .6 else 1] * self.width] * self.height]
            self.cellular_caves()
    """

    def __init__(self, mapData, depth, branch, diff_tile_dict, gateway_data):
        super().__init__(mapData.width, mapData.height)
        self.mapData = mapData
        self.track_map = []
        self.stairs = []
        self.gateway = []
        self.rooms = []
        self.depth = depth
        self.branch = branch

        # sometimes, rooms can be replaced by prefab rooms, for special quests, events etc.
        # keep track of prefabs, how many more times it can be placed, which floor they can be placed on
        # probability it will be placed and the function called to place it.
        self.prefabs = [
            # dojo (sensei quest)
            {"prefab": dojoify,
             "min_floor": 2,
             "max_floor": 5,
             "spawns_available": 1,
             # not sure if there will be prefabs we want to spawn multiple times through dungeon but left it as a possibility
             "spawn_chance": 1.0}
        ]
        self.ascaii_mapping = diff_tile_dict

        self.track_map_render = [x[:] for x in [["x"] * self.height] * self.width]
        self.image = [x[:] for x in [[-1] * self.height] * self.width]
        if depth == 1 and self.branch == "Dungeon":
            self.track_map_render = throneify(0, 0, self.track_map_render, self.image, self.width, self.height)
        else:
            # Add rooms
            for roomNum in range(mapData.numRooms):
                size = random.randint(4, mapData.roomSize)
                self.place_room(size, size, mapData.circularity)

            # if depth == 2:
            #    import pdb; pdb.set_trace()

            available_prefabs = [x for x in self.prefabs if
                                 x["min_floor"] <= depth and x["max_floor"] >= depth and x["spawns_available"] > 0 and
                                 x["spawn_chance"] > random.random()]

            if depth == 2:
                print(available_prefabs)

            for p in available_prefabs:
                room_to_replace = random.choice(self.rooms)
                self.track_map_render = p["prefab"](room_to_replace, self.track_map_render, self.image, depth)
                p["spawns_available"] -= 1

            # Connect Rooms
            for i in range(len(self.rooms) - 1):
                self.connect_rooms(self.rooms[i], self.rooms[i + 1])
            #      self.cellular_caves()
            self.place_stairs(depth)
        self.place_gateway(gateway_data)
        if depth == 1 or depth == 2:
            print(str(self))

        self.render_to_map(depth)
        # print(f"{depth}: {self.stairs}")
        self.quality_check_map()

    def __str__(self):
        map = ""
        for row in self.track_map:
            for block in row:
                if block.passable:
                    map += "."
                else:
                    map += "x"
            map += "\n"
        return map

    def get_gateway(self):
        return self.gateway

    def place_gateway(self, gateway_data):
        if gateway_data.has_gateway(self.branch, self.depth):
            print("Branch is {}".format(self.branch))
            print("Depth is {}".format(self.depth))
            startx, starty = self.get_random_location_ascaii()
            self.track_map_render[startx][starty] = "g"
            print("Placing gateway")

    def quality_check_map(self):
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    if self.track_map[x][y].type != "Wall":
                        raise Exception(
                            ("The edge of the map for depth {} at location {} is not a wall").format(self.depth,
                                                                                                     (x, y)))
        if self.isolated_cells():
            raise Exception(
                "You have isolated cells for depth {}. This will cause issues with teleport, etc.".format(self.depth))

    def isolated_cells(self):
        flood_map = FloodMap(self.track_map, self.width, self.height)
        for stairs in self.stairs:
            flood_map.update_flood_map(stairs.get_location())
        for x in range(self.width):
            for y in range(self.height):
                if flood_map.locate(x, y) < 0 and self.get_passable(x, y):
                    print(flood_map)
                    print(self)
                    return True
        return False

    def render_to_map(self, depth):
        if self.width != len(self.track_map_render) or self.height != len(self.track_map_render[0]):
            raise Exception(
                "The sizing of your map and the render map our different {}, {}, {}, {}".format(self.width, self.height,
                                                                                                len(self.track_map_render),
                                                                                                len(
                                                                                                    self.track_map_render[
                                                                                                        0])))
        self.track_map = []
        for x in range(self.width):
            temp = []
            for y in range(self.height):
                # print(x,y, self.width, self.height, len(self.track_map_render))
                text = self.track_map_render[x][y]
                #if (self.track_map_render[x][y].type == "NPCSpawn" and depth == 2) \
                #        or (self.track_map_render[x][y].type == "MonsterSpawn" and depth == 2):
                #    import pdb;
                #    pdb.set_trace()
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    if text != "x":
                        print(
                            "Warning: You did not properly buffer the edges of your map and it was overridden to walls")
                    temp.append(self.ascaii_mapping.ascaii_tile("x")(x, y))
                elif text in self.ascaii_mapping.tiles:
                    if self.image[x][y] != -1:
                        tile = self.ascaii_mapping.ascaii_tile(text)(x, y, render_tag=self.image[x][y])
                    elif text in self.ascaii_mapping.image_mapping[self.branch]:
                        tile = self.ascaii_mapping.ascaii_tile(text)(x, y,
                                                                     render_tag=self.ascaii_mapping.branchdepth_render(
                                                                         self.branch, text))
                    else:
                        tile = self.ascaii_mapping.ascaii_tile(text)(x, y)
                    temp.append(tile)
                    if tile.type == "Stairs":
                        self.stairs.append(tile)
                    elif tile.type == "Gateway":
                        self.gateway.append(tile)
                        tile.relocate(self.branch, self.depth)
                else:
                    raise Exception("You have the incorrect format in the mapping {}",
                                    format(self.track_map_render[x][y]))

            self.track_map.append(temp)

    def get_tag(self, x, y):
        return self.track_map[x][y].render_tag

    def locate(self, x, y):
        return self.track_map[x][y]

    def cellular_caves(self):
        iterations = 3
        self.track_map_render = [x[:] for x in [["x"] * self.width] * self.height]
        survival_rate = 0.45
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if (random.uniform(0, 1) >= survival_rate):
                    self.track_map_render[x][y] = "."
        for i in range(iterations):
            self.iterate_cellular_map()

    def iterate_cellular_map(self):
        temp_track_map_render = [x[:] for x in [["x"] * self.width] * self.height]
        birth_limit = 4
        death_limit = 3
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                count = self.count_neighbors(x, y)
                if count >= birth_limit and self.track_map_render[x][y] == "x":
                    temp_track_map_render[x][y] = "."
                elif count <= death_limit and self.track_map_render[x][y] == ".":
                    temp_track_map_render[x][y] = "x"
                else:
                    temp_track_map_render[x][y] = self.track_map_render[x][y]
        self.track_map_render = temp_track_map_render

    def count_neighbors(self, x, y):
        count = 0
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                neighbor_x = x + i
                neighbor_y = y + j
                if i == 0 and j == 0:
                    pass
                elif neighbor_y <= 0 or neighbor_x <= 0 or neighbor_x >= self.width - 1 or neighbor_y >= self.height - 1:
                    count += 1
                elif self.track_map_render[neighbor_x][neighbor_y] == "x":
                    count += 1
        return count

    def carve_rooms(self):
        for x in range(self.width - 2):
            for y in range(self.height - 2):
                tile = O.Tile(x + 1, y + 1, 2, True)
                self.track_map[x + 1][y + 1] = tile

    def place_stairs(self, depth):
        if depth > 2:
            startx, starty = self.get_random_location_ascaii()
            # while track_map_ren
            # tile = T.Stairs(startx, starty, 90, True, downward=False)
            self.track_map_render[startx][starty] = "<"
            # self.stairs.append(tile)
        if (depth < 10):
            for i in range(2):
                startx, starty = self.get_random_location_ascaii()
                # tile = T.Stairs(startx, starty, 91, True, downward=True)
                self.track_map_render[startx][starty] = ">"
                # self.stairs.append(tile)
        startx, starty = self.get_random_location_ascaii()
        self.track_map_render[startx][starty] = "<"

    def get_stairs(self):
        return self.stairs

    def place_tile(self, tile):
        self.track_map[tile.x][tile.y] = tile

    def get_passable(self, x, y):
        if (x >= 0) & (y >= 0) & (x < self.width) & (y < self.height):
            return (self.track_map[x][y].is_passable())
        else:
            return False

    def mark_visible(self, x, y):
        self.track_map[x][y].seen = True

    def overlaps_any(self, room):
        for other in self.rooms:
            if (room.intersects(other)):
                return True
        return False

    def point_in_squircle(self, x, y, circularity):
        originX = 1.0 * (self.width - 1) / 2
        originY = 1.0 * (self.height - 1) / 2
        radius = max(self.width, self.height) / 2

        radiusSqrd = radius ** 2
        squircConst = ((1 - circularity) / radius) ** 2
        localX = x - originX
        localY = y - originY

        xSqrd = localX ** 2
        ySqrd = localY ** 2

        squircleVal = xSqrd + ySqrd - squircConst * xSqrd * ySqrd

        return (squircleVal < radiusSqrd)

    def in_squircle(self, room, circularity):
        return self.point_in_squircle(room.x, room.y, circularity) and self.point_in_squircle(room.x + room.width - 1,
                                                                                              room.y + room.width - 1,
                                                                                              circularity)

    def place_room(self, rWidth, rHeight, circularity):
        MaxTries = 100
        startX = random.randint(1, self.width - rWidth - 1)
        startY = random.randint(1, self.height - rHeight - 1)
        room = Room(startX, startY, rWidth, rHeight)
        tries = 0
        while (self.overlaps_any(room) and self.in_squircle(room, circularity) and tries < MaxTries):
            room.x = random.randint(1, self.width - rWidth - 1)
            room.y = random.randint(1, self.height - rHeight - 1)
            tries += 1
        if (tries < MaxTries):
            self.rooms.append(room)
            self.carve_room(room, circularity)

    def carve_room(self, room, circularity):
        originX = 1.0 * (room.width - 1) / 2
        originY = 1.0 * (room.height - 1) / 2
        radius = max(room.width, room.height) / 2

        radiusSqrd = radius ** 2
        squircConst = ((1 - circularity) / radius) ** 2

        for x in range(room.width):
            for y in range(room.height):
                localX = x - originX
                localY = y - originY

                xSqrd = localX ** 2
                ySqrd = localY ** 2

                squircleVal = xSqrd + ySqrd - squircConst * xSqrd * ySqrd

                if (squircleVal < radiusSqrd):
                    self.track_map_render[x + room.x][y + room.y] = "."

    def connect_rooms(self, room1, room2):
        cornerX: int = room1.GetCenterX()
        cornerY: int = room2.GetCenterY()

        lower1X = min(room1.GetCenterX(), cornerX)
        upper1X = max(room1.GetCenterX(), cornerX) + 1
        lower1Y = min(room1.GetCenterY(), cornerY)
        upper1Y = max(room1.GetCenterY(), cornerY) + 1

        for x in range(lower1X, upper1X):
            for y in range(lower1Y, upper1Y):
                if self.track_map_render[x][y] == "x":
                    self.track_map_render[x][y] = "."

        lower2X = min(room2.GetCenterX(), cornerX)
        upper2X = max(room2.GetCenterX(), cornerX) + 1
        lower2Y = min(room2.GetCenterY(), cornerY)
        upper2Y = max(room2.GetCenterY(), cornerY) + 1

        for x in range(lower2X, upper2X):
            for y in range(lower2Y, upper2Y):
                if self.track_map_render[x][y] == "x":
                    self.track_map_render[x][y] = "."

    def get_random_location_ascaii(self, stairs_block=True):
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)
        while (not self.track_map_render[startx][starty] == "."):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
        return startx, starty

