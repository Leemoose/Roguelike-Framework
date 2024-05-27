import dill

class Memory():
    """
    Used to save the game
    """

    def __init__(self):
        self.explored_levels = 0
        self.floor_level = 0
        self.branch = ""
        self.generators = {}
        self.player = None
        self.render_exploration = True
        self.keyboard = None

    def save_objects(self):
        save = [self.explored_levels, self.floor_level, self.generators, self.player, self.branch, self.render_exploration, self.keyboard]
        try:
            with open("data.dill", "wb") as f:
                print("Saved the game")
                dill.dump(save, f)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

    def load_objects(self):
        with open('data.dill', 'rb') as f:
            # Call load method to deserialze
            print("Loaded the game")
            save = dill.load(f)
        self.explored_levels = save[0]
        self.floor_level = save[1]
        self.generators = save[2]
        self.player = save[3]
        self.branch = save[4]
        self.render_exploration = save[5]
        self.keyboard = save[6]
