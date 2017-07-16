"""
Monolith first. Services rofl.
"""

import src.database as db
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
    return 'foo'


def start_game(client_id: int):
    """
    Start a game for a client.
    If no game was active, a new game is created.
    If a game was active, nothing happens.

    Posts:
        - GAME_IN_PROGRESS
        OR
        - GAME_START
        OR
        - NOT_ENOUGH_PLAYERS
        - TOO_MANY_PLAYERS
    """
    def _check_num_players_available():
        """
        Make sure a Goldilocks number of players are registered
        """
        return (
            _MIN_PLAYERS <
            len(db.get_available_players(client_id)) <
            _MAX_PLAYERS
        )

    is_active = (db.get_game(client_id) is not None)
    # if no game is active,
    # an appropriate number of players should be available
    game_id = db.get_game


def abort_game(client_id: int):
    """
    Set the active game state for client to GameState.ABORTED
    """
    pass


def propose_team(game_id: int, proposal):
    """
    Process a team proposal
    """
    # the game needs to be ready for proposal
    # only the team leader can make proposals
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


