import objects as O
import character as C
import dice as R
import random
import skills as S


class Monster_AI():
    def __init__(self, parent):
        self.frontier = None
        self.is_awake = False
        self.parent = parent

    """
    Think it would be better to first rank each action depending on the circumstances with a number between 1-100 and 
    then pick the action that ranks the highest
    """
    def rank_actions(self, monster, monster_map, tile_map, flood_map, player, generated_maps, item_dict, loop):
        item_map = generated_maps.item_map
        max_utility = 0
        called_function = None

        utility = self.rank_combat(player)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_combat(player)
        """
        elif item_map.locate(monsterx, monstery) != -1:
            item_key = item_map.locate(monsterx, monstery)
            monster.character.grab(item_key, item_dict, generated_maps, loop)
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if monster.character.main_weapon == None and item.equipable:
                    monster.character.equip(item)
                    break
                elif monster.character.health < monster.character.max_health and item.consumeable:
                    pass #monster.character.quaff(item)
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
            monster.move(xmove, ymove, tile_map, monster, monster_map, player)
            monster.character.energy = 0
        """
        if called_function != None:
            called_function(player)

    def rank_combat(self, player):
        playerx, playery = player.get_location()
        monster = self.parent
        monsterx, monstery = monster.get_location()
        distance = self.parent.get_distance(playerx, playery)
        if distance < 1.5:
            return 90
        else:
            return -1

    def do_combat(self, player):
        monster = self.parent
        monster.character.melee(player)
        monster.character.energy -= 100


class Monster(O.Objects):
    def __init__(self, number_tag, x, y):
        super().__init__(x, y, 0, number_tag, "Unknown monster")
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.skills = S.Skills(self)
        self.experience_given = 10

    def move(self, move_x, move_y, floormap, monster, monster_map, player):
        speed = 100
        if floormap.get_passable(monster.x + move_x, monster.y + move_y) and monster_map.get_passable(monster.x + move_x, monster.y + move_y) and (monster.x + move_x != player.x and monster.y + move_y != player.y):
            self.character.energy -= 100
            monster_map.track_map[monster.x][monster.y] = -1
            monster.y += move_y
            monster.x += move_x
            monster_map.track_map[monster.x][monster.y] = monster.id_tag
