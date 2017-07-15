"""
Monolith first. Services rofl.
"""

from common.enums import GameState

_MIN_PLAYERS = 5
_MAX_PLAYERS = 10


def toggle_available(client_id: int, player_id: int):
    """
    Declare player available or unavailable for next game
    based on previously known setting
    """
    pass


def start_game(client_id: int):
    """
    Start a game for a client.
    If a game is already active, returns active game id.
    If no game was active, a new game is created and the id returned.
    """
    def _check_num_players_available():
        """
        Make sure a Goldilocks number of players are registered
        """
        pass

    # if no game is active,
    # an appropriate number of players should be available


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


def _get_player_by_name(player_name: str):
    pass
