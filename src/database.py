"""
Everything to do with data
"""

import datetime
import json
import pymysql

CONFIG_FILE = "config/db.json"


def get_game_id(client_id: int):
    """
    Retrieve active game ID from client.
    """




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
            passwd=self._settings.get("password", None),
            db=self._settings.get("database", None),
            autocommit=True
        )

        return connection.cursor(pymysql.cursors.DictCursor)
