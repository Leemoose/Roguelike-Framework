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
        called_function = self.do_nothing

        utility = self.rank_combat(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_combat

        utility = self.rank_pickup(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_item_pickup

        utility = self.rank_equip_item(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_equip

        utility = self.rank_use_consumeable(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_use_consumeable

        utility = self.rank_move(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_move

        utility = self.rank_skill(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_skill

        print(max_utility)
        called_function(loop)


    def rank_combat(self, loop):
        player=loop.player
        playerx, playery = player.get_location()
        monster = self.parent
        monsterx, monstery = monster.get_location()
        distance = self.parent.get_distance(playerx, playery)
        if distance < 1.5:
            return 75
        else:
            return -1

    def rank_pickup(self, loop):
        item_map = loop.generator.item_map
        monster = self.parent
        if item_map.locate(monster.x, monster.y) != -1:
            return 60
        else:
            return -1

    def rank_equip_item(self, loop):
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.equipable and monster.character.main_weapon == None:
                    return 80
        return -1

    def rank_use_consumeable(self, loop):
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable:
                    return 30
        return -1

    def rank_move(self, loop):
        return 20
    
    def rank_skill(self, loop):
        for skill in self.parent.skills:
            if skill.castable(loop):
                return 150
        return -1        


    def do_item_pickup(self, loop):
        item_map = loop.generator.item_map
        item_dict = loop.generator.item_dict
        generated_maps = loop.generator
        monster = self.parent
        item_key = item_map.locate(monster.x, monster.y)
        monster.character.grab(item_key, item_dict, generated_maps, loop)

    def do_combat(self, loop):
        player=loop.player
        monster = self.parent
        damage = monster.character.melee(player)
        monster.character.energy -= 100
        loop.add_message(f"{monster} attacked you for {damage} damage")

    def do_skill(self, loop):
        monster = self.parent
        for skill in monster.skills:
            if skill.castable(loop):
                skill.try_to_activate(loop.player, loop.generator, loop)
                monster.character.energy -= 100
                loop.add_message(str(monster) + " used " + str(skill) + "!")
                break

    def do_equip(self, loop):
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if monster.character.main_weapon == None and item.equipable:
                    monster.character.equip(item)

    def do_use_consumeable(self, loop):
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable:
                    item.activate(monster.character)

    def do_move(self, loop):
        tile_map = loop.generator.tile_map
        monster = self.parent
        monsterx, monstery = monster.x, monster.y
        flood_map = loop.generator.flood_map
        monster_map = loop.monster_map
        player = loop.player

        options = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        r = random.randint(0, 3)
        xmove = 0
        ymove = 0
        flood_count = 100
        for i in range(3):
            xdelta, ydelta = options[(r + i) % 4]
            if tile_map.get_passable(monsterx + xdelta, monstery + ydelta):
                if flood_count > flood_map.track_map[monsterx + xdelta][monstery + ydelta]:
                    flood_count = flood_map.track_map[monsterx + xdelta][monstery + ydelta]
                    xmove = xdelta
                    ymove = ydelta
        monster.move(xmove, ymove, tile_map, monster, monster_map, player)
        monster.character.energy -= 100

    def do_nothing(self,loop):
        pass



class Monster(O.Objects):
    def __init__(self, number_tag, x, y, name="Unknown monster"):
        super().__init__(x, y, 0, number_tag, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.skills = []
        self.experience_given = 10

    def move(self, move_x, move_y, floormap, monster, monster_map, player):
        speed = 100
        if floormap.get_passable(monster.x + move_x, monster.y + move_y) and monster_map.get_passable(monster.x + move_x, monster.y + move_y) and (monster.x + move_x != player.x and monster.y + move_y != player.y):
            self.character.energy -= 100
            monster_map.track_map[monster.x][monster.y] = -1
            monster.y += move_y
            monster.x += move_x
            monster_map.track_map[monster.x][monster.y] = monster.id_tag
    
    def __str__(self):
        return self.name

class Kobold(Monster):
    def __init__(self, x, y):
        super().__init__(107, x, y, "Kobold")
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.skills = []
        self.skills.append(S.BurningAttack(self, 10, 0, 10, 5, 5))
        self.experience_given = 10
    
    def move(self, move_x, move_y, floormap, monster, monster_map, player):
        speed = 100
        if floormap.get_passable(monster.x + move_x, monster.y + move_y) and monster_map.get_passable(monster.x + move_x, monster.y + move_y) and (monster.x + move_x != player.x and monster.y + move_y != player.y):
            self.character.energy -= 100
            monster_map.track_map[monster.x][monster.y] = -1
            monster.y += move_y
            monster.x += move_x
            monster_map.track_map[monster.x][monster.y] = monster.id_tag
