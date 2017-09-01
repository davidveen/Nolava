"""
Everything to do with data
"""


import datetime
import json
import os

from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Union
)

import pymysql

import src.common.enums as enums
import src.common.model as model


_DB_JSON = ("config/db_debug.json", "config/db.json")
CONFIG_FILE = _DB_JSON[0] if os.path.exists(_DB_JSON[0]) else _DB_JSON[1]


def add_slack_user(slack_id: str, name: str, super_user: bool) -> None:
    """
    Add Slack user to the database.
    """
    sql = "INSERT INTO SlackUser (SlackID, Name, Participating) VALUES(?, ?, 1)"

    _query(sql, slack_id, )


def player_join(client_id: int, slack_id: str) -> None:
    """
    Player will be included the next time a new game is started.
    """
    raise NotImplementedError


def player_leave(client_id: int, slack_id: str) -> None:
    """
    Player will not be included the next time a new game is started.
    """
    raise NotImplementedError


def get_game(client_id: int) -> model.Game:
    """
    Return current game.
    """
    raise NotImplementedError


def new_game(client_id: str) -> model.Game:
    """
    Create a new game.
    """
    raise NotImplementedError


def get_player_by_slack_id(slack_id: str) -> model.Player:
    raise NotImplementedError


def check_player_has_joined(client_id: int, slack_id: int) -> bool:
    raise NotImplementedError


def toggle_player_availability(client_id: int, slack_id: int) -> bool:
    raise NotImplementedError


def get_available_players(client_id: int):
    raise NotImplementedError


def set_game_state(game_id: int, target_state: enums.GameState):
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


def get_next_message():
    raise NotImplementedError


def mark_message_posted(message_id):
    raise NotImplementedError


def _settings() -> Dict[str, str]:
    with open(CONFIG_FILE) as config:
        return json.load(config)


def _query(
    query: str,
    *args: Tuple[Union[int, float, bool, str]]
) -> List[Dict[str, Union[int, float, bool, str]]]:
    with _get_cursor() as cursor:
        arguments = _stringify(args)
        cursor.execute(query, arguments)

        return cursor.fetchall()


def _stringify(args):
    arguments = []

    for arg in args:
        if not arg:
            continue
        if isinstance(arg, datetime.datetime):
            arguments.append(arg.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            arguments.append(str(arg))

    return tuple(arguments)


def _get_cursor():
    connection = pymysql.connect(
        host=_settings().get("host", None),
        port=_settings().get("port", None),
        user=_settings().get("user", None),
        passwd=_settings().get("password", None),
        db=_settings().get("database", None),
        autocommit=True
    )

    return connection.cursor(pymysql.cursors.DictCursor)
