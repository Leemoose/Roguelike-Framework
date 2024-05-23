import objects as O
import character as C
import random
import loops as L
import pathfinding
import spell
import tiles as T
import skills as S
import statistics
import shadowcasting


class Player(O.Objects):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 200, "Player")
        self.character = C.Character(self, mana=50)
        self.mage = spell.Mage(self)
        self.statistics = statistics.StatTracker()

        self.level = 1
        self.max_level = 20
        self.experience = 0
        self.experience_to_next_level = 20

        self.stat_points = 0
        self.stat_decisions = [0, 0, 0, 0]  # used at loop levelling to allocate points

        self.path = []

        self.invincible = True

        self.type = {
                     "humanoid": True
                     }

        self.quests = []
        self.quest_recieved = False

        if self.invincible:  # only get the gun if you're invincible at the start
            self.mage.known_spells.extend([
                S.Gun(self),  # 1
                spell.HypnosisSchool().Charm(self), # 2
                # S.BlinkStrike(self, cooldown=0, cost=10, damage=25, range=10, action_cost=1), # 3
                #spell.SummonGargoyle(self), # 2
                S.BurningAttack(self, cooldown=0, cost=10, damage=20, burn_damage=10, burn_duration=10, range=10),  # 2
                # S.Petrify(self, cooldown=0, cost=10, duration=3, activation_chance=1, range=10), #3
                # S.ShrugOff(self, cooldown=0, cost=10, activation_chance=1.0, action_cost=1), #4
                # S.Berserk(self, cooldown=0, cost=10, activation_threshold=50, strength_increase=10, action_cost=1), #5
                # S.Terrify(self, cooldown=0, cost=0, duration=5, activation_chance=1, range=15), #6
                # S.Escape(self, cooldown=0, cost=0, self_fear=False, activation_threshold=1.1, action_cost=1) #7
            ])
    def gain_experience(self, experience):
        self.experience += experience
        self.check_for_levelup()

    def attack_move(self, move_x, move_y, loop):
        if not self.character.movable:
            self.character.energy -= self.character.action_costs[
                "move"]  # (self.character.move_cost - int(self.character.dexterity + self.character.round_bonus()))
            loop.add_message("The player is petrified and cannot move.")
            return
        x = self.x + move_x
        y = self.y + move_y
        if (x >= 0) & (y >= 0) & (x < loop.generator.tile_map.width) & (y < loop.generator.tile_map.height):
            if loop.generator.get_passable((x, y)):
                self.move(move_x, move_y, loop)
            elif not loop.generator.monster_map.get_passable(x, y):
                defender = loop.monster_map.locate(x,y)
                self.attack(defender, loop)
            else:
                loop.add_message("You cannot move there")

    def move(self, move_x, move_y, loop):
        if loop.generator.get_passable((self.x + move_x, self.y + move_y)):
            self.character.energy -= self.character.action_costs[
                "move"]  # / (1.02**(self.character.dexterity + self.character.round_bonus())))
            self.y += move_y
            self.x += move_x
            loop.add_message("The player moved.")
        else:
            loop.add_message("You can't move there")

    def random_move(self, loop):
        random_move = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        rand_i = random.randint(0, 3)
        move_x, move_y = random_move[rand_i]
        self.move(move_x, move_y, loop)

    def attack(self, defender, loop):
        self.character.energy -= self.character.action_costs[
            "attack"]  # / (1.05**(self.character.dexterity + self.character.round_bonus())))
        loop.screen_focus = (defender.x, defender.y)
        damage = self.character.melee(defender, loop)
        loop.add_message(f"The player attacked for {damage} damage")

    def autoexplore(self, loop):
        all_seen = False
        if self.character.needs_rest():
            self.character.rest(loop, loop.currentLoop)
        tile_map = loop.generator.tile_map
        for monster in loop.generator.monster_map.all_entities():
            monster_loc = monster.get_location()
            if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible and monster.stops_autoexplore:
                loop.add_message("You cannot autoexplore while enemies are visible.")
                loop.change_loop(L.LoopType.action)
                return False
        while len(self.path) <= 1:
            start = (self.x, self.y)
            all_seen, unseen = loop.generator.all_seen()
            if all_seen:
                loop.change_loop(L.LoopType.action)
                loop.update_screen = True
                return False
            endx = unseen[0]
            endy = unseen[1]
            while (not tile_map.get_passable(endx, endy)) and not (tile_map.track_map[endx][endy].seen):
                if self.x == endx and self.y == endy:
                    loop.change_loop(L.LoopType.action)
                    return
                if endx != tile_map.width - 1:
                    endx += 1
                else:
                    endx = 0
                    if endy == tile_map.height - 1:
                        endy = 0
                    else:
                        endy += 1
            end = (endx, endy)
            self.path = pathfinding.astar_multi_goal(tile_map.track_map, start, loop.generator.get_all_frontier_tiles(),
                                                     loop.generator.monster_map, loop.player)
            # if all tiles have been seen don't autoexplore

        x, y = self.path.pop(0)
        if (x == self.x and y == self.y):
            # Pathfinding messed up - pop this just in case
            x, y = self.path.pop(0)
        self.move(x - self.x, y - self.y, loop)
        loop.update_screen = True

        self.character.energy = 0
        if not all_seen:
            shadowcasting.compute_fov(loop)
            self.autoexplore(loop)
        return True

    def find_stairs(self, loop):
        tile_map = loop.generator.tile_map
        for monster in loop.generator.monster_map.all_entities():
            monster_loc = monster.get_location()
            if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible and monster.stops_autoexplore:
                loop.add_message("You cannot autoexplore while enemies are tracking you.")
                loop.change_loop(L.LoopType.action)
                return

        start = (self.x, self.y)
        end = None
        for stairs in loop.generator.tile_map.get_stairs():
            if stairs.downward and stairs.seen:
                end = stairs.get_location()
        if end == None:
            loop.add_message("You have not found the stairs yet")
            return
        if (start == end):
            return
        self.path = pathfinding.astar(tile_map.track_map, start, end, loop.generator.monster_map, loop.player)

        x, y = self.path.pop(0)
        while len(self.path) > 0:
            x, y = self.path.pop(0)
            self.move(x - self.x, y - self.y, loop)
            shadowcasting.compute_fov(loop)
            for monster in loop.generator.monster_map.all_entities():
                monster_loc = monster.get_location()
                if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible and monster.stops_autoexplore:
                    loop.add_message("You cannot autoexplore while enemies are tracking you.")
                    loop.change_loop(L.LoopType.action)
                    return
        loop.update_screen = True

        self.character.energy = 0

    def check_for_levelup(self):
        while self.level != self.max_level and self.experience >= self.experience_to_next_level:
            self.level += 1
            self.character.level_up_max_health_and_mana()
            self.stat_points += 2
            exp_taken = self.experience_to_next_level
            self.experience_to_next_level += 20 + self.experience_to_next_level // 4
            self.experience -= exp_taken

    def modify_stat_decisions(self, i, increase=True):  # 0 = strength, 1 = dexterity, 2 = endurance, 3 = intelligence
        if increase:
            if self.stat_points > sum(self.stat_decisions):
                self.stat_decisions[i] += 1
        else:
            if self.stat_decisions[i] > 0:
                self.stat_decisions[i] -= 1

    def apply_level_up(self):
        self.character.level_up_stats(self.stat_decisions[0], self.stat_decisions[1], self.stat_decisions[2],
                                      self.stat_decisions[3])
        self.stat_points -= sum(self.stat_decisions)
        self.stat_decisions = [0, 0, 0, 0]

    def smart_attack(self, loop):
        """
        1. Get all visible monsters
        2. Get monster closest to us
        3. Get monster with lowest health and attack
        """
        attack_target = None
        distance = 1000

        tile_map = loop.generator.tile_map
        for monster in loop.generator.monster_map.all_entities():
            monster_x, monster_y = monster.get_location()
            if tile_map.locate(monster_x, monster_y).visible:
                new_distance = self.get_distance(monster_x, monster_y)
                if new_distance < distance:
                    attack_target = monster
                    distance = new_distance
                elif new_distance == distance:
                    if attack_target.character.health > monster.character.health:
                        attack_target = monster
        if attack_target != None:
            if distance <= 1.5:
                self.attack(attack_target, loop)
            else:
                path = pathfinding.astar(tile_map.track_map, self.get_location(), attack_target.get_location(),
                                         loop.generator.monster_map, self)
                path.pop(0)
                x, y = path[0]
                playerx, playery = self.get_location()
                self.move(x - playerx, y - playery, loop)

    def down_stairs(self, loop):
        if (isinstance(loop.generator.tile_map.track_map[self.x][self.y], T.Stairs)
                and loop.generator.tile_map.track_map[self.x][self.y].downward and self.character.movable):
            self.character.energy -= self.character.action_costs["move"]
            loop.down_floor()
        elif self.character.movable:
            loop.add_message("There are no stairs here!")
        else:
            self.character.energy -= self.character.action_costs["move"]
            loop.add_message("You can't move!")

    def up_stairs(self, loop):
        if (isinstance(loop.generator.tile_map.track_map[self.x][self.y], T.Stairs)
                and not loop.generator.tile_map.track_map[self.x][self.y].downward and self.character.movable):
            self.character.energy -= self.character.action_costs["move"]
            loop.up_floor()
        elif self.character.movable:
            loop.add_message("There are no stairs here!")
        else:
            self.character.energy -= self.character.action_costs["move"]
            loop.add_message("You can't move!")

    def talk(self, loop):
        spoke = False
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        location = []
        for x, y in directions:
            location.append((x + self.x, y + self.y))
        for key in loop.generator.npc_dict.subjects:
            npc = loop.generator.npc_dict.get_subject(key)
            for spot in location:
                if spot == npc.get_location():
                    loop.add_message("You say hello to your friendly neighbor.")
                    npc.welcome(loop)
                    spoke = True
                    loop.change_loop(L.LoopType.trade)
        if spoke == False:
            loop.add_message("You feel lonely.")

    def cast_spell(self, *args):
        self.mage.cast_spell(*args)

    def add_quest(self, quest):
        self.quests.append(quest)
        self.quest_recieved = True







