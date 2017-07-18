"""
Take a message and entertain the user with it
"""

from typing import Any
from .common.enums import MessageType


def post_message(recipient: str, message: MessageType, *args):
    """
    Add a message to the database for pickup by the front-end.

    - recipient:
        channel or player receiving the message
    - message:
        type of message
    - args:
        any variable content to be included
    """
    raise NotImplementedError
