import random

import objects as O
import quest

class NPC(O.Objects):
    def __init__(self, render_tag, x, y, name="Unknown npc"):
        super().__init__(x, y, 0, render_tag= render_tag, name = name)
        self.name = name
        self.items = []
        self.cost = 5
        self.purpose = None #Trade, gossip,
        self.gave_quest = False
        self.quest = None
        self.options = ["Talk", "Trade", "Quest"]
        self.has_stuff_to_say = False
        self.talking = False #In the midst of talking
        self.talking_queue = []
        self.dialogue_memory = []
        self.dialogue_file = "npc_dialogue/default.txt"
        self.init_dialogue_queue()
        self.traits["npc"] = True

    def init_dialogue_queue(self):
        # a series of data structures that different dialogue flags need to efficiently manipulate dialogue flow
        self.dialogue_queue = [] # stores dialogue in easy to track order
        self.dialogue_dict = {} # stores indices of each dialogue, keyed by dialogues
        self.repeat_dict = {} # store dialogues that if not selected by player should be appended to end of dialoque queue at index stored in value
        self.trait_dict = {} # stores dialogues tied to ! and ? flags

        with open(self.dialogue_file) as df:
            lines = df.readlines()
            for line in lines:
                if line[0] == "#" or line.strip() == "":
                    continue
                dialogue_index, dialogue = line.split(" ", 1) # split only on first space
                dialogue = dialogue.strip() # remove trailing whitespace
                player = False
                # special markers: "-" -> player dialogue
                #                  "!" -> set trait 
                #                  "?" -> conditional on trait
                to_add = []
                special_markers = ["-", "!", "?", "@"] 
                while dialogue[0] in special_markers:
                    if dialogue[0] == "-":
                        player = True
                        dialogue = dialogue.split(" ", 1)[1].strip() # split on first space again to remove the "-"
                    if dialogue[0] == "!": 
                        trait, dialogue = dialogue.split(" ", 1)
                        trait = trait[1:] # trait is in format !trait, strip leading !
                        dialogue = dialogue.strip()
                        to_add.append((trait, True)) # second param is whether setting or checking trait
                    if dialogue[0] == "?":
                        trait, dialogue = dialogue.split(" ", 1)
                        trait = trait[1:] # trait is in format ?trait, strip leading ?
                        dialogue = dialogue.strip()
                        to_add.append((trait, False)) # second param is whether setting (True) or checking (False) trait
                    if dialogue[0] == "@":
                        idx, dialogue = dialogue.split(" ", 1)
                        if len(idx) == 1:
                            idx = 1000 # default to high number if idx is not specified with @
                        else:
                            idx = int(idx[1:])
                        dialogue = dialogue.strip()
                        self.repeat_dict[dialogue] = idx
                add_to_queue = True
                for trait, set_or_check in to_add:
                    if not dialogue in self.trait_dict.keys():
                        self.trait_dict[dialogue] = []
                    self.trait_dict[dialogue].append((trait, player, set_or_check))
                    if not set_or_check and not self.has_trait(trait):
                        add_to_queue = False
                self.dialogue_dict[dialogue] = int(dialogue_index)
                if add_to_queue:
                    self.insert_into_dialogue_queue(dialogue, player)

    def change_purpose(self, purpose, loop):
        if isinstance(purpose, int):
            if purpose - 1 >= 0 and purpose -1 < len(self.options):
                purpose = self.options[purpose-1]
            else:
                print("You have a weird purpose")
        if purpose == "Talk":
            self.talk(loop)
            self.purpose = purpose
        elif purpose == "Trade":
            self.trade(loop)
            self.purpose = purpose
        elif purpose == "Quest":
            self.purpose = purpose
            self.give_quest(loop)

    def add_to_memory(self, text, left, choice, action, loop):
        self.dialogue_memory.append((text, left, choice, action))
        if not choice and text in self.trait_dict.keys():
            for trait, _, set_or_check in self.trait_dict[text]:
                if set_or_check:
                    self.traits[trait] = True
                    self.check_dialogues_to_add()
                    self.check_focus(loop)

    # subclasses can overwrite this to determine which dialogue traits affect npc_focus
    def check_focus(self, loop):
        if self.has_trait("quest_given"):
            self.change_purpose("Quest", loop)

    def check_dialogues_to_add(self):
        # import pdb; pdb.set_trace()
        for text, trait_list in self.trait_dict.items():
            added = False
            for (trait, player, set_or_check) in trait_list:
                if not set_or_check and self.has_trait(trait):
                    self.insert_into_dialogue_queue(text, player)
                    self.trait_dict[text].remove((trait, player, set_or_check)) # remove dialogue from trait list so we don't keep adding it to queue


    def insert_into_dialogue_queue(self, dialogue, player):
        idx = self.dialogue_dict[dialogue]
        idx_to_insert = len(self.dialogue_queue)
        for i, d in enumerate(self.dialogue_queue):
            conv_idx = self.dialogue_dict[d[0]]
            if conv_idx == idx:
                self.dialogue_queue[i].insert(-1, dialogue)
                return
            if idx < conv_idx:
                idx_to_insert = i
                break
        self.dialogue_queue.insert(idx_to_insert, [dialogue, player])
        

    def take_gold(self, i, loop):
        if loop.player.inventory.get_gold() >= self.cost:
            self.give_item(loop, i)
            loop.player.inventory.change_gold_amount(-self.cost)
            loop.add_message(
                self.name + " says: 'Ahhh yes, precious gold. You can take that item.'")
        else:
            loop.add_message(
                self.name + " says: 'You don't have enough gold my friend.'")


    def trade(self, loop):
        pass

    def talk(self, loop):
        loop.add_message(
            self.name + " says: 'Move along now.'")

    def interact(self, loop):
        loop.messages = []
        loop.npc_focus = self
        loop.change_loop("trade")
    def give_quest(self, loop):
        pass
    def give_item(self, loop, number):
        player = loop.player
        item = self.items[number]
        if player.character.get_item(loop, item):
            self.items.pop(number)
            loop.change_loop("trade")
    def continue_talking(self, loop):
        loop.add_message(self.talking_queue.pop(0))
        if len(self.talking_queue) == 0:
            self.talking = False

class Bob(NPC):
    def __init__(self, render_tag, x, y, name="Bob"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.quest = quest.GoblinQuest()
        self.has_stuff_to_say = True

    def welcome(self, loop):
        super().welcome(loop)
        loop.add_message(self.name + " says: 'I see you have survived til now. Not a very impressive feat to be honest."
                                     " Charles the blacksmith's son, he came down this way once to show off to his friends."
                                     " Never made it back. A shame really. There's something in the air, some miasma as you trek deeper and deeper...'")

    def trade(self, loop):
        super().trade(loop)
        loop.add_message(loop.player.name + " says: 'Enough with the chit chat. What do you have that can help me out?'")
        loop.add_message(
            self.name + " says: 'See for yourself. Nothing special but it'll get the job done.'")

    def talk(self, loop):
        # super().talk(loop)
        loop.add_message(self.name + " says: 'I didn't scare you off already? There is something foul afoot here. Young boys go missing every month."
                                     "The seamstress says there's a demon involved, sucking the souls out and leaving nothing but bones."
                                     " It's an old wives tale. My bet is they're sneaking off to the war.'")

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                self.traits["quest_completed"] = True
                self.check_dialogues_to_add()
                self.check_focus(loop)
                # loop.add_message(self.name + " says: 'Thanks to you those goblins have not been bothering me lately.'")
        else:
            loop.add_message(loop.player.name + " says: 'Anything I can help out with?'")
            loop.add_message(self.name + " says: 'Goblins. I hate those nasty buggers. They keep stealing all my stuff! If you kill 3 of them and bring me back proof, I can reward you handsomely' ;)")
            loop.player.add_quest(quest.GoblinQuest())
            self.gave_quest = True
            self.has_stuff_to_say = False

class King(NPC):
    def __init__(self, x, y, render_tag= 120, name="King Aldric"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Quest"]
        self.has_stuff_to_say = True # separate variable from gave_quest in case we want traders to keep this icon
        self.quest = quest.KingdomQuest()
        self.dialogue_file = "npc_dialogue/king.txt"
        self.init_dialogue_queue()

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                self.traits["quest_completed"] = True
                self.check_dialogues_to_add()
                self.check_focus(loop)
                # loop.add_message(self.name + " says: 'The Kingdom is now safe.'")
        else:
            self.talking = True
            # loop.add_message(self.name + "'What's this? Another failure! I can't believe we spent so much to summon you from another dimension.'")
            # self.talking_queue.append("Guards! Prepare another summoning! We can't fail again else we'll be overrun by the rift monsters. They are nearly at the palace portals!")
            # self.talking_queue.append(
            #     "Why are you still here?!? Move along to the portal room and we'll be sorted out. Maybe you'll even manage to kill a goblin or two.")
            loop.player.add_quest(quest.KingdomQuest())
            self.gave_quest = True
            self.has_stuff_to_say = False

class Guard(NPC):
    def __init__(self, x, y, render_tag= 121, name="Guard"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk"]
        self.dialogue_file = "npc_dialogue/guard.txt"
        self.init_dialogue_queue()
    def talk(self, loop):
        loop.add_message(self.dialogue)

class BobBrother(Guard):
    def __init__(self, x, y, render_tag= 121, name="Bob's Brother"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options.append("Quest")
        self.has_stuff_to_say = True
        self.quest = quest.BrothersQuest()
        self.dialogue_file = "npc_dialogue/bobbrother.txt"
        self.init_dialogue_queue()

    def check_focus(self, loop):
        if self.has_trait("quest_given"):
            self.change_purpose("Quest", loop)

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                self.traits["quest_completed"] = True
                self.check_dialogues_to_add()
                self.check_focus(loop)
                # loop.add_message("Thank you... thank you for bringing him back. I feared the worst, but seeing him... it’s heartbreaking. I owe you more than I can ever repay. At least now, he can have a proper farewell. You’ve given us closure, and for that, I am eternally grateful.")
        else:
            # loop.add_message("Please, you have to help me. My brother got lost in one of those cursed rifts, and I can't leave my post to search for him. I'm begging you, find him and bring him back. I'll owe you everything if you do.")
            loop.player.add_quest(quest.BrothersQuest())
            self.has_stuff_to_say = False
            self.gave_quest = True

class Sensei(NPC):
    def __init__(self, x, y, render_tag= 123, name="Sensei"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk", "Quest"]
        self.has_stuff_to_say = True
        self.quest = quest.DojoQuest()
        self.dialogue_file = "npc_dialogue/sensei.txt"
        self.init_dialogue_queue()

    def talk(self, loop):
        super().talk(loop)
        # loop.add_message(self.name + " says: 'No better place to train than surrounded by monsters.")
        # loop.add_message(loop.player.name + " says: 'Who are you?'")
        # loop.add_message(self.name + " doesn't seem to hear you.")

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                self.traits["quest_completed"] = True
                self.check_dialogues_to_add()
                self.check_focus(loop)
                # loop.add_message(self.name + " nods in acknolwedgement of your strength.")
        else:
            # loop.add_message(self.name + " says: 'Think yourself a master of combat? Prove your training here by destroying this training dummy.'")
            loop.player.add_quest(quest.DojoQuest())
            self.gave_quest = True
            self.has_stuff_to_say = False

class Mage(NPC):
    def __init__(self, x, y, render_tag= 126, name="Mage"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk"]
        self.has_stuff_to_say = False
        self.dialogue_file = "npc_dialogue/mage.txt"
        self.init_dialogue_queue()

    def talk(self, loop):
        if self.has_stuff_to_say:
            self.talking = True

class Archmage(NPC):
    def __init__(self, x, y, render_tag= 126, name="Archmage Thalor"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk", "Quest"]
        self.has_stuff_to_say = True
        self.quest = quest.GoblinQuest()
        self.dialogue_file = "npc_dialogue/archmage.txt"
        self.init_dialogue_queue()

    def talk(self, loop):
        if self.has_stuff_to_say:
            self.talking = True

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                self.traits["quest_completed"] = True
                self.check_dialogues_to_add()
                self.check_focus(loop)
                # loop.add_message("'Keep up the good work.'")
        else:
            self.talking = True
            # loop.add_message("'These beasts just keep coming through the rifts, don't they? I've managed to take care of this wave, but I can't be everywhere at once.'")
            # self.talking_queue.append(
            #     "'Listen, I know you might just be an unfortunate soul pulled from another world. I wish I could offer more assistance, but our resources are stretched thin.'")
            # self.talking_queue.append("'Prove your worth to me, and I can provide you with better support. Bring me back five goblin corpses, and we'll see what we can do for you.'")
            loop.player.add_quest(quest.GoblinQuest())
            self.gave_quest = True
            self.has_stuff_to_say = False

class ForestHermit(NPC):
    def __init__(self, x=-1, y=-1, render_tag= 3100, name="Forest Hermit"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk"]
        self.has_stuff_to_say = False
        self.dialogue_file = "npc_dialogue/foresthermit.txt"
        self.init_dialogue_queue()

    def talk(self, loop):
        self.talking = True
