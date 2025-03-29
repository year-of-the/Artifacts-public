from macros.get_all import content_on_map
from macros.safely import safely_move
from utils.helpers import distance
from utils.state import state

def nearest(content_code):
    x = state.get_current_character_attribute("x")
    y = state.get_current_character_attribute("y")
    locations = content_on_map(content_code=content_code)
    if not locations: return None
    distance_from_character = lambda location: distance((location["x"], location["y"]), (x,y))
    sorted(locations, key=distance_from_character)
    return locations[0] if len(locations) else None

def go_to_nearest(content_code):
    nearest_location = nearest(content_code=content_code)
    return safely_move(nearest_location["x"], nearest_location["y"]) if nearest_location else None