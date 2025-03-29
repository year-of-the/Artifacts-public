from macros.get_all import task_rewards, monsters_that_drop_item, resources_that_drop_item
from macros.get_one import item
from utils.state import state

def resource_finder(content_code):
    return {
        "monsters": monsters_that_drop_item(content_code),
        "resources": resources_that_drop_item(content_code),
        "is_task_reward": content_code in task_rewards().keys(),
        "crafting_recipe": item(content_code)["craft"]
    }

def missing_requirements_to_craft(item_code):
    recipe = item(item_code)["craft"]
    craft_skill, craft_lvl_requirement, required_ingredients = recipe["skill"], recipe["level"], recipe["items"]
    missing_levels = max(0, craft_lvl_requirement - state.get_current_character_attribute(f"{craft_skill}_level"))
    inventory = state.get_current_character_attribute("inventory")
    return {
        "craft_skill_type": craft_skill,
        "missing_levels": missing_levels,
        "missing_ingredients": [
            {
                **item,
                "missing_quantity": max(0, item["quantity"] - next((i["quantity"] for i in inventory if i["code"] == item["code"]), 0)),
            } for item in required_ingredients
        ]
    }