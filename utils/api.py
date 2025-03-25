import os
import inspect
import requests
from typing import Literal, Optional
from utils.state import state
from utils.cooldown_controller import cooldown_controller
from dotenv import load_dotenv

load_dotenv(override=True)

artifact_api_token = os.environ.get("artifact_api_token")
artifact_api_host = os.environ.get("artifact_api_host")
verbose_mode = bool(os.environ.get("verbose"))

FUNCTION_REGISTRY = {}

def register(func_type):
    def decorator(func):
        FUNCTION_REGISTRY[func.__name__] = func_type
        return func
    return decorator

# HTTP helper methods
def post_api(path, caller_name=None, body=None):
    cooldown_controller.wait_until_allowed(action_type=FUNCTION_REGISTRY[caller_name])
    url = f'{artifact_api_host}/{path}'
    response = requests.post(url=url, json=body, headers={ "Authorization": "Bearer " + artifact_api_token })
    data = response.json()
    if "error" in data:
        raise Exception(data["error"])

    cooldown_controller.tally_action(FUNCTION_REGISTRY[caller_name])
    new_cooldown_set = "cooldown" in data["data"] and isinstance(data["data"]["cooldown"], dict) and "remaining_seconds" in data["data"]["cooldown"]
    new_cooldown_timestamp = data["data"]["cooldown_expiration"] if "cooldown_expiration" in data["data"] else None

    if new_cooldown_set:
        cooldown_controller.set_cooldown(milliseconds_remaining=data["data"]["cooldown"]["remaining_seconds"]*1000)
    if new_cooldown_timestamp:
        cooldown_controller.set_cooldown_to_future_timestamp(timestamp_str=new_cooldown_timestamp)

    return data

def get_api(path, caller_name=None, params=None):
    cooldown_controller.wait_until_allowed(action_type=FUNCTION_REGISTRY[caller_name])
    url = f'{artifact_api_host}/{path}'
    response = requests.get(url=url, params=params, headers={ "Authorization": "Bearer " + artifact_api_token })
    data = response.json()
    if "error" in data:
        raise Exception(data["error"])

    cooldown_controller.tally_action(FUNCTION_REGISTRY[caller_name])
    new_cooldown_set = "cooldown" in data["data"] and isinstance(data["data"]["cooldown"], dict) and "remaining_seconds" in data["data"]["cooldown"]
    new_cooldown_timestamp = data["data"]["cooldown_expiration"] if "cooldown_expiration" in data["data"] else None

    if new_cooldown_set:
        cooldown_controller.set_cooldown(milliseconds_remaining=data["data"]["cooldown"]["remaining_seconds"]*1000)
    if new_cooldown_timestamp:
        cooldown_controller.set_cooldown_to_future_timestamp(timestamp_str=new_cooldown_timestamp)

    return data

# Basic API methods
@register("Data")
def get_bank():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking bank")
    return get_api("my/bank", func_name);

@register("Data")
def get_bank_items():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking banked items")
    return get_api("my/bank/items", func_name);

@register("Data")
def get_sell_orders():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Sell orders")
    return get_api("my/grandexchange/orders", func_name);

@register("Data")
def get_sell_history():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Exchange history")
    return get_api("my/grandexchange/history", func_name);

@register("Data")
def get_account_details():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking accounts")
    return get_api("my/details", func_name);

@register("Action")
def move(x, y):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print(f'API: Moving to {x}, {y}')
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/move', func_name, { "x": x, "y": y })

@register("Action")
def rest():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Resting")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/rest', func_name)

@register("Action")
def fight():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Fighting")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/fight', func_name)

@register("Action")
def equip(item_code, slot, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Equipping item(s)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/equip', func_name, { "code": item_code, "slot": slot, "quantity": quantity })

@register("Action")
def unequip(slot, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Unequipping item(s)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/unequip', func_name, { "slot": slot, "quantity": quantity })

@register("Action")
def use_item(item_code, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Using item(s)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/use', func_name, { "code": item_code, "quantity": quantity })

@register("Action")
def craft_item(item_code, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Crafting")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/crafting', func_name, { "code": item_code, "quantity": quantity })

@register("Action")
def delete_item(item_code, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Deleting item(s)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/delete', func_name, { "code": item_code, "quantity": quantity })

@register("Action")
def deposit_gold(quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Depositing gold")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/bank/deposit/gold', func_name, { "quantity": quantity })

@register("Action")
def deposit_item(item_code, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Depositing item(s)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/bank/deposit', func_name, { "code": item_code, "quantity": quantity })

@register("Action")
def withdraw_gold(quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Withdrawing gold")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/bank/withdraw/gold', func_name, { "quantity": quantity })

@register("Action")
def withdraw_item(item_code, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Withdrawing item(s)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/bank/withdraw', func_name, { "code": item_code, "quantity": quantity })

@register("Action")
def expand_bank():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Expanding bank")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/bank/buy_expansion', func_name)

@register("Action")
def buy_npc_item(item_code, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Buying item(s) (from NPC)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/npc/buy', func_name, { "code": item_code, "quantity": quantity })

@register("Action")
def sell_npc_item(item_code, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Selling item(s) (to NPC)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/npc/sell', func_name, { "code": item_code, "quantity": quantity })

@register("Action")
def recycle(item_code, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Recycling item(s)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/recycle', func_name, { "code": item_code, "quantity": quantity })

@register("Action")
def buy_exchange_item(order_id, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Buying item(s) (from exchange)")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/grandexchange/buy', func_name, { "id": order_id, "quantity": quantity })

@register("Action")
def create_sell_order_exchange_item(item_code, price, quantity=1):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Creating sell order")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/grandexchange/sell', func_name, { "code": item_code, "price": price, "quantity": quantity })

@register("Action")
def cancel_sell_order_exchange_item(order_id):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Canceling sell order")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/grandexchange/cancel', func_name, { "id": order_id })

@register("Action")
def complete_task():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Completing task")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/task/complete', func_name)

@register("Action")
def exchange_task():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Exchanging task for reward")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/task/exchange', func_name)

@register("Action")
def accept_new_task():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Accepting new task")
    return post_api(f'my/{state.CURRENT_CHARACTER_NAME}/action/task/new', func_name)

@register("Data")
def list_logs(page=1, page_size=100):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Getting all logs")
    return get_api("my/logs", func_name, { "page": page, "size": page_size })

@register("Data")
def list_characters():
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing characters")
    return get_api("my/characters", func_name)

@register("Data")
def get_character(name=None):
    if name == None: name = state.CURRENT_CHARACTER_NAME
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print(f'API: Getting information about {name}')
    return get_api(f'characters/{name}', func_name)

@register("Data")
def list_item_sale_history(item_code, page=1, page_size=100, buyer=None, seller=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing exchange sell history")
    return get_api(
        f'grandexchange/history/{item_code}',
        func_name,
        {
            "page": page,
            "size": page_size,
            "buyer": buyer,
            "seller": seller,
        })

@register("Data")
def list_item_listings(item_code, page=1, page_size=100, seller=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing active sell orders for item")
    return get_api(
        "grandexchange/orders",
        func_name,
        {
            "code": item_code,
            "page": page,
            "size": page_size,
            "seller": seller,
        })

@register("Data")
def list_listings(page=1, page_size=100, seller=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing all active sell orders")
    return get_api(
        "grandexchange/orders",
        func_name,
        {
            "page": page,
            "size": page_size,
            "seller": seller,
        })

@register("Data")
def get_item_listing(listing_id):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Getting active sell order")
    return get_api(f'grandexchange/orders/{listing_id}', func_name)

@register("Data")
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
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing item glossary")
    return get_api(path="items", caller_name=func_name, params={
        "page": page,
        "page_size": page_size,
        "craft_material": craft_material,
        "craft_skill": craft_skill,
        "max_level": max_level,
        "min_level": min_level,
        "name": name,
        "type": type,
    })

@register("Data")
def get_item(item_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Looking up item information from glossary")
    return get_api(f'items/{item_code}', func_name)

@register("Data")
def get_map(
    page: int = 1,
    page_size: int = 100,
    content_code: Optional[str] = None,
    content_type: Optional[Literal[None, "monster", "resource", "workshop", "bank", "grand_exchange", "tasks_master", "npc"]] = None,
    _caller_name: str = None
):
    func_name = _caller_name if _caller_name is not None else inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking map")
    return get_api("maps", func_name, { "page": page, "size": page_size, "content_code": content_code, "content_type": content_type })

@register("Data")
def get_monsters_on_map(page=1, page_size=100, content_code=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking map for monsters")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="monster", _caller_name=func_name)

@register("Data")
def get_resources_on_map(page=1, page_size=100, content_code=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking map for resources")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="resource", _caller_name=func_name)

@register("Data")
def get_workshops_on_map(page=1, page_size=100, content_code=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking map for workshops")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="workshop", _caller_name=func_name)

@register("Data")
def get_banks_on_map(page=1, page_size=100, content_code=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking map for banks")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="bank", _caller_name=func_name)

@register("Data")
def get_grand_exchanges_on_map(page=1, page_size=100, content_code=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking map for exchanges")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="grand_exchange", _caller_name=func_name)

@register("Data")
def get_tasks_masters_on_map(page=1, page_size=100, content_code=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking map for task masters")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="tasks_master", _caller_name=func_name)

@register("Data")
def get_npcs_on_map(page=1, page_size=100, content_code=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking map for NPCs")
    return get_map(page=page, page_size=page_size, content_code=content_code, content_type="npc", _caller_name=func_name)

@register("Data")
def get_location(x, y):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking location info")
    return get_api(f'maps/{x}/{y}', func_name)

@register("Data")
def list_monsters(page=1, page_size=100, item_drop_code=None, max_level=None, min_level=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing monsters from glossary")
    return get_api("monsters",
        func_name,
        {
            "page": page,
            "page_size": page_size,
            "drop": item_drop_code,
            "max_level": max_level,
            "min_level": min_level,
        })

@register("Data")
def get_monster(monster_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking monster information from glossary")
    return get_api(f'monsters/{monster_code}', func_name)

@register("Data")
def list_npcs(page=1, page_size=100):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing NPCs from glossary")
    return get_api("npcs", func_name, { "page": page, "size": page_size })

@register("Data")
def get_npc(npc_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking NPC information from glossary")
    return get_api(f'npcs/{npc_code}', func_name)

@register("Data")
def list_npc_items(npc_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking NPC items from glossary")
    return get_api(f'npcs/{npc_code}/items', func_name)

@register("Data")
def list_resources(page=1, page_size=100, drop_code=None, skill_id=None, max_level=None, min_level=None):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing resources from glossary")
    return get_api("resources",
        func_name,
        {
            "page": page,
            "size": page_size,
            "drop": drop_code,
            "skill": skill_id,
            "min_level": min_level,
            "max_level": max_level,
        })

@register("Data")
def get_resource(resource_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking resource information from glossary")
    return get_api(f'resources/{resource_code}', func_name)

@register("Data")
def list_tasks(
    page: int = 1,
    page_size: int = 100,
    max_level=None,
    min_level=None,
    type: Optional[Literal[None, "items", "monsters"]] = None,
    skill: Optional[Literal[None, "weaponcrafting", "gearcrafting", "jewelrycrafting", "cooking", "woodcutting", "mining", "alchemy", "fishing"]] = None
):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing tasks from glossary")
    return get_api("tasks/list",
        func_name,
        {
            "page": page,
            "size": page_size,
            "type": type,
            "skill": skill,
            "min_level": min_level,
            "max_level": max_level,
        })

@register("Data")
def get_task(task_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking task information from glossary")
    return get_api(f'tasks/list/{task_code}', func_name)

@register("Data")
def list_task_rewards(page=1, page_size=100):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing task rewards from glossary")
    return get_api("tasks/rewards", func_name, { "page": page, "size": page_size })

@register("Data")
def get_task_reward(task_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking task reward information from glossary")
    return get_api(f'tasks/rewards/{task_code}', func_name)

@register("Data")
def list_effects(page=1, page_size=100):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing effects from glossary")
    return get_api("effects", func_name, { "page": page, "size": page_size })

@register("Data")
def get_effect(effect_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking effect information from glossary")
    return get_api(f'effects/{effect_code}', func_name)

@register("Data")
def list_badges(page=1, page_size=100):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing badges from glossary")
    return get_api("badges", func_name, { "page": page, "size": page_size })

@register("Data")
def get_badge(badge_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking badge information from glossary")
    return get_api(f'badges/{badge_code}', func_name)

@register("Data")
def list_active_events(page=1, page_size=100):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing active events")
    return get_api("events/active", func_name, { "page": page, "size": page_size })

@register("Data")
def list_events(page=1, page_size=100):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing all events from glossary")
    return get_api("events", func_name, { "page": page, "size": page_size })

@register("Data")
def list_achievements(page=1, page_size=100):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Listing all achievements from glossary")
    return get_api("achievements", func_name, { "page": page, "size": page_size })

@register("Data")
def get_achievement(achievement_code):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print("API: Checking achievement information from glossary")
    return get_api(f'achievements/{achievement_code}', func_name)

@register("Data")
def create_character(character_name, skin):
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print(f"API: creating a new character {character_name}")
    return post_api(f'characters/create', func_name, { "name": character_name, "skin": skin })

@register("Data")
def delete_character(character_name, im_sure=False):
    if not im_sure:
        raise Exception(f"Attempted to delete {character_name}, but didn't pass `im_sure` flag to confirm.")
    func_name = inspect.currentframe().f_code.co_name
    if verbose_mode: print(f"API: deleting character {character_name}")
    return post_api(f'characters/delete', func_name, { "name": character_name })
