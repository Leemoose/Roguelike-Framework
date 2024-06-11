from collections import namedtuple

class GatewayData():
    def __init__(self):
        Lair = namedtuple("Lair", ["branch", "depth"])
        self.gateway_mapping = {
            Lair("Throne", 1): [Lair("Hub", 1)],
            Lair("Hub", 1): [Lair("Dungeon", 1), Lair("Forest", 1), Lair("Ocean",1), Lair("Throne",1)],
            Lair("Dungeon", 1): [Lair("Hub", 1)],
            Lair("Forest", 1): [Lair("Hub", 1)],
            Lair("Ocean", 1): [Lair("Hub", 1)]
        }

    def has_gateway(self, branch, depth):
        Lair = namedtuple("Lair", ["branch", "depth"])
        if Lair(branch, depth) in self.gateway_mapping:
            return True
        return False

    def get_num_gateways(self, branch, depth):
        Lair = namedtuple("Lair", ["branch", "depth"])
        if Lair(branch, depth) in self.gateway_mapping:
            return len(self.gateway_mapping[Lair(branch, depth)])
        return 0

    def all_gateways(self):
        return self.gateway_mapping.keys()

    def paired_gateway(self, old_lair):
        return self.gateway_mapping[old_lair]