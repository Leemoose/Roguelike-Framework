from monster_implementation import monster_ai
import objects as O
from character_implementation import character as C
from character_implementation import Inventory, Body, Fighter
import items as I
import skills as S


class Monster(O.Objects):
    def __init__(self, x=-1, y = -1, render_tag = -1, name="Unknown monster", experience_given = 0, brain = monster_ai.Monster_AI, rarity ="Common", health = 10, min_damage = 2, max_damage=3):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.character = C.Character(self, health = health)
        self.brain = brain(self)
        self.inventory = Inventory(self)
        self.body = Body(self)
        self.fighter = Fighter(self, min_damage=min_damage, max_damage = max_damage)

        self.asleep = False
        self.flee = False
        self.nightified = False

        self.traits["monster"] = True
        self.attributes = {}

        self.stops_autoexplore = True
        self.gold_value = 1

        self.character.experience_given = experience_given
        self.skills = []
        self.orb = False
        self.rarity = rarity

        self.stored_day_powers = []

        # parameter that is checked according to specific branch distributions, specific branches will write functions describing what a particular restriction does
        self.restriction = ""

        self.description = f"This is a {self.name}. It wants to eat you."

    def get_inventory(self):
        return self.inventory.get_inventory()

    def do_attack(self, target, loop):
        #Make sure to add energy cost here
        self.fighter.do_attack(target, loop)

    def do_grab(self, item, loop):
        if self.inventory.can_grab(item) and self.character.can_grab(item):
            # add time
            self.inventory.do_grab(item, loop)
            return True
        else:
            return False

    def do_drop(self, item, item_map):
        if self.inventory.can_drop(item) and self.character.can_drop(item):
            #add time
            self.inventory.do_drop(item, item_map)
            return True
        else:
            return False

    def die(self):
        return

    def make_friendly(self):
        self.brain = monster_ai.Friendly_AI(self)

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

    def nightify(self):
        if not self.nightified:
            self.nightified = True
            max_health_change = self.character.get_max_health()
            health_change = self.character.get_health()
            self.asleep = False
            self.character.change_max_health(max_health_change)
            self.character.change_health(health_change)
            self.stored_day_powers = [max_health_change, health_change]

    def dayify(self):
        if self.nightified:
            self.nightified = False
            max_health_change, health_change = self.stored_day_powers
            self.character.change_max_health(-max_health_change)
            self.character.change_health(-health_change)
            self.stored_day_powers = []

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

        self.description = "Covered in reddish-brown scales that radiate heat, Infernal Kobolds possess razor-sharp claws and teeth. They worship a distant star whose fiery essence imbues them with a burning touch, capable of igniting flammable materials. Despite their small size, they are cunning ambushers, using their fiery abilities to deadly effect in battle. Their eyes glow with reverence and cunning, reflecting their devotion to the star's fiery power."

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

        self.description = "A small, frail creature that lacks any mysterious power. Its translucent body shimmers with bioluminescent patterns, emitting a faint glow in the dark rift waters. With delicate, tentacle-like appendages, it navigates the currents with grace but lacks offensive capabilities. Despite its vulnerability, the Rift Squidling possesses keen survival instincts, using camouflage and swift movements to evade predators. It is often preyed upon by larger rift creatures, making it a common sight in the perilous depths of the rifts."

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

        self.description = "The Chasm Crawler is a formidable predator of the rocky depths, adorned in thick, chitinous armor that seamlessly blends with its environment. With a segmented body designed for agility and strength, it maneuvers effortlessly through both submerged caverns and dry rocky terrain. Equipped with powerful mandibles capable of crushing solid stone, it tunnels through rock formations with remarkable ease. This semi-aquatic creature patrols its territory with vigilance, defending its hunting grounds against intruders with swift, precise strikes."
        self.character.armor = 12
        self.traits["chasm_crawler"] = True
        self.attributes["water"] = True

class Slime(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1100, name="Slime"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=5, brain = monster_ai.Slime_AI, health=5)

        self.description = "These amorphous blobs of translucent, gelatinous matter emerge from the depths of the rifts. Their bodies pulse with a sickly green glow, fueled by the chaotic energies of their environment. Rift Slimes mindlessly dissolve anything they touch with acidic secretions, leaving behind only a faint, acrid odor. They show no preference or intelligence, simply drawn to any items they encounter, which they swiftly corrode beyond recognition.."
        self.character.action_costs["grab"] = 0

        self.traits["slime"] = True

"""
GOBLIN
+ Finds and pickups items
- Melee combat
"""
class Goblin(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1000, name="Goblin", experience_given=10, health=10, min_damage=3, max_damage=5, rarity = "Common", brain = monster_ai.Goblin_AI):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name, experience_given=experience_given, health=health, min_damage=min_damage, max_damage=max_damage, rarity = rarity, brain = brain)
        self.character.skills.append(S.Escape(self, cooldown=100, 
                                              cost=0, self_fear=True, 
                                              dex_buff=20, str_debuff=20, int_debuff=20, haste_duration=-100,
                                              activation_threshold=.2,
                                              action_cost=1))
        self.character.action_costs["move"] = 50
        self.character.action_costs["grab"] = 20

        self.description = "These mischievous creatures are smaller and wiry compared to their larger counterparts. Their green skin is mottled and rough, often adorned with patches of scavenged armor and trinkets. With quick, darting eyes that gleam with greed, Goblins are driven by an insatiable desire for shiny objects and valuables. They scurry through the rift-ridden landscapes with nimble steps, their clawed hands eagerly snatching up any glittering loot they come across."

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
        self.description =  "A twisted figure draped in tattered robes adorned with crude bones and fetishes, the Rift Goblin Shaman is a malevolent conduit of dark magic. With hunched posture and gnarled fingers clutching a gnarled staff, its yellowed eyes gleam with a sinister intelligence. The Shaman’s skin is marked with mystical runes that pulse with a sickly green glow, channeling the chaotic energies of the rifts. Surrounded by an aura of foul incense and the echoing chants of ancient rituals, it commands the loyalty of lesser goblins who scurry at its command. With a crooked grin revealing jagged teeth stained with blood, the Shaman unleashes curses and hexes upon its enemies, weakening their resolve and bolstering its minions. In battle, it summons swarms of lesser goblins from the rifts, overwhelming foes with sheer numbers and dark magic. Beware the Shaman’s cunning and its ability to twist the very fabric of reality to serve its malicious whims."
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

        self.description = "Carved from ancient stone and imbued with dark magic from the depths of the rifts, the Rift Gargoyle is a sentinel of terror and stone-cold fury. Perched high atop jagged spires and crumbling ruins, its chiseled form blends seamlessly with the twisted architecture of the rifts. With wings stretched wide, resembling weathered stone veined with veins of iridescent minerals, the Gargoyle looms over its domain like a silent sentinel. Glowing eyes, a pale azure hue, pierce the darkness with an otherworldly gleam, ever vigilant for intruders. Its clawed hands grip the stone tightly, ready to unleash its wrath upon any who dare to disturb its ancient slumber. When provoked, the Gargoyle descends with a thunderous flap of its wings, striking with swift and precise attacks. Its petrifying gaze and ability to turn ethereal make it a formidable foe, capable of shifting between dimensions to elude attackers."
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
        self.description = "Hailing from the brutal and war-torn realms beyond the rifts, the Orc is a towering brute with muscles rippling beneath its coarse, green skin. Adorned in crude armor fashioned from bones and scavenged metal, its bloodshot eyes burn with a fierce determination for battle. The stench of blood and sweat follows this savage warrior, who wields a jagged, rusted blade with deadly proficiency. Covered in tribal tattoos and scars earned in countless skirmishes, the Rift Orc thrives in combat, reveling in the chaos of battle cries and the clash of weapons. Its growls and guttural shouts echo through the rifts, striking fear into the hearts of all who dare to oppose it. Beware its raw strength and relentless aggression, for the Orc knows no mercy on the battlefield.."
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
        self.description = "Forged from the very bedrock of the earth and brought to life by ancient, powerful magic, the Stone Golem is a formidable guardian. Towering and imposing, its massive body is composed of jagged boulders and smooth stones, seamlessly held together by an unyielding mystical force. Glowing runes etched into its surface pulse with a dim, ethereal light, a testament to the ancient spell that animates it. The Stone Golem's eyes, deep-set and glowing with a fierce, unearthly light, scan its surroundings for any threat. With strength rivaling that of the mountains themselves, it can crush anything in its path with its colossal, stone fists. Slow but relentless, the Stone Golem is an unstoppable force of nature, driven by an unbreakable duty to protect its domain.."
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
        self.description = "The Raptor is a terrifying predator from an ancient era. Its sleek, scaly body is covered in iridescent feathers that shimmer with otherworldly hues. With razor-sharp claws and teeth honed to perfection, it moves with lethal grace and speed. The Raptor’s eyes, glowing with a predatory intelligence, lock onto its prey with unerring precision. This cunning hunter uses the shadows and its surroundings to its advantage, striking with blinding speed and ruthless efficiency. Beware its shrill, haunting screech that echoes through the rift, a prelude to the deadly hunt that follows.."

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


class Dummy(Monster):
    def __init__(self, x=-1, y=-1, render_tag=124, name="Training Dummy"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.brain = monster_ai.Dummy_AI(self)
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
        self.inventory.inventory.append(remnants)
        self.gold_value = 0

class BossOrb(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1060, name="ORB OF YENDORB"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.character = C.Character(self)
        self.character.skills = []
        self.inventory.inventory.append(I.OrbOfYendorb())
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

"""
Forest Monsters: Generally wood or animal like. Grow stronger at night. Uses poison
"""

class Stumpy(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1100, name="Stumpy"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.brain = monster_ai.Stumpy_AI(self)
        self.character.experience_given = 20
        self.description = "An ancient, gnarled tree stump brought to life by dark magic, Stumpy harbors a deep, burning desire for vengeance. Its twisted roots writhe with malicious intent, and its hollow eyes glow with a sinister, green light. With bark as tough as iron and splintered limbs that lash out like whips, this vengeful stump seeks retribution for the countless trees felled by human hands. Beware its crushing roots and poisonous sap, for Stumpy will stop at nothing to avenge its fallen brethren."
        self.character.health = 10
        self.character.max_health = 10
        self.strength = 8
        self.dexterity = 8
        self.endurance = 8
        self.intelligence = 8
        self.character.armor = 10
        self.attributes["wood"] = True
        self.traits["stumpy"] = True

class Treant(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1120, name="Treant"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.brain = monster_ai.Monster_AI(self)
        self.character.experience_given = 40
        self.description = "Towering over the forest canopy, the Treant is a massive and malevolent guardian with bark-covered armor tough as iron. Its glowing green eyes and deep, rumbling growl instill fear in all who hear it. Driven by an ancient grudge, it uses a devastating root lash attack to ensnare and immobilize foes, protecting its sacred domain with relentless strength. The Treant’s presence warps the forest, darkening and twisting the environment as it exacts vengeance on any who defile its home."
        self.character.health = 50
        self.character.max_health = 50
        self.strength = 8
        self.dexterity = 8
        self.endurance = 8
        self.intelligence = 8
        self.character.armor = 15
        self.attributes["wood"] = True
        self.traits["treant"] = True
        #Remember to add on hit effect for ensnaring
        """
        Treant
Characteristic: Lots of health
Vulnerable: Fire
Abilities: Ground Stomp
On hit: Root lash (extra damage, immobile)
        """

class Spider(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1110, name="Spider"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.brain = monster_ai.Monster_AI(self)
        self.character.experience_given = 10
        self.description = "These black and white spiders, each the size of a small dog, are swift and deadly predators of the forest. With their distinctive striped patterns, they move with alarming speed, darting through the underbrush and leaping onto unsuspecting prey. Their agile legs and sharp mandibles allow them to navigate any terrain, while their ability to weave intricate webs on tiles makes them formidable hunters and trappers. A single bite from a Rift Spider delivers potent poison, weakening and paralyzing its victims. Beware their sudden, silent approach and the venomous sting that follows, for these spiders are relentless and deadly in their pursuit."
        self.character.health = 10
        self.character.max_health = 10
        self.strength = 2
        self.dexterity = 8
        self.endurance = 2
        self.intelligence = 1
        self.character.armor = 0
        self.traits["spider"] = True
        """
        Big spiders
Characteristic: Can move fast
Abilities: Create web on tile
On hit: Poison / stun?
        """

class MetallicBear(Monster):
    def __init__(self, x=-1, y=-1, render_tag=0, name="Metallic Bear"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.brain = monster_ai.Monster_AI(self)
        self.character.experience_given = 40
        self.description = "This imposing creature, with fur interwoven with metallic threads, gleams ominously as it prowls through the forest. Its powerful, ironclad muscles and razor-sharp claws make it a fearsome opponent. When the Metallic Bear’s health drops low, it enters a terrifying fury mode, its eyes glowing with an intense, fiery light. In this state, it becomes even more dangerous, dealing increased damage and attacking with blinding speed. The sound of clashing metal and its ferocious roars echo through the trees, warning all who dare to challenge it of the deadly rage that lies within."
        self.character.health = 30
        self.character.max_health = 30
        self.strength = 20
        self.dexterity = 8
        self.endurance = 20
        self.intelligence = 1
        self.character.armor = 20
        self.traits["metallic_bear"] = True

        """
        Metallic bear
Characteristic:
Vulnerable:
Abilities: Fury (low on health goes beserk)
On hit:
        """

class InsectNest(Monster):
    def __init__(self, x=-1, y=-1, render_tag=0, name="Insect Nest"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.brain = monster_ai.Monster_AI(self)
        self.character.experience_given = 40
        self.description = "Nestled within the forest, this immobile structure is a pulsating hive of malevolent activity. Each strike against the Insect Nest provokes a swarm of flying, poisonous insects that emerge in a frenzied cloud to defend their home. Though these insects are fragile and have low health, their venomous bites can quickly overwhelm and debilitate their attackers. The nest itself is otherwise powerless, relying entirely on the relentless defense of its swarming guardians to deter any who would seek to destroy it. Approach with caution, for disturbing the nest unleashes a torrent of venomous fury."
        self.character.health = 10
        self.character.max_health = 10
        self.strength = 0
        self.dexterity = 0
        self.endurance = 0
        self.intelligence = 0
        self.character.armor = 0
        self.traits["insect_nest"] = True

"""
Yellow Jacket Nest
Characteristic: Hit it and swarms pop out
Vulnerable: Fire
Abilities: When hit summons enemies
On hit:
"""