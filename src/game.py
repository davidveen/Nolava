"""
Monolith first. Services rofl.
"""
from typing import Callable
from functools import wraps

import src.database as db
import src.game_state as gs

from .message import post_message
from .common.enums import MessageType, GameState
from .common.model import Command, Game, Player

_expected = 5
_MAX_PLAYERS = 10


def give_command(client_id, command: Command):
    """
    Receive a command from deepthought
    """
    # TODO:
    #       - get Game
    #       - get Player



def toggle_available(client_id: int, player_id):
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
        return num < _expected

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
        gs.change_state(client_id, GameState.TEAM_PROPOSAL)


def abort_game(client_id: int):
    """
    Set the active game state for client to GameState.ABORTED
    """
    # TODO: some kind of check if abortion is allowed?
    gs.change_state(client_id, GameState.ABORTED)


def propose_team(client_id: int, command: Command):
    """
    Process a team proposal
    """
    @_game_check(MessageType.UNEXPECTED_PROPOSAL)
    def _proposed_by_leader(recipient=command.user.id_):
        leader = db.get_leader(client_id).id_
        player = db.get_player_by_user(command.user.id_)
        return leader == player

    @_game_check(MessageType.NOT_ENOUGH_PLAYERS_PROPOSAL)
    def _enough_players(expected, recipient=command.user.id_):
        return not len(command.payload.split(',')) < expected

    @_game_check(MessageType.TOO_MANY_PLAYERS_PROPOSAL)
    def _too_many_players(expected, recipient=command.user.id_):
        return not len(command.payload.split(',')) > expected

    # the game needs to be ready for proposal
    if not _game_is_ready(
        client_id=client_id,
        target_state=GameState.TEAM_PROPOSAL,
        message=MessageType.UNEXPECTED_PROPOSAL
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

    # change gamestate to TEAM_VOTE
    gs.change_state(client_id, GameState.TEAM_VOTE)


def vote_team(client_id: int, command: Command):
    """
    Vote yes/no on the current team proposal
    """
    # the game needs to be ready for team vote
    if not _game_is_ready(
        client_id=client_id,
        target_state=GameState.TEAM_VOTE,
        message=MessageType.UNEXPECTED_VOTE
    ):
        return

    # TODO: check if person already voted

    # TODO: check vote content

    # TODO: register vote

    # TODO: check if all votes are in

    gs.change_state(client_id, GameState.TEAM_VOTE_COMPLETE)


def vote_mission(client_id: int, command: Command):
    """
    Vote success/fail on the current mission
    """
    @_game_check(MessageType.UNEXPECTED_VOTE)
    def _player_on_mission(recipient=command.user.id_):
        raise NotImplementedError
    
    @_game_check(MessageType.FUCKED_UP_VOTE)
    def _vote_correct(recipient=command.user.id_):
        raise NotImplementedError

    # the game needs to be ready for mission vote
    # vote is valid if the player is on the mission
    # only baddies can vote fail
    if not _game_is_ready(
        client_id=client_id,
        target_state=GameState.MISSION_VOTE,
        message=MessageType.UNEXPECTED_VOTE
        # TODO: separate message for unexpected team vote?
    ):
        return

    # TODO: check if player is on mission
    if not _player_on_mission():
        return

    # TODO: check vote content
    if not _vote_correct():
        return

    # TODO: 


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
        def _wrapper(*args, recipient=None, **kwargs) -> Callable:
            # TODO: if recipient is empty, default to public channel
            is_ok = func(*args, **kwargs)
            if not is_ok:
                post_message(recipient, message)
            return is_ok
        return _wrapper
    return _decorator


def _game_is_ready(
    client_id: int,
    target_state: GameState,
    message: MessageType
) -> None:
    @_game_check(message)
    def _check_game_state():
        return db.get_game(client_id).state == target_state
    return _check_game_state()
