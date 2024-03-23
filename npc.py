import items as I
import objects as O
import loops as L

class NPC(O.Objects):
    def __init__(self, render_tag, x, y, name="Unknown npc"):
        super().__init__(x, y, 0, render_tag, name)
        self.name = "Bob"
        self.items = [I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300), I.Ax(300)]

    def talk(self, loop):
        loop.messages = []
        loop.add_message(self.name + " says: 'Hello Adit, I've been waiting for you.'")
        loop.npc_focus = self

    def give_item(self, loop, number):
        player = loop.player
        item = self.items.pop(number)
        if item.stackable:
            if not item.name in [x.name for x in player.character.inventory]:
                if len(player.character.inventory) > player.character.inventory_limit:
                    loop.add_message("You need to drop something before you can buy this")
                    return
                else:
                    player.character.inventory.append(item)

            else:
                for i in range(len(player.character.inventory)):
                    if player.character.inventory[i].name == item.name:
                        player.character.inventory[i].stacks += 1
        else:
            if len(player.character.inventory) > player.character.inventory_limit:
                loop.add_message("You need to drop something before you can buy this")
                return
            else:
                player.character.inventory.append(item)
                if isinstance(item, I.Book):
                    item.mark_owner(self)
        loop.change_loop(L.LoopType.trade)