MONSTER_CACHE_FILE_NAME="monsters.json"
RESOURCE_CACHE_FILE_NAME = "resources.json"
EVENT_CACHE_FILE_NAME = "events.json"
ACHIEVEMENT_CACHE_FILE_NAME = "achievements.json"
EFFECT_CACHE_FILE_NAME = "effects.json"
BADGE_CACHE_FILE_NAME = "badges.json"
TASK_CACHE_FILE_NAME = "tasks.json"
TASK_REWARD_CACHE_FILE_NAME = "task_rewards.json"
NPC_CACHE_FILE_NAME = "npcs.json"
MONSTER_DROP_CACHE_FILE_NAME = lambda item_code: f'monsters_that_drop_{item_code}.json'
ITEM_CACHE_FILE_NAME = "items.json"
CHARACTER_BASE_HP = 115;
CHARACTER_HP_PER_LEVEL = 5;

timeframes = ("sec", "min", "hr")
timeframe_milliseconds = {
    "sec": 1000,
    "min": 60000,
    "hr": 3600000,
}
rate_limits = {
    "Data": {
        "sec": 15,
        "min": 200,
        "hr": 7200,
    },
    "Action": {
        "sec": 5,
        "min": 200,
        "hr": 7200,
    },
}