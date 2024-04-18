import items as I
import objects as O
import loops as L

class NPC(O.Objects):
    def __init__(self, render_tag, x, y, name="Unknown npc"):
        super().__init__(x, y, 0, render_tag= render_tag, name = name)
        self.name = name
        self.items = [I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300)]
        self.cost = 5
        self.purpose = None #Trade, gossip,
        self.quest_complete = False

    def change_purpose(self, purpose, loop):
        if purpose == "gossip":
            self.talk(loop)
            self.purpose = purpose
        elif purpose == "trade":
            self.trade(loop)
            self.purpose = purpose
        elif purpose == "quest":
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
        if self.quest_complete == False:
            if self.check_completetion(loop):
                loop.add_message(loop.player.name + " says: 'I got those little loot pin... I mean goblins.'")
                loop.add_message(self.name + " says: 'Finally, they won't be bothering me. Here's a little something to help you out.'")
                item = I.PermanentDexterityPotion(405, dexterity = 3)
                if loop.player.character.get_item(loop, item):
                    self.quest_complete = True
            else:
                loop.add_message(loop.player.name + " says: 'Anything I can help out with?'")
                loop.add_message(self.name + " says: 'Goblins. I hate those nasty buggers. They keep stealing all my stuff! If you kill 3 of them and bring me back proof, I can reward you handsomely' ;)")
        else:
            loop.add_message(self.name + " says: 'Thanks to you those goblins have not been bothering me lately.'")


    def check_completetion(self, loop):
        player = loop.player
        num_goblin_corpses = 0
        for item in loop.player.character.inventory:
            if isinstance(item, I.Corpse) and item.monster_type == "Goblin":
                num_goblin_corpses += 1
        if num_goblin_corpses == 3:
            return True
        else:
            return False

    def give_item(self, loop, number):
        player = loop.player
        item = self.items[number]
        if player.character.get_item(loop, item):
            self.items.pop(number)
            loop.change_loop(L.LoopType.trade)

class Bob(NPC):
    def __init__(self, render_tag, x, y, name="Bob"):
        super().__init__(x=x, y=y, render_tag = render_tag, name = name)

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
        loop.quest_recieved = True
        loop.player.quests.append("Succubus")
