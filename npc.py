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
        loop.change_loop("trade")

    def take_gold(self, i, loop):
        if loop.player.character.gold >= self.cost:
            self.give_item(loop, i)
            loop.player.character.gold -= self.cost
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

    def welcome(self, loop):
        loop.messages = []
        loop.npc_focus = self

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
                loop.add_message(self.name + " says: 'Thanks to you those goblins have not been bothering me lately.'")
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

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                loop.add_message(self.name + " says: 'The Kingdom is now safe.'")
        else:
            self.talking = True
            loop.add_message(self.name + "'What's this? Another failure! I can't believe we spent so much to summon you from another dimension.'")
            self.talking_queue.append("Guards! Prepare another summoning! We can't fail again else we'll be overrun by the rift monsters. They are nearly at the palace portals!")
            self.talking_queue.append(
                "Why are you still here?!? Move along to the portal room and we'll be sorted out. Maybe you'll even manage to kill a goblin or two.")
            loop.player.add_quest(quest.KingdomQuest())
            self.gave_quest = True
            self.has_stuff_to_say = False

class Guard(NPC):
    def __init__(self, x, y, render_tag= 121, name="Guard"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk"]

        guard_dialogue_options = [
            # Encouraging dialogues
            "Another summoning, huh? Honestly, I don't know how much longer we can hold out. These rift monsters are relentless. We could really use some help out there.",
            "Stay alert and be ready for anything. Those rifts can spit out all sorts of nasty creatures. If you survive out there, you might just be the hero we need.",
            "Don't let the king's frustration get to you. He's under a lot of pressure. If you can make a difference, even a small one, it'll be worth it.",
            "It's chaos out there. Every day, more of our comrades fall. If you’ve got any fighting skills, now's the time to show them. We're counting on you.",
            "Archmage Thalor believes in you, and that's good enough for me. Just remember to watch your back and take down as many of those rift monsters as you can. Good luck.",

            # Cynical dialogues
            "Another one from the rift? Great, just what we need. Don’t get your hopes up, we've seen dozens of you come and go. None of them made much of a difference.",
            "Honestly, I wouldn't expect too much. These rift monsters are brutal, and we've been losing ground every day. Just try not to get yourself killed.",
            "The king's desperate, that's why he keeps summoning people like you. If you think you can survive out there, good luck. But don’t expect any miracles.",
            "Look, it's a mess out there. We've lost too many good soldiers already. If you can fight, fine, but I wouldn’t count on making it back in one piece.",
            "Thalor might have faith in you, but I'm not so sure. These rift beasts are something else. Do what you can, but don’t expect any hero’s welcome."
        ]
        self.dialogue = guard_dialogue_options[random.randint(0,len(guard_dialogue_options) - 1)]


    def talk(self, loop):
        loop.add_message(self.dialogue)
class BobBrother(Guard):
    def __init__(self, x, y, render_tag= 121, name="Bob's Brother"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options.append("Quest")
        self.has_stuff_to_say = True
        self.quest = quest.BrothersQuest()

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                loop.add_message(self.name + " says: 'Thank you for bringing my brother back.'")
        else:
            loop.add_message(
                self.name + " says: 'Please, I can't find my brother and the king won't let me leave my post. Can you find him for me?")
            loop.player.add_quest(quest.BrothersQuest())
            self.has_stuff_to_say = False
            self.gave_quest = True

class BobBrother(Guard):
    def __init__(self, x, y, render_tag= 121, name="Bob's Brother"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options.append("Quest")
        self.has_stuff_to_say = True
        self.quest = quest.BrothersQuest()

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                loop.add_message(self.name + " says: 'Thank you for bringing my brother back.'")
        else:
            loop.add_message(
                self.name + " says: 'Please, I can't find my brother and the king won't let me leave my post. Can you find him for me?")
            loop.player.add_quest(quest.BrothersQuest())
            self.has_stuff_to_say = False
            self.gave_quest = True

class Sensei(NPC):
    def __init__(self, x, y, render_tag= 123, name="Sensei"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk", "Quest"]
        self.has_stuff_to_say = True
        self.quest = quest.DojoQuest()

    def talk(self, loop):
        # super().talk(loop)
        loop.add_message(self.name + " says: 'No better place to train than surrounded by monsters.")
        loop.add_message(loop.player.name + " says: 'Who are you?'")
        loop.add_message(self.name + " doesn't seem to hear you.")

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                loop.add_message(self.name + " nods in acknolwedgement of your strength.")
        else:
            loop.add_message(self.name + " says: 'Think yourself a master of combat? Prove your training here by destroying this training dummy.'")
            loop.player.add_quest(quest.DojoQuest())
            self.gave_quest = True
            self.has_stuff_to_say = False

class Archmage(NPC):
    def __init__(self, x, y, render_tag= 123, name="Archmage Thalor"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk", "Quest"]
        self.has_stuff_to_say = True
        self.quest = quest.GoblinQuest()

    def talk(self, loop):
        if self.has_stuff_to_say:
            self.talking = True
            loop.add_message("'Ah, the latest summon. Listen carefully. Beyond these rifts lies a chaotic realm where monsters originate.'")
            self.talking_queue.append(
                "Your task is to stem the tide of creatures and find a way to close the rifts. Each rift you seal will hopefully weaken the others.")
            self.talking_queue.append("Or strengthen, we don't actually know.")
            self.talking_queue.append("But be warned, the deeper you go, the more powerful the monsters become.")
        else:
            loop.add_message(
                "'Now hurry along before more beasts emerge.'")

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                loop.add_message("'Keep up the good work.'")
        else:
            self.talking = True
            loop.add_message("'These beasts just keep coming through the rifts, don't they? I've managed to take care of this wave, but I can't be everywhere at once.'")
            self.talking_queue.append(
                "'Listen, I know you might just be an unfortunate soul pulled from another world. I wish I could offer more assistance, but our resources are stretched thin.'")
            self.talking_queue.append("'Prove your worth to me, and I can provide you with better support. Bring me back five goblin corpses, and we'll see what we can do for you.'")
            loop.player.add_quest(quest.GoblinQuest())
            self.gave_quest = True
            self.has_stuff_to_say = False
