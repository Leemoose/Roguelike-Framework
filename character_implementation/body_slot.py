
class Body():
    def __init__(self, parent):
        self.equipment_slots = {"body_armor_slot": [None],
                                "helmet_slot": [None],
                                "gloves_slot": [None],
                                "boots_slot": [None],
                                "ring_slot": [None, None],
                                "pants_slot": [None],
                                "amulet_slot": [None],
                                "hand_slot": [None, None]
                                }
        self.parent = parent
    def free_equipment_slots(self, slot):
        if slot not in self.equipment_slots:
            raise Exception("You are trying to find a {} in {}'s equipment slot".format(slot, self.parent.name))
        free_slots = 0
        for item in self.equipment_slots[slot]:
            if item is None:
                free_slots += 1
        return free_slots

    def add_item_to_equipment_slot(self, item, slot, num_slots):
        i = 0
        while i < num_slots:
            if self.equipment_slots[slot][i] is None:
                self.equipment_slots[slot][i] = item
            i += 1
        if i >= num_slots:
            return True
        else:
            return False

    def remove_item_from_equipment_slot(self, item, slot, num_slots):
        i = 0
        while i < num_slots:
            if self.equipment_slots[slot][i] is item:
                self.equipment_slots[slot][i] = None
            i += 1
        if i >= num_slots:
            return True
        else:
            return False

    def remove_equipment_slot(self, slot):
        if slot not in self.equipment_slots:
            raise Exception("You are trying to find a {} in {}'s equipment slot".format(slot, self.parent.name))
        try:
            self.equipment_slots[slot].remove(None)
        except:
            Exception("You tried to remove a {} in {}'s equipment slot but there was nothing that could be removed".format(slot, self.parent.name))
        return False

    def add_equipment_slot(self, slot):
        if slot not in self.equipment_slots:
            raise Exception("You are trying to find a {} in {}'s equipment slot".format(slot, self.parent.name))
        self.equipment_slots[slot].append(None)
        return True

    def get_items_in_equipment_slot(self, slot):
        carried = []
        if slot not in self.equipment_slots:
            raise Exception("You are trying to find a {} in {}'s equipment slot".format(slot, self.parent.name))
        else:
            for item in self.equipment_slots[slot]:
                if item != None:
                    carried.append(item)
        return carried

    def get_nth_item_in_equipment_slot(self, slot, n):
        items = self.get_items_in_equipment_slot(slot)
        if len(items) > n:
            return items[n]


    def equip(self, item, strength):
        slot = item.get_slot()
        if strength >= item.required_strength and self.free_equipment_slots(slot) >= item.slots_taken:
            self.add_item_to_equipment_slot(item, slot, item.slots_taken)
            item.equipped = True
            item.dropable = False
            if item.attached_skill_exists:
                self.parent.add_skill(item.attached_skill(self.parent.parent))
            item.activate(self.parent)

    def unequip(self, item):
        slot = item.get_slot()
        self.remove_item_from_equipment_slot(item, slot, item.slots_taken)
        item.dropable = True
        item.equipped = False
        if item.attached_skill_exists:
            self.parent.remove_skill(item.attached_skill(self.parent.parent))
        item.deactivate(self.parent)

    def get_weapon(self):
        carried_items = self.equipment_slots["hand_slot"]
        for item in carried_items:
            print(item)
            if item is not None and item.has_trait("weapon"):
                return item
        return None




