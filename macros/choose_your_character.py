import os
import logging
from utils.api import get_character
from utils.state import state

logger = logging.getLogger()

def choose_character(name):
    logger.info(f"Setting '{name}' as current character")
    return get_character(name)["data"]