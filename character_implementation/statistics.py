
class StatTracker():
    def __init__(self):
        self.monsters_killed = {}
        self.possible_quests = {}
        self.attacks = 0
        self.moves = 0
        self.turns = 0
        self.gold_grabbed = 0
        self.items_grabbed = 0
        self.damage_dealt = 0
        self.damage_taken = 0

    def add_killed_monster(self, monster):
        monster_name = monster.name
        if monster_name in self.monsters_killed:
            self.monsters_killed[monster_name] += 1
        else:
            self.monsters_killed[monster_name] = 1

    def total_monsters_killed(self):
        return sum(self.monsters_killed.values())

    def add_turn_details(self):
        self.turns += 1

    def add_move_details(self):
        self.moves += 1

    def add_attack_details(self, damage):
        self.attacks += 1
        self.damage_dealt += damage

    def add_defense_details(self, damage_taken):
        pass

    def add_item_pickup_details(self, item):
        if item.has_trait("gold"):
            self.gold_grabbed += item.amount
        else:
            self.items_grabbed += 1