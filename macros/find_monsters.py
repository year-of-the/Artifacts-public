import os
from macros.get_all import monsters_on_map
from macros.get_one import monster

verbose_mode=bool(os.environ.get("verbose"))

def find_monsters(criteria_func):
    if verbose_mode: print("Finding certain monsters")
    
    monster_locations = monsters_on_map()
    matching_monsters = [monster_location for monster_location in monster_locations if criteria_func(monster(monster_location["content"]["code"]))]
    return matching_monsters