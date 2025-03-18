import time
from utils.constants import timeframes, timeframe_milliseconds, rate_limits
import utils.api as api

class CooldownController:
    def __init__(self):
        self.active_cooldown = 0
        self.rates = {}
    
    @property
    def now(self):
        return int(time.time() * 1000)
    
    @property
    def current_cooldown(self):
        return max(self.active_cooldown - self.now, 0)
    
    def set_cooldown(self, milliseconds_remaining=0):
        self.active_cooldown = self.now + milliseconds_remaining

    def update_rate_limit_history(self, action):
        type = getattr(api, action).api_type

        if type not in self.rates:
            self.rates[type] = { "sec": [], "min": [], "hr": [] }

        for timeframe in timeframes:
            while len(self.rates[type][timeframe]) > 0 and self.now - self.rates[type][timeframe][0] > timeframe_milliseconds[timeframe]:
                self.rates[type][timeframe].pop(0)
    
    def time_until_allowed(self, action):
        if self.allowed(action=action):
            return 0

        type = getattr(api, action).api_type

        ms_remaining = max([
            self.current_cooldown,
            max(self.rates[type]["sec"][0] + timeframe_milliseconds["sec"] - self.now, 0) if len(self.rates[type]["sec"]) > 0 else 0,
            max(self.rates[type]["min"][0] + timeframe_milliseconds["min"] - self.now, 0) if len(self.rates[type]["min"]) > 0 else 0,
            max(self.rates[type]["hr"][0] + timeframe_milliseconds["hr"] - self.now, 0) if len(self.rates[type]["hr"]) > 0 else 0,
        ])

        return ms_remaining
    
    def allowed(self, action):
        self.update_rate_limit_history(action)

        type = getattr(api, action).api_type

        if type == "Action" and self.current_cooldown > 0:
            return False
        elif len(self.rates[type]["sec"]) >= rate_limits[type]["sec"]:
            return False
        elif len(self.rates[type]["min"]) >= rate_limits[type]["min"]:
            return False
        elif len(self.rates[type]["hr"]) >= rate_limits[type]["hr"]:
            return False
        else:
            return True
    
    def tally_action(self, action):
        self.update_rate_limit_history(action)

        type = getattr(api, action).api_type

        for timeframe in timeframes:
            self.rates[type][timeframe].append(self.now)

cooldown_controller = CooldownController()