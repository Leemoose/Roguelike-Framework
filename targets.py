

class Target:
    def __init__(self):
        self.target_list= []

    def start_target(self, starting_target):
        self.target_list = [starting_target]

    def adjust(self, xdelta, ydelta):
        x, y = self.target_list[0]
        self.target_list[0] = (x+xdelta, y + ydelta)
