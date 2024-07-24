# config.py

import copy

# Constants definitions
RESIN_PER_WEEK = 180 * 7 + 60  # assuming 1 transient Resin from Teapot
RESIN_PER_RUN = 20
ARTIFACTS_PER_RUN = 1.065

TYPE_FLOWER = "Flower"
TYPE_PLUME = "Plume"
TYPE_SANDS = "Sands"
TYPE_GOBLET = "Goblet"
TYPE_CIRCLET = "Circlet"
ARTIFACT_TYPES = [
    TYPE_FLOWER,
    TYPE_PLUME,
    TYPE_SANDS,
    TYPE_GOBLET,
    TYPE_CIRCLET
]

STAT_BASE_HP = "Base HP"
STAT_FLAT_HP = "Flat HP"
STAT_HP_PCT = "HP %"
STAT_TOTAL_HP = "Total HP"

STAT_BASE_ATK = "Base ATK"
STAT_FLAT_ATK = "Flat ATK"
STAT_ATK_PCT = "ATK %"
STAT_TOTAL_ATK = "Total ATK"

STAT_BASE_DEF = "Base DEF"
STAT_FLAT_DEF = "Flat DEF"
STAT_DEF_PCT = "DEF %"
STAT_TOTAL_DEF = "Total DEF"

STAT_ER = "Energy Recharge"
STAT_EM = "Elemental Mastery"
STAT_ELEMENTAL_DMG = "Elemental DMG %"
STAT_PHYSICAL_DMG = "Physical DMG %"
STAT_OTHER_DMG = "Other DMG %"
STAT_CR = "Crit Rate %"
STAT_CD = "Crit DMG %"
STAT_HB = "Healing Bonus %"

STAT_AMPLIFYING_RXN_MULTIPLIER = "Amplifying Reaction Multiplier"
STAT_TRANSFORMATIVE_RXN_MULTIPLIER = "Transformative Reaction Multiplier"
STAT_BASE_DAMAGE = "Base Damage Output"

FLOWER_MAIN_STATS = {STAT_FLAT_HP: 4780}

PLUME_MAIN_STATS = {STAT_FLAT_ATK: 311}

SANDS_MAIN_STATS = {
    STAT_HP_PCT: 46.6,
    STAT_ATK_PCT: 46.6,
    STAT_DEF_PCT: 58.3,
    STAT_ER: 51.8,
    STAT_EM: 186.5
}

GOBLET_MAIN_STATS = {
    STAT_HP_PCT: 46.6,
    STAT_ATK_PCT: 46.6,
    STAT_DEF_PCT: 58.3,
    STAT_EM: 186.5,
    STAT_ELEMENTAL_DMG: 46.6,
    STAT_OTHER_DMG: 46.6,
    STAT_PHYSICAL_DMG: 58.3
}

CIRCLET_MAIN_STATS = {
    STAT_HP_PCT: 46.6,
    STAT_ATK_PCT: 46.6,
    STAT_DEF_PCT: 58.3,
    STAT_EM: 186.5,
    STAT_CR: 31.1,
    STAT_CD: 62.2,
    STAT_HB: 35.9
}

MAIN_STAT_VALUES = {
    TYPE_FLOWER: FLOWER_MAIN_STATS,
    TYPE_PLUME: PLUME_MAIN_STATS,
    TYPE_SANDS: SANDS_MAIN_STATS,
    TYPE_GOBLET: GOBLET_MAIN_STATS,
    TYPE_CIRCLET: CIRCLET_MAIN_STATS
}

SUBSTAT_VALUES = {
    STAT_FLAT_HP: 298.75,
    STAT_FLAT_ATK: 19.45,
    STAT_FLAT_DEF: 23.15,
    STAT_HP_PCT: 5.83,
    STAT_ATK_PCT: 5.83,
    STAT_DEF_PCT: 7.29,
    STAT_ER: 6.48,
    STAT_EM: 23.31,
    STAT_CR: 3.89,
    STAT_CD: 7.77
}

# Weights assigned to each substat which indicates the relative
# probability of each substat occurring.
SUBSTAT_POOL = [
    {"stat": STAT_FLAT_HP, "weight": 15},
    {"stat": STAT_FLAT_ATK, "weight": 15},
    {"stat": STAT_FLAT_DEF, "weight": 15},
    {"stat": STAT_HP_PCT, "weight": 10},
    {"stat": STAT_ATK_PCT, "weight": 10},
    {"stat": STAT_DEF_PCT, "weight": 10},
    {"stat": STAT_ER, "weight": 10},
    {"stat": STAT_EM, "weight": 10},
    {"stat": STAT_CR, "weight": 7.5},
    {"stat": STAT_CD, "weight": 7.5}
]

SKYWARD_ATLAS_STATS = {
    STAT_ATK_PCT: 33.1,
    STAT_ELEMENTAL_DMG: 12
}
SKYWARD_ATLAS = {
    "baseAtk": 674,
    "stats": SKYWARD_ATLAS_STATS
}

STRINGLESS_STATS = {
    STAT_EM: 165,
    STAT_ELEMENTAL_DMG: 24  # At R1.
}
STRINGLESS = {
    "baseAtk": 510,
    "stats": STRINGLESS_STATS
}

THE_CATCH_STATS = {
    STAT_ER: 41.9,
    STAT_CR: 12,
    STAT_ELEMENTAL_DMG: 32
}
THE_CATCH = {
    "baseAtk": 449,
    "stats": THE_CATCH_STATS
}

IRON_STING_STATS = {
    STAT_EM: 165,
    STAT_ELEMENTAL_DMG: 12  # At 2 stacks.
}
IRON_STING = {
    "baseAtk": 510,
    "stats": IRON_STING_STATS
}

FAVONIUS_LANCE_STATS = {STAT_ER: 30.6}
FAVONIUS_LANCE = {
    "baseAtk": 565,
    "stats": FAVONIUS_LANCE_STATS
}

DESERT_PAVILION_STATS = {STAT_ELEMENTAL_DMG: 15 + 40}  # 2P + 4P effect combined
DESERT_PAVILION_SET = {"stats": DESERT_PAVILION_STATS}

GOLDEN_TROUPE_STATS = {STAT_ELEMENTAL_DMG: 20 + 25 + 25}  # 2P + 4P effect combined
GOLDEN_TROUPE_SET = {"stats": GOLDEN_TROUPE_STATS}

EMBLEM_STATS = {STAT_ER: 20}
EMBLEM_SET = {
    "stats": EMBLEM_STATS,
    "dynamicStats": [{
        "sourceStat": STAT_ER,
        "targetStat": STAT_ELEMENTAL_DMG,
        "offset": 0,
        "multiplier": 0.25
    }]
}

PARADISE_STATS = {
    STAT_EM: 80,
    STAT_TRANSFORMATIVE_RXN_MULTIPLIER: 0.8
}
PARADISE_SET = {"stats": PARADISE_STATS}

TENACITY_STATS = {STAT_HP_PCT: 20}
TENACITY_SET = {"stats": TENACITY_STATS}

BLANK_CHARACTER_STATS = {
    STAT_FLAT_HP: 0,
    STAT_HP_PCT: 0,
    STAT_FLAT_ATK: 0,
    STAT_ATK_PCT: 0,
    STAT_FLAT_DEF: 0,
    STAT_DEF_PCT: 0,
    STAT_ER: 100,
    STAT_EM: 0,
    STAT_CR: 5,
    STAT_CD: 50,
    STAT_AMPLIFYING_RXN_MULTIPLIER: 1,
    STAT_TRANSFORMATIVE_RXN_MULTIPLIER: 1,
    STAT_ELEMENTAL_DMG: 0
}

WANDERER_STATS = copy.deepcopy(BLANK_CHARACTER_STATS)
WANDERER_STATS.update({
    STAT_ATK_PCT: 30,  # Assuming Pyro is absorbed by his Skill.
    STAT_CR: 24.2
})
WANDERER = {
    "baseHp": 10164,
    "baseAtk": 328,
    "baseDef": 607,
    "weapon": SKYWARD_ATLAS,
    "artifactSet": DESERT_PAVILION_SET,
    "stats": WANDERER_STATS
}

FISCHL_STATS = copy.deepcopy(BLANK_CHARACTER_STATS)
FISCHL_STATS[STAT_ATK_PCT] = 24
FISCHL = {
    "baseHp": 9189,
    "baseAtk": 244,
    "baseDef": 593,
    "weapon": STRINGLESS,
    "artifactSet": GOLDEN_TROUPE_SET,
    "stats": FISCHL_STATS
}

XIANGLING_STATS = copy.deepcopy(BLANK_CHARACTER_STATS)
XIANGLING_STATS[STAT_EM] = 96
XIANGLING = {
    "baseHp": 10875,
    "baseAtk": 225,
    "baseDef": 669,
    "weapon": THE_CATCH,
    "artifactSet": EMBLEM_SET,
    "stats": XIANGLING_STATS,
    "usesAmplifyingReactions": True
}

KUKI_STATS = copy.deepcopy(BLANK_CHARACTER_STATS)
KUKI_STATS[STAT_EM] = 96
KUKI = {
    "baseHp": 12289,
    "baseAtk": 212,
    "baseDef": 751,
    "weapon": IRON_STING,
    "artifactSet": PARADISE_SET,
    "stats": KUKI_STATS,
    "usesTransformativeReactions": True
}

ZHONGLI_STATS = copy.deepcopy(BLANK_CHARACTER_STATS)
ZHONGLI_STATS[STAT_ELEMENTAL_DMG] = 28.8
ZHONGLI = {
    "baseHp": 14695,
    "baseAtk": 251,
    "baseDef": 737,
    "weapon": FAVONIUS_LANCE,
    "artifactSet": TENACITY_SET,
    "stats": ZHONGLI_STATS,
    "usesHpOnly": True
}

RAIDEN_STATS = copy.deepcopy(BLANK_CHARACTER_STATS)
RAIDEN_STATS.update({
    STAT_ER: 132,
    STAT_ELEMENTAL_DMG: 26.1  # From Skill passive.
})
RAIDEN = {
    "baseHp": 12907,
    "baseAtk": 337,
    "baseDef": 789,
    "weapon": THE_CATCH,
    "artifactSet": EMBLEM_SET,
    "stats": RAIDEN_STATS,
    "dynamicStats": [{
        "sourceStat": STAT_ER,
        "targetStat": STAT_ELEMENTAL_DMG,
        "offset": -100,
        "multiplier": 0.4  # from A4 passive.
    }]
}

# Configurable input parameters
ITERATIONS = 1
MAX_NUM_WEEKS = 20
STARTING_WEEK = 1
CHARACTER_UNDER_TEST = WANDERER
USE_STRONGBOX = False
BENNETT_ATK_BUFF = 0

SET1 = "Emblem of Severed Fate"
SET2 = "Shimenawa's Reminiscence"
DESIRED_SET = SET1

DESIRED_MAIN_STATS = {
    TYPE_SANDS: [STAT_ATK_PCT],
    TYPE_GOBLET: [STAT_ELEMENTAL_DMG],
    TYPE_CIRCLET: [STAT_CR, STAT_CD]
}

DESIRED_SUBSTATS = [
    STAT_ATK_PCT,
    STAT_CR,
    STAT_CD,
    STAT_ER
]
