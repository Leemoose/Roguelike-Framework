import random

def roll_dice(min_val, max_val, number = 1):
    dice = []
    for i in range(number):
        dice.append(random.randint(min_val, max_val))
    return dice

def roll_square_rooms(min_x, max_x, min_width, max_width, min_y, max_y, min_height, max_height, number = 1):
    rooms = []
    for i in range(number):
        width = roll_dice(min_width, max_width)[0]
        height = roll_dice(min_height, max_height)[0]
        start_x = roll_dice(min_x, max_x - width)[0]
        start_y = roll_dice(min_y, max_y - height)[0]
        rooms.append((start_x, start_y, width, height))
    return rooms
