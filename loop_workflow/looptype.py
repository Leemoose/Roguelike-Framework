from enum import Enum

class LoopType(Enum):
    none = -1
    action = 0
    spell = 1
    inventory = 2
    equipment = 3
    main = 4
    race = 5
    classes = 6
    items = 7
    examine = 8
    trade = 9
    paused = 10
    targeting = 11
    specific_examine = 12
    enchant = 13
    quest = 14
    level_up = 15
    victory = 16
    help = 17
    death = 18
    story = 19
    resting = 20
    exploring = 21
    stairs = 22
    binding = 23
    spell_individual = 24