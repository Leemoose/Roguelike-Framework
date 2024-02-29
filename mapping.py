from pygame import image
import dice as R
import objects as O
import loops as L
import items as I
import monster as Mon
import random
import math
from fractions import Fraction

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
    def __init__(self, textSize, colors):
        file = 'assets/P.png'
        player_image = image.load(file)
        tiles = {}
        tiles[1] = image.load("assets/basic_wall.png")
        tiles[-1] = image.load("assets/basic_wall.png")
        tiles[2] = image.load("assets/basic_floor.png")
        tiles[-2] = image.load("assets/basic_floor_shaded.png")
        tiles[90] = image.load("assets/stairs_up.png")
        tiles[-90] = image.load("assets/stairs_up.png")
        tiles[91] = image.load("assets/stairs_down.png")
        tiles[-91] = image.load("assets/stairs_down.png")
        tiles[200] = player_image
        tiles[101] = image.load("assets/orc.png")
        tiles[102] = image.load("assets/slime.png")
        tiles[103] = image.load('assets/floatingtentacles.png')
        tiles[104] = image.load('assets/gentleman_eyeball.png')
        tiles[105] = image.load('assets/stone_golem.png')
        tiles[300] = image.load("assets/basic_ax.png")
        tiles[301] = image.load("assets/hammer.png")
        tiles[901] = image.load("assets/target.png")
        self.tiles = tiles

    def tile_string(self, key):
        return self.tiles[key]

class DungeonGenerator():
    #Generates a width by height 2d array of tiles. Each type of tile has a unique tile
    #tag ranging from 0 to 99
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.monster_map = TrackingMap(width, height) #Should I include items as well?
        self.flood_map = FloodMap(width,height)
        self.tile_map = TileMap(width, height)
        self.item_map = TrackingMap(width,height)

        self.monster_dict = L.ID() #Unique to this floor
        self.item_dict = L.ID() #Unique to this floor

        self.place_items()
        self.place_monsters()


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



    def place_monsters(self):
        number_of_orcs = 1
        number_of_slimes = 0
        number_of_tentacles = 0
        number_of_eyeballs = 0
        number_of_stone_golems = 0
        self.place_monster_hoard(number_of_orcs, 101, 2)
        self.place_monster_hoard(number_of_slimes, 102, 1)
        self.place_monster_hoard(number_of_eyeballs, 104, 3) #Gentlman eyeballs
        self.place_monster_hoard(number_of_tentacles, 103, 5) #Floating tentacles
        self.place_monster_hoard(number_of_stone_golems, 105, 8)  # Floating tentacles

    def place_monster_hoard(self, number, render_tag, level):
        for i in range(number):
            startx = random.randint(0, self.width-1)
            starty = random.randint(0,self.height-1)

            while (self.tile_map.get_passable(startx, starty)== False):
                startx = random.randint(0, self.width-1)
                starty = random.randint(0,self.height-1)

            creature = Mon.Monster(render_tag, startx, starty)
            for i in range(level):
                creature.character.level_up()
            self.monster_dict.tag_subject(creature)
            self.monster_map.place_thing(creature)

    def place_items(self):
        number_of_axes = random.randint(5,10)
        number_of_hammers = random.randint(5, 10)
        self.place_item_hoard(number_of_axes, 300, "ax")
        self.place_item_hoard(number_of_hammers, 301, "hammer")

    def place_item_hoard(self, number, render_tag, weapon_type):
        for i in range(number):
            startx = random.randint(0, self.width-1)
            starty = random.randint(0,self.height-1)

            while (self.tile_map.get_passable(startx, starty)== False):
                startx = random.randint(0, self.width-1)
                starty = random.randint(0,self.height-1)

            if weapon_type == "ax":
                weapon = I.Ax(render_tag, True, startx, starty)
            elif weapon_type == "hammer":
                weapon = I.Hammer(render_tag, True, startx, starty)
            self.item_dict.tag_subject(weapon)
            self.item_map.place_thing(weapon)

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
        if (x>=0) & (y>=0) & (x < self.width) & (y < self.height):
            return (self.track_map[x][y] == -1)
        else:
            return False

    def in_map(self, x, y):
       return x> 0 and x < self.width and y >0 and y < self.height

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
    def __init__(self, width, height):
        super().__init__(width, height)
        self.flood_queue = []

    def update_flood_map(self, player):
        self.track_map = [x[:] for x in [[-1] * self.width] * self.height]
        playerx, playery = player.get_location()
        self.flood_queue.append((playerx, playery, 0, 0, 0))
        while len(self.flood_queue) > 0:
            self.iterate_flood()

    def iterate_flood(self):
        x, y, xdelta, ydelta, count = self.flood_queue.pop(0)
        if (self.in_map(x + xdelta, y + ydelta) and self.track_map[x+xdelta][y+ydelta] == -1):
            self.track_map[x+xdelta][y+ydelta] = count
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

class TileMap(TrackingMap):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.track_map = []
        self.stairs = []
        for x in range(self.width):
            self.track_map.append([O.Tile(x, y, 1, False) for y in range(self.height)])
        self.cellular_caves()
        self.render_to_map()
        self.place_stairs()

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


    def render_to_map(self):
        self.track_map = []
        for x in range(self.width):
            temp = []
            for y in range(self.height):
                if self.track_map_render[x][y] == 1:
                    temp.append(O.Tile(x, y, 2, True))
                else:
                    temp.append(O.Tile(x, y, 1, False))
            self.track_map.append(temp)


    def carve_rooms(self):
        for x in range(self.width - 2):
            for y in range(self.height - 2):
                tile = O.Tile(x+1, y+1, 2, True)
                self.track_map[x+1][y+1] = tile

    def place_stairs(self):
        startx = random.randint(0, self.width-1)
        starty = random.randint(0,self.height-1)
        while (self.track_map[startx][starty].passable == False):
            startx = random.randint(0, self.width-1)
            starty = random.randint(0,self.height-1)
        tile = O.Stairs(startx, starty, 91, True, downward=True)
        self.track_map[startx][starty] = tile
        self.stairs.append(tile)

        startx = random.randint(0, self.width - 1)
        starty = random.randint(0, self.height - 1)
        while (self.track_map[startx][starty].passable == False):
            startx = random.randint(0, self.width - 1)
            starty = random.randint(0, self.height - 1)
        tile = O.Stairs(startx, starty, 90, True, downward=False)
        self.track_map[startx][starty] = tile
        self.stairs.append(tile)

    def get_stairs(self):
        return self.stairs

    def place_tile(self, tfile):
        self.track_map[tile.x][tile.y] = tile

    def get_passable(self, x, y):
        if (x>=0) & (y>=0) & (x < self.width) & (y < self.height):
            return (self.track_map[x][y].passable)
        else:
            return False

    def mark_visible(self,x,y):
        self.track_map[x][y].seen = True

