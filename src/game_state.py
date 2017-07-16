
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

# _STATE_MAP = (
#     (GameState.RECRUITING, (print_foo, partial(print_something, 'bar')))
# )

def change_state(target_state):
    #TODO: write new state to db

    # execute state functions
    for action in _STATE_DICT[target_state]:
        action()


# class GameMachine(object):
#     def __init__(self):
#         self._current_state = None
#         # TODO: get current state from db

#         self._states = {}
#         for game_state, funcs in _STATE_MAP:
#             self._states[game_state] = self.State(game_state, funcs)

#     def change_state(self, target_state: GameState):
#         self._current_state = self._states[target_state]
#         # TODO: update database

#         self._current_state.run()

#     class State(object):
#         def __init__(
#             self,
#             game_state: GameState,
#             actions: List[Callable]
#         ):
#             self._state = game_state
#             self._actions = actions

#         def __str__(self):
#             return self._state.name

#         def run(self):
#             for action in self._actions:
#                 action()
