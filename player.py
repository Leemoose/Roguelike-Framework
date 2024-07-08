from objects import Objects
from character_implementation import character as C, statistics, Body, Fighter
import random
import loops as L
from navigation_utility import pathfinding
import tiles as T
import skills as S
from spell_implementation import Mage
from loop_workflow import LoopType
from character_implementation import Inventory
import items as I



class Player(Objects):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 200, "Player")
        self.character = C.Character(self, mana=50)
        self.mage = Mage(self)
        self.inventory = Inventory(self)
        self.body = Body(self)
        self.fighter = Fighter(self)

        self.statistics = statistics.StatTracker()

        self.type = "Player"

        self.level = 1
        self.max_level = 20
        self.experience = 0
        self.experience_to_next_level = 20

        self.visited_stairs = []


        self.stat_points = 0
        self.stat_decisions = [0, 0, 0, 0]  # used at loop levelling to allocate points

        self.path = []
        self.explore_path = []

        self.invincible = True

        self.type = {
                     "humanoid": True
                     }

        self.quests = []
        self.quest_recieved = False

        if self.invincible:  # only get the gun if you're invincible at the start
            bug_test_spells = [
                S.Gun(self),  # 1
                # S.BlinkStrike(self, cooldown=0, cost=10, damage=25, range=10, action_cost=1), # 3
                #spell.SummonGargoyle(self), # 2
                # S.BurningAttack(self, cooldown=10, cost=10, damage=20, burn_damage=10, burn_duration=10, range=10),  # 2
                # S.Petrify(self, cooldown=0, cost=10, duration=3, activation_chance=1, range=10), #3
                # S.ShrugOff(self, cooldown=0, cost=10, activation_chance=1.0, action_cost=1), #4
                # S.Berserk(self, cooldown=0, cost=10, duration=-100, activation_threshold=50, strength_increase=10, action_cost=1), #5
                # S.Terrify(self, cooldown=0, cost=0, duration=5, activation_chance=1, range=15), #6
                # S.Escape(self, cooldown=0, cost=0, self_fear=False, dex_buff=5, str_debuff=5, int_debuff=5, haste_duration=5, activation_threshold=1.1, action_cost=1), #7
                # S.MagicMissile(self, cooldown=0, cost=10, damage=20, range=10, action_cost=100),  # 8
            ]
            for spell in bug_test_spells:
                self.mage.add_spell(spell)
            self.stat_points = 20 # free stat points for debugging

    def get_attribute(self, attribute):
        attribute = attribute.lower()
        if attribute in ["strength", 'intelligence','endurance',"dexterity"]:
            return self.character.get_attribute(attribute)
        elif attribute in ['armor']:
            return self.fighter.get_attribute(attribute)

    def change_attribute(self, attribute, change):
        attribute = attribute.lower()
        if attribute in ["strength", 'intelligence','endurance',"dexterity"]:
            return self.character.change_attribute(attribute, change)
        elif attribute in ['armor']:
            return self.fighter.change_attribute(attribute, change)

    def get_inventory(self):
        return self.inventory.get_inventory()

    def get_action_cost(self, action):
        return self.character.get_action_cost(action)

    def gain_experience(self, experience):
        self.experience += experience
        self.check_for_levelup()

    def attack_move(self, move_x, move_y, loop):
        if not self.character.can_take_actions:
            self.character.energy -= self.character.action_costs[
                "move"]  # (self.character.move_cost - int(self.character.dexterity + self.character.round_bonus()))
            loop.add_message("The player is petrified and cannot move.")
            return
        x = self.x + move_x
        y = self.y + move_y
        if (x >= 0) & (y >= 0) & (x < loop.generator.tile_map.width) & (y < loop.generator.tile_map.height):
            if loop.generator.get_passable((x, y)) and self.character.can_move:
                self.move(move_x, move_y, loop)
            elif not loop.generator.monster_map.get_passable(x, y):
                defender = loop.generator.monster_map.locate(x,y)
                self.attack(defender, loop)
            elif not loop.generator.interact_map.get_passable(x, y):
                self.do_interact(loop, input_direction=(move_x, move_y))
            elif not self.character.can_move:
                loop.add_message("You are currently restricted!")
            else:
                loop.add_message("You cannot move there")

    def move(self, move_x, move_y, loop):
        if loop.generator.get_passable((self.x + move_x, self.y + move_y)) and self.character.can_move and self.character.can_take_actions:
            self.character.energy -= self.character.action_costs[
                "move"]  # / (1.02**(self.character.dexterity + self.character.round_bonus())))
            self.y += move_y
            self.x += move_x
            self.statistics.add_move_details()
            if loop.currentLoop != LoopType.pathing:
                loop.add_message("The player moved.")
        else:
            loop.add_message("You can't move there")

    def random_move(self, loop):
        random_move = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        rand_i = random.randint(0, 3)
        move_x, move_y = random_move[rand_i]
        self.move(move_x, move_y, loop)

    def attack(self, defender, loop):
        if self.character.can_take_actions:
            self.character.energy -= self.character.action_costs[
                "attack"]  # / (1.05**(self.character.dexterity + self.character.round_bonus())))
            loop.screen_focus = (defender.x, defender.y)
            damage = self.fighter.do_attack(defender, loop)
            self.statistics.add_attack_details(damage)
            loop.add_message(f"The player attacked for {damage} damage")
        else:
            loop.add_message("You cannot currently take actions")

    def autopath(self, loop):

        # if loop.branch == "Forest":
        #     loop.add_message("You cannot autopath in the forest (otherwise we'd have to figure out time).")
        #     loop.change_loop(LoopType.action)
        #     return False
        if loop.branch != "Forest" and self.character.needs_rest(self):
            loop.after_rest = LoopType.pathing
            loop.change_loop(LoopType.resting)
            return
        loop.after_rest = LoopType.action # in case we rested need to reset this to default
        tile_map = loop.generator.tile_map
        for monster in loop.generator.monster_map.all_entities():
            monster_loc = monster.get_location()
            if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible and monster.stops_autoexplore:
                if loop.pathing_count == 0:
                    loop.add_message("You cannot autopath while enemies are visible.")
                else:
                    loop.add_message(f"A {monster.name} interrupted your exploration.")
                loop.change_loop(LoopType.action)
                return False
        
        if self.path:
            x, y = self.path.pop(0)
            if (x == self.x and y == self.y):
                # Pathfinding messed up - pop this just in case
                x, y = self.path.pop(0)
            self.move(x - self.x, y - self.y, loop)
            #loop.time_passes(self.character.energy)
            #self.character.energy = 0 #need to find a way to make time pass as autoexplore happens

            # auto pickup gold
            for item in loop.generator.item_map.all_entities():
                    if item.has_trait("gold"):
                        if item.x == self.x and item.y == self.y:
                            self.do_grab(item, loop)

            self.explore_path.append((x, y))
            loop.update_screen = True

        if not self.path:
            still_pathing = loop.after_pathing(loop) # whatever we set after_pathing to should change away from pathing LoopType if needed
            
        self.character.energy = 0
        #if not all_seen:
            #shadowcasting.compute_fov(loop)
            # self.autoexplore(loop)
        return True

    def autoexplore(self, loop):
        all_seen = False
        
        # auto pickup gold
        good_item_locations = []
        good_item_dict = {}
        for item in loop.generator.item_map.all_entities():
                if item.has_trait("gold") or item.has_trait("potion") or item.has_trait("scroll"):
                    good_item_locations.append((item.x, item.y))
                    good_item_dict[(item.x, item.y)] = item
        
        tile_map = loop.generator.tile_map

        if len(self.path) <= 1:
            start = (self.x, self.y)

            # special case to make sure we don't path to gold we are standing on
            if start in good_item_locations:
                self.do_grab(good_item_dict[start], loop)
                good_item_locations.remove(start)
                            

            all_seen, unseen = loop.generator.all_seen()
            if all_seen:
                loop.change_loop(LoopType.action)
                loop.after_pathing = LoopType.action
                loop.add_message("Finished exploring this level. Press s to path to stairs")
                # print(self.explore_path)
                # print(len(self.explore_path))
                loop.update_screen = True
                self.path = []
                return False

            # Attempt to redo autoexplore with simpler BFS
            # in-line end condition so we can use tile_map
            def autoexplore_condition(position_tuple):
                return position_tuple in good_item_locations or \
                       (tile_map.get_passable(position_tuple[0], position_tuple[1]) and \
                        not (tile_map.track_map[position_tuple[0]][position_tuple[1]].seen))
            self.path = pathfinding.conditional_bfs(tile_map.track_map, start, autoexplore_condition, loop.generator.interact_map.dict)
            if not self.path:
                self.path = []
                loop.change_loop(LoopType.action)
                return False
            else:
                loop.after_pathing = self.autoexplore
        
        return True

    def find_stairs(self, loop):
        tile_map = loop.generator.tile_map
        if len(self.path) <= 1:
            start = (self.x, self.y)
            all_stairs_seen = []
            to_visit_stairs = []
            for stairs in loop.generator.tile_map.get_stairs():
                if stairs.downward and stairs.seen:
                    all_stairs_seen.append(stairs.get_location())
                    if stairs.get_location() not in self.visited_stairs and stairs.get_location() != start:
                        to_visit_stairs.append(stairs.get_location())

            for gateway in loop.generator.tile_map.get_gateway():
                if gateway.seen:
                    all_stairs_seen.append(gateway.get_location())
                    if gateway.get_location() not in self.visited_stairs:
                        to_visit_stairs.append(gateway.get_location())

            if len(all_stairs_seen) == 0:
                loop.add_message("You have not found the stairs or a portal yet")
                loop.change_loop(LoopType.action)
                return
            
            # special case to avoid trying to path to current location
            if len(all_stairs_seen) == 1:
                if all_stairs_seen[0] == start:
                    loop.add_message("You have not found a different staircase or portal yet")
                    loop.change_loop(LoopType.action)
                    return
                else:
                    # if we move away from the only seen staircase, still try to path back to it
                    to_visit_stairs = all_stairs_seen
            
            # if visited all stairs once, allow cycle of pathing to repeat
            if len(to_visit_stairs) == 0:
                to_visit_stairs = [self.visited_stairs[0]] # specically return to first pathed staircase to make the pathing more cyclical
                if start == to_visit_stairs[0]:
                    to_visit_stairs = [self.visited_stairs[1]] # all_stairs_seen length >= 2 and to_visit_stairs length = 0 => self.visited_stairs >= 2
                
                self.visited_stairs = []
                if start in all_stairs_seen:
                    self.visited_stairs.append(start)
            
            def stairs_condition(position_tuple):
                return position_tuple in to_visit_stairs
            
            self.path = pathfinding.conditional_bfs(tile_map.track_map, start, stairs_condition, loop.generator.interact_map.dict)
            if not self.path: # checks null and empty
                self.path = []
                loop.change_loop(LoopType.action)
                return
            
            def after_stairs(loop):
                player = loop.player
                player.visited_stairs.append((player.x, player.y))
                loop.change_loop(LoopType.action)
            loop.after_pathing = after_stairs

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
                and loop.generator.tile_map.track_map[self.x][self.y].downward and self.character.can_take_actions):
            self.character.energy -= self.character.action_costs["move"]
            loop.change_floor(downward = True)
        elif (isinstance(loop.generator.tile_map.track_map[self.x][self.y], T.Gateway) and self.character.can_take_actions):
            self.character.energy -= self.character.action_costs["move"]
            loop.change_branch()
        elif self.character.can_take_actions:
            loop.add_message("There are no stairs here!")
        else:
            self.character.energy -= self.character.action_costs["move"]
            loop.add_message("You can't move!")

    def up_stairs(self, loop):
        if (isinstance(loop.generator.tile_map.track_map[self.x][self.y], T.Stairs)
                and not loop.generator.tile_map.track_map[self.x][self.y].downward and self.character.can_take_actions):
            self.character.energy -= self.character.action_costs["move"]
            loop.change_floor(downward = False)
        elif self.character.can_take_actions:
            loop.add_message("There are no stairs here!")
        else:
            self.character.energy -= self.character.action_costs["move"]
            loop.add_message("You can't move!")

    def cast_spell(self, *args):
        self.mage.cast_spell(*args)

    def add_quest(self, quest):
        self.quests.append(quest)
        self.quest_recieved = True

    def do_grab(self, item, loop):
        if self.inventory.can_grab(item) and self.character.can_grab(item):
            self.statistics.add_item_pickup_details(item)
            # add time
            self.inventory.do_grab(item, loop)

    def do_drop(self, item, item_map):
        if self.inventory.can_drop(item) and self.character.can_drop(item):
            #add stats, time
            self.inventory.do_drop(item, item_map)
            return True
        else:
            return False

    def do_equip(self, item):
        if self.body.can_equip(item) and item.can_be_equipped(self):
            self.body.equip(item, self.character.get_attribute("Strength"))
            # self.energy -= self.action_costs["equip"]

    def do_unequip(self, item):
        if item == None:
            return
        if self.body.can_unequip(item) and item.can_be_unequipped(self):
            self.body.unequip(item)
            #self.energy -= self.action_costs["unequip"]

    def do_interact(self, loop, input_direction=None):
        interact = False
        if input_direction == None:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        else:
            directions = [input_direction]
        location = []
        for x, y in directions:
            location.append((x + self.x, y + self.y))
            if loop.generator.interact_map.locate(x + self.x, y + self.y) != -1:
                loop.generator.interact_map.locate(x + self.x, y + self.y).interact(loop)
                spoke = True


        # if spoke == False:
        #    loop.add_message("You feel lonely.")







