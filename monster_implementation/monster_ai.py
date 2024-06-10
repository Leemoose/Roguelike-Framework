from .do_actions_utility import *
from .ranking_actions_utility import *

class Monster_AI():
    def __init__(self, parent):
        self.frontier = None
        self.is_awake = False
        self.parent = parent
        self.grouped = False
        self.target = None
        self.stairs_location = None
        self.old_key = None

        self.personality = {"Goblin": 0,
                            "Kobold": 0,
                            "Player": -90,
                            "Hobgoblin": -10,
                            "Gargoyle": 10,
                            "Orc": -100,
                            "Golem": 50,
                            "Slime": 50
                            }

        # first number is average, second is spread
        self.tendencies = {"combat": (90, 10),
                           "pickup": (30, 5),
                           "find_item": (20, 10),
                           "equip": (40, 5),
                           "consume": (40, 5),
                           "move": (40, 20),
                           "ungroup": (60, 20),
                           "skill": (-1, 0),
                           "flee": (100, 20),
                           "stairs": (100, 10)
                           }
        #what it can actually do
        self.options = {"combat": (rank_combat, do_combat),
                        "pickup": (rank_pickup, do_item_pickup),
                        "find_item": (rank_find_item, do_find_item),
                        "equip": (rank_equip_item, do_equip),  # need to be fixed
                        "consume": (rank_use_consumeable, do_use_consumeable),
                        "move": (rank_move, do_move),
                        "ungroup": (rank_ungroup, do_ungroup),
                        "skill": (rank_skill, do_skill),
                        "flee": (rank_flee, do_flee),
                        "stairs": (rank_stairs, do_stairs),
                        }

    """
    Think it would be better to first rank each action depending on the circumstances with a number between 1-100 and 
    then pick the action that ranks the highest
    """

    def rank_actions(self, loop):
        # print(ai.parent.character.energy)
        max_utility = 0
        called_function = (0, do_nothing)

        for action in self.options:
            utility = self.options[action][0](self, loop)
            if utility > max_utility:
                max_utility = utility
                called_function = action

        # print(max_utility)
        self.parent.character.energy -= 1
        # print(f"{ai.parent} is doing {called_function} with utility {max_utility}")
        self.options[called_function][1](self,loop)
    def change_tendency(self, type, new_value):
        if type in self.tendencies:
            self.tendencies[type] = new_value
        else:
            print("That {} cannot change their tendency ({})".format(self.parent, type))

    def get_tendency(self, type):
        if type in self.tendencies:
            return self.tendencies[type]
        else:
            print("That {} does not have that tendency ({})".format(self.parent, type))
            return -1

    def randomize_action(self, action):
        average, spread = self.tendencies[action]
        return max(-1, random.randint(average - spread, average + spread))

class Goblin_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (60, 10),
                           "pickup": (100, 5),
                           "find_item": (80, 10),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (60, 20),
                           "skill": (80, 10),
                           "flee": (105, 10),
                           "stairs": (-1, 0)
                           }

        self.personality["Goblin"] =  100

class Stumpy_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (90, 10),
                           "pickup": (-1, 0),
                           "find_item": (-1, 00),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (80, 20),
                           "skill": (80, 10),
                           "flee": (-1, 0),
                           "stairs": (-1, 0)
                           }
        
class Dummy_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (-1, 0),
                           "pickup": (-1, 0),
                           "find_item": (-1, 0),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (100, 10),
                           "ungroup": (-1, 0),
                           "skill": (-1, 0),
                           "flee": (-1, 0),
                           "stairs": (-1, 0)
                           }
    
    def do_move(self, loop):
        return

class Slime_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "pickup": (100, 0),
                           "find_item": (-1, 0),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (-1, 0),
                           "skill": (-1, 0),
                           "flee": (-1, 0),
                           "stairs": (-1, 0)
                           }


class Friendly_AI(Monster_AI):
    def __init__(self, parent):
        super().__init__(parent)
        self.tendencies = {"combat": (80, 10),
                           "pickup": (-1, 0),
                           "find_item": (-1, 0),
                           "equip": (-1, 0),
                           "consume": (-1, 0),
                           "move": (40, 20),
                           "ungroup": (-1, 0),
                           "skill": (-1, 0),
                           "flee": (-1, 0),
                           "stairs": (100, 10)
                           }

        self.personality = {"Goblin": -100,
                            "Kobold": -100,
                            "Player": 100,
                            "Hobgoblin": -100,
                            "Gargoyle": -100,
                            "Orc": -100,
                            "Golem": -100,
                            "Slime": -100,
                            "Stumpy": -100
                            }


