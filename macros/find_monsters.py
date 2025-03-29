import os
import logging
from macros.get_all import monsters_on_map
from macros.get_one import monster

logger = logging.getLogger()

def find_monsters(criteria_func):
    logging.info("Finding certain monsters")
    monster_locations = monsters_on_map()
    matching_monsters = [monster_location for monster_location in monster_locations if criteria_func(monster(monster_location["content"]["code"]))]
    return matching_monsters