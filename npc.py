import items as I
import objects as O
import loops as L
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
        loop.change_loop(L.LoopType.trade)

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
        pass
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
            loop.change_loop(L.LoopType.trade)

class Bob(NPC):
    def __init__(self, render_tag, x, y, name="Bob"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.quest = quest.GoblinQuest()

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
        super().talk(loop)
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

class King(NPC):
    def __init__(self, x, y, render_tag= 120, name="King"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Quest"]

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                loop.add_message(self.name + " says: 'The Kingdom is now safe.'")
        else:
            loop.add_message(self.name + " says: 'I have summoned you at great expense and with time quickly running out. The monsters grow stronger. Please defeat them.")
            loop.player.add_quest(quest.KingdomQuest())
            self.gave_quest = True

class Guard(NPC):
    def __init__(self, x, y, render_tag= 121, name="Guard"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options = ["Talk"]

    def talk(self, loop):
        super().talk(loop)
        loop.add_message(self.name + " says: 'Now move along.")

class BobBrother(Guard):
    def __init__(self, x, y, render_tag= 121, name="Bob's Brother"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)
        self.options.append("Quest")

    def give_quest(self, loop):
        if self.gave_quest == True:
            if self.quest.check_for_completion(loop):
                loop.add_message(self.name + " says: 'Thank you for bringing my brother back.'")
        else:
            loop.add_message(
                self.name + " says: 'Please, I can't find my brother and the king won't let me leave my post. Can you find him for me?")
            loop.player.add_quest(quest.BrothersQuest())
            self.gave_quest = True

