"""
Everything to do with data
"""

import datetime
import json
import pymysql
import os

from .common.enums import GameState

_DB_JSON = ("config/db_debug.json", "config/db.json")
CONFIG_FILE = _DB_JSON[0] if os.path.exists(_DB_JSON[0]) else _DB_JSON[1]


def toggle_player_availability(
    client_id: int,
    player_id: int,
) -> bool:
    def _get_player_availability() -> bool:
        raise NotImplementedError

    is_available = _get_player_availability()
    raise NotImplementedError


def get_available_players(client_id: int):
    raise NotImplementedError


def set_game_state(game_id: int, target_state: GameState):
    raise NotImplementedError


def register_proposal(game_id: int):
    raise NotImplementedError


def register_team_vote(
    game_id: int,
    player_id: int,
    vote: bool,
    message: str
) -> bool:
    """
    Register team vote
    Return False if player already voted.
    """
    raise NotImplementedError


def register_mission_vote(
    game_id: int,
    player_id: int,
    vote: bool
) -> bool:
    """
    Register team vote
    Return False if player already voted.
    """
    raise NotImplementedError


def get_player_by_name(game_id: int, player_name: str):
    raise NotImplementedError


def get_game(client_id: int) -> bool:
    # get active game
    # return False if no active game on client
    raise NotImplementedError


def get_next_message():
    db = BaseAccessor()


def mark_message_posted(message_id):
    pass


def _get_mission(game_id):
    # get active mission
    raise NotImplementedError


def _get_proposal(mission_id):
    # get active proposal
    raise NotImplementedError


def _get_players(game_id):
    raise NotImplementedError


def _get_leader(game_id):
    # get active leader
    raise NotImplementedError


def _get_assassin(game_id):
    # get assassin player id
    raise NotImplementedError
