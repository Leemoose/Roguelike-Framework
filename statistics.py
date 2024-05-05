
class StatTracker():
    def __init__(self):
        self.monsters_killed = {}

    def add_killed_monster(self, monster):
        monster_name = monster.name
        if monster_name in self.monsters_killed:
            self.monsters_killed[monster_name] += 1
        else:
            self.monsters_killed[monster_name] = 1

    def total_monsters_killed(self):
        return sum(self.monsters_killed.values())