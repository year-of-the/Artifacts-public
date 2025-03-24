import os
import json
from macros.find_monsters import find_monsters
from utils.api import rest, choose_character, move, get_character
from utils.cooldown_controller import cooldown_controller
from tactics.sim_battle import simulate_battles
from dotenv import load_dotenv

load_dotenv()

verbose_mode = bool(os.environ.get("verbose"))

def main():
    print("VS blue_slime", simulate_battles("Sonko", "blue_slime"))
    print("VS cow", simulate_battles("Sonko", "cow"))

if __name__ == "__main__":
    main()