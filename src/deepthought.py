"""
Deep shit, yo.
"""

import datetime
import time

import src.slack as slack

from src.common.model import SlackChannel, SlackMessage, SlackUser


def is_game_command(message: SlackMessage) -> bool:
    """
    Simple predicate to determine if message should be interpreted as a game
    command.

    A message is interpreted as a game command if the first character is an
    exclamation mark ("!").
    """
    return message.text.startswith("!")


def commence(debug: bool=False) -> None:
    """
    Start deepthought.
    """
    # set timestamp to current time
    now = datetime.datetime.now()
    timestamp = str(time.mktime(now.timetuple()))
    channel = slack.channel_by_name("nolava")
