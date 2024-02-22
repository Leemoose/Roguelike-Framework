import shadowcasting
import objects as O
# Minimal shadowcasting example


map_str = '''
##################
#................#
##################
#................#
#................#
#................#
##################
'''[1:] # Use [1:] to remove first newline

width = 18
height = 7
player_location = (9, 3)

map_list = list(map_str.splitlines())

tile_map = []
for x in range(width):
    temp = []
    for y in range(height):
        if y == 2 or x == 0 or y == 0 or x == width-1 or y == height-1:
            temp.append(O.Tile(x, y, 0, False))
        else:
            temp.append(O.Tile(x, y, 1, True))
    tile_map.append(temp)


def is_blocking(x, y):
    return not tile_map[x][y].passable

is_visible = set()
def reveal(x, y):
    tile_map[x][y].seen = True

shadowcasting.compute_fov(player_location, is_blocking, reveal, tile_map)


for y in range(height):
    for x in range(width):
        if (x, y) == player_location:
            print('@', end='')
        elif not tile_map[x][y].seen:
            print(' ', end='')
        elif tile_map[x][y].passable:
            print('.', end='')
        else:
            print('#', end='')
    print()

'''
for y in range(height):
    for x in range(width):
        if (x, y) == player_location:
            print('@', end='')
        elif (x, y) in is_visible:
            print(map_list[y][x], end='')
        else:
            print(' ', end='')
    print()
'''