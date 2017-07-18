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
