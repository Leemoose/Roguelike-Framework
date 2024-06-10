import items as I
from .spawn_params import ItemSpawnParams

#Spawn lists!
ItemSpawns = []                                                         

# Can specify min_floor, max_floor, branch allowed - by default can spawn anywhere
#Corpse
ItemSpawns.append(ItemSpawnParams(I.GuardCorpse(), branch = "hub"))

# Weapons
ItemSpawns.append(ItemSpawnParams( I.Ax(300) ))
ItemSpawns.append(ItemSpawnParams( I.Hammer(301) ))
ItemSpawns.append(ItemSpawnParams( I.Dagger() ))
ItemSpawns.append(ItemSpawnParams( I.MagicWand(332) ))

# Swords
ItemSpawns.append(ItemSpawnParams( I.Sword() ))
ItemSpawns.append(ItemSpawnParams( I.BroadSword() ))
ItemSpawns.append(ItemSpawnParams( I.LongSword() ))
ItemSpawns.append(ItemSpawnParams( I.Claymore() ))
ItemSpawns.append(ItemSpawnParams( I.TwoHandedSword() ))
ItemSpawns.append(ItemSpawnParams( I.GreatSword() ))

# Rare Weapons
ItemSpawns.append(ItemSpawnParams( I.ScreamingDagger(322) ))
ItemSpawns.append(ItemSpawnParams( I.SleepingSword(341) ))
ItemSpawns.append(ItemSpawnParams( I.FlamingSword(331) ))
ItemSpawns.append(ItemSpawnParams( I.CrushingHammer(302) ))
ItemSpawns.append(ItemSpawnParams( I.SlicingAx(303) ))

# Shields
ItemSpawns.append(ItemSpawnParams( I.BasicShield(311) ))
ItemSpawns.append(ItemSpawnParams( I.Aegis(312) ))
ItemSpawns.append(ItemSpawnParams( I.TowerShield(313) ))
ItemSpawns.append(ItemSpawnParams( I.MagicFocus(314) ))

# Body Armor
ItemSpawns.append(ItemSpawnParams( I.Chestarmor(600) ))
ItemSpawns.append(ItemSpawnParams( I.LeatherArmor(601) ))
ItemSpawns.append(ItemSpawnParams( I.GildedArmor(602) ))
ItemSpawns.append(ItemSpawnParams( I.WarlordArmor(603) ))
ItemSpawns.append(ItemSpawnParams( I.WizardRobe(604) ))
ItemSpawns.append(ItemSpawnParams( I.KarateGi(605) ))
ItemSpawns.append(ItemSpawnParams( I.BloodstainedArmor(606) ))

# Boots
ItemSpawns.append(ItemSpawnParams( I.Boots(700) ))
ItemSpawns.append(ItemSpawnParams( I.BootsOfEscape(701) ))
ItemSpawns.append(ItemSpawnParams( I.BlackenedBoots(702) ))
ItemSpawns.append(ItemSpawnParams( I.AssassinBoots(703) ))

# Helmets
ItemSpawns.append(ItemSpawnParams( I.Helmet(770) ))
ItemSpawns.append(ItemSpawnParams( I.VikingHelmet(771) ))
ItemSpawns.append(ItemSpawnParams( I.SpartanHelmet(772) ))
ItemSpawns.append(ItemSpawnParams( I.ThiefHood(774) ))
ItemSpawns.append(ItemSpawnParams( I.WizardHat(775) ))

# Gloves
ItemSpawns.append(ItemSpawnParams( I.Gloves(750) ))
ItemSpawns.append(ItemSpawnParams( I.Gauntlets(751) ))
ItemSpawns.append(ItemSpawnParams( I.BoxingGloves(752) ))
ItemSpawns.append(ItemSpawnParams( I.HealingGloves(753) ))
ItemSpawns.append(ItemSpawnParams( I.LichHand(754) ))

# Pants
ItemSpawns.append(ItemSpawnParams( I.Pants(100), minFloor=5, maxFloor=10))

# Rings
ItemSpawns.append(ItemSpawnParams( I.RingOfSwiftness(500) ))
# ItemSpawns.append(ItemSpawnParams( I.RingOfTeleportation(505) ))
ItemSpawns.append(ItemSpawnParams( I.BloodRing(501) ))
ItemSpawns.append(ItemSpawnParams( I.RingOfMana(502) ))
ItemSpawns.append(ItemSpawnParams( I.RingOfMight(503) ))
ItemSpawns.append(ItemSpawnParams( I.BoneRing(504) ))

# Amulets
ItemSpawns.append(ItemSpawnParams( I.Amulet(550) ))

# Potiorbs
ItemSpawns.append(ItemSpawnParams( I.HealthPotion(401) ))
ItemSpawns.append(ItemSpawnParams( I.ManaPotion(402) ))
ItemSpawns.append(ItemSpawnParams( I.CurePotion(403) ))
ItemSpawns.append(ItemSpawnParams( I.MightPotion(404) ))
ItemSpawns.append(ItemSpawnParams( I.DexterityPotion(405) ))
ItemSpawns.append(ItemSpawnParams( I.PermanentStrengthPotion(404) ))
ItemSpawns.append(ItemSpawnParams( I.PermanentDexterityPotion(405) ))

# Scrorbs
ItemSpawns.append(ItemSpawnParams( I.EnchantScrorb(450) ))
ItemSpawns.append(ItemSpawnParams( I.BurningAttackScrorb(450) ))
#ItemSpawns.append(ItemSpawnParams( I.TeleportScroll(450), ))
ItemSpawns.append(ItemSpawnParams( I.MassTormentScroll(450) ))
ItemSpawns.append(ItemSpawnParams( I.InvincibilityScroll(450) ))
ItemSpawns.append(ItemSpawnParams( I.CallingScroll(450) ))
#ItemSpawns.append(ItemSpawnParams( I.SleepScroll(450),      1,               10,          1,              5))
#ItemSpawns.append(ItemSpawnParams( I.ExperienceScroll(450),      1,               10,          5,              5))
ItemSpawns.append(ItemSpawnParams( I.BlinkScrorb(450) ))
ItemSpawns.append(ItemSpawnParams( I.MassHealScrorb(450) ))

# Books
#ItemSpawns.append(ItemSpawnParams( I.BookofMassTorment,      1,               10,          1,              5))
#ItemSpawns.append(ItemSpawnParams( I.BookofMassHeal,      1,               10,          1,              5))
#ItemSpawns.append(ItemSpawnParams( I.BookofSummoning,      1,               10,          1,              1))