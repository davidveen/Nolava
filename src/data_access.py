"""
Everything to do with data
"""

import datetime
import json
import pymysql
import os

from typing import Any, Dict, List, Tuple, Union

from .common.enums import GameState

_DB_JSON = ("config/db_debug.json", "config/db.json")
<<<<<<< HEAD
CONFIG_FILE = _DB_JSON[0] if os.path.exists(_DB_JSON[0]) else _DB_JSON[1]


def _settings():
    with open(CONFIG_FILE) as config:
        return json.load(config)


def query(query_, *args, model=None):
    with _get_cursor() as cursor:
        arguments = _stringify(args)
        cursor.execute(query_, arguments)

        if model:
            return [model(**row) for row in cursor if row]
        else:
            return cursor.fetchall()


def _stringify(args):
    arguments = []

    for arg in args:
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
=======

with open(
    _DB_JSON[0] if os.path.exists(_DB_JSON[0]) else _DB_JSON[1]
) as config:
    _SETTINGS = json.load(config)

_CONNECTION = pymysql.connect(
    host=_SETTINGS["host"],
    user=_SETTINGS["user"],
    password=_SETTINGS["password"],
    db=_SETTINGS["database"],
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)


def query(sql: str, *args) -> List[Dict[str, Any]]:
    """
    Query the database.
    """
    with _CONNECTION.cursor() as cursor:
        cursor.execute(sql, args)

    return cursor.fetchall()
>>>>>>> jorard
