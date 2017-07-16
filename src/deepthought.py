"""
Deep shit, yo.
"""

import datetime
import time

import src.slack as slack


def commence(debug: bool=False) -> None:
    """
    Start deepthought.
    """
    # set timestamp to current time
    now = datetime.datetime.now()
    timestamp = str(time.mktime(now.timetuple()))
    channel = slack.channel_by_name("nolava")

    while True:
        # check the main channel for messages
        channel_messages = slack.chat_history(channel, timestamp=timestamp)

        if not channel_messages:
            continue

        for message in channel_messages:
            print(message.text)
        
        # set timestamp to timestamp of last message
        timestamp = channel_messages[-1].timestamp
