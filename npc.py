import items as I
import objects as O
import loops as L

class NPC(O.Objects):
    def __init__(self, render_tag, x, y, name="Unknown npc"):
        super().__init__(x, y, 0, render_tag, name)
        self.name = "Bob"
        self.items = [I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300)]
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

    def trade(self, loop):
        loop.add_message(loop.player.name + " says: 'You got anything to trade?'")
        loop.add_message(
            self.name + " says: 'I may have an ax or two...'")

    def talk(self, loop):
        loop.add_message(self.name + " says: 'They say last night Molly's son turned into a gemstone. Can you believe that? Personally, I think he ran off into the night. Good riddance to him.'")

    def welcome(self, loop):
        loop.messages = []
        loop.add_message(self.name + " says: 'Welcome weary traveller.'")
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
            print(item.name)
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