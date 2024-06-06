

class Spell():
    def __init__(self, parent, name = "Unknown spell", cooldown=0, cost=0, range=-1, action_cost=100, required_intelligence = 0):
        self.parent = parent
        self.cooldown = cooldown
        self.cost = cost
        self.ready = 0  # keeps track of how long before we can cast, ready = 0 means we can cast
        self.name = name
        self.range = range
        self.targetted = False
        self.targets_monster = False
        self.action_cost = action_cost
        self.threshold = 0.0
        self.render_tag = 902  # placeholder icon, skill assets are fixed so not given in user input
        self.required_intelligence = required_intelligence

    def activate(self, target, generator):
        self.parent.character.mana -= self.cost

    def try_to_activate(self, target, loop):
        # check cooldowns and costs
        if self.castable(target):
            self.ready = self.cooldown
            print("Spell is activated")
            return self.activate(target, loop)
        loop.add_message("You were unable to cast the spell due to certain conditions.")
        return False

    def tick_cooldown(self):
        if self.ready > 0:
            self.ready -= 1

    def castable(self, target):
        if self.ready == 0 and self.parent.character.mana >= self.cost:
            return True
        return False

    def in_range(self, target):
        # print(target)
        if isinstance(target, tuple):
            targetx, targety = target
        else:
            targetx, targety = target.get_location()
        distance = self.parent.get_distance(targetx, targety)
        if distance < self.range:
            return True

    def __str__(self):
        return self.name

    def description(self):
        return self.name + "(" + str(self.cost) + " cost, " + str(self.cooldown) + " turn cooldown"
    
    # overwrite for spells that need a more detailed description
    def full_description(self):
        return self.description()

    def can_learn(self):
        return self.parent.character.intelligence >= self.required_intelligence
