

def throneify(startx, starty, render_tile_map, width, height):
    height = min(height, len(render_tile_map[0]) - starty)
    width = min(width, len(render_tile_map) - startx)
    print(width, height)

    for x in range(width):
        for y in range(height):
            if x == startx or y == starty or x == startx + width - 1 or y == starty + height - 1:
                render_tile_map[startx + x][starty + y] = "x"
            else:
                render_tile_map[startx + x][starty + y] = "."

    if width > 10:
        for x in range(width):
            for y in range(height):
                if ((x == 3 or x == width - 5) and y % 4 == 2):
                    pillerify(render_tile_map, x, y)

    midpoint = width // 2
    top = height // 6
    bottom = height * 5 // 6
    render_tile_map[midpoint][top] = ">"
    render_tile_map[midpoint][top - 1] = "K"
    render_tile_map[midpoint][bottom] = "<"

    return render_tile_map



def pillerify(room, startx, starty):
    for row in range(2):
        for col in range(2):
            if startx + row < len(room)-1 and starty + col <len(room[row])-1:
                room[startx + row][starty + col] = "x"
