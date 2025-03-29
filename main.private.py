import os
from utils.api import fight, rest
from macros.get_all import get_whole_map
from macros.find_monsters import find_monsters
from macros.safely import safely_move
from macros.choose_your_character import choose_character
from macros.go_to_nearest import go_to_nearest
from macros.resource_finder import missing_requirements_to_craft, resource_finder
from tactics.sim_battle import simulate_battles, get_character_battle_stats
from dotenv import load_dotenv
import logging

load_dotenv(override=True)
verbose_mode = bool(os.environ.get("verbose"))
logging.basicConfig(level=logging.INFO if verbose_mode else logging.ERROR)
logger = logging.getLogger()

def main():
    character_name = "Sonko"
    choose_character(character_name)
    result = missing_requirements_to_craft("fire_staff")
    missing_resources = [resource for resource in result["missing_ingredients"] if resource["missing_quantity"] > 0]
    for missing in missing_resources:
        logger.info(resource_finder(missing["code"]))
    logger.info(result)

if __name__ == "__main__":
    main()