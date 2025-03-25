class State :
    def __init__(self):
        self.CURRENT_CHARACTER_NAME = None
        self.CHARACTER_SEGREGATED_STATE = {}
    
    def set_current_character(self, name):
        if name not in self.CHARACTER_SEGREGATED_STATE:
            self.CHARACTER_SEGREGATED_STATE[name] = {}
        self.CURRENT_CHARACTER_NAME = name

    def get(self, key):
        return self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME][key] if key in self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME] else None
    
    def set(self, key, value):
        self.CHARACTER_SEGREGATED_STATE[self.CURRENT_CHARACTER_NAME][key] = value

state = State()