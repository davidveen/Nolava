
from typing import List, Callable
from functools import partial

from .database import get_game
from .common.enums import GameState


def print_something(x):
    print(x)


def print_foo():
    print('foo')

_STATE_DICT = {
    GameState.RECRUITING: (print_foo, partial(print_something, 'bar'))
}


def change_state(client_id, target_state, *args):
    #TODO: write new state to db

    # execute state functions
    for action in _STATE_DICT[target_state]:
        action()
