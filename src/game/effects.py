
import src.common.enums as enums
import src.common.model as model


def _assign_player_positions(game_id: int):
    pass


def _assign_player_roles(game_id: int):
    pass


def _check_game_state(game_id: int, target_state: enums.GameState) -> bool:
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
