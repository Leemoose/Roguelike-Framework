import monster as M
import objects as O
import character as C
import dice as R
import items as I
import random

import pathfinding
import skills as S


class Monster_AI():
    def __init__(self, parent):
        self.frontier = None
        self.is_awake = False
        self.parent = parent
        self.grouped = False

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

        utility = self.rank_equip_item(loop) #Needs to be fixed so that works with shields and swords
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

        utility = self.rank_ungroup(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_ungroup

        utility = self.rank_skill(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_skill

        utility = self.rank_flee(loop)
        if utility > max_utility:
            max_utility = utility
            called_function = self.do_flee

        # print(max_utility)
        self.parent.character.energy -= 1
        if isinstance(self.parent,M.Minotaur):
            print(utility)
        # print(f"{self.parent} is doing {called_function.__name__} with utility {max_utility}")
        called_function(loop)

    def rank_flee(self, loop):
        if self.parent.character.flee:
            return 1000 # must flee if flag is set
        return -1

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

    def rank_equip_item(self, loop): #Needs to be fixed
        monster = self.parent
        if len(monster.character.inventory) != 0:
            utility = -1
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.equipable:
                    if item.equipment_type == "Weapon" and monster.character.main_weapon == None:
                        utility = 80
                        return utility
                    elif item.equipment_type == "Shield" and monster.character.main_shield == None:
                        return -1
                    elif item.equipment_type == "Body Armor" and monster.character.main_armor == None:
                        return -1
                    elif item.equipment_type == "Helmet" and monster.character.helmet == None:
                        return -1
                    elif item.equipment_type == "Boots" and monster.character.boots == None:
                        return -1
                    elif item.equipment_type == "Gloves" and monster.character.gloves == None:
                        return -1
                    elif item.equipment_type == "Ring" and (monster.character.ring_1 == None or monster.character.ring_2 == None):
                        return -1
        return -1

    def rank_use_consumeable(self, loop):
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable and item.equipment_type == "Potiorb": # monsters can't read so no scrolls
                    return -1
        return -1

    def rank_move(self, loop):
        return 20

    def rank_ungroup(self, loop):
        player = loop.player
        x,y = self.parent.x, self.parent.y
        tile_map = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        if player.get_distance(x,y) < 1.5:
            xplayer, yplayer = player.get_location()
            xdiff = xplayer - x
            ydiff = yplayer - y
            grouped = False
            goals = []
            if xdiff != 0:
                if (not tile_map.get_passable(x,y + 1) and not tile_map.get_passable(x,y - 1) and not monster_map.get_passable(x-xdiff,y)):
                    self.grouped = True
                    goals = [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer +ydiff)]
                for position in [(xplayer, yplayer + 1), (xplayer, yplayer - 1), (xplayer + xdiff, yplayer +ydiff)]:
                    xposition, yposition = position
                    if not monster_map.get_passable(xposition,yposition):
                        monster = loop.generator.monster_dict.get_subject(monster_map.track_map[xposition][yposition])
                        if monster.brain.grouped:
                            self.grouped = True
                            xdiff = xplayer - monster.x
                            ydiff = yplayer - monster.y
                            goals = [(xplayer + xdiff, yplayer + ydiff)]
                            break
            elif ydiff != 0:
                if not tile_map.get_passable(x - 1,y) and not tile_map.get_passable(x + 1,y) and not monster_map.get_passable(x,y-ydiff):
                    self.grouped = True
                    goals = [(xplayer + 1, yplayer), (xplayer -1, yplayer), (xplayer + xdiff, yplayer + ydiff)]
                for position in [(xplayer + 1, yplayer), (xplayer -1, yplayer), (xplayer + xdiff, yplayer + ydiff)]:
                    xposition, yposition = position
                    if not monster_map.get_passable(xposition,yposition):
                        monster = loop.generator.monster_dict.get_subject(monster_map.track_map[xposition][yposition])
                        if monster.brain.grouped:
                            self.grouped = True
                            xdiff = xplayer - monster.x
                            ydiff = yplayer - monster.y
                            goals = [(xplayer + xdiff, yplayer + ydiff)]
                            break
            if (self.grouped == True):
                self.move_path = (pathfinding.astar_multi_goal(tile_map.track_map, (x, y), goals,
                                             monster_map, player, True, True))
                if len(self.move_path) > 0:
                    return 90
        return -1
    
    def rank_skill(self, loop):
        if not self.parent.orb: # only orbs can cast skills
            return -1
        for skill in self.parent.character.skills:
            if skill.castable(loop.player):
                return 95
        return -1

    def do_item_pickup(self, loop):
        # print("Picking up item")
        item_map = loop.generator.item_map
        item_dict = loop.generator.item_dict
        generated_maps = loop.generator
        monster = self.parent
        item_key = item_map.locate(monster.x, monster.y)
        monster.character.grab(item_key, item_dict, generated_maps, loop)

    def do_combat(self, loop):
        # print("Attacking player")
        player=loop.player
        monster = self.parent
        if not monster.character.movable:
            monster.character.energy -= (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot attack.")
            return
        if not player.character.dodge():
            damage = monster.character.melee(player)
            if damage < 0:
                damage = 0
            loop.add_message(f"{monster} attacked you for {damage} damage")
        else:
            loop.add_message("You dodged the monsters attack")

    def do_skill(self, loop):
        monster = self.parent
        for i in range(len(monster.character.skills)):
            print(monster.character.skills[i].name)
            # use first castable skill
            if monster.character.skills[i].castable(loop.player):
                skill = monster.character.skills[i]
                skill_cast = monster.character.cast_skill(i, loop.player, loop)
                message_addition = "" if skill_cast else ". But it failed."
                loop.add_message(f"{monster} used {skill.name}" + message_addition)
                # print(f"{monster} used {skill.name}")
                break

    def do_equip(self, loop):
        # print("Equipping item")
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if monster.character.main_weapon == None and item.equipable:
                    monster.character.equip(item)
                    return

    def do_use_consumeable(self, loop):
        # print("Using consumeable")
        monster = self.parent
        if len(monster.character.inventory) != 0:
            stuff = monster.character.inventory
            for i, item in enumerate(stuff):
                if item.consumeable and item.equipment_type == "Potiorb": # monster's can't read so no scrolls
                    item.activate(monster.character)

    def do_move(self, loop):
        # print("Moving")
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player

        if not monster.character.movable:
            monster.character.energy -= (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.target_to_display == (monster.x, monster.y):
            update_target = True

        start = (monster.x, monster.y)
        end = (player.x, player.y)
        if player.get_distance(monster.x, monster.y) <= 2.5:
            moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player, monster_blocks=True)
        else:
            moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player)
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            monster.move(xmove - monster.x, ymove-monster.y, tile_map, monster, monster_map, player)
        if update_target:
            loop.add_target((monster.x, monster.y))

    def do_ungroup(self, loop):
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player
        x,y = self.parent.x, self.parent.y

        if not monster.character.movable:
            monster.character.energy -= (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.target_to_display == (monster.x, monster.y):
            update_target = True

        if player.get_distance(monster.x, monster.y) <= 2.5:
            moves = self.move_path
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            monster.move(xmove - monster.x, ymove-monster.y, tile_map, monster, monster_map, player)
            self.grouped = False
        if update_target:
            loop.add_target((monster.x, monster.y))
    def do_flee(self, loop):
        # print("Fleeing")
        tile_map = loop.generator.tile_map
        monster = self.parent
        monster_map = loop.generator.monster_map
        player = loop.player

        if not monster.character.movable:
            monster.character.energy -= (monster.character.move_cost - monster.character.dexterity)
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        update_target = False
        if loop.target_to_display == (monster.x, monster.y):
            update_target = True

        start = (monster.x, monster.y)
        end = (player.x, player.y)
        moves = pathfinding.astar(tile_map.track_map, start, end, monster_map, loop.player)
        if len(moves) > 1:
            xmove, ymove = moves.pop(1)
            # if one direciton is blocked, still move in the other
            opposite_move = (-xmove + monster.x, -ymove + monster.y)
            if tile_map.get_passable(monster.x + opposite_move[0], monster.y + opposite_move[1]):
                monster.move(opposite_move[0], opposite_move[1], tile_map, monster, monster_map, player)
            elif tile_map.get_passable(monster.x, monster.y + opposite_move[1]):
                monster.move(0, opposite_move[1], tile_map, monster, monster_map, player)
            elif tile_map.get_passable(monster.x + opposite_move[0], monster.y):
                monster.move(opposite_move[0], 0, tile_map, monster, monster_map, player)
            else:
                monster.character.energy -= (monster.character.move_cost - monster.character.dexterity)
                loop.add_message(f"{monster} cowers in a corner since it can't run further.")
        if update_target:
            loop.add_target((monster.x, monster.y))

    def do_nothing(self,loop):
        # print("doing nothing")
        pass



class Monster(O.Objects):
    def __init__(self, number_tag, x, y, name="Unknown monster"):
        super().__init__(x, y, 0, number_tag, name)
        self.character = C.Character(self)
        self.asleep = False
        self.character.experience_given = 10
        self.brain = Monster_AI(self)
        self.skills = []
        self.orb = False
        self.kill_count = 0
        self.rarity = "Common"

        self.description = f"This is a {self.name}. It wants to eat you."

    def move(self, move_x, move_y, floormap, monster, monster_map, player):
        # print(self.character.movable)
        # print(move_x)
        # print(move_y)
        if not self.character.movable:
            self.character.energy -= (self.character.move_cost - self.character.dexterity)
            return

        self.character.energy -= (self.character.move_cost - self.character.dexterity)
        #Monsters can move ontop of players
        if floormap.get_passable(monster.x + move_x, monster.y + move_y) and monster_map.get_passable(monster.x + move_x, monster.y + move_y):
            self.character.energy -= self.character.move_cost
            monster_map.track_map[monster.x][monster.y] = -1
            monster.y += move_y
            monster.x += move_x
            monster_map.track_map[monster.x][monster.y] = monster.id_tag
    

    def __str__(self):
        return self.name

class Kobold(Monster):
    def __init__(self, x, y, render_tag=105, name="Kobold"):
        super().__init__(render_tag, x, y, name)
        self.skills = []
        self.character.skills.append(S.BurningAttack(self, cooldown=10, cost=0, damage=10, burn_damage=5, burn_duration=5, range=1.5))
        self.character.experience_given = 10
        self.endurance = 2
        self.strength = 2
        self.dexterity = 1
        self.intelligence = 1

        self.description = "A small, scaly creature with a mysterious satchel on its back."

class Korbold(Kobold):
    def __init__(self, x, y, render_tag=155, name="Korbold"):
        super().__init__(x, y, render_tag, name)
        self.character.experience_given += 15
        self.orb = True
        self.endurance = 2
        self.strength = 2
        self.dexterity = 2
        self.intelligence = 2

        self.description = "A scaly orb with a penchant for setting things on fire. Including you."

class Goblin(Monster):
    def __init__(self, x, y, render_tag=103, name="Goblin", activation_threshold=0.4):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.skills.append(S.Escape(self, cooldown=100, 
                                              cost=0, self_fear=True, 
                                              dex_buff=20, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=activation_threshold, 
                                              action_cost=1))
        self.character.experience_given = 10
        self.description = "A cowardly creature with a tiny dagger"

        self.endurance = 1
        self.strength = 1
        self.dexterity = 3
        self.intelligence = 1

class Gorblin(Goblin):
    def __init__(self, x, y, render_tag=153, name="Gorblin", activation_threshold=0.4):
        super().__init__(x, y, render_tag, name, activation_threshold)
        self.character.experience_given += 15
        self.orb = True
        self.endurance = 1
        self.strength = 2
        self.dexterity = 5
        self.intelligence = 1

        self.description = "A cowardly orb with a tiny dagger. It can blink to escape when it's afraid."

class Hobgoblin(Monster):
    def __init__(self, x, y, render_tag=104, name="Hobgoblin"):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.skills.append(S.BlinkStrike(self, cooldown=10, cost=0, damage=10, range=5, action_cost=1))
        self.character.skills.append(S.Escape(self, cooldown=100, 
                                              cost=0, self_fear=True, 
                                              dex_buff=30, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=0.3, 
                                              action_cost=1))
        self.character.experience_given = 10
        self.description = "The older cousin of its smaller green relatives."

        self.endurance = 2
        self.strength = 2
        self.dexterity = 4
        self.intelligence = 2

class Hobgorblin(Hobgoblin):
    def __init__(self, x, y, render_tag=154, name="Hobgorblin"):
        super().__init__(x, y, render_tag, name)
        self.character.experience_given += 15
        self.orb = True
        self.endurance = 3
        self.strength = 4
        self.dexterity = 8
        self.intelligence = 3

        self.description = "An orb that can blink at you to engage a fight but knows when to tactically retreat"

class Gargoyle(Monster):
    def __init__(self, x, y, render_tag=106, name="Gargoyle"):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.endurance = 5
        self.strength = 3
        self.dexterity = 1
        self.intelligence = 1
        self.skills = []
        # 20% chance to petrify for 2 turns
        self.character.skills.append(S.Petrify(self, cooldown=10, cost=0, duration=2, activation_chance=0.2, range=3))
        self.character.experience_given = 20

        self.description = "A stone creature that you feel could petrify you if it was rounder."

class Gorbgoyle(Gargoyle):
    def __init__(self, x, y, render_tag=156, name="Gorbgoyle"):
        super().__init__(x, y, render_tag, name)
        self.character.experience_given += 25
        self.orb = True
        self.endurance = 4
        self.strength = 4
        self.dexterity = 4
        self.intelligence = 4

        self.description = "A stone orb that can petrify you with its gaze."

class Minotaur(Monster):
    def __init__(self, x, y, render_tag=108, name="Minotaur"):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.skills.append(S.ShrugOff(self, cooldown=3, cost=0, activation_chance=0.75, action_cost=1))
        self.character.experience_given = 20
        self.description = "A large, angry bull with mighty horns."

        self.endurance = 4
        self.strength = 4
        self.dexterity = 1
        self.intelligence = 1

class Minotaurb(Minotaur):
    def __init__(self, x, y, render_tag=158, name="Minotaurb"):
        super().__init__(x, y, render_tag, name)
        self.character.experience_given += 25
        self.orb = True
        self.endurance = 8
        self.strength = 8
        self.dexterity = 3
        self.intelligence = 1

        self.description = "A large, angry orb wiht horns that can shrug off your status effects."

class Orc(Monster):
    def __init__(self, x, y, render_tag=101, name="Orc"):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        # below 25% health, gains 25 strength
        self.character.skills.append(S.Berserk(self, cooldown=0, cost=0, duration=-100, activation_threshold=0.25, strength_increase=25, action_cost=1))
        self.character.experience_given = 20
        self.description = "A strong humanoid with anger issues."

        self.endurance = 3
        self.strength = 7
        self.dexterity = 3
        self.intelligence = 1

class Orbc(Orc):
    def __init__(self, x, y, render_tag=151, name="Orbc"):
        super().__init__(x, y, render_tag, name)
        self.character.experience_given += 25
        self.orb = True
        self.endurance = 4
        self.strength = 10
        self.dexterity = 4
        self.intelligence = 1

        self.description = "A strong orb that can channel its anger issues to make itself stronger."

class Golem(Monster):
    def __init__(self, x, y, render_tag=102, name="Golem"):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.experience_given = 30
        self.description = "A large, slow creature made of stone."

        self.endurance = 10
        self.strength = 8
        self.dexterity = -3
        self.intelligence = 1
    
class Gorblem(Golem):
    def __init__(self, x, y, render_tag=152, name="Gorblem"):
        super().__init__(x, y, render_tag, name)
        self.character.experience_given += 35
        self.orb = True
        self.endurance = 15
        self.strength = 15
        self.dexterity = -5
        self.intelligence = 1

        self.description = "A large, slow orb made of stone. Don't let it catch up to you but that shouldn't be hard."

class Raptor(Monster):
    def __init__(self, x, y, render_tag=107, name="Velociraptor"):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        
        self.endurance = 1
        self.strength = 5
        self.dexterity = 10
        self.intelligence = 1

        self.brain = Monster_AI(self)
        self.character.experience_given = 30
        self.description = "A very fast and very angry dinosaur."

class Raptorb(Raptor):
    def __init__(self, x, y, render_tag=157, name="Velociraptorb"):
        super().__init__(x, y, render_tag, name)
        self.character.experience_given += 35
        self.orb = True
        self.endurance = 1
        self.strength = 9
        self.dexterity = 20
        self.intelligence = 1

        self.description = "A ferocious orb that can move and attack with great speed."

class Tormentorb(Monster):
    def __init__(self, x, y, render_tag=159, name="Tormentorb"):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.orb = True
        # self, parent, cooldown, cost, slow_duration, damage_percent, slow_amount, range, action_cost
        self.character.skills.append(S.Torment(self, cooldown=10, cost=0, slow_duration=3, damage_percent=0.5, slow_amount=5, range=4, action_cost=100))
        self.character.experience_given = 65
        self.description = "A floating orb that can torment and slow you with its gaze."

        self.endurance = 5
        self.strength = 1
        self.dexterity = 1
        self.intelligence = 15

class BossOrb(Monster):
    def __init__(self, x, y, render_tag=160, name="ORB OF YENDORB"):
        super().__init__(render_tag, x, y, name)
        self.character = C.Character(self)
        self.brain = Monster_AI(self)
        self.character.skills = []
        self.character.inventory.append(I.OrbOfYendorb())
        self.orb = True
        # self, parent, cooldown, cost, slow_duration, damage_percent, slow_amount, range, action_cost
      #  self.character.skills.append(S.Torment(self, cooldown=10, cost=0, slow_duration=3, damage_percent=0.5, slow_amount=5, range=4, action_cost=100))
        self.character.skills.append(S.SummonGorblin(self, cooldown=20, cost=0, range=4,action_cost=20))
      #  self.character.skills.append(S.Heal(self, cooldown = 20, cost = 10, heal_amount = 30, activation_threshold = .25, action_cost = 100))
       # self.character.skills.append(S.Invinciblity(self, cooldown=1000, cost=0))

        self.character.experience_given = 1000
        self.description = "The orb of all orbs, the orbiest of orbs, the archetype of orbs... you get the idea."

        self.endurance = 25
        self.strength = 25
        self.dexterity = 25
        self.intelligence = 25