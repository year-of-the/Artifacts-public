import os
from utils.api import get_character
from utils.state import state
from dotenv import load_dotenv

load_dotenv(override=True)

verbose_mode = bool(os.environ.get("verbose"))

def choose_character(name):
    if verbose_mode: print(f"Setting '{name}' as current character")
    state.set_current_character(name)
    character_stats = get_character(state.CURRENT_CHARACTER_NAME)["data"]
    state.set("x", character_stats["x"])
    state.set("y", character_stats["y"])
    return character_stats