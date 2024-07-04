import random


class Star():
    def __init__(self, name = "Star"):
        self.name = name
        self.interested = False
        self.invested = False
        self.interest = 0 # star interest goes from 0 - 100, at higher interested, negative actions have bigger impact on interest
        self.interest_thresholds = [10, 25, 45, 70, 100] # gain a benefit at 10, 25, 45, 70, 100 

    def take_action(self, loop):
        self.check_interesting_action(loop)
        if not self.invested:
            self.check_interest(loop)
        elif random.random() > .8:
            self.grant_boon(loop)

    def grant_boon(self, loop, level):
        pass

    def check_interest(self, loop):
        self.interested = True

    def check_interesting_action(self, loop):
        self.interest += 1 

class GreenBuck(Star):
    def __init__(self):
        super().__init__(name = "Green Buck")

    def check_interest(self, loop):
        if loop.player.inventory.get_gold() > 10 and not self.interested:
            loop.add_message("A star turns its eye on you")
            self.interested = True
        elif loop.player.inventory.get_gold() > 25 and not self.invested:
            loop.add_message("Ah, I see a potential profit in you. Your lust for gold and treasure has caught my eye. Prove to me your worth by amassing great wealth, and I shall bestow upon you power beyond your wildest dreams. Let the coins flow, and let us see just how rich you can become.")
            self.invested = True

    def grant_boon(self, loop):
        loop.add_message("Hey there, treasure hunter. You've caught my eye with all that shiny gold you're collecting. Not bad, not bad at all. Here, take some extra gold on me. Why? Because I felt like it. Keep the riches coming, and who knows, maybe I'll throw more your way whenever I'm in the mood. Just keep things interesting, alright?")
        loop.player.inventory.change_gold_amount(10)
