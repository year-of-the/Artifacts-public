import logging
from utils.api import fight, rest
from macros.find_monsters import find_monsters
from macros.safely import safely_move
from macros.choose_your_character import choose_character
from tactics.sim_battle import simulate_battles, get_character_battle_stats

logger = logging.getLogger()

# some example code
def main():
    character_name = "FatMan"
    choose_character(character_name)
    character_battle_stats = get_character_battle_stats(character_name)

    def easy_to_beat(monster):
        return simulate_battles(monster["code"], character_battle_stats, 100)["win_rate"] > 90

    logger.info(character_battle_stats)
    rest()
    weaker_monster_locations = find_monsters(easy_to_beat)
    if len(weaker_monster_locations) > 0:
        x, y = (weaker_monster_locations[0]["x"], weaker_monster_locations[0]["y"])
        safely_move(x, y)
        result = fight()
        logger.info(result)
        rest()
    else:
        logger.info("you've defeated every easy monster already")

if __name__ == "__main__":
    main()