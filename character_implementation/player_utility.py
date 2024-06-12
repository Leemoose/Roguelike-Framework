
def talk(player, loop, input_direction=None):
    spoke = False
    if input_direction == None:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    else:
        directions = [input_direction]
    location = []
    for x, y in directions:
        location.append((x + player.x, y + player.y))
        if loop.generator.interact_map.locate(x + player.x, y + player.y) != -1:
            loop.add_message("You say hello to your friendly neighbor.")
            loop.generator.interact_map.locate(x + player.x, y + player.y).welcome(loop)
            spoke = True
            loop.change_loop("trade")

    if spoke == False:
        loop.add_message("You feel lonely.")