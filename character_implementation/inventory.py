class Inventory():
    def __init__(self, parent):
        self.parent = parent
        self.inventory_limit = 18
        self.inventory = []
        self.orb_inventory = []
        self.gold = 0
        self.ready_scroll = None # index of actively used scroll
        self.limit_inventory = "item"

        self.active_inventory = self.inventory

    def get_orb_inventory(self):
        return self.orb_inventory

    def get_inventory(self):
        return self.active_inventory

    def get_limit_inventory(self, limit = None):
        if limit == None:
            limit = self.limit_inventory
        allowable = []
        for item in self.active_inventory:
            if item.has_trait(limit):
                allowable.append(item)
        return allowable

    def get_inventory_size(self):
        return len(self.active_inventory)

    def get_gold(self):
        return self.gold

    def get_enchantable(self):
        enchantable = []
        for item in self.inventory:
            if item.can_be_levelled:
                if item.level < 6: # items can be levelled upto +5
                    enchantable.append(item)
        return enchantable

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

    def change_limit_inventory(self, change):
        self.limit_inventory = change

    def change_active_inventory(self, change):
        if change == "orb":
            self.active_inventory=self.orb_inventory
            self.limit_inventory = "item"
        elif change == "main":
            self.active_inventory = self.inventory

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
    def get_item(self, item, loop = None):
        if item.yendorb:
            loop.change_loop("victory")
        elif item.has_trait("orb"):
            self.orb_inventory.append(item)
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
            item.x = self.parent.x
            item.y = self.parent.y
            item_map.place_thing(item)
            self.remove_item(item)
            return True
        return False

    def remove_item(self, item):
        if item.has_trait("orb") and len(self.orb_inventory) > 0 :
            i = 0
            while (self.orb_inventory[i] != item) and i < len(self.orb_inventory):
                i += 1
            if i < len(self.orb_inventory):
                self.orb_inventory.pop(i)
                return True
        elif len(self.inventory) > 0:
            i = 0
            while (self.inventory[i] != item) and i < len(self.inventory):
                i += 1
            if i < len(self.inventory):
                self.inventory.pop(i)
                return True
        return False