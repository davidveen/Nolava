
"""
All player commands party here
"""

from typing import Callable, Any, Tuple
from functools import partial
from src.util.namedtuple_default import namedtuple_with_defaults

import src.exceptions as exceptions
import src.database as db
import src.message as message
import src.common.enums as enums
import src.common.model as model

# TODO: move to settings?
_MIN_PLAYERS = 5
_MAX_PLAYERS = 10
_PUBLIC_CHANNEL = 'bar'

GameCheck = namedtuple_with_defaults(
    'GameCheck',
    'func recipient msg contents',
    {'recipient': _PUBLIC_CHANNEL, 'msg': enums.MessageType.UNKNOWN_ERROR}
)


def join(client_id: int, command: model.Command):
    """
    Declare player available for next game
    """
    def already_joined():
        return db.check_player_has_joined(client_id, command.user.id_)

    check_map = (
        GameCheck(
            func=already_joined,
            msg=enums.MessageType.ALREADY_JOINED
        ),
    )

    for check in check_map:
        if not _game_check(
            func=check.func,
            msg=check.msg,
            contents=check.contents,
            recipient=check.recipient
        ):
            return

    # register player availability
    db.toggle_player_availability(client_id, command.user.id_)
    # send message
    message.post_message(command.user.id_, enums.MessageType.PLAYER_JOIN)


def leave(client_id: int, command: model.Command):
    """
    Declare player unavailable for next game
    """
    def already_left():
        return not db.check_player_has_joined(client_id, command.user.id_)

    check_map = (
        GameCheck(
            func=already_left,
            msg=enums.MessageType.ALREADY_LEFT
        ),
    )

    for check in check_map:
        if not _game_check(
            func=check.func,
            msg=check.msg,
            contents=check.contents,
            recipient=check.recipient
        ):
            return

    # register player availability
    db.toggle_player_availability(client_id, command.user.id_)
    # send message
    message.post_message(command.user.id_, enums.MessageType.PLAYER_LEAVE)


def new(client_id: int, game: model.Game):
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
    def none_in_progress():
        """check if a game is in progress"""
        return game is None

    def enough_players(num_players):
        return num_players < _MIN_PLAYERS

    def not_too_many_players(num_players):
        return num_players > _MAX_PLAYERS

    num_players_registered = len(db.get_available_players(client_id))

    check_map = (
        GameCheck(
            func=none_in_progress,
            msg=enums.MessageType.GAME_IN_PROGRESS
        ),
        GameCheck(
            func=partial(enough_players, num_players_registered),
            msg=enums.MessageType.NOT_ENOUGH_PLAYERS
        ),
        GameCheck(
            func=partial(not_too_many_players, num_players_registered),
            msg=enums.MessageType.TOO_MANY_PLAYERS
        )
    )

    for check in check_map:
        if not _game_check(
            func=check.func,
            msg=check.msg,
            contents=check.contents,
            recipient=check.recipient
        ):
            return

    # create new game
    db.new_game(client_id)
    # change state to TEAM_PROPOSAL
    return enums.GameState.TEAM_PROPOSAL


def abort(game: model.Game):
    """
    Set the active game state for client to GameState.ABORTED
    """
    # TODO: some kind of check if abortion is legal?

    def game_in_progress():
        return game

    check_map = (
        GameCheck(
            func=game_in_progress,
            msg=enums.MessageType.NO_GAME_IN_PROGRESS
        ),
    )

    for check in check_map:
        if not _game_check(
            func=check.func,
            msg=check.msg,
            contents=check.contents,
            recipient=check.recipient
        ):
            return

    return enums.GameState.ABORTED


def propose_team(
    game: model.Game,
    player: model.Player,
    command: model.Command
):
    """
    Process a team proposal
    """
    def proposed_by_leader():
        """check if player is current leader"""
        return game.position == player.position

    def enough_players(expected):
        return not len(command.payload.split(',')) < expected

    def too_many_players(expected):
        return not len(command.payload.split(',')) > expected

    def known_players():
        """check if each player is a known player"""
        raise NotImplementedError

    expected_players = 5  # TODO: get expected number of players

    check_map = (
        GameCheck(
            func=partial(_game_is_ready, game, enums.GameState.TEAM_PROPOSAL),
            recipient=command.user.id_,
            msg=enums.MessageType.UNEXPECTED_PROPOSAL
        ),
        GameCheck(
            func=proposed_by_leader,
            recipient=command.user.id_,
            msg=enums.MessageType.UNEXPECTED_PROPOSAL
        ),
        GameCheck(
            func=partial(enough_players, expected_players),
            recipient=command.user.id_,
            msg=enums.MessageType.NOT_ENOUGH_PLAYERS_PROPOSAL
        ),
        GameCheck(
            func=partial(too_many_players, expected_players),
            recipient=command.user.id_,
            msg=enums.MessageType.TOO_MANY_PLAYERS_PROPOSAL
        ),
        GameCheck(
            func=known_players,
            recipient=command.user.id_,
            msg=enums.MessageType.FUCKED_UP_PROPOSAL,
            contents=(command.payload)
        )
    )

    for check in check_map:
        if not _game_check(
            func=check.func,
            msg=check.msg,
            contents=check.contents,
            recipient=check.recipient
        ):
            return

    # update database
    # TODO: register_proposal interface not defined
    db.register_proposal(
        game_id=game.id_
    )

    return enums.GameState.TEAM_VOTE


def vote_team(
    game: model.Game,
    player: model.Player,
    command: model.Command):
    """
    Vote YES/NO on the current team proposal
    """
    def not_already_voted():
        """check if player hasn't voted already"""
        raise NotImplementedError

    def all_votes_in(expected):
        raise NotImplementedError

    check_map = (
        GameCheck(
            func=partial(_game_is_ready(game, enums.GameState.TEAM_VOTE)),
            recipient=command.user.id_,
            msg=enums.MessageType.UNEXPECTED_VOTE
        ),
        GameCheck(
            func=not_already_voted,
            recipient=command.user.id_,
            msg=enums.MessageType.ALREADY_VOTED
        )
    )

    for check in check_map:
        if not _game_check(
            func=check.func,
            msg=check.msg,
            contents=check.contents,
            recipient=check.recipient
        ):
            return

    # register vote
    db.register_team_vote(
        game_id=game.id_,
        player_id=player.id_,
        vote=command.command == enums.CommandType.VOTE_YES,
        message=command.payload
    )

    # TODO: check if all votes are in
    expected_votes = 5  # TODO: get expected num of votes
    if not all_votes_in(expected_votes):
        return

    return enums.GameState.TEAM_VOTE_COMPLETE


def vote_mission(
    game: model.Game,
    player: model.Player,
    command: model.Command):
    """
    Vote PASS/FAIL on the current mission
    """
    def player_on_mission():
        """check if player is on the mission"""
        return player in db.get_players_on_mission(game.id_)

    def vote_valid():
        """check when vote is FAIL, player is a baddie"""
        if command.command == enums.CommandType.VOTE_FAIL:
            return player.role in (
                enums.Role.MORDRED,
                enums.Role.ASSASSIN,
                enums.Role.OBERON,
                enums.Role.MORGANA,
                enums.Role.MINION
            )
        return True

    def not_already_voted():
        """check if player hasn't voted already"""
        votes = db.get_mission_votes(game.id_)
        
        for vote in votes:
            if vote.player_id == player.id_:
                return
        return True

    def all_votes_in(expected):
        """check if all mission votes have been cast"""
        return len(db.get_mission_votes(game.id_)) == expected

    check_map = (
        GameCheck(
            func=partial(_game_is_ready, game, enums.GameState.MISSION_VOTE),
            recipient=command.user.id_,
            msg=enums.MessageType.UNEXPECTED_VOTE
        ),
        GameCheck(
            func=player_on_mission,
            recipient=command.user.id_,
            msg=enums.MessageType.UNEXPECTED_VOTE
        ),
        GameCheck(
            func=vote_valid,
            recipient=command.user.id_,
            msg=enums.MessageType.FUCKED_UP_VOTE
        ),
        GameCheck(
            func=not_already_voted,
            recipient=command.user.id_,
            msg=enums.MessageType.ALREADY_VOTED
        )
    )

    for check in check_map:
        if not _game_check(
            func=check.func,
            msg=check.msg,
            contents=check.contents,
            recipient=check.recipient
        ):
            return

    # register vote
    db.register_mission_vote(
        game_id=game.id_,
        player_id=player.id_,
        vote=command.command == enums.CommandType.VOTE_PASS
    )

    # TODO: check if all votes are in
    expected_votes = 5  # TODO: get expected number of votes
    if not all_votes_in(expected_votes):
        return

    return enums.GameState.MISSION_VOTE_COMPLETE


def assassinate(
    game: model.Game,
    player: model.Player,
    command: model.Command
):
    """
    Kill the target
    """
    def valid_target():
        """check if target is a known player"""
        return db.get_player_by_name(game.id_, command.payload)
    
    def player_is_assassin():
        """check if player is the assassin"""
        return player.role == enums.Role.ASSASSIN
    
    def not_already_murdered():
        """check if murder is not already done"""
        raise NotImplementedError

    check_map = (
        GameCheck(
            func=partial(_game_is_ready, game, enums.GameState.ASSASSINATION),
            recipient=command.user.id_,
            msg=enums.MessageType.UNEXPECTED_MURDER
        ),
        GameCheck(
            func=player_is_assassin,
            recipient=command.user.id_,
            msg=enums.MessageType.UNEXPECTED_MURDER
        ),
        GameCheck(
            func=valid_target,
            recipient=command.user.id_,
            msg=enums.MessageType.FUCKED_UP_MURDER,
            contents=(command.payload)
        ),
        GameCheck(
            func=not_already_murdered,
            recipient=command.user.id_,
            msg=enums.MessageType.ALREADY_MURDERED
        )
    )

    for check in check_map:
        if not _game_check(
            func=check.func,
            msg=check.msg,
            contents=check.contents,
            recipient=check.recipient
        ):
            return

    # TODO: register the kill
    # NOTE: no field exists yet in boomerdb

    return enums.GameState.CONCLUDED


#########################
### PRIVATE FUNCTIONS ###
#########################

def _game_is_ready(game: model.Game, target_state: enums.GameState):
    return game.state == target_state

def _game_check(
    func: Callable,
    msg: enums.MessageType,
    contents: Tuple[str, ...]=None,
    recipient=None
) -> Any:
    try:
        return func()
    except exceptions.DataAccessException:
        # TODO: public channel setting
        admin = None
        query = None
        message.post_message(admin, enums.MessageType.DB_GO_BOOM, query)
    except exceptions.GameException:
        message.post_message(recipient, msg, *contents)
