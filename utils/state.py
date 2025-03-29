class State :
    def __init__(self):
        self.CURRENT_CHARACTER_NAME = None
        self.CHARACTER_SEGREGATED_STATE = {}
    
    def set_current_character(self, stats):
        name = stats["name"]
        if name not in self.CHARACTER_SEGREGATED_STATE:
            self.CHARACTER_SEGREGATED_STATE[name] = { "__character": {} }
        for attribute in stats.keys():
            self.CHARACTER_SEGREGATED_STATE[name]["__character"][attribute] = stats[attribute]
        self.CURRENT_CHARACTER_NAME = name

    def get(self, key):
        return self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME][key] if key in self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME] else None
    
    def set(self, key, value):
        self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME][key] = value

    def get_current_character_attribute(self, key):
        if "__character" not in self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME]:
            self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME]["__character"] = {}
            return None
        return self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME]["__character"][key] 

state = State()