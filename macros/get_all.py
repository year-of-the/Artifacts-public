import os
import json
from macros.repeat import repeatedly
from utils.constants import (
        MONSTER_CACHE_FILE_NAME,
        RESOURCE_CACHE_FILE_NAME,
        EVENT_CACHE_FILE_NAME,
        ACHIEVEMENT_CACHE_FILE_NAME,
        EFFECT_CACHE_FILE_NAME,
        TASK_CACHE_FILE_NAME,
        TASK_REWARD_CACHE_FILE_NAME,
        NPC_CACHE_FILE_NAME,
        ITEM_CACHE_FILE_NAME,
        BADGE_CACHE_FILE_NAME,
        MONSTER_DROP_CACHE_FILE_NAME,
        RESOURCE_DROP_CACHE_FILE_NAME
    )
import utils.api as api

def get_all(paginated_list_api_func, data_file_name=None, cache=True):
    file_path = f'cached_data/{data_file_name}'

    if cache and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        things = None

        def gather_page(i, page_size=100):
            nonlocal things
            things_batch = paginated_list_api_func(page=i, page_size=page_size)
            
            if len(things_batch["data"]) > 0 and "code" in things_batch["data"][0]:
                if things is None:
                    things = dict()
                for _, thing in enumerate(things_batch["data"]):
                    things[thing["code"]] = thing
            elif len(things_batch["data"]) > 0:
                if things is None:
                    things = []
                things.extend(things_batch["data"])
                
            return things_batch["total"] > i*page_size

        repeatedly(gather_page)
        
        if cache:
            with open(file_path, "w") as f:
                json.dump(things, f, indent=2)
        
        return things

def resources():
    return get_all(api.list_resources, RESOURCE_CACHE_FILE_NAME)

def resources_that_drop_item(item_code):
    return get_all(
        paginated_list_api_func=lambda page, page_size: api.list_resources(page=page, page_size=page_size, drop_code=item_code),
        data_file_name=RESOURCE_DROP_CACHE_FILE_NAME(item_code=item_code)
    )

def monsters():
    return get_all(api.list_monsters, MONSTER_CACHE_FILE_NAME)

def monsters_that_drop_item(item_code):
    return get_all(
        paginated_list_api_func=lambda page, page_size: api.list_monsters(page=page, page_size=page_size, item_drop_code=item_code),
        data_file_name=MONSTER_DROP_CACHE_FILE_NAME(item_code=item_code)
    )

def active_events():
    return get_all(paginated_list_api_func=api.list_active_events, cache=False)

def events():
    return get_all(api.list_events, EVENT_CACHE_FILE_NAME)

def achievements():
    return get_all(api.list_achievements, ACHIEVEMENT_CACHE_FILE_NAME)

def effects():
    return get_all(api.list_effects, EFFECT_CACHE_FILE_NAME)

def badges():
    return get_all(api.list_badges, BADGE_CACHE_FILE_NAME)

def tasks():
    return get_all(api.list_tasks, TASK_CACHE_FILE_NAME)

def task_rewards():
    return get_all(api.list_task_rewards, TASK_REWARD_CACHE_FILE_NAME)

def npcs():
    return get_all(api.list_npcs, NPC_CACHE_FILE_NAME)

def items():
    return get_all(api.list_items, ITEM_CACHE_FILE_NAME)

def get_whole_map():
    return get_all(paginated_list_api_func=api.get_map, cache=False)

def monsters_on_map():
    return get_all(paginated_list_api_func=api.get_monsters_on_map, cache=False)

def resources_on_map():
    return get_all(paginated_list_api_func=api.get_resources_on_map, cache=False)

def workshops_on_map():
    return get_all(paginated_list_api_func=api.get_workshops_on_map, cache=False)

def banks_on_map():
    return get_all(paginated_list_api_func=api.get_banks_on_map, cache=False)

def exchanges_on_map():
    return get_all(paginated_list_api_func=api.get_grand_exchanges_on_map, cache=False)

def task_masters_on_map():
    return get_all(paginated_list_api_func=api.get_tasks_masters_on_map, cache=False)

def npcs_on_map():
    return get_all(paginated_list_api_func=api.get_npcs_on_map, cache=False)

def content_on_map(content_code):
    return get_all(paginated_list_api_func=lambda page, page_size: api.get_content_locations_on_map(page=page, page_size=page_size, content_code=content_code), cache=False)

def listings():
    return get_all(paginated_list_api_func=api.list_listings, cache=False)

def item_listings(item_code, seller):
    return get_all(
            paginated_list_api_func=lambda x: api.list_item_listings(page=x, item_code=item_code, seller=seller),
            cache=False
        )

def item_sale_history(item_code, buyer, seller):
    return get_all(
            paginated_list_api_func=lambda x: api.list_item_sale_history(page=x, item_code=item_code, seller=seller, buyer=buyer),
            cache=False
        )

def logs():
    return get_all(paginated_list_api_func=api.list_logs, cache=False)