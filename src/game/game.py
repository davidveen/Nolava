"""
Embraces all commands as its own,
but only gets to route them to their true home.
At least when the commands grow up they come back here,
and maybe cause some effects.
"""

from functools import partial

import commands as cmd
import effects as efx
import src.exceptions as exceptions
import src.database as db
import src.common.enums as enums
import src.common.model as model


def issue_command(client_id, command: model.Command):
    """
    Receive a command from deepthought
    """
    ct = enums.CommandType
    
    # get game from database
    try:
        game = db.get_game(client_id)
    except exceptions.GameException:
        # don't allow anything but START, JOIN, LEAVE commands if no game active
        if command.command not in (ct.JOIN, ct.LEAVE, ct.START):
            # TODO: post message in channel?
            return
        else:
            pass

    # make sure the issuer is a registered slack user
    try:
        db.get_slackuser(command.user.id_)
    except exceptions.DataAccessException:
        # register the unknown user
        db.add_slack_user(command.user.id_, command.user.name)

    # get player from database, if there is a game
    try:
        player = db.get_player_by_slack_id(command.user.id_)
    except exceptions.DataAccessException:
        # unknown player issued command
        # TODO: determine behaviour
        return

    # link each command to a function, with the required parameters
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

    # the START command is exceptional, in that there was no game before
    # but there is one now
    if command.command == ct.START:
        game = db.get_game(client_id)
    # in all other cases if there is no game, we're doomed
    elif game is None:
        # TODO: determine behaviour
        pass

    # if command returned a new_state, down the rabbit hole go we must
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

    gs = enums.GameState
    # go through all corresponding change functions
    state_change_map = {
        gs.RECRUITING: efx.recruit,
        gs.TEAM_PROPOSAL: efx.team_proposal
    }

    # execute new state function
    newer_state = state_change_map[new_state](game)

    if newer_state:
        _change_state(client_id, game, command, new_state)
