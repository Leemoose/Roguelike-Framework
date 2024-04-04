from pygame import image
import pygame
import dice as R
import objects as O
import loops as L
import items as I
import monster as Mon
import random
import math
import spawnparams as Spawns
import npc as N
from fractions import Fraction

class MapData():
    def __init__(self, width, height, numRooms, roomSize, circularity, squarelike):
        self.width = width
        self.height = height
        self.numRooms = numRooms
        self.roomSize = roomSize
        self.circularity = circularity
        self.squarelike = squarelike

# Config data!
MapOptions = {}
MapOptions[1]  = MapData(20, 20, 4, 5, 1.0, 1)
MapOptions[2]  = MapData(60, 60, 15, 10, .05, 1)
MapOptions[3]  = MapData(60, 60, 15, 10, .1, 0)
MapOptions[4]  = MapData(30, 30, 6, 5, 0.0 , 0)   #Square floor!
MapOptions[5]  = MapData(35, 35, 7, 6, 0.2, 0 )
MapOptions[6]  = MapData(35, 35, 8, 7, 0.3, 0 )
MapOptions[7]  = MapData(40, 40, 9, 7, 0.5, 0 )
MapOptions[8]  = MapData(40, 40, 10, 8, .6 , 0 )
MapOptions[9]  = MapData(45, 45, 11, 9, 0.0, 0 ) #Square floor!
MapOptions[10] = MapData(50, 50, 12, 10, 1.0, 0 )


MaxTries = 100
CirclesBeginOn = 7 #Circular walls on 7 and below

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
class TileDict():
    def __init__(self, textSize):
        tiles = {}
        #1-99 are tile
        tiles[1] = pygame.transform.scale(image.load("assets/tiles/colorful_wall.png"), (32,32))
        tiles[-1] = pygame.transform.scale(image.load("assets/tiles/colorful_wall_shaded.png"), (32,32))
        tiles[2] = pygame.transform.scale(image.load("assets/tiles/colorful_floor.png"), (32,32))
        tiles[-2] = pygame.transform.scale(image.load("assets/tiles/colorful_floor_shaded.png"), (32,32))
        tiles[3] = pygame.transform.scale(image.load("assets/floor_dirty.png"), (32,32))
        tiles[-3] = pygame.transform.scale(image.load("assets/floor_dirty_shaded.png"), (32,32))
        tiles[4] = pygame.transform.scale(image.load("assets/floor_dirty1.png"), (32,32))
        tiles[-4] = pygame.transform.scale(image.load("assets/floor_dirty1_shaded.png"), (32,32))

        tiles[11] = pygame.transform.scale(image.load("assets/tiles/wall_extra_rounded.png"), (32,32))
        tiles[-11] = pygame.transform.scale(image.load("assets/tiles/wall_extra_rounded_shaded.png"), (32,32))
        tiles[12] = pygame.transform.scale(image.load("assets/tiles/floor_rounded.png"), (32,32))
        tiles[-12] = pygame.transform.scale(image.load("assets/tiles/floor_rounded_shaded.png"), (32,32))

        # basic assets
        tiles[90] = image.load("assets/tiles/stairs_up.png")
        tiles[-90] = image.load("assets/tiles/stairs_up_shaded.png")
        tiles[91] = image.load("assets/tiles/stairs_down.png")
        tiles[-91] = image.load("assets/tiles/stairs_down_shaded.png")

        # ui assets
        tiles[50] = image.load("assets/stat_up.png")
        tiles[51] = image.load("assets/stat_down.png")
        tiles[-50] = image.load("assets/stat_up_dark.png")
        tiles[-51] = image.load("assets/stat_down_dark.png")

        # 200-299 player assets
        tiles[200] = image.load("assets/Player.png")
        tiles[-200] = image.load("assets/player_under_armor.png")
        tiles[201] = image.load("assets/player_boots.png")
        tiles[202] = image.load("assets/player_gloves.png")
        tiles[203] = image.load("assets/player_helmet.png")
        tiles[204] = image.load("assets/player_armor.png")
        tiles[210] = image.load("assets/items/gold.png")

        # 300-399 weapon assets
        tiles[300] = image.load("assets/items/weapons/basic_ax.png")
        tiles[303] = image.load("assets/items/weapons/bleeding_ax.png")
        tiles[301] = image.load("assets/items/weapons/hammer.png")
        tiles[302] = image.load("assets/items/weapons/crushing_hammer.png")
        tiles[321] = image.load("assets/items/weapons/dagger.png")
        tiles[322] = image.load("assets/items/weapons/screaming_dagger.png")
        tiles[331] = image.load("assets/items/weapons/burning_sword.png")
        tiles[332] = image.load("assets/items/weapons/magic_wand.png")
        tiles[340] = image.load("assets/items/weapons/sword.png")
        tiles[341] = image.load("assets/items/weapons/sleeping_sword.png")


        # 400-499 consumeables assets
        tiles[401] = image.load("assets/items/consumeables/health_orb_bigger.png")
        tiles[402] = image.load("assets/items/consumeables/mana_orb_bigger.png")
        tiles[403] = image.load("assets/items/consumeables/curing_orb_bigger.png")
        tiles[404] = image.load("assets/items/consumeables/might_orb_bigger.png")
        tiles[405] = image.load("assets/items/consumeables/haste_orb_bigger.png")

        # scroll assets
        tiles[450] = image.load("assets/items/consumeables/scroll.png")

        tiles[480] = image.load("assets/items/consumeables/book.png")

        # ring assets
        tiles[500] = image.load("assets/items/jewelry/green_ring_gold.png")
        tiles[501] = image.load("assets/items/jewelry/blood_ring.png")
        tiles[502] = image.load("assets/items/jewelry/blue_ring.png")
        tiles[503] = image.load("assets/items/jewelry/red_ring.png")
        tiles[504] = image.load("assets/items/jewelry/bone_ring.png")
        tiles[505] = image.load("assets/items/jewelry/ring_of_teleport.png")

        #amulet
        tiles[550] = image.load("assets/items/jewelry/amulet.png")

        # armor assets
        # list of armor: basic, leather, golden, warmonger, wizard robe
        tiles[600] = image.load("assets/items/armor/armor.png")
        tiles[601] = image.load("assets/items/armor/leather_armor.png")
        tiles[602] = image.load("assets/items/armor/golden_armor.png")
        tiles[603] = image.load("assets/items/armor/warmonger_armor.png")
        tiles[604] = image.load("assets/items/armor/wizard_robe.png")
        tiles[605] = image.load("assets/items/armor/karate_gi.png")
        tiles[606] = image.load("assets/items/armor/bloodstained_armor.png")

        # shield assets
        # list of shields: basic, aegis, tower, magic focus
        tiles[311] = image.load("assets/items/armor/shield.png")
        tiles[312] = image.load("assets/items/armor/aegis.png")
        tiles[313] = image.load("assets/items/armor/tower_shield.png")
        tiles[314] = image.load("assets/items/armor/magic_focus.png")

        # boots assets
        # list of boots: basic, escape
        tiles[700] = image.load("assets/items/armor/boots.png")
        tiles[701] = image.load("assets/items/armor/boots_of_escape.png")
        tiles[702] = image.load("assets/items/armor/blackened_boots.png")
        tiles[703] = image.load("assets/items/armor/assassin_boots.png")

        # gloves assets
        # list of gloves: basic, gauntlets
        tiles[750] = image.load("assets/items/armor/gloves.png")
        tiles[751] = image.load("assets/items/armor/gauntlets.png")
        tiles[752] = image.load("assets/items/armor/boxing_gloves.png")
        tiles[753] = image.load("assets/items/armor/healer_gloves.png")
        tiles[754] = image.load("assets/items/armor/lich_hand.png")

        # helmet assets
        tiles[770] = image.load("assets/items/armor/helmet.png")
        tiles[771] = image.load("assets/items/armor/viking_helmet.png")
        tiles[772] = image.load("assets/items/armor/spartan_helmet.png")
        tiles[773] = image.load("assets/items/armor/great_helm.png")
        tiles[774] = image.load("assets/items/armor/thief_hood.png")
        tiles[775] = image.load("assets/items/armor/wizard_hat.png")

        # empty equipment assets
        tiles[801] = image.load("assets/items/icons/empty_armor.png")
        tiles[802] = image.load("assets/items/icons/empty_boots.png")
        tiles[803] = image.load("assets/items/icons/empty_gloves.png")
        tiles[804] = image.load("assets/items/icons/empty_helmet.png")
        tiles[805] = image.load("assets/items/icons/empty_weapon.png")
        tiles[806] = image.load("assets/items/icons/empty_shield.png")
        tiles[807] = image.load("assets/items/icons/empty_ring.png")
        tiles[811] = image.load("assets/items/icons/empty_armor_open.png")
        tiles[812] = image.load("assets/items/icons/empty_boots_open.png")
        tiles[813] = image.load("assets/items/icons/empty_gloves_open.png")
        tiles[814] = image.load("assets/items/icons/empty_helmet_open.png")
        tiles[815] = image.load("assets/items/icons/empty_weapon_open.png")
        tiles[816] = image.load("assets/items/icons/empty_shield_open.png")
        tiles[817] = image.load("assets/items/icons/empty_ring_open.png")
        tiles[818] = image.load("assets/items/icons/empty_pants_open.png")
        tiles[819] = image.load("assets/items/icons/empty_pants.png")
        tiles[820] = image.load("assets/items/icons/empty_amulet_open.png")
        tiles[821] = image.load("assets/items/icons/empty_amulet.png")

        # skill assets
        tiles[901] = image.load("assets/target.png")
        tiles[902] = image.load("assets/placeholder_skill_icon.png")
        tiles[-902] = image.load("assets/placeholder_skill_icon.png")
        tiles[903] = image.load("assets/gun_skill_icon.png")
        tiles[-903] = image.load("assets/gun_skill_icon.png")
        tiles[904] = image.load("assets/BurningAttack_skill_icon.png")
        tiles[-904] = image.load("assets/BurningAttack_skill_icon_dark.png")
        tiles[905] = image.load("assets/MagicMissile_skill_icon.png")
        tiles[-905] = image.load("assets/MagicMissile_skill_icon_dark.png")
        tiles[906] = image.load("assets/Petrify_skill_icon.png")
        tiles[-906] = image.load("assets/Petrify_skill_icon_dark.png")
        tiles[907] = image.load("assets/ShrugOff_skill_icon.png")
        tiles[-907] = image.load("assets/ShrugOff_skill_icon_dark.png")
        tiles[908] = image.load("assets/Berserk_skill_icon.png")
        tiles[-908] = image.load("assets/Berserk_skill_icon_dark.png")
        tiles[909] = image.load("assets/BloodPact_skill_icon.png")
        tiles[-909] = image.load("assets/BloodPact_skill_icon_dark.png")
        tiles[910] = image.load("assets/Terrify_skill_icon.png")
        tiles[-910] = image.load("assets/Terrify_skill_icon_dark.png")
        tiles[911] = image.load("assets/Escape_skill_icon.png")
        tiles[-911] = image.load("assets/Escape_skill_icon_dark.png")
        tiles[912] = image.load("assets/Heal_skill_icon.png")
        tiles[-912] = image.load("assets/Heal_skill_icon_dark.png")
        tiles[913] = image.load("assets/Torment_skill_icon.png")
        tiles[-913] = image.load("assets/Torment_skill_icon_dark.png")
        tiles[914] = image.load("assets/teleport_skill_icon.png")
        tiles[-914] = image.load("assets/teleport_skill_icon_dark.png")
        tiles[915] = image.load("assets/invincible_skill_icon.png")
        tiles[-915] = image.load("assets/invincible_skill_icon_dark.png")

        tiles[100] = image.load("assets/items/armor/pants.png")
        tiles[110] = image.load("assets/shopkeeper.png")

        # 100-199 monster assets
        tiles[1000] = image.load('assets/monsters/goblin.png')
        tiles[1001] = image.load('assets/monsters/gorblin_shaman.png')
        tiles[1002] = image.load('assets/monsters/hobgoblin.png')
        tiles[1010] = image.load('assets/monsters/kobold.png')
        tiles[1020] = image.load('assets/monsters/gargoyle.png')
        tiles[1030] = image.load('assets/monsters/velociraptor.png')
        tiles[1040] = image.load('assets/monsters/minotaur.png')
        tiles[1050] = image.load('assets/monsters/tormentorb.png')
        tiles[1060] = image.load('assets/monsters/yendorb.png')
        tiles[1070] = image.load("assets/monsters/orc.png")
        tiles[1080] = image.load('assets/monsters/golem.png')
        tiles[1090] = image.load('assets/monsters/stumpy.png')
        tiles[1100] = image.load('assets/monsters/slime.png')
        tiles[161] = image.load('assets/yendorb_deactivated.png')

        tiles[199] = image.load('assets/monsters/monster_corpse.png')


        self.tiles = tiles

    def tile_string(self, key):
        return self.tiles[key]

class DungeonGenerator():
    #Generates a width by height 2d array of tiles. Each type of tile has a unique tile
    #tag ranging from 0 to 99
    def __init__(self, depth, player):
        self.mapData = MapOptions[depth]
        self.depth = depth
        self.width = self.mapData.width
        self.height = self.mapData.height
        self.summoner = []
        self.monster_map = TrackingMap(self.width, self.height) #Should I include items as well?
        self.flood_map = FloodMap(self, self.width, self.height)
        self.tile_map = TileMap(self.mapData, depth)
        self.item_map = TrackingMap(self.width, self.height)

        self.player = player
        self.summoner = []

        self.monster_dict = L.ID() #Unique to this floor
        self.item_dict = L.ID() #Unique to this floor
        self.npc_dict = L.ID()

        self.place_items(depth)
        self.place_monsters(depth)
        self.place_npcs(depth)


        """
        for x in range(self.width):
            self.tile_map.append([O.Tile(x, y, 1, False) for y in range(self.height)])
        maxtunnels = 40
        maxlength = 6
        currentx = random.randint(0, self.width - 1)
        currenty = random.randint(0,self.height - 1)
        tile = O.Tile(currentx, currenty, 0, True)
        self.tile_map[currentx][currenty] = tile
        carve_direction = (0,0)
        while maxtunnels > 0:
            xdelta, ydelta = self.random_direction(old = carve_direction)
            while (not self.in_map(currentx+xdelta, currenty + ydelta)):
                xdelta, ydelta = self.random_direction(old = carve_direction)
            carve_direction = (xdelta, ydelta)
            carve_length = random.randint(1,maxlength)
            while carve_length > 0 and self.in_map(currentx+xdelta, currenty + ydelta):
                currentx = currentx + xdelta
                currenty = currenty + ydelta
                tile = O.Tile(currentx, currenty, 0, True)
                self.tile_map[currentx][currenty] = tile
                carve_length -= 1
            maxtunnels -= 1
"""

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
        print(location)
        print(self.player.name)
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
       return x> 0 and x < self.width and y >0 and y < self.height


    def random_direction(self, old):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        new = (0,0)
        while new != old:
            ran = random.randint(0,3)
            new = directions[ran]
        return new


    """   
        rooms = R.roll_square_rooms(0, self.width, 3, 20, 0, self.height, 3, 20, 5)
        for room in rooms:
            startx = room[0]
            starty = room[1]
            length = room[2]
            depth = room[3]
            self.square_room(startx, starty, length, depth)

        rooms = R.roll_square_rooms(0, self.width, 1, 4, 0, self.height, 3, 20, 30)
        for room in rooms:
            startx1 = room[0]
            starty2 = room[1]
            length = room[2]
            depth = room[3]
            self.square_room(startx, starty, length, depth)
        
 #       self.square_room(startx, starty, startx1 - startx, 1)

        rooms = R.roll_square_rooms(0, self.width, 3, 20, 0, self.height, 1, 4, 30)
        for room in rooms:
            startx = room[0]
            starty = room[1]
            length = room[2]
            depth = room[3]
            self.square_room(startx, starty, length, depth)

"""
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
        startx = random.randint(0, self.width-1)
        starty = random.randint(0,self.height-1)

        check_on_stairs = self.on_stairs(startx, starty, self.tile_map.stairs)
        
        while ((self.tile_map.get_passable(startx, starty) == False) or 
               (self.monster_map.get_passable(startx, starty) == False) or
               (self.tile_map.track_map[startx][starty].visible) or
               check_on_stairs):
            startx = random.randint(0, self.width-1)
            starty = random.randint(0,self.height-1)
            check_on_stairs = self.on_stairs(startx, starty, self.tile_map.stairs)
        
        self.place_monster_at_location(creature, startx, starty)

    def place_monster_at_location(self, creature, x, y):
        creature.x = x
        creature.y = y
        self.monster_dict.tag_subject(creature)
        self.monster_map.place_thing(creature)

    def place_npcs(self, depth):
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)

        check_on_stairs = self.on_stairs(startx, starty, self.tile_map.stairs)

        while ((self.tile_map.get_passable(startx, starty) == False) or
               (self.monster_map.get_passable(startx, starty) == False) or
               (self.tile_map.track_map[startx][starty].visible) or
               check_on_stairs):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
            check_on_stairs = self.on_stairs(startx, starty, self.tile_map.stairs)

        npc = N.NPC(110, startx, starty)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for change in directions:
            if not self.tile_map.get_passable(startx + change[0], starty + change[1]):
                self.tile_map.track_map[startx + change[0]][starty + change[1]] = O.Tile(startx + change[0], starty + change[1], 2, True)

        self.npc_dict.tag_subject(npc)

    def place_items(self, depth):
        itemSpawns = Spawns.item_spawner.spawnItems(depth)
        first = True
        force_near_stairs = False
        for item in itemSpawns:
            if first and depth == 1:
                # manually force a weapon to spawn near the stairs on the first floor
                force_near_stairs = True
                first = False # only do so for first item
            self.place_item(item, force_near_stairs)
            force_near_stairs = False

    def on_stairs(self, x, y, stairs):
        for stair in stairs:
            if stair.x == x and stair.y == y:
                return True
        return False

    def place_item(self, item, force_near_stairs=False):
        startx = random.randint(0, self.width-1)
        starty = random.randint(0,self.height-1)

        # make sure the item is placed on a passable tile that does not already have an item and is not stairs
        check_on_stairs = self.on_stairs(startx, starty, self.tile_map.stairs)
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
                check_on_stairs = self.on_stairs(startx, starty, self.tile_map.stairs)
            
        item.x = startx
        item.y = starty

        self.item_dict.tag_subject(item)
        self.item_map.place_thing(item)

    def get_map(self):
        return self.tile_map


class Maps():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.track_map = [x[:] for x in [[-1] * self.width] * self.height]

    def locate(self, x, y):
        return self.track_map[x][y]

    def get_passable(self,x,y):
        if self.in_map(x,y):
            return (self.track_map[x][y] == -1)
        else:
            return False

    def in_map(self, x, y):
       return x> 0 and x < self.width and y >0 and y < self.height

"""
This map will either track items or monsters.
"""
class TrackingMap(Maps):
    def __init__(self, width, height):
        super().__init__(width, height)

    def place_thing(self, thing):
        self.track_map[thing.x][thing.y] = thing.id_tag

    def clear_location(self, x, y):
        self.track_map[x][y] = -1

    def __str__(self):
        allrows = ""
        for x in range(self.width):
            row = ' '.join(str(self.track_map[x][y].render_tag) for y in range(self.height))
            allrows = allrows + row + "\n"      
        return allrows

class FloodMap(Maps):
    def __init__(self, parent, width, height):
        super().__init__(width, height)
        self.flood_queue = []
        self.parent = parent

    def update_flood_map(self, location, search = False):
        self.track_map = [x[:] for x in [[-1] * self.width] * self.height]
        x, y = location
        self.flood_queue.append((x, y, 0, 0, 0))
        while len(self.flood_queue) > 0:
            return self.iterate_flood(search)

    def iterate_flood(self, search):
        x, y, xdelta, ydelta, count = self.flood_queue.pop(0)
        if (self.in_map(x + xdelta, y + ydelta) and self.track_map[x+xdelta][y+ydelta] == -1):
            self.track_map[x+xdelta][y+ydelta] = count
            if search == True and self.parent.track_map[x+xdelta][y+ydelta].visible and self.parent.get_passable((x+xdelta,y+ydelta)):
                return (x+xdelta,y+ydelta)
            options = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            r = random.randint(0, 3)
            for i in range(3):
                xdeltanew, ydeltanew = options[(r + i) % 4]
                if self.in_map(x + xdelta + xdeltanew, y + ydelta+ydeltanew) and (self.track_map[x+xdelta+xdeltanew][y+ydelta+ydeltanew] == -1):
                    self.flood_queue.append((x + xdelta, y+ydelta, xdeltanew, ydeltanew, count+1))

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
    def __init__(self, mapData, depth):
        super().__init__(mapData.width, mapData.height)
        self.mapData = mapData
        self.track_map = []
        self.stairs = []
        self.rooms = []
        # Add an empty map

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

        self.render_to_map(depth)
        self.place_stairs(depth)

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

    def get_tag(self, x, y):
        return self.track_map[x][y].render_tag

    def cellular_caves(self):
        iterations = 3
        self.track_map_render = [x[:] for x in [[0] * self.width] * self.height]
        survival_rate = 0.45
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                if (random.uniform(0,1) <= survival_rate):
                    self.track_map_render[x][y] = 1
        for i in range(iterations):
            self.iterate_cellular_map()

    def iterate_cellular_map(self):
        temp_track_map_render = [x[:] for x in [[0] * self.width] * self.height]
        birth_limit = 4
        death_limit = 3
        for x in range(1,self.width-1):
            for y in range(1,self.height-1):
                count = self.count_neighbors(x,y)
                if count >= birth_limit and self.track_map_render[x][y] == 0:
                    temp_track_map_render[x][y] = 1
                elif count <= death_limit and self.track_map_render[x][y] == 1:
                    temp_track_map_render[x][y] = 0
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
                elif self.track_map_render[neighbor_x][neighbor_y] == 1:
                    count += 1
        return count


    def render_to_map(self, depth):
        self.track_map = []
        for x in range(self.width):
            temp = []
            for y in range(self.height):
                if self.track_map_render[x][y] == 1:
                    if (depth >= CirclesBeginOn):
                        temp.append(O.Tile(x, y, 12, True))
                    else:
                        temp.append(O.Tile(x, y, 2, True))
                else:
                    if (depth >= CirclesBeginOn):
                        temp.append(O.Tile(x, y, 11, False))
                    else:
                        temp.append(O.Tile(x, y, 1, False))
                    
            self.track_map.append(temp)


    def carve_rooms(self):
        for x in range(self.width - 2):
            for y in range(self.height - 2):
                tile = O.Tile(x+1, y+1, 2, True)
                self.track_map[x+1][y+1] = tile

    def place_stairs(self, depth):
        if depth != 1:
            startx = random.randint(0, self.width-1)
            starty = random.randint(0,self.height-1)
            while (self.track_map[startx][starty].passable == False):
                startx = random.randint(0, self.width-1)
                starty = random.randint(0,self.height-1)
            tile = O.Stairs(startx, starty, 90, True, downward=False)
            self.track_map[startx][starty] = tile
            self.stairs.append(tile)
        if (depth < 10):
            for i in range(2):
                startx = random.randint(0, self.width - 1)
                starty = random.randint(0, self.height - 1)
                while (self.track_map[startx][starty].passable == False):
                    startx = random.randint(0, self.width - 1)
                    starty = random.randint(0, self.height - 1)
                tile = O.Stairs(startx, starty, 91, True, downward=True)
                self.track_map[startx][starty] = tile
                self.stairs.append(tile)
        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)
        while (self.track_map[startx][starty].passable == False and self.track_map[startx][starty].render_tag != 91):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
        tile = O.Stairs(startx, starty, 90, True, downward=False)
        self.track_map[startx][starty] = tile
        self.stairs.append(tile)

    def get_stairs(self):
        return self.stairs

    def place_tile(self, tile):
        self.track_map[tile.x][tile.y] = tile

    def get_passable(self, x, y):
        if (x>=0) & (y>=0) & (x < self.width) & (y < self.height):
            return (self.track_map[x][y].passable)
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
                    self.track_map_render[x + room.x][y + room.y] = 1


    def connect_rooms(self, room1, room2):
        cornerX : int = room1.GetCenterX()
        cornerY : int = room2.GetCenterY()

        lower1X = min(room1.GetCenterX(), cornerX)
        upper1X = max(room1.GetCenterX(), cornerX) + 1
        lower1Y = min(room1.GetCenterY(), cornerY)
        upper1Y = max(room1.GetCenterY(), cornerY) + 1

        for x in range(lower1X, upper1X):
            for y in range(lower1Y, upper1Y):
                self.track_map_render[x][y] = 1

        lower2X = min(room2.GetCenterX(), cornerX)
        upper2X = max(room2.GetCenterX(), cornerX) + 1
        lower2Y = min(room2.GetCenterY(), cornerY)
        upper2Y = max(room2.GetCenterY(), cornerY) + 1

        for x in range(lower2X, upper2X):
            for y in range(lower2Y, upper2Y):
                self.track_map_render[x][y] = 1

