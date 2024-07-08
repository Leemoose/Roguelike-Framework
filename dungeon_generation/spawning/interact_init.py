from interactables import *
from .spawn_params import InteractableSpawnParams

InteractableSpawns = []
InteractableSpawns.append(InteractableSpawnParams(Campfire(), minFloor=1, maxFloor=5,branch = "Forest"))
InteractableSpawns.append(InteractableSpawnParams(ForestOrbPedastool(), minFloor=5, maxFloor=5,branch = "Forest"))


InteractableSpawns.append(InteractableSpawnParams(OceanOrbPedastool(), minFloor=5, maxFloor=5,branch = "Ocean"))