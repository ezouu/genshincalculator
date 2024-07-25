# artifact_simulation_utils.py

from config import (
    RESIN_PER_WEEK,
    RESIN_PER_RUN,
    ARTIFACTS_PER_RUN,
    TYPE_FLOWER,
    TYPE_PLUME,
    TYPE_SANDS,
    TYPE_GOBLET,
    TYPE_CIRCLET,
    ARTIFACT_TYPES,
    STAT_BASE_HP,
    STAT_FLAT_HP,
    STAT_HP_PCT,
    STAT_TOTAL_HP,
    STAT_BASE_ATK,
    STAT_FLAT_ATK,
    STAT_ATK_PCT,
    STAT_TOTAL_ATK,
    STAT_BASE_DEF,
    STAT_FLAT_DEF,
    STAT_DEF_PCT,
    STAT_TOTAL_DEF,
    STAT_ER,
    STAT_EM,
    STAT_ELEMENTAL_DMG,
    STAT_PHYSICAL_DMG,
    STAT_OTHER_DMG,
    STAT_CR,
    STAT_CD,
    STAT_HB,
    STAT_AMPLIFYING_RXN_MULTIPLIER,
    STAT_TRANSFORMATIVE_RXN_MULTIPLIER,
    STAT_BASE_DAMAGE,
    FLOWER_MAIN_STATS,
    PLUME_MAIN_STATS,
    SANDS_MAIN_STATS,
    GOBLET_MAIN_STATS,
    CIRCLET_MAIN_STATS,
    MAIN_STAT_VALUES,
    SUBSTAT_VALUES,
    SUBSTAT_POOL,
    SKYWARD_ATLAS_STATS,
    SKYWARD_ATLAS,
    STRINGLESS_STATS,
    STRINGLESS,
    THE_CATCH_STATS,
    THE_CATCH,
    IRON_STING_STATS,
    IRON_STING,
    FAVONIUS_LANCE_STATS,
    FAVONIUS_LANCE,
    DESERT_PAVILION_STATS,
    DESERT_PAVILION_SET,
    GOLDEN_TROUPE_STATS,
    GOLDEN_TROUPE_SET,
    EMBLEM_STATS,
    EMBLEM_SET,
    PARADISE_STATS,
    PARADISE_SET,
    TENACITY_STATS,
    TENACITY_SET,
    BLANK_CHARACTER_STATS,
    WANDERER_STATS,
    WANDERER,
    FISCHL_STATS,
    FISCHL,
    XIANGLING_STATS,
    XIANGLING,
    KUKI_STATS,
    KUKI,
    ZHONGLI_STATS,
    ZHONGLI,
    RAIDEN_STATS,
    RAIDEN,
    ITERATIONS,
    MAX_NUM_WEEKS,
    STARTING_WEEK,
    CHARACTER_UNDER_TEST,
    USE_STRONGBOX,
    BENNETT_ATK_BUFF,
    SET1,
    SET2,
    DESIRED_SET,
    DESIRED_MAIN_STATS,
    DESIRED_SUBSTATS
)

from utils import (
    get_artifact, upgrade_to_four, upgrade_artifact, debug_log, custom_round
)

def simulate_multi_week_artifact_progression(
    character, resin_per_week, resin_per_run, artifacts_per_run, 
    stat_base_damage, iterations, starting_week, max_num_weeks, bennett_atk_buff
):
    results_by_week = []
    
    for current_week in range(starting_week, max_num_weeks + 1):
        num_artifacts_to_farm = int(current_week * resin_per_week / resin_per_run * artifacts_per_run)
        result = simulate_artifact_progression(character, num_artifacts_to_farm)
        results_by_week.append(result)
    
    if starting_week == max_num_weeks:
        print(f"Average total stats: \n{format_stats(character, results_by_week[0]['averageTotalStats'])}")
    
    print(multi_week_results_to_csv(character, results_by_week))

def simulate_artifact_progression(character, num_artifacts_per_iteration):
    total_artifacts_obtained = 0
    total_artifacts_upgraded = 0
    total_upgraded_to_four_but_skipped = 0
    average_total_stats = None
    
    for _ in range(ITERATIONS):
        equipped_artifacts = {}
        best_total_stats = None

        artifacts_to_roll = num_artifacts_per_iteration
        debug_log(f"Number of Artifacts to simulate: {artifacts_to_roll}", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
        
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
                    debug_log(f"Equipped Artifact of type {artifact_type}", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
                    debug_log(format_artifact(artifact), ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
                    best_total_stats = get_total_stats(character, list(equipped_artifacts.values()))
                    continue

                if is_three_line_starter:
                    if is_worth_upgrading(artifact):
                        artifact = upgrade_to_four(artifact)
                    else:
                        debug_log("Artifact is not worth upgrading.", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
                        continue

                if not is_worth_upgrading(artifact):
                    if is_three_line_starter:
                        upgraded_to_four_but_skipped += 1
                    debug_log("Artifact is not worth upgrading.", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
                    continue

                upgrade_artifact(artifact)
                artifacts_upgraded += 1

                existing_artifact = equipped_artifacts.get(artifact_type)
                total_stats1 = get_total_stats(character, list(equipped_artifacts.values()))

                equipped_artifacts[artifact_type] = artifact
                total_stats2 = get_total_stats(character, list(equipped_artifacts.values()))

                if total_stats2[STAT_BASE_DAMAGE] > total_stats1[STAT_BASE_DAMAGE]:
                    best_total_stats = total_stats2
                    debug_log(f"Replaced {artifact_type} with better Artifact:", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
                    debug_log(format_artifact(artifact), ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
                else:
                    best_total_stats = total_stats1
                    equipped_artifacts[artifact_type] = existing_artifact
                    debug_log(f"Currently equipped {artifact_type} is better.", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)

            total_artifacts_obtained += artifacts_obtained
            total_artifacts_upgraded += artifacts_upgraded
            total_upgraded_to_four_but_skipped += upgraded_to_four_but_skipped

            remaining_artifacts = artifacts_to_roll - artifacts_upgraded - upgraded_to_four_but_skipped
            artifacts_to_recycle = remaining_artifacts + leftover_artifacts

            debug_log(f"Artifacts obtained: {artifacts_obtained}", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
            debug_log(f"Upgraded to +20: {artifacts_upgraded}", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
            debug_log(f"Upgraded to +4, but skipped: {upgraded_to_four_but_skipped}", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)
            debug_log(f"Artifacts to recycle: {artifacts_to_recycle}", ITERATIONS, MAX_NUM_WEEKS, STARTING_WEEK)

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
        file.write("Week,Obtained Artifacts,Upgraded Artifacts,Upgraded to Four but Skipped,HP %,DEF %,ATK %,Total ATK,EM,ER,Crit Rate %,Crit DMG %,Elemental DMG,Base Damage\n")

        for week, result in enumerate(results_by_week, start=1):
            line = f"{week},{result['obtainedArtifacts']},{result['upgradedArtifacts']},{result['upgradedToFourButSkipped']}"
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

