
import objects as O
import static_configs
import tiles as T

import random

import configs
import prefab
import spawnparams as Spawns
import npc as N


class Room():
    def __init__(self, x : int, y : int, width : int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other):
        xPositive = min(self.x + self.width + 1, other.x + other.width + 1) > max(self.x, other.x)
        yPositive = min(self.y + self.height + 1, other.y + other.height + 1) > max(self.y, other.y)
        return xPositive and yPositive
    
    def GetCenterX(self):
        return (self.x + self.width // 2)
    
    def GetCenterY(self):
        return (self.y + self.height // 2)

"""
Theme: Mapping is responsible for creating all maps at the start of the level, placing monsters, placing items,
 as well as providing basic information about those maps.
Classes:
    TileDict --> Maps a render tag to the actual image (makes it easy to switch out the image)
    DungeonGenerator --> Sets up the dungeon when the player goes downward. Creates several different maps
        MonsterMap --> Has a unique tag for each monster at their x, y coordinates
        MonsterDict --> Maps the unique tag to the actual monster
        TileMap --> Has each tile in an x, y position
"""

class ID():
    """
    All unique entities (monsters and items) are tagged with an ID and put into dictionary.
    IDs are generally used in arrays and other places and then the ID can be used to get actual object
    """

    def __init__(self):
        self.subjects = {}
        self.ID_count = 0

    def __str__(self):
        allrows = ""
        for entity in self.all_entities():
            allrows += ' '.join("Entity: {}, ID: {} \n".format(entity, entity.id_tag))
        return allrows

    def tag_subject(self, subject):
        self.ID_count += 1
        subject.gain_ID(self.ID_count)
        self.add_subject(subject)

    def get_subject(self, key):
        if key in self.subjects:
            return self.subjects[key]
        elif key == -1:
            raise Exception("You should not be getting a negative subject (id = {})".format(key))
        else:
            raise Exception("You should not be passing a id not in the subjects (id = {}).".format(key))

    def remove_subject(self, key):
        print("Item Dictionary:")
        print("You are trying to remove key {} from item dictionary".format(key))
        if key in self.subjects:
            return self.subjects.pop(key)
        elif key == -1:
            raise Exception("You should not be removing a negative subject")
        else:
            raise Exception("You should not be removing an id not in the subjects.")

    def add_subject(self, subject):
        self.subjects[subject.id_tag] = subject

    def all_entities(self):
        return list(self.subjects.values())

    def num_entities(self):
        return len(self.subjects)


class DungeonGenerator():
    #Generates a width by height 2d array of tiles. Each type of tile has a unique tile
    #tag ranging from 0 to 99
    def __init__(self, depth, player, branch):
        self.mapData = configs.get_map_data(depth, branch)
        self.depth = depth
        self.branch = branch
        self.width = self.mapData.width
        self.height = self.mapData.height
        self.summoner = []
        self.tile_map = TileMap(self.mapData, depth, self.branch)
        self.monster_map = TrackingMap(self.width, self.height) #Should I include items as well?
        #self.flood_map = FloodMap(self, self.width, self.height)
        self.item_map = TrackingMap(self.width, self.height)

        self.player = player
        self.summoner = []

        if depth == 1 or depth == 2:
            print(str(self.tile_map))

        self.npc_dict = ID()
        if self.depth != 1:
            self.place_monsters(depth)
            self.place_items(depth)
        self.place_npcs(depth)


    def get_random_location(self, stairs_block = True):
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)
        while (not self.get_passable((startx,starty)) or (not stairs_block or self.on_stairs(startx, starty))):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
        return startx, starty

    def monsters_in_sight(self):
        in_sight = []
        for monster in self.monster_map.all_entities():
            monster_x, monster_y = monster.get_location()
            tile = self.tile_map.locate(monster_x, monster_y)
            if tile.is_visible():
                in_sight.append(monster)
        return in_sight

    def all_seen(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tile_map.track_map[x][y].passable :
                    if not (self.all_neighbors_seen(x, y)):
                        return False, (x, y)
        return True, (-1, -1)
    
    def get_all_frontier_tiles(self):
        tiles = []
        for x in range(self.width):
            for y in range(self.height):
                if self.tile_map.track_map[x][y].passable and self.is_frontier_tile(x, y):
                    tiles.append((x, y))
        return tiles
    
    def is_frontier_tile(self, x, y):
        if (self.tile_map.track_map[x][y].seen):
            for neighborX in range(x-1, x+2):
                for neighborY in range(y-1, y+2):
                    if not (self.tile_map.track_map[neighborX][neighborY].seen):
                        return True
        return False
    
    def all_neighbors_seen(self, x, y):
        for neighborX in range(x-1, x+2):
            for neighborY in range(y-1, y+2):
                if not (self.tile_map.track_map[neighborX][neighborY].seen):
                    return False
        return True

    def count_passable_neighbors(self, x, y):
        count = 0
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if self.tile_map.get_passable(x + direction[0], y + direction[1]):
                count += 1
        return count

    def nearest_exit (self, entity):
        # find the nearest exit to some entity, exit is adjacent to a tile with only tiles adjacent to it that are passable
        # if no such tile exists, return None
        list_of_exits = []
        for x in range(self.width):
            for y in range(self.height):
                if self.tile_map.track_map[x][y].passable:
                    if self.count_passable_neighbors(x, y) == 2:
                        list_of_exits.append((x, y))
        entityx, entityy = entity.get_location()
        closest_exit = None
        closest_distance = 100000
        for exit in list_of_exits:
            distance = ((entityx - exit[0]) ** 2 + (entityy - exit[1]) ** 2) ** 0.5
            if distance < closest_distance:
                closest_distance = distance
                closest_exit = exit
        adjacent_to_exit = None
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            # check all directions to find tile adjacent to exit that isnt an exit
            if self.tile_map.get_passable(closest_exit[0] + direction[0], closest_exit[1] + direction[1]):
                if self.count_passable_neighbors(closest_exit[0] + direction[0], closest_exit[1] + direction[1]) > 2:
                    # if tile has a character on it already
                    adjacent_to_exit = (closest_exit[0] + direction[0], closest_exit[1] + direction[1])
                    break
        return adjacent_to_exit
    
    def not_on_player(self, x, y):
        if self.player == None:
            return True
        else:
            return (x != self.player.x or y != self.player.y)

    def get_passable(self, location):
        if type(location) is not tuple:
            print("You are trying to parse a non tuple")
        if location == None:
            return None
        elif self.monster_map.get_passable(location[0], location[1]) and self.not_on_player(location[0], location[1]) and self.tile_map.get_passable(location[0], location[1]):
            for key in self.npc_dict.subjects:
                npc = self.npc_dict.get_subject(key)
                if location == npc.get_location():
                    return False
            return True
        return False

    def nearest_empty_tile(self, location, move = False, search = False):
      #  import pdb; pdb.set_trace()
        if location == None:
            return None
        if not move and self.monster_map.get_passable(location[0], location[1]) and self.not_on_player(location[0], location[1]) and self.tile_map.get_passable(location[0], location[1]):
            return location
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            if self.monster_map.get_passable(location[0] + direction[0], location[1] + direction[1]) and self.not_on_player(location[0] + direction[0], location[1] + direction[1]) and self.tile_map.get_passable(location[0] + direction[0], location[1] + direction[1]):
                return (location[0] + direction[0], location[1] + direction[1])
        if search:
            return self.flood_map.update_flood_map(location)
        return None

    def in_map(self, x, y):
       return x>= 0 and x < self.width and y >= 0 and y < self.height

    def random_direction(self, old):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        new = (0,0)
        while new != old:
            ran = random.randint(0,3)
            new = directions[ran]
        return new

    def square_room(self, startx, starty, length, depth):
        for x in range(length):
            for y in range(depth):
                if startx + x >= 0 and startx + x < self.width and starty+y >= 0 and starty + y < self.height:
                    tile = O.Tile(startx + x, starty + y, 1, True)
                    self.tile_map[startx + x][starty + y] = tile

    def place_monsters(self, depth):
        monsterSpawns = Spawns.monster_spawner.spawnMonsters(depth)
        for monster in monsterSpawns:
            self.place_monster(monster)

    def place_monster(self, creature):
        x, y = self.get_random_location()
        self.place_monster_at_location(creature, x, y)

    def place_monster_at_location(self, creature, x, y):
        creature.x = x
        creature.y = y
        self.monster_map.place_thing(creature)

    def place_npcs(self, depth):
        if depth == 2:
            startx, starty = self.get_random_location()
            npc = N.Bob(110, startx, starty)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for change in directions:
                if not self.tile_map.get_passable(startx + change[0], starty + change[1]):
                    self.tile_map.track_map[startx + change[0]][starty + change[1]] = O.Tile(startx + change[0], starty + change[1], 2, True)

            self.npc_dict.tag_subject(npc)
        
        for x in range(self.width):
            for y in range(self.height):
                if isinstance(self.tile_map.locate(x,y), T.NPCSpawn):
                    self.npc_dict.tag_subject(self.tile_map.locate(x,y).spawn_entity())
                if isinstance(self.tile_map.locate(x,y), T.MonsterSpawn):
                    self.place_monster_at_location(self.tile_map.locate(x,y).spawn_entity(), x, y)

    def place_items(self, depth):
        itemSpawns = Spawns.item_spawner.spawnItems(depth)
        first = True
        force_near_stairs = False
        for item in itemSpawns:
            if first and depth == 2:
                # manually force a weapon to spawn near the stairs on the second floor
                force_near_stairs = True
                first = False # only do so for first item
            self.place_item(item, force_near_stairs)
            force_near_stairs = False

    def on_stairs(self, x, y):
        for stair in self.tile_map.stairs:
            if stair.x == x and stair.y == y:
                return True
        return False

    def place_item(self, item, force_near_stairs=False):
        startx = random.randint(0, self.width-1)
        starty = random.randint(0,self.height-1)

        # make sure the item is placed on a passable tile that does not already have an item and is not stairs
        check_on_stairs = self.on_stairs(startx, starty)
        if force_near_stairs:
            directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            while ((self.tile_map.get_passable(startx, starty) == False) or
                   (self.item_map.get_passable(startx, starty) == False)):
                random_direction = random.choice(directions)
                startx = self.tile_map.stairs[1].x + random_direction[0]
                starty = self.tile_map.stairs[1].y + random_direction[1]
        else:
            while ((self.tile_map.get_passable(startx, starty) == False) or 
                (self.item_map.get_passable(startx, starty) == False) or
                check_on_stairs):
                startx = random.randint(0, self.width-1)
                starty = random.randint(0,self.height-1)
                check_on_stairs = self.on_stairs(startx, starty)
            
        item.x = startx
        item.y = starty

        self.item_map.place_thing(item)

    def get_map(self):
        return self.tile_map


class Maps():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.track_map = [x[:] for x in [[-1] * self.height] * self.width]

    def locate(self, x, y):
        return self.track_map[x][y]

    def get_passable(self,x,y):
        if self.in_map(x,y):
            return (self.track_map[x][y] == -1)
        else:
            return False

    def in_map(self, x, y):
       return x>= 0 and x < self.width and y >= 0 and y < self.height

"""
This map will either track items or monsters.
"""
class TrackingMap(Maps):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.dict = ID()  # Unique to this floor

    def place_thing(self, thing):
        self.dict.tag_subject(thing)
        self.track_map[thing.x][thing.y] = thing.id_tag

    def clear_location(self, x, y):
        self.track_map[x][y] = -1

    def num_entities(self):
        return self.dict.num_entities()

    def remove_thing(self, thing):
        self.clear_location(thing.x, thing.y)
        return self.dict.remove_subject(thing.id_tag)

    def locate(self, x, y):
        if self.get_passable(x, y):
            return -1
        else:
            return self.dict.get_subject(self.track_map[x][y])

    def all_entities(self):
        return self.dict.all_entities()

    def __str__(self):
        allrows = ""
        for x in range(self.width):
            row = ' '.join(str(self.track_map[x][y].render_tag) for y in range(self.height))
            allrows = allrows + row + "\n"      
        return allrows

class FloodMap(Maps):
    def __init__(self, map, width, height):
        super().__init__(width, height)
        self.flood_queue = []
        self.tile_map = map
        self.track_map = [x[:] for x in [[-2] * self.height] * self.width]

    def update_flood_map(self, location, search = False, reset = False):
        if reset:
            self.track_map = [x[:] for x in [[-2] * self.height] * self.width]
        x, y = location
        self.track_map[x][y] = -1
        self.flood_queue.append((x, y, 0, 0, 0))
        while (len(self.flood_queue) > 0):
            self.iterate_flood(search)

    def iterate_flood(self, search = False):
        x, y, xdelta, ydelta, count = self.flood_queue.pop(0)
        if (self.in_map(x + xdelta, y + ydelta) and self.track_map[x + xdelta][y + ydelta] == -1 and self.tile_map[x+xdelta][y+ydelta].is_passable()):
            self.track_map[x + xdelta][y + ydelta] = count
            options = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            r = random.randint(0, 3)
            for i in range(4):
                xdeltanew, ydeltanew = options[(r + i) % 4]
                if self.in_map(x + xdelta + xdeltanew, y + ydelta + ydeltanew) and (
                        self.track_map[x + xdelta + xdeltanew][y + ydelta + ydeltanew] == -2):
                    self.flood_queue.append((x + xdelta, y + ydelta, xdeltanew, ydeltanew, count + 1))
                    self.track_map[x + xdelta + xdeltanew][y + ydelta + ydeltanew] = -1

    def __str__(self):
        allrows = ""
        for x in range(self.width):
            row = ' '.join(str(self.track_map[x][y]) for y in range(self.height))
            allrows = allrows + row + "\n"
        return allrows


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
    def __init__(self, mapData, depth, branch):
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
            {"prefab": prefab.dojoify, 
             "min_floor": 2,
             "max_floor": 5,
             "spawns_available": 1, # not sure if there will be prefabs we want to spawn multiple times through dungeon but left it as a possibility
             "spawn_chance": 1.0}
        ]
        self.ascaii_mapping = static_configs.AscaiiTileDict()

        self.track_map_render = [x[:] for x in [["x"] * self.height] * self.width]
        self.image = [x[:] for x in [[-1] * self.height] * self.width]
        if depth == 1 and self.branch == "Dungeon":
            self.track_map_render = prefab.throneify(0,0, self.track_map_render, self.image, self.width, self.height)
        else:
            # Add rooms
            for roomNum in range(mapData.numRooms):
                size = random.randint(4, mapData.roomSize)
                self.place_room(size, size, mapData.circularity)

            #if depth == 2:
            #    import pdb; pdb.set_trace()

            available_prefabs = [x for x in self.prefabs if x["min_floor"] <= depth and x["max_floor"] >= depth and x["spawns_available"] > 0 and x["spawn_chance"] > random.random()]

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
        self.place_gateway()
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
    def place_gateway(self):
        if self.branch == "Dungeon":
            print("Branch is {}".format(self.branch))
            print("Depth is {}".format(self.depth))
            if self.depth == 5:
                startx, starty = self.get_random_location_ascaii()
                self.track_map_render[startx][starty] = "fg"
                print("Placing gateway")
        elif self.branch == "Forest":
            if self.depth == 1:
                startx, starty = self.get_random_location_ascaii()
                self.track_map_render[startx][starty] = "dg"
    def quality_check_map(self):
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 or x == self.width-1 or y == 0 or y == self.height -1:
                    if not isinstance(self.track_map[x][y], T.Wall):
                        raise Exception(("The edge of the map for depth {} at location {} is not a wall").format(self.depth, (x, y)))
        if self.isolated_cells():
            raise Exception("You have isolated cells for depth {}. This will cause issues with teleport, etc.".format(self.depth))

    def isolated_cells(self):
        flood_map = FloodMap(self.track_map, self.width, self.height)
        for stairs in self.stairs:
            flood_map.update_flood_map(stairs.get_location())
        for x in range(self.width):
            for y in range(self.height):
                if flood_map.locate(x, y) < 0 and self.get_passable(x,y):
                    print(flood_map)
                    print(self)
                    return True
        return False

    def render_to_map(self, depth):
        if self.width != len(self.track_map_render) or self.height != len(self.track_map_render[0]):
            raise Exception("The sizing of your map and the render map our different {}, {}, {}, {}".format(self.width,self.height, len(self.track_map_render), len(self.track_map_render[0])))
        self.track_map = []
        for x in range(self.width):
            temp = []
            for y in range(self.height):
                #print(x,y, self.width, self.height, len(self.track_map_render))
                text = self.track_map_render[x][y]
                if (isinstance(self.track_map_render[x][y], T.NPCSpawn) and depth == 2) \
                    or (isinstance(self.track_map_render[x][y], T.MonsterSpawn) and depth == 2):
                    import pdb; pdb.set_trace()
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    if text != "x":
                        print("Warning: You did not properly buffer the edges of your map and it was overridden to walls")
                    temp.append(self.ascaii_mapping.ascaii_tile("x")(x,y))
                elif text in self.ascaii_mapping.tiles:
                    if self.image[x][y] != -1:
                        tile = self.ascaii_mapping.ascaii_tile(text)(x, y, render_tag=self.image[x][y])
                    elif text in self.ascaii_mapping.image_mapping[self.branch]:
                        tile = self.ascaii_mapping.ascaii_tile(text)(x, y, render_tag=self.ascaii_mapping.branchdepth_render(self.branch, text))
                    else:
                        tile = self.ascaii_mapping.ascaii_tile(text)(x, y)
                    temp.append(tile)
                    if isinstance(tile, T.Stairs):
                        self.stairs.append(tile)
                    elif isinstance(tile, T.Gateway):
                        self.gateway.append(tile)
                else:
                    raise Exception("You have the incorrect format in the mapping {}",format(self.track_map_render[x][y]))

            self.track_map.append(temp)

    def get_tag(self, x, y):
        return self.track_map[x][y].render_tag

    def locate(self, x, y):
        return self.track_map[x][y]

    def cellular_caves(self):
        iterations = 3
        self.track_map_render = [x[:] for x in [["x"] * self.width] * self.height]
        survival_rate = 0.45
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                if (random.uniform(0,1) >= survival_rate):
                    self.track_map_render[x][y] = "."
        for i in range(iterations):
            self.iterate_cellular_map()

    def iterate_cellular_map(self):
        temp_track_map_render = [x[:] for x in [["x"] * self.width] * self.height]
        birth_limit = 4
        death_limit = 3
        for x in range(1,self.width-1):
            for y in range(1,self.height-1):
                count = self.count_neighbors(x,y)
                if count >= birth_limit and self.track_map_render[x][y] == "x":
                    temp_track_map_render[x][y] = "."
                elif count <= death_limit and self.track_map_render[x][y] == ".":
                    temp_track_map_render[x][y] = "x"
                else:
                    temp_track_map_render[x][y] = self.track_map_render[x][y]
        self.track_map_render = temp_track_map_render
    def count_neighbors(self, x, y):
        count = 0
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                neighbor_x = x+ i
                neighbor_y = y +j
                if i == 0 and j == 0:
                    pass
                elif neighbor_y <= 0 or neighbor_x <= 0 or neighbor_x >= self.width-1 or neighbor_y >= self.height-1:
                    count += 1
                elif self.track_map_render[neighbor_x][neighbor_y] == "x":
                    count += 1
        return count



    def carve_rooms(self):
        for x in range(self.width - 2):
            for y in range(self.height - 2):
                tile = O.Tile(x+1, y+1, 2, True)
                self.track_map[x+1][y+1] = tile

    def place_stairs(self, depth):
        if depth > 2:
            startx, starty = self.get_random_location_ascaii()
            # while track_map_ren
            #tile = T.Stairs(startx, starty, 90, True, downward=False)
            self.track_map_render[startx][starty] = "<"
            #self.stairs.append(tile)
        if (depth < 10):
            for i in range(2):
                startx, starty = self.get_random_location_ascaii()
                #tile = T.Stairs(startx, starty, 91, True, downward=True)
                self.track_map_render[startx][starty] = ">"
                #self.stairs.append(tile)
        startx, starty = self.get_random_location_ascaii()
        self.track_map_render[startx][starty] = "<"


    def get_stairs(self):
        return self.stairs

    def place_tile(self, tile):
        self.track_map[tile.x][tile.y] = tile

    def get_passable(self, x, y):
        if (x>=0) & (y>=0) & (x < self.width) & (y < self.height):
            return (self.track_map[x][y].is_passable())
        else:
            return False

    def mark_visible(self,x,y):
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

        radiusSqrd = radius**2
        squircConst = ((1 - circularity)/radius)**2
        localX = x - originX
        localY = y - originY

        xSqrd = localX**2
        ySqrd = localY**2

        squircleVal = xSqrd + ySqrd - squircConst * xSqrd * ySqrd
                
        return (squircleVal < radiusSqrd)
    
    def in_squircle(self, room, circularity):
        return self.point_in_squircle(room.x, room.y, circularity) and self.point_in_squircle(room.x + room.width - 1, room.y + room.width - 1, circularity)

    def place_room(self, rWidth, rHeight, circularity):
        MaxTries = 100
        startX = random.randint(1, self.width - rWidth - 1)
        startY = random.randint(1,self.height - rHeight - 1)
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

        radiusSqrd = radius**2
        squircConst = ((1 - circularity)/radius)**2

        for x in range(room.width):
            for y in range(room.height):
                localX = x - originX
                localY = y - originY

                xSqrd = localX**2
                ySqrd = localY**2

                squircleVal = xSqrd + ySqrd - squircConst * xSqrd * ySqrd
                
                if (squircleVal < radiusSqrd):
                    self.track_map_render[x + room.x][y + room.y] = "."


    def connect_rooms(self, room1, room2):
        cornerX : int = room1.GetCenterX()
        cornerY : int = room2.GetCenterY()

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

    def get_random_location_ascaii(self, stairs_block = True):
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)
        while (not self.track_map_render[startx][starty] == "."):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
        return startx, starty

