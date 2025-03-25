from utils.api import move
from utils.state import state

def safe_move(x, y):
    if state.get("x") != x or state.get("y") != y:
        move(x, y)
        state.set("x", x)
        state.set("y", y)