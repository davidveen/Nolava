"""
Embraces all commands as its own,
but only gets to route them to their true home.
At least when the commands grow up they come back here,
and maybe cause some effects.
"""

from functools import partial

import commands as cmd
import effects as efx
import src.database as db
import src.common.enums as enums
import src.common.model as model


def give_command(client_id, command: model.Command):
    """
    Receive a command from deepthought
    """
    # get game and player models from database
    # based on client id and slack user id
    game = db.get_game(client_id)
    player = db.get_player_by_slack_id(command.user.id_)

    # link each command to a function, with the required parameters
    ct = enums.CommandType
    command_map = {
        ct.JOIN: partial(cmd.join, client_id, command),
        ct.LEAVE: partial(cmd.leave, client_id, command),
        ct.START: partial(cmd.new, client_id, game),
        ct.ABORT: partial(cmd.abort, game),
        ct.PROPOSE_TEAM: partial(cmd.propose_team, game, player, command),
        ct.VOTE_YES: partial(cmd.vote_team, game, player, command),
        ct.VOTE_NO: partial(cmd.vote_team, game, player, command),
        ct.VOTE_PASS: partial(cmd.vote_mission, game, player, command),
        ct.VOTE_FAIL: partial(cmd.vote_mission, game, player, command),
        ct.ASSASSINATE: partial(cmd.assassinate, game, player, command)
    }

    # perform command
    new_state = command_map[command.command]()
    # if there's a new state in town, down the rabbit hole go
    if new_state:
        _change_state(client_id, game, command, new_state)


def _change_state(
    client_id: int,
    game: model.Game,
    command: model.Command,
    new_state: enums.GameState
):
    # write new state to db
    db.set_game_state(game.id_, new_state)

    # go through all corresponding change functions
    state_change_map = {
        enums.GameState.RECRUITING: 'bar',
    }

    # execute state functions
    for action in state_change_map[new_state]:
        action()
