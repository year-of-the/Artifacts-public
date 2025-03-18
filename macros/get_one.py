import os
import json
import utils.api as api
import macros.get_all as get_all
from utils.constants import MONSTER_CACHE_FILE_NAME, RESOURCE_CACHE_FILE_NAME, EVENT_CACHE_FILE_NAME, ACHIEVEMENT_CACHE_FILE_NAME, EFFECT_CACHE_FILE_NAME, BADGE_CACHE_FILE_NAME, TASK_CACHE_FILE_NAME, TASK_REWARD_CACHE_FILE_NAME, NPC_CACHE_FILE_NAME, ITEM_CACHE_FILE_NAME

def get_one(thing_code, api_func=None, data_file_name=None, collection_api_func=None):
    file_path = f'cached_data/{data_file_name}'

    if data_file_name is not None and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            return json.load(f)[thing_code]
    elif api_func is not None:
        return api_func(thing_code)["data"]
    else:
        things = collection_api_func()
        return things[thing_code]
        
    
def monster(monster_code):
    return get_one(
        thing_code=monster_code,
        api_func=api.get_monster,
        data_file_name=MONSTER_CACHE_FILE_NAME
    )

def item(item_code):
    return get_one(
        thing_code=item_code,
        api_func=api.get_item,
        data_file_name=ITEM_CACHE_FILE_NAME
    )

def npc(npc_code):
    return get_one(
        thing_code=npc_code,
        api_func=api.get_npc,
        data_file_name=NPC_CACHE_FILE_NAME
    )

def resource(resource_code):
    return get_one(
        thing_code=resource_code,
        api_func=api.get_resource,
        data_file_name=RESOURCE_CACHE_FILE_NAME
    )

def task(task_code):
    return get_one(
        thing_code=task_code,
        api_func=api.get_task,
        data_file_name=TASK_CACHE_FILE_NAME
    )

def task_reward(task_code):
    return get_one(
        thing_code=task_code,
        api_func=api.get_task_reward,
        data_file_name=TASK_REWARD_CACHE_FILE_NAME
    )

def effect(effect_code):
    return get_one(
        thing_code=effect_code,
        api_func=api.get_effect_reward,
        data_file_name=EFFECT_CACHE_FILE_NAME
    )

def achievement(achievement_code):
    return get_one(
        thing_code=achievement_code,
        api_func=api.get_achievement_reward,
        data_file_name=ACHIEVEMENT_CACHE_FILE_NAME
    )

def event(event_code):
    return get_one(
        thing_code=event_code,
        collection_api_func=get_all.events
    )

def badge(badge_code):
    return get_one(
        thing_code=badge_code,
        api_func=api.get_badge,
        data_file_name=BADGE_CACHE_FILE_NAME
    )