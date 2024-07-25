# utils.py

import random
from config import (
    MAIN_STAT_VALUES, SUBSTAT_VALUES, SUBSTAT_POOL, DESIRED_SET, 
    DESIRED_MAIN_STATS, DESIRED_SUBSTATS, ARTIFACT_TYPES, TYPE_FLOWER, 
    TYPE_PLUME, TYPE_SANDS, TYPE_GOBLET, TYPE_CIRCLET, STAT_FLAT_HP, 
    STAT_FLAT_ATK, STAT_HP_PCT, STAT_ATK_PCT, STAT_DEF_PCT, STAT_ER, 
    STAT_EM, STAT_ELEMENTAL_DMG, STAT_PHYSICAL_DMG, STAT_OTHER_DMG, 
    STAT_CR, STAT_CD, STAT_HB, SET1, SET2
)

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

def custom_round(value, decimal_places):
    multiplier = 10 ** decimal_places
    return round(value * multiplier) / multiplier

def debug_log(message, iterations, max_num_weeks, starting_week):
    if iterations == 1 and max_num_weeks == starting_week:
        print(message)
