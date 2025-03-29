from utils.api import move
from utils.state import state

def safely_move(x, y):
    if state.get_current_character_attribute("x") != x or state.get_current_character_attribute("y") != y:
        return move(x, y)

