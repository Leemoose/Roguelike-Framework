from .id import ID
from .maps import Maps
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