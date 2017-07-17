"""
Take a message and entertain the user with it
"""

from typing import Any
from .common.enums import MessageType


def post_message(recipient_id: Any, message: MessageType):
    """
    Add a message to the database for pickup by the front-end.
    """
    raise NotImplementedError
