
"""
All player commands party here
"""

from typing import Callable
from functools import wraps

import src.database as db
import src.message as message
import src.common.enums as enums
import src.common.model as model

_MIN_PLAYERS = 5
_MAX_PLAYERS = 10


def join(client_id: int, command: model.Command):
    """
    Declare player available for next game
    """
    @_game_check(enums.MessageType.ALREADY_JOINED)
    def _already_joined():
        return db.check_player_has_joined(client_id, command.user.id_)

    # check if user already registered
    if _already_joined():
        return

    # register player availability
    db.toggle_player_availability(client_id, command.user.id_)
    # send message
    message.post_message(command.user.id_, enums.MessageType.PLAYER_JOIN)


def leave(client_id: int, command: model.Command):
    """
    Declare player unavailable for next game
    """
    @_game_check(enums.MessageType.ALREADY_LEFT)
    def _already_left():
        return not db.check_player_has_joined(client_id, command.user.id_)

    # check if user has already unregistered
    if _already_left():
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
    @_game_check(enums.MessageType.GAME_IN_PROGRESS)
    def _none_in_progress():
        return game is None

    @_game_check(enums.MessageType.NOT_ENOUGH_PLAYERS)
    def _enough_players(num):
        return num < _MIN_PLAYERS

    @_game_check(enums.MessageType.TOO_MANY_PLAYERS)
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
        db.new_game(client_id)
        # change state to TEAM_PROPOSAL
        return enums.GameState.TEAM_PROPOSAL
    else:
        return

def abort(game: model.Game):
    """
    Set the active game state for client to GameState.ABORTED
    """
    # TODO: some kind of check if abortion is legal?
    
    @_game_check(enums.MessageType.NO_GAME_IN_PROGRESS)
    def _game_in_progress():
        return game

    if not game:
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
    @_game_check(enums.MessageType.UNEXPECTED_PROPOSAL)
    def _proposed_by_leader(recipient=command.user.id_):
        return game.position == player.position

    @_game_check(enums.MessageType.NOT_ENOUGH_PLAYERS_PROPOSAL)
    def _enough_players(expected, recipient=command.user.id_):
        return not len(command.payload.split(',')) < expected

    @_game_check(enums.MessageType.TOO_MANY_PLAYERS_PROPOSAL)
    def _too_many_players(expected, recipient=command.user.id_):
        return not len(command.payload.split(',')) > expected

    # the game needs to be ready for proposal
    if not _game_is_ready(
        game=game,
        target_state=enums.GameState.TEAM_PROPOSAL,
        msg=enums.MessageType.UNEXPECTED_PROPOSAL
        # TODO: this is not the correct message type
        # create a message for game not ready for proposal
    ):
        return

    # only the current leader can make proposals
    if not _proposed_by_leader():
        return

    # check if the proposal contains the correct number of players
    # TODO: derive correct number of players from mission
    #       and number of players in the game
    _expected_players = 5  # TODO
    if (
        not _enough_players(_expected_players) or
        not _too_many_players(_expected_players)
    ):
        return

    # TODO: update database

    return enums.GameState.TEAM_VOTE


def vote_team(
    game: model.Game,
    command: model.Command):
    """
    Vote YES/NO on the current team proposal
    """

    @_game_check(enums.MessageType.ALREADY_VOTED)
    def _vote_desired(recipient=command.user.id_):
        raise NotImplementedError

    @_game_check(enums.MessageType.FUCKED_UP_VOTE)
    def _vote_valid(recipient=command.user.id_):
        raise NotImplementedError

    def _all_votes_in(expected):
        raise NotImplementedError

    # the game needs to be ready for team vote
    if not _game_is_ready(
        game=game,
        target_state=enums.GameState.TEAM_VOTE,
        msg=enums.MessageType.UNEXPECTED_VOTE
    ):
        return

    # TODO: check if person already voted
    if not _vote_desired():
        return
    # TODO: check vote content
    if not _vote_valid():
        return

    # TODO: register vote

    # TODO: check if all votes are in
    expected_votes = 5  # TODO: get expected num of votes
    if not _all_votes_in(expected_votes):
        return

    return enums.GameState.TEAM_VOTE_COMPLETE


def vote_mission(
    game: model.Game,
    command: model.Command):
    """
    Vote PASS/FAIL on the current mission
    """
    @_game_check(enums.MessageType.UNEXPECTED_VOTE)
    def _player_on_mission(recipient=command.user.id_):
        raise NotImplementedError
    
    @_game_check(enums.MessageType.FUCKED_UP_VOTE)
    def _vote_valid(recipient=command.user.id_):
        raise NotImplementedError


    def _all_votes_in(expected):
        raise NotImplementedError

    # the game needs to be ready for mission vote
    if not _game_is_ready(
        game=game,
        target_state=enums.GameState.MISSION_VOTE,
        msg=enums.MessageType.UNEXPECTED_VOTE
        # TODO: separate message for unexpected team vote?
    ):
        return

    # TODO: check if player is on mission
    if not _player_on_mission():
        return
    # TODO: check vote content
    # TODO: if vote is FAIL, check if player is a baddie
    if not _vote_valid():
        return

    # TODO: register vote

    # TODO: check if all votes are in
    expected_votes = 5  # TODO: get expected number of votes
    if not _all_votes_in(expected_votes):
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
    @_game_check(enums.MessageType.FUCKED_UP_MURDER)
    def _valid_target(recipient=command.user.id_):
        return db.get_player_by_name(game.id_, command.payload)

    @_game_check(enums.MessageType.UNEXPECTED_MURDER)
    def _player_is_assassin(recipient=command.user.id_):
        return player.role == enums.Role.ASSASSIN

    @_game_check(enums.MessageType.ALREADY_MURDERED)
    def _murder_desired(recipient=command.user.id_):
        raise NotImplementedError

    # the game needs to be ready for assassination
    if not _game_is_ready(
        game=game,
        target_state=enums.GameState.ASSASSINATION,
        msg=enums.MessageType.UNEXPECTED_MURDER
    ):
        return

    # the murderer must be an assassin
    if not _player_is_assassin():
        return
    # the assassin may only strike once
    if not _murder_desired():
        return
    # the target must be an existing player
    if not _valid_target():
        return
    
    # TODO: register the kill
    # NOTE: no field exists yet in boomerdb

    return enums.GameState.CONCLUDED


#########################
### PRIVATE FUNCTIONS ###
#########################

def _game_check(msg: enums.MessageType) -> Callable:
    def _decorator(func: Callable) -> Callable:
        @wraps(func)
        def _wrapper(*args, recipient=None, **kwargs) -> Callable:
            # TODO: if recipient is empty, default to public channel
            # TODO: somehow include content parameters in message
            is_ok = func(*args, **kwargs)
            if not is_ok:
                message.post_message(recipient, msg)
            return is_ok
        return _wrapper
    return _decorator

def _game_is_ready(
    game: model.Game,
    target_state: enums.GameState,
    msg: enums.MessageType
) -> None:
    @_game_check(msg)
    def _check_game_state():
        return game.state == target_state
    return _check_game_state()
