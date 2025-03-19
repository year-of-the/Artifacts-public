import os
from macros.find_monsters import find_monsters
from utils.api import rest, choose_character, move
from utils.cooldown_controller import cooldown_controller
from dotenv import load_dotenv

load_dotenv()

verbose_mode = bool(os.environ.get("verbose"))

def main():
    choose_character("Sonko")
    resp0 = rest()
    resp1 = move(1,4)
    resp2 = move(0,4)

if __name__ == "__main__":
    main()