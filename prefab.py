
width = 10
height = 15
room = [x[:] for x in [[0] * width] * height]

def throneify(startx, starty, render_tile_map, monster_map, npc_map, item_map, width = 10, height = 10):
    width = min(width, len(render_tile_map) - startx)
    height = min(height, len(render_tile_map[0]) - starty)

    for x in range(width):
        for y in range(height):
            if x == 0 or y == 0 or x == width-1 or y == height-1:
                render_tile_map[startx + x][starty + y] = "."
            else:
                render_tile_map[startx + x][starty + y] = "."

    #for x in range(len(render_tile_map) - 1):
    #    for y in range(len(render_tile_map[x]) - 1):
    #        if (x == 3 or x == len(room)-5) and y % 4 == 2:
    #            pillerify(render_tile_map, x, y)

    midpoint = width // 2
    bottom = height // 4
    top = height * 3 // 4
    render_tile_map[2][2] = "sd"
    render_tile_map[2][3] = "su"

    return render_tile_map



def pillerify(room, startx, starty):
    for row in range(2):
        for col in range(2):
            if startx + row < len(room)-1 and starty + col <len(room[row])-1:
                room[startx + row][starty + col] = "x"

