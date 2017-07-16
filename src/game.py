"""
Monolith first. Services rofl.
"""

import src.database as db
import src.game_state as gs
from typing import Callable
from functools import wraps
from .message import post_message
from .common.enums import MessageType, GameState

_MIN_PLAYERS = 5
_MAX_PLAYERS = 10


def toggle_available(client_id: int, player_id: int):
    """
    Declare player available or unavailable for next game
    based on previously known setting
    """
    db.toggle_player_availability(client_id, player_id)


def new(client_id: int):
    """
    Start a game for a client.
    If no game was active, a new game is created.
    If a game was active, nothing happens.

    Posts:
        - GAME_IN_PROGRESS
        OR
        - NOT_ENOUGH_PLAYERS
        - TOO_MANY_PLAYERS
    Changes state to:
        - TEAM_PROPOSAL
    """
    @_game_check(MessageType.GAME_IN_PROGRESS)
    def _none_in_progress():
        return db.get_game(client_id) is None

    @_game_check(MessageType.NOT_ENOUGH_PLAYERS)
    def _enough_players(num):
        return num < _MIN_PLAYERS

    @_game_check(MessageType.TOO_MANY_PLAYERS)
    def _not_too_many_players(num):
        return num > _MAX_PLAYERS

    # make sure a game is not already in progress
    if not _none_in_progress():
        return

    # make sure a Goldilocks number of players is registered
    num_players = len(db.get_available_players(client_id))
    if (
        _enough_players(num_players) and
        _not_too_many_players(num_players)
    ):
        # TODO: create new game

        # change state to TEAM_PROPOSAL
        gs.change_state(GameState.TEAM_PROPOSAL)


def abort_game(client_id: int):
    """
    Set the active game state for client to GameState.ABORTED
    """
    gs.change_state(GameState.ABORTED)


def propose_team(client_id: int, player_id: int, proposal):
    """
    Process a team proposal
    """
    @_game_check(MessageType.UNEXPECTED_PROPOSAL)
    def _proposed_by_leader():
        return db.get_current_leader(client_id) == player_id

    # the game needs to be ready for proposal
    if not _game_is_ready(
        target_state=GameState.TEAM_PROPOSAL,
        message=MessageType.UNEXPECTED_PROPOSAL  # TODO: message for game not ready for proposal
    ):
        return

    # only the current leader can make proposals
    pass


def vote_team(game_id: int, vote):
    """
    Vote yes/no on the current team proposal
    """
    # the game needs to be ready for team vote
    pass


def vote_mission(game_id: int, vote):
    """
    Vote success/fail on the current mission
    """
    # the game needs to be ready for mission vote
    # vote is valid if the player is on the mission
    # only baddies can vote fail
    pass


def assassinate(game_id: int, target_player_name: str):
    """
    Kill the target
    """
    # the game needs to be ready for assassination
    # the target must be a valid player
    pass


def _assign_player_positions(game_id: int):
    pass


def _assign_player_roles(game_id: int):
    pass


def _check_game_state(game_id: int, target_state: GameState) -> bool:
    """
    Check if current game state is target game state.
    """
    pass


def _get_leader(game_id: int):
    """
    Retrieve current leader
    """
    pass


def _next_leader(game_id: int):
    """
    Rotate leadership to next player position
    """
    pass


def _check_team_vote_complete(game_id: int):
    pass


def _check_mission_vote_complete(game_id: int):
    pass


def _game_check(message: MessageType) -> Callable:
    def _decorator(func: Callable) -> Callable:
        @wraps(func)
        def _wrapper(*args, **kwargs) -> Callable:
            is_ok = func(*args, **kwargs)
            if not is_ok:
                post_message(message)
            return is_ok
        return _wrapper
    return _decorator


def _game_is_ready(target_state: GameState, message: MessageType):
    @_game_check(message)
    def _check_game_state():
        return db.get_game_state() == target_state
    return _check_game_state()
