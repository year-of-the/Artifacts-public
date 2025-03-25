from utils.api import fight, rest
from macros.find_monsters import find_monsters
from macros.safe_move import safe_move
from macros.choose_your_character import choose_character
from tactics.sim_battle import simulate_battles, get_character_battle_stats

# some example code
def main():
    character_name = "FatMan"
    choose_character(character_name)
    character_battle_stats = get_character_battle_stats(character_name)

    def easy_to_beat(monster):
        return simulate_battles(monster["code"], character_battle_stats, 100)["win_rate"] > 90

    print(character_battle_stats)
    rest()
    weaker_monster_locations = find_monsters(easy_to_beat)
    if len(weaker_monster_locations) > 0:
        x, y = (weaker_monster_locations[0]["x"], weaker_monster_locations[0]["y"])
        safe_move(x, y)
        result = fight()
        print(result)
        rest()
    else:
        print("you've defeated every easy monster already")

if __name__ == "__main__":
    main()