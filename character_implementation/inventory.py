class Inventory():
    def __init__(self, parent):
        self.parent = parent
        self.inventory_limit = 18
        self.inventory = []
        self.gold = 0

    def get_inventory(self):
        return self.inventory

    def get_inventory_size(self):
        return len(self.inventory)

    def can_grab(self, item):
        if len(self.inventory) < self.inventory_limit:
            return True
        elif item.has_trait("gold"):
            return True
        elif item.stackable:
            if item.name in [x.name for x in self.inventory]:
                return True
        else:
            return False

    def can_drop(self, item):
        return item.dropable

    def change_gold_amount(self, amount):
        self.gold += amount

    """
    Grab should be called when it is being picked off the floor
    """
    def do_grab(self, item, loop):
        self.get_item(item, loop)
        loop.generator.item_map.remove_thing(item)
        loop.add_message("The " + str(self.parent.name) + " picked up a " + str(item.name))

    """
    Get item should be called when it is not being picked off the floor
    """
    def get_item(self, item, loop):
        if item.yendorb:
            loop.change_loop("victory")
        elif item.has_trait("gold"):
            self.change_gold_amount(item.amount)
            loop.change_loop(loop.currentLoop)
        elif item.stackable:
            if not item.name in [x.name for x in self.inventory]:
                self.inventory.append(item)
            else:
                for i in range(len(self.inventory)):
                    if self.inventory[i].name == item.name:
                        self.inventory[i].stacks += 1
        else:
            self.inventory.append(item)
            if item.has_trait("book"):
                item.mark_owner(self)

    def do_drop(self, item, item_map):
        if len(self.inventory) != 0: #Seems unnecessary? Good to be safe...
            if item.equipable and item.equipped:
                self.parent.unequip(item)
            self.remove_item(item)
            return True
        return False

    def remove_item(self, item):
        i = 0
        while (self.inventory[i] != item) and i < len(self.inventory):
            i += 1
        if i < len(self.inventory):
            self.inventory.pop(i)
            return True
        return False