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

    def update_rate_limit_history(self, action_type):
        if action_type not in self.rates:
            self.rates[action_type] = { "sec": [], "min": [], "hr": [] }

        for timeframe in timeframes:
            while len(self.rates[action_type][timeframe]) > 0 and self.now - self.rates[action_type][timeframe][0] > timeframe_milliseconds[timeframe]:
                self.rates[action_type][timeframe].pop(0)
    
    def time_until_allowed(self, action_type):
        if self.allowed(action_type=action_type):
            return 0

        ms_remaining = max([
            self.current_cooldown,
            max(self.rates[action_type]["sec"][0] + timeframe_milliseconds["sec"] - self.now, 0) if len(self.rates[action_type]["sec"]) == rate_limits[action_type]["sec"] else 0,
            max(self.rates[action_type]["min"][0] + timeframe_milliseconds["min"] - self.now, 0) if len(self.rates[action_type]["min"]) == rate_limits[action_type]["min"] else 0,
            max(self.rates[action_type]["hr"][0] + timeframe_milliseconds["hr"] - self.now, 0) if len(self.rates[action_type]["hr"]) == rate_limits[action_type]["hr"] else 0,
        ])

        return ms_remaining
    
    def allowed(self, action_type):
        self.update_rate_limit_history(action_type)

        if action_type == "Action" and self.current_cooldown > 0:
            return False
        elif len(self.rates[action_type]["sec"]) >= rate_limits[action_type]["sec"]:
            return False
        elif len(self.rates[action_type]["min"]) >= rate_limits[action_type]["min"]:
            return False
        elif len(self.rates[action_type]["hr"]) >= rate_limits[action_type]["hr"]:
            return False
        else:
            return True
    
    def tally_action(self, action_type):
        self.update_rate_limit_history(action_type)
        for timeframe in timeframes:
            self.rates[action_type][timeframe].append(self.now)

    def wait_until_allowed(self, action_type):
        ms_remaining = self.time_until_allowed(action_type)
        time.sleep(ms_remaining/1000)

cooldown_controller = CooldownController()