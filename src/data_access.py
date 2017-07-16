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


class BaseAccessor(object):
    """ Base database accessor (MYSQL). """
    def __init__(self):
        with open(CONFIG_FILE) as config:
            self._settings = json.load(config)

    def query(self, query, *args, model=None):
        cursor = self._get_cursor()
        arguments = self._stringify(args)
        result = cursor.execute(query, arguments)

        if model:
            return [model(**row) for row in cursor if row]
        else:
            return cursor

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
            passwd=self._settings.get("password", None),
            db=self._settings.get("database", None),
            autocommit=True
        )

        return connection.cursor(pymysql.cursors.DictCursor)
