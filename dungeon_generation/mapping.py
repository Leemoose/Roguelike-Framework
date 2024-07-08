import random

import static_configs
from dungeon_generation import *
from .spawning import branch_params, item_spawner, monster_spawner, interactable_spawner
from .maps import TileMap, TrackingMap

from interactables import Campfire


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


class DungeonGenerator():
    #Generates a width by height 2d array of tiles. Each type of tile has a unique tile
    #tag ranging from 0 to 99
    def __init__(self, depth, player, branch, gateway_data, dungeon_data):
        self.mapData = dungeon_data.get_map_data(branch, depth)
        self.depth = depth
        self.branch = branch
        self.spawn_params = branch_params[branch]
        self.width = self.mapData.width
        self.height = self.mapData.height
        self.summoner = []

        self.tile_map = TileMap(self.mapData, depth, self.branch, static_configs.AscaiiTileDict(), gateway_data)
        self.monster_map = TrackingMap(self.width, self.height) #Should I include items as well?
        self.interact_map = TrackingMap(self.width, self.height)
        self.item_map = TrackingMap(self.width, self.height)

        self.player = player
        self.summoner = []


        if (self.depth != 1 or (branch != "Throne" and branch != "Hub")): # prefab first floor of dungeon has no monsters and items
            self.place_monsters(depth)
            self.place_items(depth)
        if (self.depth != 1 or (branch != "Throne")):
            self.place_items(depth)
        self.place_npcs(depth)
        self.place_interactables(branch, depth)

    def get_random_location_basic(self, stairs_block = True):
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)

        while (not self.get_passable((start_x, start_y))) or (not stairs_block or self.on_stairs(start_x, start_y)):
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)

        return start_x, start_y

    def get_random_location(self, stairs_block = True, condition = None):
        candidates = []
        if condition == None:
            return self.get_random_location_basic(stairs_block)
        for x in range(0, self.width):
            for y in range(0, self.height):
                if condition((x, y)) or \
                    (not stairs_block or self.on_stairs(x, y)):
                    candidates.append((x, y))
        startx, starty = random.choice(candidates)
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
        elif self.monster_map.get_passable(location[0], location[1]) and self.not_on_player(location[0], location[1]) and self.tile_map.get_passable(location[0], location[1]) and self.interact_map.get_passable(location[0], location[1]):
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

    def place_monsters(self, depth):
        monsterSpawns = monster_spawner.spawnMonsters(depth, self.branch)
        for monster in monsterSpawns:
            if type(monster) == list:
                self.place_pack(monster)
            else:
                self.place_monster(monster)

    def place_monster(self, creature):
        if self.spawn_params.check_monster_restrictions != None:
            def monster_restriction(location):
                return self.spawn_params.check_monster_restrictions(creature, self.tile_map, location, self)
        else:
            monster_restriction = None
        x, y = self.get_random_location(condition=monster_restriction)
        self.place_monster_at_location(creature, x, y)

    def place_pack(self, pack):
        pack_size = len(pack)
        count = 0
        iters = 0

        area_to_check = 2 # check all tiles in radius 2 (this technically caps pack size at 25, up this area if any dungeon has a higher max pack size)
        directions = [(dx, dy) for dx in range(-1 * area_to_check, area_to_check + 1) for dy in range(-1 * area_to_check, area_to_check + 1)]

        while count < pack_size:
            x, y = self.get_random_location()
            locations = []
            count = 0
            random.shuffle(directions) # varies the arangement of packs

            for (dx, dy) in directions:
                if self.get_passable((x + dx, y + dy)):
                    locations.append((x + dx, y + dy))
                    count += 1
                    # break early as soon as we find a location that can fit the full pack
                    if count >= pack_size:
                        break

        for i, monster in enumerate(pack):
            if i >= len(locations):
                import pdb; pdb.set_trace()
            x, y = locations[i]
            self.place_monster_at_location(monster, x, y)

    def place_monster_at_location(self, creature, x, y):
        creature.x = x
        creature.y = y
        self.monster_map.place_thing(creature)

    def place_npcs(self, depth):
        for x in range(self.width):
            for y in range(self.height):
                if self.tile_map.locate(x,y).has_trait("npc_spawn"):
                    self.interact_map.place_thing(self.tile_map.locate(x,y).spawn_entity())
                if self.tile_map.locate(x,y).has_trait("monster_spawn"): # this is used for static monster spawns
                    self.place_monster_at_location(self.tile_map.locate(x,y).spawn_entity(), x, y)

    def place_interactables(self, branch, depth):
        interactable_spawns = interactable_spawner.spawn_interactables(depth, branch)
        first = True
        force_near_stairs = False
        for interactable in interactable_spawns:
            self.place_interactable(interactable)

    def place_interactable(self, interactable, force_near_stairs=False):
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)
        map = self.interact_map

        # make sure the item is placed on a passable tile that is not stairs or in a corridor
        check_on_stairs = self.on_stairs(startx, starty)
        check_in_corridor = self.in_corridor(startx, starty)
        while ((not self.tile_map.get_passable(startx, starty)) or
                   (not map.get_passable(startx, starty)) or
                   check_on_stairs or check_in_corridor):
                startx = random.randint(0, self.width - 1)
                starty = random.randint(0, self.height - 1)
                check_on_stairs = self.on_stairs(startx, starty)
                check_in_corridor = self.in_corridor(startx, starty)


        interactable.x = startx
        interactable.y = starty

        map.place_thing(interactable)

    def place_items(self, depth):
        itemSpawns = item_spawner.spawnItems(depth, self.branch)
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
    
    def in_corridor(self, x, y):
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        count_passable = 0 # count number of adjacent passable tiles
        count_adjacent_passable = 0 # count number of adjacent tiles that have > 2 passable neighbours (this is for case where x, y is end of corridor)
        for dx, dy in directions:
            adj_x = x + dx
            adj_y = y + dy
            if self.tile_map.get_passable(adj_x, adj_y):
                count_passable += 1
                if count_passable > 4: # no way for this to be in a corridor
                    return False
                temp_count = 0
                for dx2, dy2 in directions:
                    if self.tile_map.get_passable(adj_x + dx2, adj_y + dy2):
                        temp_count += 1
                    if temp_count > 2:
                        break
                if temp_count > 2:
                    count_adjacent_passable += 1
                if count_adjacent_passable > 4:
                    return False
        return True


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




