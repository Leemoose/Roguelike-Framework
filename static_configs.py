from pygame import image
import pygame
import tiles as T


class TileDict():
    def __init__(self, textSize):
        tiles = {}
        # 1-99 are tile
        tiles[1] = pygame.transform.scale(image.load("assets/tiles/colorful_wall.png"), (32, 32))
        tiles[-1] = pygame.transform.scale(image.load("assets/tiles/colorful_wall_shaded.png"), (32, 32))
        tiles[2] = pygame.transform.scale(image.load("assets/tiles/colorful_floor.png"), (32, 32))
        tiles[-2] = pygame.transform.scale(image.load("assets/tiles/colorful_floor_shaded.png"), (32, 32))
        tiles[3] = pygame.transform.scale(image.load("assets/tiles/floor_dirty.png"), (32, 32))
        tiles[-3] = pygame.transform.scale(image.load("assets/tiles/floor_dirty_shaded.png"), (32, 32))
        tiles[4] = pygame.transform.scale(image.load("assets/tiles/floor_dirty1.png"), (32, 32))
        tiles[-4] = pygame.transform.scale(image.load("assets/tiles/floor_dirty1_shaded.png"), (32, 32))
        tiles[5] = image.load("assets/tiles/red_carpet.png")
        tiles[-5] = image.load("assets/tiles/red_carpet_shaded.png")
        tiles[6] = image.load("assets/tiles/wooden_floor.png")
        tiles[-6] = image.load("assets/tiles/wooden_floor_shaded.png")
        tiles[7] = image.load("assets/tiles/forest_wall.png")
        tiles[-7] = image.load("assets/tiles/forest_wall_shaded.png")
        tiles[8] = image.load("assets/tiles/ocean_floor.png")
        tiles[-8] = image.load("assets/tiles/ocean_floor_shaded.png")
        tiles[9] = image.load("assets/tiles/sand_floor.png")
        tiles[-9] = image.load("assets/tiles/sand_floor_shaded.png")
        tiles[10] = image.load("assets/tiles/deep_ocean_floor.png")
        tiles[-10] = image.load("assets/tiles/deep_ocean_floor_shaded.png")


        tiles[11] = pygame.transform.scale(image.load("assets/tiles/wall_extra_rounded.png"), (32, 32))
        tiles[-11] = pygame.transform.scale(image.load("assets/tiles/wall_extra_rounded_shaded.png"), (32, 32))
        tiles[12] = pygame.transform.scale(image.load("assets/tiles/floor_rounded.png"), (32, 32))
        tiles[-12] = pygame.transform.scale(image.load("assets/tiles/floor_rounded_shaded.png"), (32, 32))
        tiles[13] = image.load("assets/tiles/forest_floor.png")
        tiles[-13] = image.load("assets/tiles/forest_floor_shaded.png")
        tiles[14] = image.load("assets/tiles/ocean_wall.png")
        tiles[-14] = image.load("assets/tiles/ocean_wall_shaded.png")
        tiles[15] = image.load("assets/tiles/stone_floor.png")
        tiles[-15] = image.load("assets/tiles/stone_floor_shaded.png")

        tiles[20] = pygame.transform.scale(image.load("assets/fire.png"), (32, 32))

        tiles[30] = image.load("assets/tiles/door.png")
        tiles[-30] = image.load("assets/tiles/door_shaded.png")
        tiles[31] = image.load("assets/tiles/open_door.png")
        tiles[-31] = image.load("assets/tiles/open_door_shaded.png")

        # ui assets
        tiles[50] = image.load("assets/ui/stat_up.png")
        tiles[51] = image.load("assets/ui/stat_down.png")
        tiles[-50] = image.load("assets/ui/stat_up_dark.png")
        tiles[-51] = image.load("assets/ui/stat_down_dark.png")

        # basic assets
        tiles[90] = image.load("assets/tiles/stairs_up.png")
        tiles[-90] = image.load("assets/tiles/stairs_up_shaded.png")
        tiles[91] = image.load("assets/tiles/stairs_down.png")
        tiles[-91] = image.load("assets/tiles/stairs_down_shaded.png")
        tiles[92] = image.load("assets/tiles/gateway.png")
        tiles[-92] = image.load("assets/tiles/gateway_shaded.png")

        # pants
        tiles[100] = image.load("assets/items/armor/pants.png")

        # npc assets
        tiles[110] = image.load("assets/npc/shopkeeper.png")
        tiles[120] = image.load("assets/npc/king.png")
        tiles[121] = image.load("assets/npc/guard.png")
        tiles[122] = image.load("assets/npc/speech_bubble.png")
        tiles[123] = image.load("assets/npc/sensei.png")
        tiles[124] = image.load("assets/npc/training_dummy.png")
        tiles[125] = image.load("assets/npc/destroyed_dummy.png")

        # 200-299 player assets
        tiles[200] = image.load("assets/player/Player.png")
        tiles[-200] = image.load("assets/player/player_under_armor.png")
        tiles[201] = image.load("assets/player/player_boots.png")
        tiles[202] = image.load("assets/player/player_gloves.png")
        tiles[203] = image.load("assets/player/player_helmet.png")
        tiles[204] = image.load("assets/player/player_armor.png")
        tiles[210] = image.load("assets/items/gold.png")

        # 300-399 weapon assets
        tiles[300] = image.load("assets/items/weapons/basic_ax.png")
        tiles[303] = image.load("assets/items/weapons/bleeding_ax.png")
        tiles[301] = image.load("assets/items/weapons/hammer.png")
        tiles[302] = image.load("assets/items/weapons/crushing_hammer.png")
        tiles[321] = image.load("assets/items/weapons/dagger.png")
        tiles[322] = image.load("assets/items/weapons/screaming_dagger.png")
        tiles[331] = image.load("assets/items/weapons/burning_sword.png")
        tiles[332] = image.load("assets/items/weapons/magic_wand.png")
        tiles[340] = image.load("assets/items/weapons/sword.png")
        tiles[341] = image.load("assets/items/weapons/sleeping_sword.png")

        # 400-499 consumeables assets
        tiles[401] = image.load("assets/items/consumeables/health_orb_bigger.png")
        tiles[402] = image.load("assets/items/consumeables/mana_orb_bigger.png")
        tiles[403] = image.load("assets/items/consumeables/curing_orb_bigger.png")
        tiles[404] = image.load("assets/items/consumeables/might_orb_bigger.png")
        tiles[405] = image.load("assets/items/consumeables/haste_orb_bigger.png")

        # scroll assets
        tiles[450] = image.load("assets/items/consumeables/scroll.png")

        tiles[480] = image.load("assets/items/consumeables/book.png")

        # ring assets
        tiles[500] = image.load("assets/items/jewelry/green_ring_gold.png")
        tiles[501] = image.load("assets/items/jewelry/blood_ring.png")
        tiles[502] = image.load("assets/items/jewelry/blue_ring.png")
        tiles[503] = image.load("assets/items/jewelry/red_ring.png")
        tiles[504] = image.load("assets/items/jewelry/bone_ring.png")
        tiles[505] = image.load("assets/items/jewelry/ring_of_teleport.png")

        # amulet
        tiles[550] = image.load("assets/items/jewelry/amulet.png")

        # armor assets
        # list of armor: basic, leather, golden, warmonger, wizard robe
        tiles[600] = image.load("assets/items/armor/armor.png")
        tiles[601] = image.load("assets/items/armor/leather_armor.png")
        tiles[602] = image.load("assets/items/armor/golden_armor.png")
        tiles[603] = image.load("assets/items/armor/warmonger_armor.png")
        tiles[604] = image.load("assets/items/armor/wizard_robe.png")
        tiles[605] = image.load("assets/items/armor/karate_gi.png")
        tiles[606] = image.load("assets/items/armor/bloodstained_armor.png")

        # shield assets
        # list of shields: basic, aegis, tower, magic focus
        tiles[311] = image.load("assets/items/armor/shield.png")
        tiles[312] = image.load("assets/items/armor/aegis.png")
        tiles[313] = image.load("assets/items/armor/tower_shield.png")
        tiles[314] = image.load("assets/items/armor/magic_focus.png")

        # boots assets
        # list of boots: basic, escape
        tiles[700] = image.load("assets/items/armor/boots.png")
        tiles[701] = image.load("assets/items/armor/boots_of_escape.png")
        tiles[702] = image.load("assets/items/armor/blackened_boots.png")
        tiles[703] = image.load("assets/items/armor/assassin_boots.png")

        # gloves assets
        # list of gloves: basic, gauntlets
        tiles[750] = image.load("assets/items/armor/gloves.png")
        tiles[751] = image.load("assets/items/armor/gauntlets.png")
        tiles[752] = image.load("assets/items/armor/boxing_gloves.png")
        tiles[753] = image.load("assets/items/armor/healer_gloves.png")
        tiles[754] = image.load("assets/items/armor/lich_hand.png")

        # helmet assets
        tiles[770] = image.load("assets/items/armor/helmet.png")
        tiles[771] = image.load("assets/items/armor/viking_helmet.png")
        tiles[772] = image.load("assets/items/armor/spartan_helmet.png")
        tiles[773] = image.load("assets/items/armor/great_helm.png")
        tiles[774] = image.load("assets/items/armor/thief_hood.png")
        tiles[775] = image.load("assets/items/armor/wizard_hat.png")

        # empty equipment assets
        tiles[801] = image.load("assets/items/icons/empty_armor.png")
        tiles[802] = image.load("assets/items/icons/empty_boots.png")
        tiles[803] = image.load("assets/items/icons/empty_gloves.png")
        tiles[804] = image.load("assets/items/icons/empty_helmet.png")
        tiles[805] = image.load("assets/items/icons/empty_weapon.png")
        tiles[806] = image.load("assets/items/icons/empty_shield.png")
        tiles[807] = image.load("assets/items/icons/empty_ring.png")
        tiles[811] = image.load("assets/items/icons/empty_armor_open.png")
        tiles[812] = image.load("assets/items/icons/empty_boots_open.png")
        tiles[813] = image.load("assets/items/icons/empty_gloves_open.png")
        tiles[814] = image.load("assets/items/icons/empty_helmet_open.png")
        tiles[815] = image.load("assets/items/icons/empty_weapon_open.png")
        tiles[816] = image.load("assets/items/icons/empty_shield_open.png")
        tiles[817] = image.load("assets/items/icons/empty_ring_open.png")
        tiles[818] = image.load("assets/items/icons/empty_pants_open.png")
        tiles[819] = image.load("assets/items/icons/empty_pants.png")
        tiles[820] = image.load("assets/items/icons/empty_amulet_open.png")
        tiles[821] = image.load("assets/items/icons/empty_amulet.png")

        # skill assets
        tiles[901] = image.load("assets/ui/target.png")
        tiles[902] = image.load("assets/skills/placeholder_skill_icon.png")
        tiles[-902] = image.load("assets/skills/placeholder_skill_icon.png")
        tiles[903] = image.load("assets/skills/gun_skill_icon.png")
        tiles[-903] = image.load("assets/skills/gun_skill_icon.png")
        tiles[904] = image.load("assets/skills/BurningAttack_skill_icon.png")
        tiles[-904] = image.load("assets/skills/BurningAttack_skill_icon_dark.png")
        tiles[905] = image.load("assets/skills/MagicMissile_skill_icon.png")
        tiles[-905] = image.load("assets/skills/MagicMissile_skill_icon_dark.png")
        tiles[906] = image.load("assets/skills/Petrify_skill_icon.png")
        tiles[-906] = image.load("assets/skills/Petrify_skill_icon_dark.png")
        tiles[907] = image.load("assets/skills/ShrugOff_skill_icon.png")
        tiles[-907] = image.load("assets/skills/ShrugOff_skill_icon_dark.png")
        tiles[908] = image.load("assets/skills/Berserk_skill_icon.png")
        tiles[-908] = image.load("assets/skills/Berserk_skill_icon_dark.png")
        tiles[909] = image.load("assets/skills/BloodPact_skill_icon.png")
        tiles[-909] = image.load("assets/skills/BloodPact_skill_icon_dark.png")
        tiles[910] = image.load("assets/skills/Terrify_skill_icon.png")
        tiles[-910] = image.load("assets/skills/Terrify_skill_icon_dark.png")
        tiles[911] = image.load("assets/skills/Escape_skill_icon.png")
        tiles[-911] = image.load("assets/skills/Escape_skill_icon_dark.png")
        tiles[912] = image.load("assets/skills/Heal_skill_icon.png")
        tiles[-912] = image.load("assets/skills/Heal_skill_icon_dark.png")
        tiles[913] = image.load("assets/skills/Torment_skill_icon.png")
        tiles[-913] = image.load("assets/skills/Torment_skill_icon_dark.png")
        tiles[914] = image.load("assets/skills/teleport_skill_icon.png")
        tiles[-914] = image.load("assets/skills/teleport_skill_icon_dark.png")
        tiles[915] = image.load("assets/skills/invincible_skill_icon.png")
        tiles[-915] = image.load("assets/skills/invincible_skill_icon_dark.png")

        # 100-199 monster assets
        tiles[1000] = image.load('assets/monsters/goblin.png')
        tiles[1001] = image.load('assets/monsters/gorblin_shaman.png')
        tiles[1002] = image.load('assets/monsters/hobgoblin.png')
        tiles[1009] = image.load('assets/monsters/Looter.png')

        tiles[1010] = image.load('assets/monsters/kobold.png')
        tiles[1020] = image.load('assets/monsters/gargoyle.png')
        tiles[1030] = image.load('assets/monsters/velociraptor.png')
        tiles[1040] = image.load('assets/monsters/minotaur.png')
        tiles[1050] = image.load('assets/monsters/tormentorb.png')
        tiles[1060] = image.load('assets/monsters/yendorb.png')
        tiles[1070] = image.load("assets/monsters/orc.png")
        tiles[1079] = image.load("assets/monsters/Bobby.png")
        tiles[1080] = image.load('assets/monsters/golem.png')
        tiles[1090] = image.load('assets/monsters/stumpy.png')
        tiles[1100] = image.load('assets/monsters/slime.png')
        tiles[161] = image.load('assets/monsters/yendorb_deactivated.png')

        tiles[199] = image.load('assets/monsters/monster_corpse.png')

        self.tiles = tiles

    def tile_string(self, key):
        return self.tiles[key]

class AscaiiTileDict():
    def __init__(self):
        tiles = {}
        tiles["x"] = T.Wall
        tiles["."] = T.Floor
        tiles["w"] = T.Water
        tiles["dw"] = T.DeepWater
        tiles[">"] = T.DownStairs
        tiles["<"] = T.UpStairs
        tiles["g"] = T.Gateway
        tiles["K"] = T.KingTile
        tiles["G"] = T.GuardTile
        tiles["d"] = T.Door
        tiles["BB"] = T.BobBrotherTile
        tiles["S"] = T.SenseiTile
        tiles["D"] = T.DummyTile
        self.tiles = tiles

        self.image_mapping = {"Forest":
                            {
                                "x": 7,
                                ".": 13
                            },
                        "Dungeon":
                            {
                            },
                        "Ocean":
                            {
                                "x": 15,
                                ".": 9
                            }
                        }


    def ascaii_tile(self, ascaii):
        return self.tiles[ascaii]

    def branchdepth_render(self, branch, ascaii):
        return self.image_mapping[branch][ascaii]
