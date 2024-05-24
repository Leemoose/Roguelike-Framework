class Room():
    def __init__(self, x: int, y: int, width: int, height: int):
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