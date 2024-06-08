import monster as M
from .spawn_params import MonsterSpawnParams, BossSpawnParams

MonsterSpawns = []

# all branches
MonsterSpawns.append(MonsterSpawnParams(M.Slime(), group="slime", minFloor=1, maxFloor=4, branch="all"))

# early floors dungeon only
MonsterSpawns.append(MonsterSpawnParams(M.Kobold(-1, -1), minFloor=1, maxFloor=4))

# goblin type monsters dungeon only
MonsterSpawns.append(MonsterSpawnParams(M.Goblin(-1, -1), group="goblin", minFloor=1, maxFloor=4))
MonsterSpawns.append(MonsterSpawnParams(M.Hobgoblin(-1, -1), minFloor=1, maxFloor=4, rarity="Rare", group="goblin"))
MonsterSpawns.append(MonsterSpawnParams(M.Looter(), group="goblin", minFloor=1, maxFloor=4))
#MonsterSpawns.append(MonsterSpawnParams(M.GoblinShaman(-1, -1), group="goblin"))


# middle floors
MonsterSpawns.append(MonsterSpawnParams(M.Gargoyle(-1, -1), group="gargoyle", minFloor=5, maxFloor=7))
MonsterSpawns.append(MonsterSpawnParams(M.Minotaur(-1, -1), minFloor=5, maxFloor=7))
MonsterSpawns.append(MonsterSpawnParams(M.Orc(-1, -1), group="orc", minFloor=5, maxFloor=7))
MonsterSpawns.append(MonsterSpawnParams(M.Bobby(), group="orc", rarity="rare", minFloor=5, maxFloor=7))

# forest branch
MonsterSpawns.append(MonsterSpawnParams(M.Stumpy(), minFloor=1, maxFloor=5, branch="Forest")) # maybe move to forest branch

# late floors
MonsterSpawns.append(MonsterSpawnParams(M.Raptor(-1, -1), minFloor=8, maxFloor=10, group="dinosaur")) # maybe move to forest branch
MonsterSpawns.append(MonsterSpawnParams(M.Tormentorb(-1, -1), minFloor=8, maxFloor=10))
MonsterSpawns.append(MonsterSpawnParams(M.Golem(-1, -1), minFloor=8, maxFloor=10))

# TEMPORARY CHANGE TO TEST TILE RESTRICTED MONSTERS
MonsterSpawns.append(MonsterSpawnParams(M.Golem(-1, -1), minFloor=1, maxFloor=1, branch="Ocean"))

# boss spawning
MonsterSpawns.append(BossSpawnParams(M.BossOrb(-1, -1), depth=10))