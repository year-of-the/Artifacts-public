import os
import inspect
import requests
from typing import Literal, Optional
from utils.cooldown_controller import cooldown_controller
from dotenv import load_dotenv

load_dotenv()

artifact_api_token = os.environ.get("artifact_api_token")
artifact_api_host = os.environ.get("artifact_api_host")
verbose_mode = bool(os.environ.get("verbose"))

_current_character_name = None

# Decorators
def Action(func):
    func.api_type = "Action"
    return func

def Data(func):
    func.api_type = "Data"
    return func

# HTTP helper methods
def post_api(path, body=None):
    url = f'{artifact_api_host}/{path}'
    response = requests.post(url=url, json=body, headers={ "Authorization": "Bearer " + artifact_api_token })
    data = response.json()
    action_name = inspect.currentframe().f_back.f_code.co_name
    cooldown_controller.tally_action(action_name)
    if "cooldown" in data:
        cooldown_controller.set_cooldown(milliseconds_remaining=data["cooldown"]["remaining_seconds"]*1000)
    return data

def get_api(path, params=None):
    url = f'{artifact_api_host}/{path}'
    response = requests.get(url=url, params=params, headers={ "Authorization": "Bearer " + artifact_api_token })
    data = response.json()
    action_name = inspect.currentframe().f_back.f_code.co_name
    cooldown_controller.tally_action(action_name)
    if "cooldown" in data:
        cooldown_controller.set_cooldown(milliseconds_remaining=data["cooldown"]["remaining_seconds"]*1000)
    return data

# Basic API methods
@Data
def get_bank():
  if verbose_mode: print("API: Checking bank")
  return get_api("my/bank");

@Data
def get_bank_items():
  if verbose_mode: print("API: Checking banked items")
  return get_api("my/bank/items");

@Data
def get_sell_orders():
  if verbose_mode: print("API: Sell orders")
  return get_api("my/grandexchange/orders");

@Data
def get_sell_history():
  if verbose_mode: print("API: Exchange history")
  return get_api("my/grandexchange/history");

@Data
def get_account_details():
  if verbose_mode: print("API: Checking accounts")
  return get_api("my/details");

@Action
def move(x, y):
    if verbose_mode: print(f'API: Moving to {x}, {y}')
    return post_api(f'my/{_current_character_name}/action/move', { "x": x, "y": y })

@Action
def rest():
    if verbose_mode: print("API: Resting")
    return post_api(f'my/{_current_character_name}/action/rest')

@Action
def fight():
    if verbose_mode: print("API: Fighting")
    return post_api(f'my/{_current_character_name}/action/fight')

@Action
def equip(item_code, slot, quantity=1):
    if verbose_mode: print("API: Equipping item(s)")
    return post_api(f'my/{_current_character_name}/action/equip', { "code": item_code, "slot": slot, "quantity": quantity })

@Action
def unequip(slot, quantity=1):
    if verbose_mode: print("API: Unequipping item(s)")
    return post_api(f'my/{_current_character_name}/action/unequip', { "slot": slot, "quantity": quantity })

@Action
def use_item(item_code, quantity=1):
    if verbose_mode: print("API: Using item(s)")
    return post_api(f'my/{_current_character_name}/action/use', { "code": item_code, "quantity": quantity })

@Action
def craft_item(item_code, quantity=1):
    if verbose_mode: print("API: Crafting")
    return post_api(f'my/{_current_character_name}/action/crafting', { "code": item_code, "quantity": quantity })

@Action
def delete_item(item_code, quantity=1):
    if verbose_mode: print("API: Deleting item(s)")
    return post_api(f'my/{_current_character_name}/action/delete', { "code": item_code, "quantity": quantity })

@Action
def deposit_gold(quantity=1):
    if verbose_mode: print("API: Depositing gold")
    return post_api(f'my/{_current_character_name}/action/bank/deposit/gold', { "quantity": quantity })

@Action
def deposit_item(item_code, quantity=1):
    if verbose_mode: print("API: Depositing item(s)")
    return post_api(f'my/{_current_character_name}/action/bank/deposit', { "code": item_code, "quantity": quantity })

@Action
def withdraw_gold(quantity=1):
    if verbose_mode: print("API: Withdrawing gold")
    return post_api(f'my/{_current_character_name}/action/bank/withdraw/gold', { "quantity": quantity })

@Action
def withdraw_item(item_code, quantity=1):
    if verbose_mode: print("API: Withdrawing item(s)")
    return post_api(f'my/{_current_character_name}/action/bank/withdraw', { "code": item_code, "quantity": quantity })

@Action
def expand_bank():
    if verbose_mode: print("API: Expanding bank")
    return post_api(f'my/{_current_character_name}/action/bank/buy_expansion')

@Action
def buy_npc_item(item_code, quantity=1):
    if verbose_mode: print("API: Buying item(s) (from NPC)")
    return post_api(f'my/{_current_character_name}/action/npc/buy', { "code": item_code, "quantity": quantity })

@Action
def sell_npc_item(item_code, quantity=1):
    if verbose_mode: print("API: Selling item(s) (to NPC)")
    return post_api(f'my/{_current_character_name}/action/npc/sell', { "code": item_code, "quantity": quantity })

@Action
def recycle(item_code, quantity=1):
    if verbose_mode: print("API: Recycling item(s)")
    return post_api(f'my/{_current_character_name}/action/recycle', { "code": item_code, "quantity": quantity })

@Action
def buy_exchange_item(order_id, quantity=1):
    if verbose_mode: print("API: Buying item(s) (from exchange)")
    return post_api(f'my/{_current_character_name}/action/grandexchange/buy', { "id": order_id, "quantity": quantity })

@Action
def create_sell_order_exchange_item(item_code, price, quantity=1):
    if verbose_mode: print("API: Creating sell order")
    return post_api(f'my/{_current_character_name}/action/grandexchange/sell', { "code": item_code, "price": price, "quantity": quantity })

@Action
def cancel_sell_order_exchange_item(order_id):
    if verbose_mode: print("API: Canceling sell order")
    return post_api(f'my/{_current_character_name}/action/grandexchange/cancel', { "id": order_id })

@Action
def complete_task():
    if verbose_mode: print("API: Completing task")
    return post_api(f'my/{_current_character_name}/action/task/complete')

@Action
def exchange_task():
    if verbose_mode: print("API: Exchanging task for reward")
    return post_api(f'my/{_current_character_name}/action/task/exchange')

@Action
def accept_new_task():
    if verbose_mode: print("API: Accepting new task")
    return post_api(f'my/{_current_character_name}/action/task/new')

@Data
def list_logs(page=1, page_size=100):
    if verbose_mode: print("API: Getting all logs")
    return get_api("my/logs", { "page": page, "size": page_size })

@Data
def list_characters():
    if verbose_mode: print("API: Listing characters")
    return get_api("my/characters")

@Data
def get_character(name=_current_character_name):
    if verbose_mode: print(f'API: Getting information about {name}')
    return get_api(f'characters/{name}')

@Data
def list_item_sale_history(item_code, page=1, page_size=100, buyer=None, seller=None):
    if verbose_mode: print("API: Listing exchange sell history")
    return get_api(
        f'grandexchange/history/{item_code}',
        {
            "page": page,
            "size": page_size,
            "buyer": buyer,
            "seller": seller,
        })

@Data
def list_item_listings(item_code, page=1, page_size=100, seller=None):
    if verbose_mode: print("API: Listing active sell orders for item")
    return get_api(
        "grandexchange/orders",
        {
            "code": item_code,
            "page": page,
            "size": page_size,
            "seller": seller,
        })

@Data
def list_listings(page=1, page_size=100, seller=None):
    if verbose_mode: print("API: Listing all active sell orders")
    return get_api(
        "grandexchange/orders",
        {
            "page": page,
            "size": page_size,
            "seller": seller,
        })

@Data
def get_item_listing(listing_id):
    if verbose_mode: print("API: Getting active sell order")
    return get_api(f'grandexchange/orders/{listing_id}')

@Data
def list_items(
    page=1,
    page_size=100,
    craft_material=None,
    craft_skill: Optional[Literal[None, "weaponcrafting", "gearcrafting", "jewelrycrafting", "cooking", "woodcutting", "mining", "alchemy"]] = None,
    max_level=None,
    min_level=None,
    name=None,
    type: Optional[Literal[None, "utility", "body_armor", "weapon", "resource", "leg_armor", "helmet", "boots", "shield", "amulet", "ring", "artifact", "currency", "consumable", "rune", "bag"]] = None,
):
    if verbose_mode: print("API: Listing item glossary")
    return get_api(path="items", params={
        "page": page,
        "page_size": page_size,
        "craft_material": craft_material,
        "craft_skill": craft_skill,
        "max_level": max_level,
        "min_level": min_level,
        "name": name,
        "type": type,
    })

@Data
def get_item(item_code):
    if verbose_mode: print("API: Looking up item information from glossary")
    return get_api(f'items/{item_code}')

@Data
def get_map(
    page: int = 1,
    page_size: int = 100,
    content_code: Optional[str] = None,
    content_type: Optional[Literal[None, "monster", "resource", "workshop", "bank", "grand_exchange", "tasks_master", "npc"]] = None
):
    if verbose_mode: print("API: Checking map")
    return get_api("maps", { "page": page, "size": page_size, "content_code": content_code, "content_type": content_type })

@Data
def get_monsters_on_map(page=1, page_size=100, content_code=None):
    if verbose_mode: print("API: Checking map for monsters")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="monster")

@Data
def get_resources_on_map(page=1, page_size=100, content_code=None):
    if verbose_mode: print("API: Checking map for resources")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="resource")

@Data
def get_workshops_on_map(page=1, page_size=100, content_code=None):
    if verbose_mode: print("API: Checking map for workshops")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="workshop")

@Data
def get_banks_on_map(page=1, page_size=100, content_code=None):
    if verbose_mode: print("API: Checking map for banks")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="bank")

@Data
def get_grand_exchanges_on_map(page=1, page_size=100, content_code=None):
    if verbose_mode: print("API: Checking map for exchanges")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="grand_exchange")

@Data
def get_tasks_masters_on_map(page=1, page_size=100, content_code=None):
    if verbose_mode: print("API: Checking map for task masters")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="tasks_master")

@Data
def get_npcs_on_map(page=1, page_size=100, content_code=None):
    if verbose_mode: print("API: Checking map for NPCs")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="npc")

@Data
def get_location(x, y):
    if verbose_mode: print("API: Checking location info")
    return get_api(f'maps/{x}/{y}')

@Data
def list_monsters(page=1, page_size=100, item_drop_code=None, max_level=None, min_level=None):
    if verbose_mode: print("API: Listing monsters from glossary")
    return get_api("monsters", {
        "page": page,
        "page_size": page_size,
        "drop": item_drop_code,
        "max_level": max_level,
        "min_level": min_level,
    })

@Data
def get_monster(monster_code):
    if verbose_mode: print("API: Checking monster information from glossary")
    return get_api(f'monsters/{monster_code}')

@Data
def list_npcs(page=1, page_size=100):
    if verbose_mode: print("API: Listing NPCs from glossary")
    return get_api("npcs", { "page": page, "size": page_size })

@Data
def get_npc(npc_code):
    if verbose_mode: print("API: Checking NPC information from glossary")
    return get_api(f'npcs/{npc_code}')

@Data
def list_npc_items(npc_code):
    if verbose_mode: print("API: Checking NPC items from glossary")
    return get_api(f'npcs/{npc_code}/items')

@Data
def list_resources(page=1, page_size=100, drop_code=None, skill_id=None, max_level=None, min_level=None):
    if verbose_mode: print("API: Listing resources from glossary")
    return get_api("resources", {
        "page": page,
        "size": page_size,
        "drop": drop_code,
        "skill": skill_id,
        "min_level": min_level,
        "max_level": max_level,
    })

@Data
def get_resource(resource_code):
    if verbose_mode: print("API: Checking resource information from glossary")
    return get_api(f'resources/{resource_code}')

@Data
def list_tasks(
    page: int = 1,
    page_size: int = 100,
    max_level=None,
    min_level=None,
    type: Optional[Literal[None, "items", "monsters"]] = None,
    skill: Optional[Literal[None, "weaponcrafting", "gearcrafting", "jewelrycrafting", "cooking", "woodcutting", "mining", "alchemy", "fishing"]] = None
):
    if verbose_mode: print("API: Listing tasks from glossary")
    return get_api("tasks/list", {
        "page": page,
        "size": page_size,
        "type": type,
        "skill": skill,
        "min_level": min_level,
        "max_level": max_level,
    })

@Data
def get_task(task_code):
    if verbose_mode: print("API: Checking task information from glossary")
    return get_api(f'tasks/list/{task_code}')

@Data
def list_task_rewards(page=1, page_size=100):
    if verbose_mode: print("API: Listing task rewards from glossary")
    return get_api("tasks/rewards", { "page": page, "size": page_size })

@Data
def get_task_reward(task_code):
    if verbose_mode: print("API: Checking task reward information from glossary")
    return get_api(f'tasks/rewards/{task_code}')

@Data
def list_effects(page=1, page_size=100):
    if verbose_mode: print("API: Listing effects from glossary")
    return get_api("effects", { "page": page, "size": page_size })

@Data
def get_effect(effect_code):
    if verbose_mode: print("API: Checking effect information from glossary")
    return get_api(f'effects/{effect_code}')

@Data
def list_badges(page=1, page_size=100):
    if verbose_mode: print("API: Listing badges from glossary")
    return get_api("badges", { "page": page, "size": page_size })

@Data
def get_badge(badge_code):
    if verbose_mode: print("API: Checking badge information from glossary")
    return get_api(f'badges/{badge_code}')

@Data
def list_active_events(page=1, page_size=100):
    if verbose_mode: print("API: Listing active events")
    return get_api("events/active", { "page": page, "size": page_size })

@Data
def list_events(page=1, page_size=100):
    if verbose_mode: print("API: Listing all events from glossary")
    return get_api("events", { "page": page, "size": page_size })

@Data
def list_achievements(page=1, page_size=100):
    if verbose_mode: print("API: Listing all achievements from glossary")
    return get_api("achievements", { "page": page, "size": page_size })

@Data
def get_achievement(achievement_code):
    if verbose_mode: print("API: Checking achievement information from glossary")
    return get_api(f'achievements/{achievement_code}')

# Synthetic API methods
get_current_character = lambda: get_character()

def choose_character(name):
    global _current_character_name
    _current_character_name = name
    return get_current_character()