import dice as R
import objects as O

class Weapon(O.Item):
    def __init__(self, x, y, id_tag, render_tag, name, equipable):
        super().__init__(x,y, id_tag, render_tag, name, equipable)


class Ax(Weapon):
    def __init__(self, render_tag, equipable, x, y):
        super().__init__(x, y, 0, render_tag, "Ax", equipable)
        self.melee = True
        self.name = "Ax"

    def attack(self):
        damage = R.roll_dice(20, 40)[0]
        return damage

class Hammer(Weapon):
    def __init__(self, render_tag, equipable, x, y):
        super().__init__(x, y, 0, render_tag, "Hammer", equipable)
        self.melee = True
        self.name = "Hammer"

    def attack(self):
        damage = R.roll_dice(5, 60)[0]
        return damage



