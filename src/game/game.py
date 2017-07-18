"""
Monolith first. Services rofl.
"""

from functools import partial

import commands as cmd
import src.database as db
import src.common.enums as enums
import src.common.model as model


def receive_command(client_id, command: model.Command):
    """
    Receive a command from deepthought
    """
    # get game and player models from database
    # based on client id and slack user id
    _game = db.get_game(client_id)
    _player = db.get_player_by_slack_id(command.user.id_)

    # link each command to a function, with the required parameters
    ct = enums.CommandType
    _command_map = {
        ct.JOIN: partial(cmd.join, client_id, command),
        ct.LEAVE: partial(cmd.leave, client_id, command),
        ct.START: partial(cmd.new, client_id, _game),
        ct.ABORT: partial(cmd.abort, client_id),
        ct.PROPOSE_TEAM: partial(cmd.propose_team, _game, _player, command),
        ct.VOTE_YES: partial(cmd.vote_team),
        ct.VOTE_NO: partial(cmd.vote_team),
        ct.VOTE_PASS: partial(cmd.vote_mission),
        ct.VOTE_FAIL: partial(cmd.vote_mission),
        ct.ASSASSINATE: partial(cmd.assassinate)
    }

    # perform command
    _command_map[command.command]()


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



