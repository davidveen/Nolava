
"""
Retrieve game settings
"""

from contextlib import contextmanager
import configparser as cp

_SETTINGS_PATH = 'config/game.ini'


@contextmanager
def get():
    parser = cp.ConfigParser()
    parser.read(_SETTINGS_PATH)
    try:
        yield parser
    # TODO: error handling for non-existing settings?
    finally:
        del parser
