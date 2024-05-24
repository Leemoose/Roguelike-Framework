
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