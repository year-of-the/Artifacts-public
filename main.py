import time
from macros.find_monsters import find_monsters
from utils.api import rest, choose_character, move
from utils.cooldown_controller import cooldown_controller

def main():
    choose_character("Sonko")
    rest()
    print(cooldown_controller.time_until_allowed("rest"))
    resp=move(1,4)
    print("RESP:", resp)
    time.sleep(1)
    print(cooldown_controller.time_until_allowed("rest"))

main()