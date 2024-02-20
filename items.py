import dice as R
import objects as O

class Weapon(O.Item):
    def __init__(self, x, y, id_tag, render_tag, name, equipable):
        super().__init__(x,y, id_tag, render_tag, name, equipable)


class Ax(Weapon):
    def __init__(self, render_tag, equipable, x, y):
        super().__init__(x, y, 0, render_tag, "Ax", equipable)
        self.melee = True

    def attack(self):
        damage = R.roll_dice(100, 200)[0]
        return damage

