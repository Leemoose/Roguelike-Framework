import random
from .body_slot import Body

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
        self.can_move = True
        self.can_take_actions = True
        self.flee = False
        self.can_teleport = True
        self.safe_rest = True

        self.energy = 0

        self.alive = True

        self.main_weapon = None


        self.action_costs = {"attack": 80,
                             "move": 100,
                             "grab": 30,
                             "equip": 100,
                             "unequip": 50,
                             "quaff": 10,
                             "read": 20,
                             "drop": 10
                            }



        self.parent = parent
        self.status_effects = []

        self.skills = []
        self.invincible = False

        self.experience_given = 0 # monsters will overwrite this attribute, it just makes some class stuff easier if its stored in character
        self.experience = 0

        self.health_partial = 0.0
        self.mana_partial = 0.0

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_action_cost(self, action):
        return self.action_costs[action]

    def get_attribute(self, attribute):
        attribute = attribute.lower()
        if attribute == "strength":
            return self.strength
        elif attribute == "intelligence":
            return self.intelligence
        elif attribute == "endurance":
            return self.endurance
        elif attribute == "dexterity":
            return self.dexterity

    def change_attribute(self, attribute, change):
        attribute = attribute.lower()
        if attribute == "strength":
            self.strength += change
        elif attribute == "intelligence":
            self.intelligence += change
        elif attribute == "endurance":
            self.endurance += change
        elif attribute == "dexterity":
            self.dexterity += change
        else:
            raise Exception("You tried to change an attribute but it doesn't exist")
    def change_health(self, change):
        self.health += change

    def change_max_health(self, change):
        self.max_health += change

    def change_action_cost(self, action, newcost):
        self.action_costs[action] = newcost

    def can_grab(self, item):
        return True #Should check if any conditions would apply (like effects)

    def can_drop(self, item):
        return True

    def is_alive(self):
        if self.health <= 0 and not self.invincible:
            self.alive = False
            return False
        return True

    def take_damage(self, dealer, damage):
        if damage > 0:
            for effect in self.status_effects:
                if effect.has_trait("asleep"):
                    effect.duration = 0
        if damage < 0:
            damage = 0
        self.health -= damage
        if not self.is_alive():
            if hasattr(dealer, "experience"): # acts as a check for it its a player
                dealer.statistics.add_killed_monster(self.parent)
                dealer.gain_experience(self.experience_given)
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


    def skill_damage_increase(self):
        return int(((self.intelligence) * 1.5 ) // 2)

    def skill_duration_increase(self):
        return (self.intelligence // 3)

    def wait(self):
        self.energy -=  self.action_costs["move"]

    def level_up(self, strength_up=1, dexterity_up=1, endurance_up=1, intelligence_up=1):
        self.level += 1 # separate from player level which is stored in player object
        self.level_up_stats(strength_up, dexterity_up, endurance_up, intelligence_up)
        self.level_up_max_health_and_mana()
        
    def level_up_max_health_and_mana(self):
        self.max_health += 5
     #   self.health = self.max_health
        self.max_mana += 3
      #  self.mana = self.max_mana
        #self.base_damage += 1

    def level_up_stats(self, strength_up=1, dexterity_up=1, endurance_up=1, intelligence_up=1):
        self.endurance += endurance_up
        self.intelligence += intelligence_up
        self.dexterity += dexterity_up
        self.strength += strength_up

        self.max_health += (strength_up * 2)
        self.max_health += (endurance_up * 10)
        self.max_mana += (intelligence_up * 2)


    def quaff(self, potion, item_dict, item_map):
        if potion.consumeable and potion.equipment_type == "Potiorb":
            potion.activate(self)
            if potion.stacks < 1:
                self.drop(potion, item_dict, item_map)
                potion.destroy = True
            self.energy -= self.action_costs["quaff"]
            return True
    
    def read(self, scroll, loop, item_dict, item_map):
        if scroll.consumeable and scroll.equipment_type == "Scrorb":
            scroll.activate(self, loop)
            self.energy -= self.action_costs["read"]
            return True
        elif scroll.equipment_type == "Book":
            scroll.activate(self, loop)
            self.energy -= self.action_costs["read"]

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
                    if x.is_cumulative():
                        x.change_duration(effect.get_duration()) #add more duration
                    else:
                        x.change_duration(effect.get_duration() - x.get_duration()) #reset duration
    def status_messages(self):
        messages = []
        for effect in self.status_effects:
            messages.append(effect.message)
        return messages
    
    def tick_cooldowns(self):
        if self.parent.has_trait("monster"):
            for skill in self.skills: # monsters still use skill system instead of spells
                skill.tick_cooldown()
        else:
            for skill in self.player.known_spells: # players use spell system
                skill.tick_cooldown()

    def cast_skill(self, skill_num, target, loop, quick_cast=False):
        self.parent.mage.cast_spell(skill_num, target, loop, quick_cast)
    
    # should be outdated and unused with updated spell system
    # def cast_skill_by_name(self, skill_name, target, loop):
    #     for skill in self.skills:
    #         if skill.name == skill_name:
    #             self.energy -= skill.action_cost
    #             return skill.try_to_activate(target, loop)
    #     return False

    def tick_regen(self):
        self.health_partial += self.health_regen
        self.mana_partial += self.mana_regen
        if abs(self.health_partial) >= 1:
            self.gain_health(self.health_partial // 1)
            self.health_partial = self.health_partial % 1
        if abs(self.mana_partial) >= 1:
            self.gain_mana(self.mana_partial // 1)
            self.mana_partial = self.mana_partial % 1

    def needs_rest(self, player):
        # skills_ready = True
        for skill in player.mage.known_spells:
            if skill.ready != 0:
                return True
        return self.health < self.max_health or self.mana < self.max_mana
    
    def rest(self, loop, returnLoop):
        # print("in_rest")
        if not self.safe_rest:
            loop.add_message("Your ring is draining your health, it is not safe to rest now.")
            loop.change_loop("action")
            return
        
        if not self.needs_rest(loop.player): # and returnLoop == L.LoopType.action: <- Don't think we need this?
            loop.add_message("No point in resting right now.")
            loop.change_loop(returnLoop)
            return
        """
        if loop.branch == "Forest":
            loop.add_message("No resting with these predators lurking nearby")
            loop.change_loop(returnLoop)
            return
        """
        tile_map = loop.generator.tile_map
        no_monster_active = True
        for monster in loop.generator.monster_map.all_entities():
            if monster.brain.is_awake and monster.stops_autoexplore:
                no_monster_active = False
                break
        if no_monster_active or loop.rest_count > 50: # if you've rested peacefully for 50 turns, your probably not getting hunted, if we dont put this check, rest sometimes seems laggy
            # can freely rest to full health
            self.health = self.max_health
            self.mana = self.max_mana
            for skill in loop.player.mage.known_spells:
                skill.ready = 0
            for effect in self.status_effects:
                if effect.duration != -100: # remove any non-permanent effects
                    self.remove_status_effect(effect)
            loop.add_message("You rest for a while")
            loop.change_loop(returnLoop)
            return

        for monster in loop.generator.monster_map.all_entities():
            monster_loc = monster.get_location()
            if tile_map.track_map[monster_loc[0]][monster_loc[1]].visible and monster.stops_autoexplore:
                loop.add_message("You cannot rest while enemies are nearby.")
                loop.change_loop("action")
                return

        self.wait()
        #print(self.energy)
        #print(self.health)
        #print(self.max_health)
        if not self.needs_rest(loop.player):
            loop.add_message("You rest for a while")
            loop.change_loop(returnLoop)
        
    def add_skill(self, new_skill):
        for skill in self.parent.mage.known_spells:
            if skill.name == new_skill.name:
                return
        self.parent.mage.add_spell(new_skill)

    def remove_skill(self, skill_name):
        for skill in self.parent.mage.known_spells:
            if skill.name == skill_name:
                self.parent.mage.known_spells.remove(skill)
                if skill in self.parent.mage.quick_cast_spells:
                    idx = self.parent.mage.quick_cast_spells.index(skill)
                    self.parent.mage.quick_cast_spells[idx] = None
                break


    def get_closest_monster(self, loop):
        player = loop.player
        monsterID = loop.generator.monster_map.dict
        tile_map = loop.generator.tile_map
        closest_dist = 100000
        closest_monster = player
        for monster_key in monsterID.subjects:
            monster = monsterID.get_subject(monster_key)
            dist = player.get_distance(monster.x, monster.y)
                        
            if dist < closest_dist and tile_map.track_map[monster.x][monster.y].visible:
                closest_dist = dist
                closest_monster = monster
        return closest_monster

