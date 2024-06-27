import random
from .body_slot import Body

class Character():
    def __init__(self, parent, endurance = 0, intelligence = 0, dexterity = 0, strength = 0, health = 100, mana = 0, health_regen=0.2, mana_regen=0.2, min_damage = 2, max_damage = 3):
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
        
        self.force_ring = 1 # by default rings are equipped to slot 1

        self.inventory_limit = 18

        self.energy = 0

        self.alive = True

        self.body = Body(self)

        self.inventory = []
        self.gold = 0

        self.ready_scroll = None # index of actively used scroll

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

        self.unarmed_damage_min = min_damage
        self.unarmed_damage_max = max_damage

    def change_action_cost(self, action, newcost):
        self.action_costs[action] = newcost

    def free_equipment_slots(self, slot):
        return self.body.free_equipment_slots(slot)

    def add_item_to_equipment_slot(self, item, slot, num_slots):
        return self.body.add_item_to_equipment_slot(item, slot, num_slots)

    def remove_item_from_equipment_slot(self, item, slot, num_slots):
        return self.body.remove_item_from_equipment_slot(item, slot, num_slots)

    def remove_equipment_slot(self, slot):
        return self.body.remove_equipment_slot(slot)

    def add_equipment_slot(self, slot):
        return self.body.add_equipment_slot(slot)

    def get_items_in_equipment_slot(self, slot):
        return self.body.get_items_in_equipment_slot(slot)

    def get_nth_item_in_equipment_slot(self, slot, n):
        return self.body.get_nth_item_in_equipment_slot(slot, n)

    def get_gold(self):
        return self.gold

    def change_gold_amount(self, value):
        self.gold += value

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

    def defend(self):
        defense = self.armor + (self.endurance // 3)
        return defense

    def skill_damage_increase(self):
        return int(((self.intelligence) * 1.5 ) // 2)

    def skill_duration_increase(self):
        return (self.intelligence // 3)


    def grab(self, item, loop):
        if self.get_item(loop, item):
            loop.generator.item_map.remove_thing(item)
            loop.add_message("The " + str(self.parent.name) + " picked up a " + str(item.name))
            self.energy -= self.action_costs["grab"]

    def get_item(self, loop, item):
        if self.parent.has_trait("player"):
            self.parent.statistics.add_item_pickup_details(item)
        if item.yendorb:
            loop.change_loop("victory")
            return
        elif item.has_trait("gold"):
            self.change_gold_amount(item.amount)
            loop.change_loop(loop.currentLoop)
        elif item.stackable:
            if not item.name in [x.name for x in self.inventory]:
                if len(self.inventory) > self.inventory_limit:
                    loop.add_message("You need to drop something first")
                    return False
                else:
                    self.inventory.append(item)

            else:
                for i in range(len(self.inventory)):
                    if self.inventory[i].name == item.name:
                        self.inventory[i].stacks += 1
        else:
            if len(self.inventory) > self.inventory_limit:
                loop.add_message("You need to drop something first")
                return False
            else:
                self.inventory.append(item)
                if item.has_trait("book"):
                    item.mark_owner(self)
        return True
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
                item.x = self.parent.x
                item.y = self.parent.y
                item_map.place_thing(item)
                self.energy -= self.action_costs["drop"]
                return True
        return False

    def equip(self, item):
        if item.can_be_equipped(self):
            self.body.equip(item, self.strength)
            self.energy -= self.action_costs["equip"]

    def unequip(self, item):
        if item == None:
            return
        if item.can_be_unequipped(self):
            self.body.unequip(item)
            self.energy -= self.action_costs["unequip"]

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
        weapon = self.body.get_weapon()
        if not weapon:
            return self.base_damage + self.unarmed_damage_min, self.base_damage + self.unarmed_damage_max
        else:
            return self.base_damage + weapon.damage_min, self.base_damage + weapon.damage_max

    """
    1. Damage: Calculate how much damage opponent you would deal
    2. Chance to hit: dexterity vs dexterity affected by how heavy the armor is for both sides (% shave off damage?)
    2. On hit effects
    3. Armor: Armor flat damage decrease vs armor piercing 
    4. Take damage
    
    """
    def melee(self, defender, loop):
        self.energy -= self.action_costs["attack"]
        effect = None
        weapon = self.body.get_weapon()

        if weapon is None:
            damage = random.randint(self.base_damage + self.unarmed_damage_min, self.base_damage + self.unarmed_damage_max) #Should make object for unarmed damage
        else:
            if weapon.on_hit == None:
                damage = weapon.attack()
            else:
                damage, effect = weapon.attack() 

        dodge_damage = defender.character.dodge() - self.strike()

        damage_shave = 1 - ((min(dodge_damage, 0) // 10) / 10)

        if effect is not None and damage_shave == 0:
            effect = effect(self.parent) # some effects need an inflictor
            defender.character.add_status_effect(effect)

        effectiveness = 0
        if weapon is not None:
            defense = defender.character.defend() - weapon.armor_piercing
            for types in weapon.effective:
                if types in defender.attributes:
                    if defender.attributes[types] == True:
                        effectiveness += 1
                        loop.add_message("The attack is effective against {} as it is a {} type.".format(defender.name, types))
        else:
            defense = defender.character.defend()

        finalDamage = max(0, int((damage + self.base_damage) * damage_shave * (max(1,1.5 * effectiveness)) - defense))
        defender.character.take_damage(self.parent, finalDamage)
        return finalDamage

    def strike(self):
        strike_chance = random.randint(1,100) + self.dexterity * 2
        return min(100, strike_chance)


    def dodge(self):
        dodge_chance = random.randint(1,100) + self.dexterity * 2
        return (min(100, dodge_chance))

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
                    x.duration = effect.duration
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
    
    def get_enchantable(self):
        enchantable = []
        for item in self.inventory:
            if item.can_be_levelled:
                if item.level < 6: # items can be levelled upto +5
                    enchantable.append(item)
        return enchantable

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

