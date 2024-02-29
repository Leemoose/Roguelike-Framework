import objects as O
import character as C
import dice as R
import random


class Monster_AI():
    def __init__(self):
        self.frontier = None
        self.is_awake = False

    def rank_actions(self, monster, monster_map, tile_map, flood_map, player, generated_maps, item_dict, loop):
        item_map = generated_maps.item_map
        playerx, playery = player.get_location()
        monsterx, monstery = monster.get_location()
        distance = monster.get_distance(playerx, playery)
        if distance < 1.5:
            monster.character.melee(player)
            monster.character.energy -= 100
        elif item_map.locate(monsterx, monstery) != -1:
            item_key = item_map.locate(monsterx, monstery)
            monster.character.grab(item_key, item_dict, generated_maps, loop)
            monster.character.equip(monster.character.inventory[0])
        else:
            options = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            r = random.randint(0, 3)
            xmove = 0
            ymove = 0
            flood_count = 100
            for i in range(3):
                xdelta, ydelta = options[(r + i) % 4]
                if tile_map.get_passable(monsterx+xdelta,monstery+ydelta):
                    if flood_count > flood_map.track_map[monsterx+xdelta][monstery+ydelta]:
                        flood_count = flood_map.track_map[monsterx+xdelta][monstery+ydelta]
                        xmove = xdelta
                        ymove = ydelta
            monster.move(xmove, ymove, tile_map, monster, monster_map)
            monster.character.energy = 0


class Monster(O.Objects):
    def __init__(self, number_tag, x, y):
        super().__init__(x, y, 0, number_tag, "Unknown monster")
        self.character = C.Character(self)
        self.brain = Monster_AI()
        self.experience_given = 10

    def move(self, move_x, move_y, floormap, monster, monster_map):
        speed = 100
        if floormap.get_passable(monster.x + move_x, monster.y + move_y) and monster_map.get_passable(monster.x + move_x, monster.y + move_y):
            self.character.energy -= 100
            monster_map.track_map[monster.x][monster.y] = -1
            monster.y += move_y
            monster.x += move_x
            monster_map.track_map[monster.x][monster.y] = monster.id_tag
