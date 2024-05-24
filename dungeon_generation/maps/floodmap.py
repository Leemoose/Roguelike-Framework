from .maps import Maps
import random

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
