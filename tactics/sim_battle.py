import math
import copy
from random import randint
from utils.state import state
from utils.api import get_character
from macros import get_one

item_slots = ["rune_slot","shield_slot","helmet_slot","body_armor_slot","leg_armor_slot","boots_slot","ring1_slot","ring2_slot","amulet_slot","artifact1_slot","artifact2_slot","artifact3_slot"]
relevant_battle_effects = ["healing", "lifesteal", "burn", "reconstitution"]
dots_types = ["poison", "burn"]

def game_round(value):
    return math.floor(value + 0.5)

def get_multiplied_attack(attack, dmg_multiplier):
    return game_round(attack * (1 + (dmg_multiplier * 0.01)))

def get_attack_after_resist(attack, defender_resist):
    return game_round(attack * (1 - (defender_resist * 0.01)))

def restore_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if entity_stats["hp"] <= game_round(entity_stats["max_hp"]/2) and utility["quantity"] > 0:
        entity_stats["hp"] = min(entity_stats["hp"] + utility["value"], entity_stats["max_hp"])
        utility["quantity"] -= 1

def boost_dmg_fire_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    round_index = math.floor((turn_num-1)/2)
    if round_index == 0 and utility["quantity"] > 0:
        entity_stats["fire_dmg"] += utility["value"]
        utility["quantity"] -= 1

def boost_dmg_earth_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if round_index == 0 and utility["quantity"] > 0:
        entity_stats["earth_dmg"] += utility["value"]
        utility["quantity"] -= 1

def boost_dmg_water_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if round_index == 0 and utility["quantity"] > 0:
        entity_stats["water_dmg"] += utility["value"]
        utility["quantity"] -= 1

def boost_dmg_air_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if round_index == 0 and utility["quantity"] > 0:
        entity_stats["air_dmg"] += utility["value"]
        utility["quantity"] -= 1

def boost_res_fire_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if round_index == 0 and utility["quantity"] > 0:
        entity_stats["fire_resist"] += utility["value"]
        utility["quantity"] -= 1

def boost_res_earth_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if round_index == 0 and utility["quantity"] > 0:
        entity_stats["earth_resist"] += utility["value"]
        utility["quantity"] -= 1

def boost_res_water_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if round_index == 0 and utility["quantity"] > 0:
        entity_stats["water_resist"] += utility["value"]
        utility["quantity"] -= 1

def boost_res_air_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if round_index == 0 and utility["quantity"] > 0:
        entity_stats["air_resist"] += utility["value"]
        utility["quantity"] -= 1

def boost_hp_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    if round_index == 0:
        entity_stats["hp_max"] += utility["value"]
        entity_stats["hp"] += utility["value"]
        utility["quantity"] -= 1

def antipoison_func(entity_stats, opponent_stats, utility, round_index, turn_num):
    currently_poisoned = "poisoned" in entity_stats and entity_stats["poison"] > 0
    if currently_poisoned and utility["quantity"] > 0:
        entity_stats["poisoned"] = max(entity_stats["poisoned"] - utility["value"], 0)
        utility["quantity"] -= 1

def apply_burn_func(entity_stats, opponent_stats, effect, round_index, turn_num):
    total_attack = sum([
        get_multiplied_attack(entity_stats["fire_attack"], entity_stats["fire_dmg"]),
        get_multiplied_attack(entity_stats["earth_attack"], entity_stats["earth_dmg"]),
        get_multiplied_attack(entity_stats["water_attack"], entity_stats["water_dmg"]),
        get_multiplied_attack(entity_stats["air_attack"], entity_stats["air_dmg"])
    ])

    burn_percent = effect["value"]
    burn_amount = game_round(total_attack * burn_percent * 0.01)

    staggered_round_index = round_index - (max(turn_num - 2, 0) % 2)
    # this math means the sequence of range upper bounds marches with the turn as such
    # turn:     1 2 3 4 5 6 7 8 9 ...
    # sequence: 0 0 0 1 1 2 2 3 3 ...
    # thus, exactly matching the number of times burn damage diminishment should happen if burn dmg occurred on that turn
    for _ in range(staggered_round_index):
        burn_amount = max(min(game_round(burn_amount * 0.9), burn_amount - 1), 0)
    
    opponent_stats["burn"] = burn_amount

def apply_poison_func(entity_stats, opponent_stats, effect, round_index, turn_num):
    if round_index == 0:
        opponent_stats["poison"] = effect["value"]

def healing_func(entity_stats, opponent_stats, effect, round_index, turn_num):
    if round_index % 3 == 2:
        entity_stats["hp"] = min(entity_stats["max_hp"], game_round(entity_stats["hp"] + (entity_stats["max_hp"] * effect["value"] * 0.01)))

def reconstitution_func(entity_stats, opponent_stats, effect, round_index, turn_num):
    if effect["value"] == turn_num:
        entity_stats["hp"] = entity_stats["max_hp"]

battle_effect_function_glossary = {
    "burn": apply_burn_func,
    "poison": apply_poison_func,
    "healing": healing_func,
    "reconstitution": reconstitution_func,
}

utility_function_glossary = {
    "restore": restore_func,
    "boost_dmg_fire": boost_dmg_fire_func,
    "boost_dmg_earth": boost_dmg_earth_func,
    "boost_dmg_water": boost_dmg_water_func,
    "boost_dmg_air": boost_dmg_air_func,
    "boost_res_fire": boost_res_fire_func,
    "boost_res_earth": boost_res_earth_func,
    "boost_res_water": boost_res_water_func,
    "boost_res_air": boost_res_air_func,
    "boost_hp": boost_hp_func,
    "antipoison": antipoison_func,
}

def get_monster_stats(monster_code):
    monster = get_one.monster(monster_code)
    return {
        "max_hp": monster["hp"],
        "hp": monster["hp"],
        "fire_attack": monster["attack_fire"],
        "earth_attack": monster["attack_earth"],
        "water_attack": monster["attack_water"],
        "air_attack": monster["attack_air"],
        "fire_dmg": 0,
        "earth_dmg": 0,
        "water_dmg": 0,
        "air_dmg": 0,
        "fire_resist": monster["res_fire"],
        "earth_resist": monster["res_earth"],
        "water_resist": monster["res_water"],
        "air_resist": monster["res_air"],
        "critical_strike": monster["critical_strike"],
        "battle_effects": monster["effects"],
        "utilities": [],
        "poison": 0,
        "burn": 0,
    }

def get_character_battle_stats(character_name=state.CURRENT_CHARACTER_NAME):
    response = get_character(character_name)
    character = response["data"]

    utilities = []

    if character["utility1_slot"] != "" and character["utility1_slot_quantity"] > 0:
        utility = get_one.item(character["utility1_slot"])
        utilities.append({ **utility["effects"][0], "quantity": character["utility1_slot_quantity"] })
    if character["utility2_slot"] != "" and character["utility2_slot_quantity"] > 0:
        utility = get_one.item(character["utility2_slot"])
        utilities.append({ **utility["effects"][1], "quantity": character["utility2_slot_quantity"] })

    battle_effects = []
    for item_slot in item_slots:
        item_code = character[item_slot]
        if item_code != "":
            item = get_one.item(item_code)
            battle_effects += [effect for effect in item["effects"] if effect["code"] in relevant_battle_effects]
    
    return {
        "max_hp": character["max_hp"],
        "hp": character["hp"],
        "fire_attack": character["attack_fire"],
        "earth_attack": character["attack_earth"],
        "water_attack": character["attack_water"],
        "air_attack": character["attack_air"],
        "fire_dmg": character["dmg_fire"] + character["dmg"],
        "earth_dmg": character["dmg_earth"] + character["dmg"],
        "water_dmg": character["dmg_water"] + character["dmg"],
        "air_dmg": character["dmg_air"] + character["dmg"],
        "fire_resist": character["res_fire"],
        "earth_resist": character["res_earth"],
        "water_resist": character["res_water"],
        "air_resist": character["res_air"],
        "critical_strike": character["critical_strike"],
        "battle_effects": battle_effects,
        "utilities": utilities,
        "poison": 0,
        "burn": 0,
    }

def simulate_turn(entity_stats, opponent_entity_stats, round_index, turn_num):
    # utilities
    if "utilities" in entity_stats:
        for utility in entity_stats["utilities"]:
            if utility["quantity"] > 0:
                utility_func = utility_function_glossary[utility["code"]]
                utility_func(entity_stats, opponent_entity_stats, utility, round_index, turn_num)
    
    # applying dots
    for dots_type in dots_types:
        if dots_type in entity_stats:
            entity_stats["hp"] -= entity_stats[dots_type]

    # short circuit turn if dead
    if entity_stats["hp"] <= 0: return
    
    # other effects
    if "battle_effects" in entity_stats:
        for effect in entity_stats["battle_effects"]:
            if effect in relevant_battle_effects:
                battle_effect_func = battle_effect_function_glossary[effect["code"]]
                battle_effect_func(entity_stats, opponent_entity_stats, effect, round_index, turn_num)
    
    # attacking
    for attack_type, dmg_multiplier, res_type in [("fire_attack", "fire_dmg", "fire_resist"), ("earth_attack", "earth_dmg", "earth_resist"), ("water_attack", "water_dmg", "water_resist"), ("air_attack", "air_dmg", "air_resist")]:
        opponent_blocked = randint(1, 1000) <= opponent_entity_stats[res_type]
        if opponent_blocked: continue

        is_crit = randint(1, 100) <= entity_stats["critical_strike"]
        entity_attack = get_multiplied_attack(entity_stats[attack_type], entity_stats[dmg_multiplier])
        opponent_resist = opponent_entity_stats[res_type]
        lifesteal_effect = next((effect for effect in entity_stats["battle_effects"] if effect["code"] == "lifesteal"), None)
        actual_damage = game_round(get_attack_after_resist(entity_attack, opponent_resist) * (1.5 if is_crit else 1))

        opponent_entity_stats["hp"] -= actual_damage
        if lifesteal_effect and is_crit:
            entity_stats["hp"] = min(entity_stats["max_hp"], entity_stats["hp"] + game_round(actual_damage * 0.1 * lifesteal_effect["value"]))

def simulate_battle(character_battle_stats, monster_battle_stats):
    temp_char_stats = copy.deepcopy(character_battle_stats)
    temp_monster_stats = copy.deepcopy(monster_battle_stats)

    for round_index in range(50):
        character_turn_num = (round_index*2)+1
        monster_turn_num = (round_index+1)*2

        simulate_turn(temp_char_stats, temp_monster_stats, round_index, character_turn_num)
        if temp_monster_stats["hp"] <= 0:
            return True, character_turn_num
        elif temp_char_stats["hp"] <= 0:
            return False, character_turn_num

        simulate_turn(temp_monster_stats, temp_char_stats, round_index, monster_turn_num)
        if temp_monster_stats["hp"] <= 0:
            return True, monster_turn_num
        elif temp_char_stats["hp"] <= 0:
            return False, monster_turn_num
    
    return False, 101 # an impossible turn to indicate what happened

def simulate_battles(
        monster_code,
        character_battle_stats,
        iterations=1000
    ):
    monster_battle_stats = get_monster_stats(monster_code)
    wins = []
    losses = []
    
    for _ in range(iterations):
        won, on_turn = simulate_battle(character_battle_stats, monster_battle_stats)
        if won: wins.append(on_turn)
        else: losses.append(on_turn)
    
    return {
        "wins": { "num": len(wins), "average_turn": round(sum(wins)/len(wins)) if len(wins) > 0 else None },
        "losses": { "num": len(losses), "average_turn": round(sum(losses)/len(losses)) if len(losses) > 0 else None },
        "win_rate": round(100 * len(wins) / iterations, 2),
    }