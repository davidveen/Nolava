"""
Everything to do with data
"""

import datetime
import json
import pymysql

from .common.enums import GameState

CONFIG_FILE = "config/db.json"


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


class BaseAccessor(object):
    """ Base database accessor (MYSQL). """
    def __init__(self):
        with open(CONFIG_FILE) as config:
            self._settings = json.load(config)

    def _query(self, query, *args, model=None):
        cursor = self._get_cursor()
        arguments = self._stringify(args)
        result = cursor.execute(query, arguments)

        if model:
            return [model(**row) for row in cursor if row]
        else:
            return bool(result)

    def _stringify(self, args):
        arguments = []

        for arg in args:
            if isinstance(arg, datetime.datetime):
                arguments.append(arg.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                arguments.append(str(arg))

        return tuple(arguments)

    def _get_cursor(self):
        connection = pymysql.connect(
            host=self._settings.get("host", None),
            port=self._settings.get("port", None),
            user=self._settings.get("user", None),
            passwd=self._settings.get("passwd", None),
            db=self._settings.get("database", None),
            autocommit=True
        )

        return connection.cursor(pymysql.cursors.DictCursor)
