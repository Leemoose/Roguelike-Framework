import random

def throneify(startx, starty, render_tile_map, image_map, width, height):
    height = min(height, len(render_tile_map[0]) - starty)
    width = min(width, len(render_tile_map) - startx)
    print(width, height)
    midpoint = width // 2
    top = height // 6
    bottom = height * 5 // 6

    for x in range(width):
        for y in range(height):
            if x == startx or y == starty or x == startx + width - 1 or y == starty + height - 1:
                render_tile_map[startx + x][starty + y] = "x"
            else:
                render_tile_map[startx + x][starty + y] = "."

    placed_brother = False
    if width > 10:
        for x in range(width):
            for y in range(height):
                if ((x == 3 or x == width - 5) and y % 4 == 2):
                    pillerify(render_tile_map, x, y)
            for y in range(height):
                if (x == 4 or x == width - 5) and y > 3 and y < height - 3 and render_tile_map[x][y] != "x":
                    if placed_brother == False and random.random() > .9:
                        render_tile_map[x][y] = "BB"
                        placed_brother = True
                    else:
                        render_tile_map[x][y] = "G"
                elif (x == 4 or x == width - 5) and (y <= 3 or y >= height - 3) and render_tile_map[x][y] != "x":
                    render_tile_map[x][y] = "d"
    render_tile_map[midpoint][top] = "g"
    render_tile_map[midpoint][top + 1] = "K"
    render_tile_map[midpoint][bottom] = "<"

    for y in range(height):
        if y > top and y < bottom and render_tile_map[x][y] == ".":
            image_map[midpoint][y] = 5

    return render_tile_map



def pillerify(room, startx, starty):
    for row in range(2):
        for col in range(2):
            if startx + row < len(room)-1 and starty + col <len(room[row])-1:
                room[startx + row][starty + col] = "x"

def dojoify(room, render_map, image, depth):
    for row in range(room.x, room.x + room.width):
        for col in range(room.y, room.y + room.height):
            image[row][col] = 6
    
    midpoint = (room.x + room.width // 2, room.y + room.height // 2)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    rand_direction = random.choice(directions)
    dummypoint = (midpoint[0] + rand_direction[0], midpoint[1] + rand_direction[1])

    render_map[midpoint[0]][midpoint[1]] = "S"
    render_map[dummypoint[0]][dummypoint[1]] = "D"

    if depth == 2:
        outpit = ""
        for row in render_map:
            outpit += "".join(row) + "\n"
        print(outpit)

    return render_map

def hubify(startx, starty, render_tile_map, image_map, width, height):
    height = min(height, len(render_tile_map[0]) - starty)
    width = min(width, len(render_tile_map) - startx)
    print(width, height)

    for x in range(width):
        for y in range(height):
            if x == startx or y == starty or x == startx + width - 1 or y == starty + height - 1:
                render_tile_map[startx + x][starty + y] = "x"
            else:
                render_tile_map[startx + x][starty + y] = "."

    right = width - 2
    top = height - 2
    for i in range(3):
        render_tile_map[right][top-i] = "g"

    render_tile_map[1][1] = "g"
    render_tile_map[1][2] = "A"
    return render_tile_map