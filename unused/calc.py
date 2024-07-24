import random
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


def simulate_multi_week_artifact_progression():
    results_by_week = []
    
    for current_week in range(STARTING_WEEK, MAX_NUM_WEEKS + 1):
        num_artifacts_to_farm = int(current_week * RESIN_PER_WEEK / RESIN_PER_RUN * ARTIFACTS_PER_RUN)
        result = simulate_artifact_progression(CHARACTER_UNDER_TEST, num_artifacts_to_farm)
        results_by_week.append(result)
    
    if STARTING_WEEK == MAX_NUM_WEEKS:
        print(f"Average total stats: \n{format_stats(CHARACTER_UNDER_TEST, results_by_week[0]['averageTotalStats'])}")
    
    print(multi_week_results_to_csv(CHARACTER_UNDER_TEST, results_by_week))


def simulate_artifact_progression(character, num_artifacts_per_iteration):
    total_artifacts_obtained = 0
    total_artifacts_upgraded = 0
    total_upgraded_to_four_but_skipped = 0
    average_total_stats = None
    
    for _ in range(ITERATIONS):
        equipped_artifacts = {}
        best_total_stats = None

        artifacts_to_roll = num_artifacts_per_iteration
        debug_log(f"Number of Artifacts to simulate: {artifacts_to_roll}")
        
        leftover_artifacts = 0
        get_artifacts_from_strongbox = False
        
        while artifacts_to_roll > 0:
            artifacts_obtained = 0
            artifacts_upgraded = 0
            upgraded_to_four_but_skipped = 0
            for _ in range(artifacts_to_roll):
                artifact = get_artifact(get_artifacts_from_strongbox)
                artifacts_obtained += 1
                artifact_type = artifact["type"]
                is_three_line_starter = len(artifact["substats"]) == 3

                is_slot_empty = artifact_type not in equipped_artifacts
                if is_slot_empty and artifact["set"] == DESIRED_SET:
                    if is_three_line_starter:
                        artifact = upgrade_to_four(artifact)
                    upgrade_artifact(artifact)
                    artifacts_upgraded += 1
                    equipped_artifacts[artifact_type] = artifact
                    debug_log(f"Equipped Artifact of type {artifact_type}")
                    debug_log(format_artifact(artifact))
                    best_total_stats = get_total_stats(character, list(equipped_artifacts.values()))
                    continue

                if is_three_line_starter:
                    if is_worth_upgrading(artifact):
                        artifact = upgrade_to_four(artifact)
                    else:
                        debug_log("Artifact is not worth upgrading.")
                        continue

                if not is_worth_upgrading(artifact):
                    if is_three_line_starter:
                        upgraded_to_four_but_skipped += 1
                    debug_log("Artifact is not worth upgrading.")
                    continue

                upgrade_artifact(artifact)
                artifacts_upgraded += 1

                existing_artifact = equipped_artifacts.get(artifact_type)
                total_stats1 = get_total_stats(character, list(equipped_artifacts.values()))

                equipped_artifacts[artifact_type] = artifact
                total_stats2 = get_total_stats(character, list(equipped_artifacts.values()))

                if total_stats2[STAT_BASE_DAMAGE] > total_stats1[STAT_BASE_DAMAGE]:
                    best_total_stats = total_stats2
                    debug_log(f"Replaced {artifact_type} with better Artifact:")
                    debug_log(format_artifact(artifact))
                else:
                    best_total_stats = total_stats1
                    equipped_artifacts[artifact_type] = existing_artifact
                    debug_log(f"Currently equipped {artifact_type} is better.")

            total_artifacts_obtained += artifacts_obtained
            total_artifacts_upgraded += artifacts_upgraded
            total_upgraded_to_four_but_skipped += upgraded_to_four_but_skipped

            remaining_artifacts = artifacts_to_roll - artifacts_upgraded - upgraded_to_four_but_skipped
            artifacts_to_recycle = remaining_artifacts + leftover_artifacts

            debug_log(f"Artifacts obtained: {artifacts_obtained}")
            debug_log(f"Upgraded to +20: {artifacts_upgraded}")
            debug_log(f"Upgraded to +4, but skipped: {upgraded_to_four_but_skipped}")
            debug_log(f"Artifacts to recycle: {artifacts_to_recycle}")

            if not USE_STRONGBOX or artifacts_to_recycle < 3:
                break

            artifacts_to_roll = artifacts_to_recycle // 3
            leftover_artifacts = artifacts_to_recycle % 3
            get_artifacts_from_strongbox = True

        average_total_stats = aggregate_total_stats(average_total_stats, best_total_stats)

        if ITERATIONS == 1:
            print("Best artifact setup:")
            print(format_artifacts(equipped_artifacts))
            print(format_stats(character, average_total_stats))

    map_onto_total_stats(average_total_stats, lambda stat: stat / ITERATIONS)
    
    result = {
        "obtainedArtifacts": total_artifacts_obtained,
        "upgradedArtifacts": total_artifacts_upgraded,
        "upgradedToFourButSkipped": total_upgraded_to_four_but_skipped,
        "averageTotalStats": average_total_stats
    }

    if ITERATIONS == 1:
        print("\n\n\n")
        print(f"Artifacts obtained: {total_artifacts_obtained}")
        print(f"Upgraded to +20: {total_artifacts_upgraded}")
        print("\n\n")

    return result


def is_worth_upgrading(artifact):
    artifact_type = artifact["type"]
    if artifact["set"] != DESIRED_SET and artifact_type != TYPE_GOBLET:
        return False

    num_substats = len(artifact["substats"])
    desirable_substats = sum(1 for substat in artifact["substats"] if substat["stat"] in DESIRED_SUBSTATS)
    
    if artifact_type in [TYPE_FLOWER, TYPE_PLUME]:
        return (num_substats == 3 and desirable_substats >= 1) or (num_substats == 4 and desirable_substats >= 2)

    if artifact["mainStat"]["stat"] not in DESIRED_MAIN_STATS[artifact_type]:
        return False

    return (num_substats == 4 and desirable_substats >= 1) or (num_substats != 4)


def get_total_stats(character, artifacts):
    weapon = character["weapon"]
    artifact_set = character["artifactSet"]
    base_atk = character["baseAtk"] + weapon["baseAtk"]
    base_def = character["baseDef"]
    base_hp = character["baseHp"]
    
    # Initialize all expected stats to zero
    total_stats = {
        STAT_FLAT_HP: 0,
        STAT_HP_PCT: 0,
        STAT_FLAT_ATK: 0,
        STAT_ATK_PCT: 0,
        STAT_FLAT_DEF: 0,
        STAT_DEF_PCT: 0,
        STAT_ER: 0,
        STAT_EM: 0,
        STAT_CR: 0,
        STAT_CD: 0,
        STAT_AMPLIFYING_RXN_MULTIPLIER: 0,
        STAT_TRANSFORMATIVE_RXN_MULTIPLIER: 0,
        STAT_ELEMENTAL_DMG: 0
    }

    aggregate_stats(character["stats"], total_stats)
    aggregate_stats(weapon["stats"], total_stats)
    aggregate_stats(artifact_set["stats"], total_stats)
    for artifact in artifacts:
        aggregate_artifact_stats(artifact, total_stats)

    if "dynamicStats" in character:
        for dynamic_stat in character["dynamicStats"]:
            source_stat_value = total_stats[dynamic_stat["sourceStat"]]
            total_stats[dynamic_stat["targetStat"]] += (source_stat_value + dynamic_stat["offset"]) * dynamic_stat["multiplier"]
    if "dynamicStats" in artifact_set:
        for dynamic_stat in artifact_set["dynamicStats"]:
            source_stat_value = total_stats[dynamic_stat["sourceStat"]]
            total_stats[dynamic_stat["targetStat"]] += (source_stat_value + dynamic_stat["offset"]) * dynamic_stat["multiplier"]

    total_em = total_stats[STAT_EM]
    total_stats[STAT_AMPLIFYING_RXN_MULTIPLIER] += 2.78 * total_em / (total_em + 1400)
    total_stats[STAT_TRANSFORMATIVE_RXN_MULTIPLIER] += 16 * total_em / (total_em + 2000)

    total_atk = base_atk * (1 + total_stats[STAT_ATK_PCT] / 100) + total_stats[STAT_FLAT_ATK] + BENNETT_ATK_BUFF
    total_hp = base_hp * (1 + total_stats[STAT_HP_PCT] / 100) + total_stats[STAT_FLAT_HP]
    total_def = base_def * (1 + total_stats[STAT_DEF_PCT] / 100) + total_stats[STAT_FLAT_DEF]
    total_stats[STAT_BASE_ATK] = base_atk
    total_stats[STAT_TOTAL_ATK] = total_atk
    total_stats[STAT_TOTAL_HP] = total_hp
    total_stats[STAT_TOTAL_DEF] = total_def
    total_stats[STAT_BASE_DAMAGE] = get_base_damage(character, total_stats)

    return total_stats

def get_base_damage(character, total_stats):
    if character.get("usesTransformativeReactions"):
        base_reaction_damage = 4340.56
        return base_reaction_damage * total_stats[STAT_TRANSFORMATIVE_RXN_MULTIPLIER]

    if character.get("usesHpOnly"):
        return total_stats[STAT_TOTAL_HP]

    total_atk = total_stats[STAT_TOTAL_ATK]
    dmg_pct_multiplier = 1 + total_stats[STAT_ELEMENTAL_DMG] / 100
    crit_multiplier = 1 + (total_stats[STAT_CR] * total_stats[STAT_CD] / 10000)
    amplifying_reaction_multiplier = 1
    if character.get("usesAmplifyingReactions"):
        base_reaction_multiplier = 1.5  # Assuming reverse Melt/Vaporize
        amplifying_reaction_multiplier = base_reaction_multiplier * total_stats[STAT_AMPLIFYING_RXN_MULTIPLIER]
    return total_atk * dmg_pct_multiplier * crit_multiplier * amplifying_reaction_multiplier


def aggregate_stats(stats, total_stats):
    for stat_name, value in stats.items():
        add_or_set_stat(stat_name, value, total_stats)


def aggregate_artifact_stats(artifact, total_stats):
    if not artifact:
        return

    main_stat = artifact["mainStat"]
    add_or_set_stat(main_stat["stat"], main_stat["value"], total_stats)

    for substat in artifact["substats"]:
        add_or_set_stat(substat["stat"], substat["value"], total_stats)


def add_or_set_stat(stat, value, total_stats):
    if not value:
        return

    if stat not in total_stats or not total_stats[stat]:
        total_stats[stat] = value
    else:
        total_stats[stat] += value


def aggregate_total_stats(total_stats1, total_stats2):
    if not total_stats1:
        return total_stats2

    if not total_stats2:
        return total_stats1

    for stat, value in total_stats1.items():
        total_stats1[stat] += total_stats2[stat]
    return total_stats1


def map_onto_total_stats(total_stats, map_function):
    for stat, value in total_stats.items():
        total_stats[stat] = map_function(value)


def get_artifact(from_strongbox):
    artifact_set = get_set()
    artifact_type = get_type()
    main_stat = get_main_stat(artifact_type)
    num_substats = get_num_substats(from_strongbox)
    num_upgrades_remaining = 5
    substats = get_substats(main_stat, [], num_substats)

    artifact = {
        "set": artifact_set,
        "type": artifact_type,
        "mainStat": {
            "stat": main_stat,
            "value": 0  # placeholder value until artifact is upgraded
        },
        "numUpgradesRemaining": num_upgrades_remaining,
        "substats": substats
    }
    return artifact


def get_set():
    return SET1 if random.random() < 0.5 else SET2


def get_type():
    return random.choice(ARTIFACT_TYPES)


def get_main_stat(artifact_type):
    random_number = random.random()
    if artifact_type == TYPE_FLOWER:
        return STAT_FLAT_HP
    elif artifact_type == TYPE_PLUME:
        return STAT_FLAT_ATK
    elif artifact_type == TYPE_SANDS:
        return get_sands_main_stat(random_number)
    elif artifact_type == TYPE_GOBLET:
        return get_goblet_main_stat(random_number)
    elif artifact_type == TYPE_CIRCLET:
        return get_circlet_main_stat(random_number)


def get_sands_main_stat(random_number):
    if random_number < 0.2668:
        return STAT_HP_PCT
    elif random_number < 0.5334:
        return STAT_ATK_PCT
    elif random_number < 0.80:
        return STAT_DEF_PCT
    elif random_number < 0.90:
        return STAT_ER
    else:
        return STAT_EM


def get_goblet_main_stat(random_number):
    if random_number < 0.1925:
        return STAT_HP_PCT
    elif random_number < 0.3850:
        return STAT_ATK_PCT
    elif random_number < 0.5750:
        return STAT_DEF_PCT
    elif random_number < 0.60:
        return STAT_EM
    elif random_number < 0.65:
        return STAT_ELEMENTAL_DMG
    elif random_number < 0.70:
        return STAT_PHYSICAL_DMG
    else:
        return STAT_OTHER_DMG


def get_circlet_main_stat(random_number):
    if random_number < 0.22:
        return STAT_HP_PCT
    elif random_number < 0.44:
        return STAT_ATK_PCT
    elif random_number < 0.66:
        return STAT_DEF_PCT
    elif random_number < 0.76:
        return STAT_CR
    elif random_number < 0.86:
        return STAT_CD
    elif random_number < 0.96:
        return STAT_HB
    else:
        return STAT_EM


def get_num_substats(from_strongbox):
    random_number = random.random()
    if from_strongbox:
        return 3 if random_number < 0.66 else 4
    else:
        return 3 if random_number < 0.80 else 4


def get_substats(main_stat, existing_substats, num_substats):
    existing_substats_list = [substat["stat"] for substat in existing_substats]
    available_substats = [substat for substat in SUBSTAT_POOL if substat["stat"] != main_stat and substat["stat"] not in existing_substats_list]

    substats = [get_substat(available_substats) for _ in range(num_substats)]
    return substats


def get_substat(available_substats):
    substat_dist = []
    cumulative_weight = 0
    for substat in available_substats:
        cumulative_weight += substat["weight"]
        substat_dist.append(cumulative_weight)

    random_number = random.random() * cumulative_weight
    selected_substat_index = 0
    for i, weight in enumerate(substat_dist):
        selected_substat_index = i
        if random_number < weight:
            break

    substat = {"stat": available_substats[selected_substat_index]["stat"]}
    substat["value"] = get_substat_value(SUBSTAT_VALUES[substat["stat"]])

    available_substats.pop(selected_substat_index)
    return substat


def get_substat_value(original_value):
    random_number = random.random()
    if random_number < 0.25:
        return original_value * 0.7
    elif random_number < 0.50:
        return original_value * 0.8
    elif random_number < 0.75:
        return original_value * 0.9
    else:
        return original_value


def upgrade_to_four(artifact):
    if len(artifact["substats"]) == 4:
        return artifact

    new_substat = get_substats(artifact["mainStat"]["stat"], artifact["substats"], 1)[0]
    artifact["substats"].append(new_substat)
    artifact["numUpgradesRemaining"] = 4
    return artifact


def upgrade_artifact(artifact):
    artifact["mainStat"]["value"] = MAIN_STAT_VALUES[artifact["type"]][artifact["mainStat"]["stat"]]

    substats = artifact["substats"]
    for _ in range(artifact["numUpgradesRemaining"]):
        random_index = random.randint(0, len(substats) - 1)
        substat_to_upgrade = substats[random_index]

        value = get_substat_value(SUBSTAT_VALUES[substat_to_upgrade["stat"]])
        substat_to_upgrade["value"] += value


def format_stats(character, total_stats):
    output = ""

    output += f"\nHP %: {custom_round(total_stats[STAT_HP_PCT], 1)}"
    output += f"\nDEF %: {custom_round(total_stats[STAT_DEF_PCT], 1)}"
    output += f"\nBase ATK: {custom_round(total_stats[STAT_BASE_ATK], 0)}"
    output += f"\nATK %: {custom_round(total_stats[STAT_ATK_PCT], 1)}"
    output += f"\nFlat ATK: {custom_round(total_stats[STAT_FLAT_ATK], 0)}"
    if BENNETT_ATK_BUFF > 0:
        output += f"\nBennett ATK Buff: {custom_round(BENNETT_ATK_BUFF, 0)}"
    output += f"\nTotal ATK: {custom_round(total_stats[STAT_TOTAL_ATK], 0)}"
    output += "\n"
    output += f"\nEM: {custom_round(total_stats[STAT_EM], 0)}"
    if character.get("usesAmplifyingReactions"):
        output += f"\nAmplifying Reaction Multiplier: {custom_round(total_stats[STAT_AMPLIFYING_RXN_MULTIPLIER], 2)}"
    output += "\n"
    output += f"\nCrit Rate %: {custom_round(total_stats[STAT_CR], 1)}"
    output += f"\nCrit DMG %: {custom_round(total_stats[STAT_CD], 1)}"
    output += "\n"
    output += f"\nER %: {custom_round(total_stats[STAT_ER], 1)}"
    output += "\n"
    output += f"\nTotal DMG %: {custom_round(total_stats[STAT_ELEMENTAL_DMG], 1)}"
    output += "\n"
    output += f"\nExpected Base Damage: {custom_round(total_stats[STAT_BASE_DAMAGE], 0)}"

    return output


def format_artifacts(artifacts):
    output = ""

    for artifact_type in ARTIFACT_TYPES:
        artifact = artifacts.get(artifact_type)
        output += format_artifact(artifact)
        output += "\n"

    return output


def format_artifact(artifact):
    if not artifact:
        return "No available artifact."

    output = ""
    main_stat = artifact["mainStat"]
    substats = artifact["substats"]
    output += f"\n{artifact['type']} - {artifact['set']}"
    output += f"\n{main_stat['stat']}"
    if main_stat["value"] > 0:
        output += f": {custom_round(main_stat['value'], 1)}"
    for substat in substats:
        output += f"\n\t{substat['stat']}: {custom_round(substat['value'], 1)}"

    return output


def to_csv_format(character, total_stats, artifacts_upgraded, artifacts_upgraded_to_four):
    output = ""

    output += f"\n{artifacts_upgraded}"
    output += f"\n{artifacts_upgraded_to_four}"
    output += "\n"
    output += f"\n{custom_round(total_stats[STAT_HP_PCT], 1)}"
    output += f"\n{custom_round(total_stats[STAT_DEF_PCT], 1)}"
    output += f"\n{custom_round(total_stats[STAT_ATK_PCT], 1)}"
    output += f"\n{custom_round(total_stats[STAT_TOTAL_ATK], 0)}"
    output += "\n"
    output += f"\n{custom_round(total_stats[STAT_EM], 0)}"
    output += f"\n{custom_round(total_stats[STAT_ER], 1)}"
    output += f"\n{custom_round(total_stats[STAT_CR], 1)}"
    output += f"\n{custom_round(total_stats[STAT_CD], 1)}"
    output += f"\n{custom_round(total_stats[STAT_ELEMENTAL_DMG], 1)}"
    output += f"\n{custom_round(total_stats[STAT_BASE_DAMAGE], 0)}"
    output += "\n"

    return output


def multi_week_results_to_csv(character, results_by_week, filename="results.csv"):
    with open(filename, 'w') as file:
        # Write header line for CSV file
        file.write("Obtained Artifacts,Upgraded Artifacts,Upgraded to Four but Skipped,HP %,DEF %,ATK %,Total ATK,EM,ER,Crit Rate %,Crit DMG %,Elemental DMG,Base Damage\n")

        for result in results_by_week:
            line = f"{result['obtainedArtifacts']},{result['upgradedArtifacts']},{result['upgradedToFourButSkipped']}"
            total_stats = result['averageTotalStats']
            line += f",{round(total_stats[STAT_HP_PCT], 1)}"
            line += f",{round(total_stats[STAT_DEF_PCT], 1)}"
            line += f",{round(total_stats[STAT_ATK_PCT], 1)}"
            line += f",{round(total_stats[STAT_TOTAL_ATK], 0)}"
            line += f",{round(total_stats[STAT_EM], 0)}"
            line += f",{round(total_stats[STAT_ER], 1)}"
            line += f",{round(total_stats[STAT_CR], 1)}"
            line += f",{round(total_stats[STAT_CD], 1)}"
            line += f",{round(total_stats[STAT_ELEMENTAL_DMG], 1)}"
            line += f",{round(total_stats[STAT_BASE_DAMAGE], 0)}"
            line += "\n"
            file.write(line)

def custom_round(value, decimal_places):
    multiplier = 10 ** decimal_places
    return round(value * multiplier) / multiplier


def debug_log(message):
    if ITERATIONS == 1 and MAX_NUM_WEEKS == STARTING_WEEK:
        print(message)


# Entry point
simulate_multi_week_artifact_progression()
