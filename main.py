import os
import json
from macros.find_monsters import find_monsters
from utils.api import rest, choose_character, move, get_character
from utils.cooldown_controller import cooldown_controller
import macros.get_one as get_one
from tactics.sim_battle import simulate_battles
from dotenv import load_dotenv

load_dotenv()

verbose_mode = bool(os.environ.get("verbose"))

def main():
    sonko = get_character("Sonko")["data"]
    monster = get_one.monster("yellow_slime")
    print(monster["hp"], monster["res_earth"], monster["attack_earth"])
    print(sonko["hp"], sonko["res_earth"], sonko["attack_earth"])
    print("VS yellow_slime", simulate_battles("Sonko", "yellow_slime"))
    print("VS cow", simulate_battles("Sonko", "cow"))

if __name__ == "__main__":
    main()