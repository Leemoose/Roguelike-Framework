import random


def create_castle(render_tile_map, image_map, width, height):
    throneheight = height // 3
    render_tile_map = throneify(0, 0, render_tile_map, image_map, width, throneheight)
    midpoint = width // 2
    render_tile_map[midpoint][throneheight-1] = "d"
    for y in range(throneheight, height):
        render_tile_map[midpoint][y] = "."
    render_tile_map = create_grab_tutorial(0, throneheight + 2, midpoint - 1, 10, render_tile_map, image_map)
    return render_tile_map

def create_grab_tutorial(startx, starty, width, height, render_tile_map, image_map):
    for x in range(startx, startx+ width):
        for y in range(starty, starty + height):
            render_tile_map[x][y] = "."
    render_tile_map[width-1][starty + height // 2] = "."
    render_tile_map[width][starty + height // 2] = "d"
    render_tile_map[width - 1][starty + height // 2 - 1] = "GE"
    render_tile_map[startx + (width) //2][(starty) + height // 2] = "bs"
    return render_tile_map


def throneify(startx, starty, render_tile_map, image_map, width, height):
    height = min(height, len(render_tile_map[0]) - starty)
    width = min(width, len(render_tile_map) - startx)
    print(width, height)
    midpoint = startx + width // 2
    top = starty + height // 6
    bottom = starty + height * 5 // 6

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
                    pillerify(render_tile_map, startx+x, starty+y)
            for y in range(height):
                if (x == 4 or x  == width - 5) and y > 3 and y < height - 3 and render_tile_map[startx+x][starty+ y] != "x":
                    if placed_brother == False and random.random() > .9:
                        render_tile_map[startx+x][starty+ y] = "BB"
                        placed_brother = True
                    else:
                        render_tile_map[startx+x][starty+ y]  = "G"
                elif (x == 4 or x == width - 5) and (y <= 3 or y >= height - 3) and render_tile_map[startx+x][starty+ y] != "x":
                    render_tile_map[startx+x][starty+ y] = "d"
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

# list of prefabs not tied to specific full floors but overwrite random rooms
random_prefabs_list = [
            # dojo (sensei quest)
            {"prefab": dojoify,
             "min_floor": 2,
             "max_floor": 5,
             "spawns_available": 1,
             # not sure if there will be prefabs we want to spawn multiple times through dungeon but left it as a possibility
             "spawn_chance": 0.5, 
             "branch": "Dungeon"}
        ]