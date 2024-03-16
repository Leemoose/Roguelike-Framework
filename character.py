import random
import dice as R
import objects as O
import effect as E
import pathfinding
import shadowcasting
import skills as S
import items as I
import loops as L

class Character():
    def __init__(self, parent, endurance = 0, intelligence = 0, dexterity = 0, strength = 0, health = 100, mana = 0, health_regen=0.2, mana_regen=0.2):
        self.endurance = endurance
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.strength = strength

        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.health_regen = health_regen
        self.mana_regen = mana_regen

        self.level = 1

        # flags altered by status conditions
        self.movable = True
        self.flee = False
        self.can_teleport = True
        self.safe_rest = True

        self.round_bonus_factor = 2 # stat bonus for being rounded

        self.inventory_limit = 18

        self.energy = 0
        self.move_cost = 100
        self.equip_cost = 20
        self.quaff_cost = 10
        self.read_cost = 100
        self.attack_cost = 100

        self.alive = True

        self.inventory = []
        self.main_weapon = None
        self.main_shield = None

        self.ready_scroll = None # index of actively used scroll

        self.equipment_slots = {"body_armor_slot": [None],
                                "helmet_slot": [None],
                                "gloves_slot": [None],
                                "boots_slot": [None],
                                "ring_slot": [None, None],
                                "pants_slot": [None],
                                "amulet_slot": [None],
                                "hand_slot": [None, None]
                                }
        self.base_damage = 0
        self.armor = 0

        self.parent = parent
        self.status_effects = []

        self.skills = []
        self.invincible = False

        self.experience_given = 0 # monsters will overwrite this attribute, it just makes some class stuff easier if its stored in character
        self.experience = 0

        self.health_partial = 0.0
        self.mana_partial = 0.0

        self.unarmed_damage_min = 1
        self.unarmed_damage_max = 2

    def rounded(self):
        # check all stats are equal
        return self.endurance == self.intelligence == self.dexterity == self.strength
    
    def round_bonus(self):
        if self.rounded():
            return self.round_bonus_factor
        return 0

    def is_alive(self):
        # print(self.invincible)
        if self.health <= 0 and not self.invincible:
            self.alive = False
            return False
        return True

    def take_damage(self, dealer, damage):
        if damage > 0:
            for effect in self.status_effects:
                if isinstance(effect, E.Asleep):
                    effect.duration = 0
        if damage < 0:
            damage = 0
        self.health -= damage
        if not self.is_alive():
            dealer.kill_count += 1
            if hasattr(dealer, "experience"): # acts as a check for it its a player
                dealer.experience += self.experience_given
                dealer.check_for_levelup()
        return self.is_alive()

    def gain_health(self, heal):
        self.health += heal
        self.health = int(self.health)
        if self.health > self.max_health:
            self.health = self.max_health

    def gain_mana(self, mana):
        self.mana += mana
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def defend(self):
        defense = self.armor + ((self.endurance + self.round_bonus()) // 3)
        return defense

    def skill_damage_increase(self):
        return int(((self.intelligence + self.round_bonus()) * 1.5 ) // 2)

    def skill_duration_increase(self):
        return ((self.intelligence + self.round_bonus()) // 3)


    def grab(self, key, item_ID, generated_maps, loop):
        item = item_ID.get_subject(key)
        if item.yendorb:
            loop.change_loop(L.LoopType.victory)
            return
        if item.stackable:
            if not item.name in [x.name for x in self.inventory]:
                if len(self.inventory) > self.inventory_limit:
                    loop.add_message("You need to drop something first")
                    return
                else:
                    self.inventory.append(item)
            else:
                for i in range(len(self.inventory)):
                    if self.inventory[i].name == item.name:
                        self.inventory[i].stacks += 1
        else:
            if len(self.inventory) > self.inventory_limit:
                loop.add_message("You need to drop something first")
                return
            else:
                self.inventory.append(item)
        
        item_ID.remove_subject(key)
        itemx, itemy = item.get_location()
        generated_maps.item_map.clear_location(itemx, itemy)
        loop.add_message("The " + str(self.parent.name) + " picked up a " + str(item.name))

    def drop(self, item, item_dict,  item_map):
        if len(self.inventory) != 0 and item.dropable:
            if item.equipable and item.equipped:
                self.unequip(item)
            i = 0
            while (self.inventory[i] != item) and i < len(self.inventory):
                i += 1
            if i < len(self.inventory):
                # import pdb; pdb.set_trace()
                self.inventory.pop(i)
                item_dict.add_subject(item)
                item.x = self.parent.x
                item.y = self.parent.y
                item_map.place_thing(item)
                return True
        return False

    def equip(self, item):
        if item.can_be_equipped(self):
            item.equip(self)
            item.equipped = True
            item.dropable = False
            self.energy -= self.equip_cost

    def unequip(self, item):
        if item.can_be_unequipped(self):
            item.unequip(self)
            item.dropable = True
            item.equipped = False

    def wait(self):
        self.energy -=  self.move_cost

    def level_up(self, strength_up=1, dexterity_up=1, endurance_up=1, intelligence_up=1):
        self.level += 1 # separate from player level which is stored in player object
        self.level_up_stats(strength_up, dexterity_up, endurance_up, intelligence_up)
        self.level_up_max_health_and_mana()
        
    def level_up_max_health_and_mana(self):
        self.max_health += 5
     #   self.health = self.max_health
        self.max_mana += 3
      #  self.mana = self.max_mana
        self.base_damage += 1

    def level_up_stats(self, strength_up=1, dexterity_up=1, endurance_up=1, intelligence_up=1):
        self.endurance += endurance_up
        self.intelligence += intelligence_up
        self.dexterity += dexterity_up
        self.strength += strength_up

        self.max_health += (strength_up * 2)
        self.max_health += (endurance_up * 10)
        self.max_mana += (intelligence_up * 2)

    def get_damage_min(self):
        return self.get_damage()[0]
    
    def get_damage_max(self):
        return self.get_damage()[1]

    def get_damage(self):
        if self.main_weapon == None:
            return self.base_damage + self.unarmed_damage_min, self.base_damage + self.unarmed_damage_max
        else:
            return self.base_damage + self.main_weapon.damage_min, self.base_damage + self.main_weapon.damage_max

    def melee(self, defender):
        effect = None
        if self.main_weapon == None:
            damage = R.roll_dice(self.unarmed_damage_min, self.unarmed_damage_max)[0]
        else:
            if self.main_weapon.on_hit == None:
                damage = self.main_weapon.attack()
            else:
                damage, effect = self.main_weapon.attack()
            # this formula is pumping damage numbers way up
            damage += random.randint(1, max(1,int(11 + (self.dexterity + self.round_bonus())* 1.5)))
        defense = defender.character.defend()
        if defense < 0:
            defense = 0
        finalDamage = self.base_damage + int((self.strength + self.round_bonus()) * 3) + damage - defense
        defender.character.take_damage(self.parent, finalDamage)
        if effect != None:
            effect = effect(self.parent) # some effects need an inflictor
            defender.character.add_status_effect(effect)
        self.energy -= self.attack_cost
        return (finalDamage)

    def dodge(self):
        dodge_chance = random.randint(1,100)
        if dodge_chance <= (int(self.dexterity + self.round_bonus()) * 2):
            return True
        else:
            return False

    def quaff(self, potion, item_dict, item_map):
        if potion.consumeable and potion.equipment_type == "Potiorb":
            potion.activate(self)
            if potion.stacks < 1:
                self.drop(potion, item_dict, item_map)
                potion.destroy = True
            self.energy -= self.quaff_cost
            return True
    
    def read(self, scroll, loop, item_dict, item_map):
        if scroll.consumeable and scroll.equipment_type == "Scrorb":
            scroll.activate(self, loop)
            self.energy -= self.read_cost
            return True
    
    def tick_all_status_effects(self, loop):
        for effect in self.status_effects:
            effect.tick(self)
            status_messages = [self.parent.name + " " + mes for mes in self.status_messages()] #Still need to fix
            for message in status_messages:
                loop.add_message(message)
        for effect in self.status_effects:
            if not effect.active:
                self.remove_status_effect(effect)
              #  loop.add_message(message)

    def remove_status_effect(self, effect):
        if not effect.active:
            effect.remove(self)
            self.status_effects.remove(effect)

    def has_negative_effects(self):
        for x in self.status_effects:
            if not x.positive:
                return True
        return False

    def has_effect(self, effect_name):
        if effect_name in [x.name for x in self.status_effects]:
            return True
        return False

    def add_status_effect(self, effect):
        if not self.has_effect(effect.name):
            effect.apply_effect(self)
            self.status_effects.append(effect)
        else:
            # refresh duration of existing status effect
            for x in self.status_effects:
                if x.id_tag == effect.id_tag:
                    x.duration = effect.duration
    
    def status_messages(self):
        messages = []
        for effect in self.status_effects:
            messages.append(effect.message)
        return messages
    
    def tick_cooldowns(self):
        for skill in self.skills:
            skill.tick_cooldown()

    def cast_skill(self, skill_num, target, loop):
        skill = self.skills[skill_num]
        self.energy -= skill.action_cost
        return skill.try_to_activate(target, loop.generator)
    
    def cast_skill_by_name(self, skill_name, target, loop):
        for skill in self.skills:
            if skill.name == skill_name:
                self.energy -= skill.action_cost
                return skill.try_to_activate(target, loop.generator)
        return False

    def tick_regen(self):
        self.health_partial += self.health_regen
        self.mana_partial += self.mana_regen
        if abs(self.health_partial) >= 1:
            self.gain_health(self.health_partial // 1)
            self.health_partial = self.health_partial % 1
        if abs(self.mana_partial) >= 1:
            self.gain_mana(self.mana_partial // 1)
            self.mana_partial = self.mana_partial % 1

    def needs_rest(self):
        return self.health < self.max_health or self.mana < self.max_mana
    
    def rest(self, loop, returnLoopType):
        #print("in_rest")
        if not self.safe_rest:
            loop.add_message("Your ring is draining your health, it is not safe to rest now.")
            loop.change_loop(L.LoopType.action)
            return
        monster_dict = loop.monster_dict
        tile_map = loop.generator.tile_map
        no_monster_active = True
        for monster_key in monster_dict.subjects:
            if monster_dict.get_subject(monster_key).brain.is_awake:
                no_monster_active = False
                break
        if no_monster_active:
            # can freely rest to full health
            self.health = self.max_health
            self.mana = self.max_mana
            for skill in self.skills:
                skill.ready = 0
            for effect in self.status_effects:
                if not effect.positive:
                    self.remove_status_effect(effect)
            loop.add_message("You rest for a while")
            loop.change_loop(returnLoopType)
            return

        for monster_key in monster_dict.subjects:
            monster_loc = monster_dict.get_subject(monster_key).get_location()
            if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible:
                loop.add_message("You cannot rest while enemies are nearby.")
                loop.change_loop(L.LoopType.action)
                return
        self.wait()
        #print(self.energy)
        #print(self.health)
        #print(self.max_health)
        if not self.needs_rest():
            loop.add_message("You rest for a while")
            loop.change_loop(returnLoopType)

    def add_skill(self, new_skill):
        for skill in self.skills:
            if skill.name == new_skill.name:
                return
        self.skills.append(new_skill)

    def remove_skill(self, skill_name):
        for skill in self.skills:
            if skill.name == skill_name:
                self.skills.remove(skill)
                break
    
    def get_enchantable(self):
        enchantable = []
        for item in self.inventory:
            if item.can_be_levelled:
                if item.level < 6: # items can be levelled upto +5
                    enchantable.append(item)
        return enchantable

    def get_closest_monster(self, player, monsterID, tile_map):
        closest_dist = 100000
        closest_monster = player
        for monster_key in monsterID.subjects:
            monster = monsterID.subjects[monster_key]
            dist = player.get_distance(monster.x, monster.y)
                        
            if dist < closest_dist and tile_map.track_map[monster.x][monster.y].visible:
                closest_dist = dist
                closest_monster = monster
        return closest_monster


class Player(O.Objects):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 200, "Player")
        self.character = Character(self, mana=50)
        self.character.skills = []

        self.level = 1
        self.max_level = 20
        self.experience = 0
        self.experience_to_next_level = 20

        self.kill_count = 0

        self.stat_points = 0
        self.stat_decisions = [0, 0, 0, 0] # used at loop levelling to allocate points

        self.path = []

        self.invincible = True

        if self.invincible: # only get the gun if you're invincible at the start
            self.character.skills.extend([
                S.Gun(self), # 1
                # S.BlinkToEmpty(self, cooldown=0, cost=0, range=10, action_cost=1), # 2
                # S.BlinkStrike(self, cooldown=0, cost=10, damage=25, range=10, action_cost=1), # 3
                # S.SummonGorblin(self, cooldown=0, cost=10, range=10, action_cost=1), # 2
                 S.BurningAttack(self, cooldown=0, cost=10, damage=20, burn_damage=10, burn_duration=10, range=10), #2
                # S.Petrify(self, cooldown=0, cost=10, duration=3, activation_chance=1, range=10), #3
                # S.ShrugOff(self, cooldown=0, cost=10, activation_chance=1.0, action_cost=1), #4
                # S.Berserk(self, cooldown=0, cost=10, activation_threshold=50, strength_increase=10, action_cost=1), #5
                # S.Terrify(self, cooldown=0, cost=0, duration=5, activation_chance=1, range=15), #6
                # S.Escape(self, cooldown=0, cost=0, self_fear=False, activation_threshold=1.1, action_cost=1) #7
            ])

    def attack_move(self, move_x, move_y, loop):
        if not self.character.movable:           
            self.character.energy -= (self.character.move_cost - int(self.character.dexterity + self.character.round_bonus()))
            loop.add_message("The player is petrified and cannot move.")
            return
        x = self.x + move_x
        y = self.y + move_y
        if (x >= 0) & (y >= 0) & (x < loop.generator.tile_map.width) & (y < loop.generator.tile_map.height):
            if (loop.generator.monster_map.track_map[x][y]) != -1:
                defender = loop.monster_dict.get_subject(loop.generator.monster_map.track_map[x][y])
                self.attack(defender, loop)
            else:
                self.move(move_x, move_y, loop)

    def move(self, move_x, move_y, loop):
        if loop.generator.tile_map.get_passable(self.x + move_x, self.y + move_y) and loop.generator.monster_map.get_passable(self.x + move_x, self.y + move_y):
            self.character.energy -= int(self.character.move_cost/ (1.02**(self.character.dexterity + self.character.round_bonus())))
            self.y += move_y
            self.x += move_x
        loop.add_message("The player moved.")

    def random_move(self, loop):
        random_move = [(0,1),(1,0),(-1,0),(0,-1)]
        rand_i = random.randint(0,3)
        move_x,move_y = random_move[rand_i]
        self.move(move_x,move_y, loop)

    def attack(self, defender, loop):
        self.character.energy -= int(self.character.attack_cost / (1.05**(self.character.dexterity + self.character.round_bonus())))
        loop.screen_focus = (defender.x, defender.y)
        if not self.character.dodge():
            damage = self.character.melee(defender)
            if damage < 0:
                damage = 0
            # if not defender.character.is_alive():
            #     self.experience += defender.experience_given
            #     self.check_for_levelup()
            loop.add_message(f"The player attacked for {damage} damage")
        else:
            loop.add_message("The monster dodged the attack")

    def autoexplore(self, loop):
        all_seen = False
        if self.character.needs_rest():
            self.character.rest(loop, loop.currentLoop)
        monster_dict = loop.monster_dict
        tile_map = loop.generator.tile_map
        for monster_key in monster_dict.subjects:
            monster_loc = monster_dict.get_subject(monster_key).get_location()
            if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible:
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
            self.path = pathfinding.astar_multi_goal(tile_map.track_map, start, loop.generator.get_all_frontier_tiles(), loop.generator.monster_map, loop.player)
            # if all tiles have been seen don't autoexplore
            
        x, y = self.path.pop(0)
        if (x == self.x and y == self.y):
            #Pathfinding messed up - pop this just in case
            x, y = self.path.pop(0)
        self.move(x-self.x, y-self.y, loop)
        loop.update_screen = True

        self.character.energy = 0
        if not all_seen:
            shadowcasting.compute_fov(loop)
            self.autoexplore(loop)
        return True

    def find_stairs(self, loop):
        monster_dict = loop.monster_dict
        tile_map = loop.generator.tile_map
        for monster_key in monster_dict.subjects:
            monster_loc = monster_dict.get_subject(monster_key).get_location()
            if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible:
                loop.add_message("You cannot autoexplore while enemies are tracking you.")
                loop.change_loop(L.LoopType.action)
                return
            
        start = (self.x, self.y)
        end = loop.generator.tile_map.stairs[0].get_location()
        if (start == end):
            loop.change_loop(L.LoopType.action)
            return
        self.path = pathfinding.astar(tile_map.track_map, start, end, loop.generator.monster_map, loop.player)
        
        x, y = self.path.pop(0)
        while len(self.path) > 0:
            x,y = self.path.pop(0)
            self.move(x - self.x, y - self.y, loop)
            shadowcasting.compute_fov(loop)
            for monster_key in monster_dict.subjects:
                monster_loc = monster_dict.get_subject(monster_key).get_location()
                if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible:
                    loop.add_message("You cannot autoexplore while enemies are tracking you.")
                    loop.change_loop(L.LoopType.action)
                    return
        loop.update_screen = True

        self.character.energy = 0


    def check_for_levelup(self):
        while self.level != self.max_level and self.experience >= self.experience_to_next_level:
            self.level += 1
            # self.character.level_up()
            # self.awaiting_level_up = True
            self.character.level_up_max_health_and_mana()
            self.stat_points += 2
            exp_taken = self.experience_to_next_level
            self.experience_to_next_level += 20 + self.experience_to_next_level // 4
            self.experience -= exp_taken

    def modify_stat_decisions(self, i, increase=True): # 0 = strength, 1 = dexterity, 2 = endurance, 3 = intelligence

        if increase:
            if self.stat_points > sum(self.stat_decisions):
                self.stat_decisions[i] += 1
        else:
            if self.stat_decisions[i] > 0:
                self.stat_decisions[i] -= 1
    
    def apply_level_up(self):
        self.character.level_up_stats(self.stat_decisions[0], self.stat_decisions[1], self.stat_decisions[2], self.stat_decisions[3])
        self.stat_points -= sum(self.stat_decisions)
        self.stat_decisions = [0, 0, 0, 0]

