from monster_implementation import monster_ai as ai
import objects as O
from character_implementation import character as C
import items as I
import skills as S


class Monster(O.Objects):
    def __init__(self, x=-1, y = -1, render_tag = -1, name="Unknown monster", experience_given = 0, brain = ai.Monster_AI, rarity ="Common", health = 10, min_damage = 2, max_damage=3):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.character = C.Character(self, health = health, min_damage=min_damage, max_damage = max_damage)
        self.asleep = False
        self.flee = False

        self.traits["monster"] = True
        self.attributes = {}

        self.stops_autoexplore = True
        self.gold_value = 1

        self.character.experience_given = experience_given
        self.brain = brain(self)
        self.skills = []
        self.orb = False
        self.rarity = rarity

        # parameter that is checked according to specific branch distributions, specific branches will write functions describing what a particular restriction does
        self.restriction = ""

        self.description = f"This is a {self.name}. It wants to eat you."

    def die(self):
        return

    def make_friendly(self):
        self.brain = ai.Friendly_AI(self)

    def move(self, move_x, move_y, loop):
        monster_map = loop.generator.monster_map
        generator = loop.generator
        if not self.character.movable:
            self.character.energy -= self.character.action_costs["move"]#(self.character.move_cost - self.character.dexterity)
            return

        #Monsters can move ontop of players
        if generator.get_passable((self.x + move_x, self.y + move_y)):
            self.character.energy -= self.character.action_costs["move"]
            monster_map.track_map[self.x][self.y] = -1
            self.y += move_y
            self.x += move_x
            monster_map.track_map[self.x][self.y] = self.id_tag
    

    def __str__(self):
        return self.name

class Kobold(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1010, name="Kobold"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=10,health=20)
        self.skills = []
        self.character.skills.append(S.BurningAttack(self, cooldown=10, cost=0, damage=10, burn_damage=4, burn_duration=5, range=1.5))
        self.character.health = 10
        self.character.max_health = 10
        self.endurance = 0
        self.strength = 0
        self.dexterity = 4
        self.intelligence = 4

        self.description = "A small, scaly creature with a mysterious satchel on its back."

        self.traits["kobold"] = True
        self.attributes["humanoid"] = True

class Squid(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1500, name="Squid"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=10,health=20)
        self.skills = []
        self.character.health = 10
        self.character.max_health = 10
        self.endurance = 0
        self.strength = 0
        self.dexterity = 4
        self.intelligence = 4

        self.description = "A small, squidlike creature lurking in the water."

        self.traits["squid"] = True
        self.attributes["water"] = True

class Leviathon(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1510, name="Leviathon"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=20,health=100)
        self.skills = []
        self.endurance = 0
        self.strength = 10
        self.dexterity = 4
        self.intelligence = 4

        self.description = "A massive, eel-like creature with bioluminescent patterns along its body. Its eyes glow a menacing red, and its mouth is filled with rows of razor-sharp teeth."

        self.traits["leviathon"] = True
        self.attributes["water"] = True

class ChasmCrawler(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1520, name="Chasm Crawler"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=20,health=100)
        self.skills = []
        self.endurance = 0
        self.strength = 10
        self.dexterity = 4
        self.intelligence = 4

        self.description = "Large, crab-like monsters with armored shells and glowing eyes. Their claws are immense and serrated."
        self.character.armor = 12
        self.traits["chasm_crawler"] = True
        self.attributes["water"] = True

class Slime(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1100, name="Slime"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=5, brain = ai.Slime_AI, health=5, min_damage=1, max_damage=1)

        self.description = "A small blob of experienc... I mean ooze."
        self.character.action_costs["grab"] = 0

        self.traits["slime"] = True

"""
GOBLIN
+ Finds and pickups items
- Melee combat
"""
class Goblin(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1000, name="Goblin", experience_given=10, health=10, min_damage=3, max_damage=5, rarity = "Common", brain = ai.Goblin_AI):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=experience_given, health=health, min_damage=min_damage, max_damage=max_damage, rarity = rarity, brain = brain)
        self.character.skills.append(S.Escape(self, cooldown=100, 
                                              cost=0, self_fear=True, 
                                              dex_buff=20, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=.2,
                                              action_cost=1))
        self.character.action_costs["move"] = 50
        self.character.action_costs["grab"] = 20

        self.description = "A cowardly creature that some adventurers nicknamed \"Loot Pinata\"."

        self.strength = 1
        self.dexterity = 1
        self.endurance = 0
        self.intelligence = 0

        self.traits["goblin"] = True
        self.attributes["humanoid"] = True

    def die(self):
        corpse = I.Corpse(self.x, self.y, -1, 2000, self.name + " Monster Corpse")
        corpse.monster_type = self.name #Should be fixed to monster type at some point
        return corpse

class Looter(Goblin):
    def __init__(self, x=-1, y=-1, render_tag=1009, name="Looter", experience_given=25, health=100, min_damage=3,
                 max_damage=8, rarity="Rare"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name, experience_given=experience_given, health=health,
                         min_damage=min_damage, max_damage=max_damage, rarity=rarity)
        self.character.action_costs["move"] = 25
        self.character.action_costs["grab"] = 1

        self.traits["looter"] = True

class GoblinShaman(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1001, name="Goblin Shaman", activation_threshold=0.4):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.orb = True
        self.character.skills = []
        self.character.skills.append(S.SummonGoblin(self, cooldown=15, cost=0, range=4,action_cost=20))
        self.character.skills.append(S.Escape(self, cooldown=100,
                                              cost=0, self_fear=True,
                                              dex_buff=20, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=activation_threshold,
                                              action_cost=1))
        self.character.experience_given = 25
        self.description = "What's more cowardly than summoning your pals?"
        self.character.health = 20
        self.character.max_health = 20
        self.strength = 1
        self.dexterity = 1
        self.endurance = 1
        self.intelligence = 1
        self.character.armor = 0

class Hobgoblin(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1002, name="Hobgoblin"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character.skills = []
        self.character.skills.append(S.BlinkStrike(self, cooldown=10, cost=0, damage=15, range=5, action_cost=1))
        self.character.skills.append(S.Escape(self, cooldown=100, 
                                              cost=0, self_fear=True, 
                                              dex_buff=30, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=0.3, 
                                              action_cost=1))
        self.character.experience_given = 10
        self.description = "The older cousin of its smaller green relatives."
        self.character.health = 25
        self.character.max_health = 25
        self.strength = 15
        self.dexterity = 5
        self.endurance = 10
        self.intelligence = 4
        self.character.armor = 0



class Gargoyle(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1020, name="Gargoyle"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.endurance = 5
        self.strength = 3
        self.dexterity = 1
        self.intelligence = 1
        self.skills = []
        # 30% chance to petrify for 3 turns
        self.character.skills.append(S.Petrify(self, cooldown=10, cost=0, duration=3, activation_chance=0.3, range=3))
        self.character.experience_given = 20

        self.description = "A stone creature that you feel could petrify you if it was rounder."
        self.character.health = 20
        self.character.max_health = 20
        self.strength = 2
        self.dexterity = 0
        self.endurance = 6
        self.intelligence = 5
        self.character.armor = 3

class Minotaur(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1040, name="Minotaur"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character.skills = []
        self.character.skills.append(S.ShrugOff(self, cooldown=3, cost=0, activation_chance=0.75, action_cost=1))
        self.character.experience_given = 20
        self.description = "A large, angry bull with mighty horns."
        self.character.health = 40
        self.character.max_health = 40
        self.character.move_cost = 80
        self.strength = 5
        self.dexterity = 2
        self.endurance = 3
        self.intelligence = 0
        self.character.armor = 0
"""
ORC
+ Combat
- Not very smart
"""
class Orc(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1070, name="Orc", experience_given=20, health=30, min_damage=5, max_damage=10, rarity = "Common"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=experience_given, health=health, min_damage=min_damage, max_damage=max_damage, rarity = rarity)
        self.character.skills = []
        # below 25% health, gains 25 strength
        self.character.skills.append(S.Berserk(self, cooldown=0, cost=0, duration=-100, activation_threshold=0.25, strength_increase=10, action_cost=1))
        self.description = "A strong humanoid with anger issues."
        self.strength = 3
        self.dexterity = 0
        self.endurance = 3
        self.intelligence = 0
        self.character.armor = 1

class Bobby(Orc):
    def __init__(self, x=-1, y=-1):
        super().__init__(x=x, y=y, render_tag=1079, name="Bobby", experience_given=45, health=50,
                     min_damage=10, max_damage=20, rarity="Rare")

#########

class Golem(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1080, name="Golem"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character.skills = []
        self.character.experience_given = 30
        self.description = "A large, slow creature made of stone."
        self.character.health = 25
        self.character.max_health = 25
        self.character.move_cost = 200
        self.strength = 2
        self.dexterity = 10
        self.endurance = 2
        self.intelligence = 2
        self.character.armor = 1
        self.attributes["stone"] = True
        self.restriction = "deep water"

class Raptor(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1030, name="Velociraptor"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character.move_cost = 50
        self.character.health = 20
        self.character.max_health = 20
        self.strength = 5
        self.dexterity = 12
        self.endurance = 0
        self.intelligence = 0
        self.character.armor = 0

        self.character.experience_given = 30
        self.description = "A very fast and very angry dinosaur."

class Tormentorb(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1050, name="Tormentorb"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character.skills = []
        self.orb = True
        # self, parent, cooldown, cost, slow_duration, damage_percent, slow_amount, range, action_cost
        self.character.skills.append(S.Torment(self, cooldown=10, cost=0, slow_duration=3, damage_percent=0.5, slow_amount=5, range=4, action_cost=100))
        self.character.experience_given = 65
        self.description = "A floating orb that can torment and slow you with its gaze."
        self.character.health = 45
        self.character.max_health = 45
        self.strength = 8
        self.dexterity = 8
        self.endurance = 8
        self.intelligence = 8
        self.character.armor = 6

class Stumpy(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1090, name="Stumpy"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.brain = ai.Stumpy_AI(self)
        self.character.experience_given = 20
        self.description = "An evil stump that wants revenge for its dead brethren."
        self.character.health = 10
        self.character.max_health = 10
        self.strength = 8
        self.dexterity = 8
        self.endurance = 8
        self.intelligence = 8
        self.character.armor = 10
        self.attributes["wood"] = True

class Dummy(Monster):
    def __init__(self, x=-1, y=-1, render_tag=124, name="Training Dummy"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.brain = ai.Dummy_AI(self)
        self.character.experience_given = 0
        self.description = "A training dummy that will not move or attack, but seems to repair itself if not one-shot."
        self.character.health = 25
        self.character.max_health = 25
        self.strength = 0
        self.dexterity = 0
        self.endurance = 0
        self.intelligence = 0
        self.character.armor = 0
        self.attributes["wood"] = True
        self.traits["dummy"] = True
        self.character.health_regen = 50
        self.stops_autoexplore = False
        remnants = I.DestroyedDummy()
        self.character.inventory.append(remnants)
        self.gold_value = 0

class BossOrb(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1060, name="ORB OF YENDORB"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.character.skills = []
        self.character.inventory.append(I.OrbOfYendorb())
        self.orb = True
        # self, parent, cooldown, cost, slow_duration, damage_percent, slow_amount, range, action_cost
        self.character.skills.append(S.Torment(self, cooldown=10, cost=0, slow_duration=3, damage_percent=0.5, slow_amount=5, range=4, action_cost=100))
        self.character.skills.append(S.Heal(self, cooldown = 20, cost = 10, heal_amount = 40, activation_threshold = .25, action_cost = 100))
        self.character.skills.append(S.Invinciblity(self, cooldown=1000, cost=0, duration=8, activation_threshold=0.1, by_scroll=False))

        self.character.experience_given = 0 # otherwise this inflates the outputted final levle
        self.description = "The orb of all orbs, the orbiest of orbs, the archetype of orbs... you get the idea."
        self.character.health = 45
        self.character.max_health = 45

        self.character.move_cost = 75
        self.character.attack_cost = 75
        self.strength = 18
        self.dexterity = 18
        self.endurance = 18
        self.intelligence = 18
        self.character.armor = 10

