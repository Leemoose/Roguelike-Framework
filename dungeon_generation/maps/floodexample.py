from dungeon_generation import mapping
import random
import tiles as T

class FloodMap(mapping.Maps):
    def __init__(self, map, width, height):
        super().__init__(width, height)
        self.flood_queue = []
        self.track_map = [x[:] for x in [[-1] * self.height] * self.width]
        self.map = map

    def update_flood_map(self, location, search=False, reset=False):
        if reset:
            self.track_map = [x[:] for x in [[-1] * self.height] * self.width]
        x, y = location
        self.flood_queue.append((x, y, 0, 0, 0))
        self.iterate_flood(search)

    def iterate_flood(self, search = False):
        x, y, xdelta, ydelta, count = self.flood_queue.pop(0)
        if (self.in_map(x + xdelta, y + ydelta) and self.track_map[x + xdelta][y + ydelta] == -1 and self.map[x+xdelta][y+ydelta].is_passable()):
            self.track_map[x + xdelta][y + ydelta] = count
            options = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            r = random.randint(0, 3)
            for i in range(4):
                xdeltanew, ydeltanew = options[(r + i) % 4]
                if self.in_map(x + xdelta + xdeltanew, y + ydelta + ydeltanew) and (
                        self.track_map[x + xdelta + xdeltanew][y + ydelta + ydeltanew] == -1):
                    self.flood_queue.append((x + xdelta, y + ydelta, xdeltanew, ydeltanew, count + 1))
        if len(self.flood_queue) > 0:
            self.iterate_flood()

    def __str__(self):
        allrows = ""
        for x in range(self.width):
            row = ' '.join(str(self.track_map[x][y]) for y in range(self.height))
            allrows = allrows + row + "\n"
        return allrows

width = 5
height = 10
map = [x[:] for x in [[-1] * height] * width]
for x in range(width):
    for y in range(height):
        if x == 0 or x == width -1 or x == 2 or y == 0 or y ==height - 1:
            map[x][y] = T.Wall(x,y)
        else:
            map[x][y] = T.Floor(x,y)

flood_map = FloodMap(map, width, height)
flood_map.update_flood_map((1,1))
print(flood_map)

allrows = ""
for x in range(width):
    row = ' '.join(str(map[x][y]) for y in range(height))
    allrows = allrows + row + "\n"
print(allrows)