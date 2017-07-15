"""
Compact Slack API client.
"""


import json
from typing import List, NamedTuple

import slacker

with open("config/slackbot.json", "r") as config:
    _CONFIG = json.load(config)

_SLACK = slacker.Slacker(_CONFIG["token"])


SlackMessage = NamedTuple(
    "SlackMessage",
    [("user_id", str), ("timestmap", str), ("text", str)]
)


SlackUser = NamedTuple(
    "SlackUser",
    [("name", str), ("id", str)]
)


SlackChannel = NamedTuple(
    "SlackChannel",
    [("name", str), ("id", str), ("users", List[SlackUser])]
)


def message(target: str, text: str) -> None:
    """
    Post a message to target (either a Slack User ID or channel name) as
    deepthought.
    """
    _SLACK.chat.post_message(target, text, as_user=True)


def chat_history(
    source_id: str,
    private: bool=False,
    timestamp: float=0.0
) -> List[SlackMessage]:
    """
    Get chat history of either target channel or user (IM).

    Optionally include timestamp from which time on messages will be
    retrieved.
    """
    get_history = _SLACK.im.history if private else _SLACK.channels.history
    history = get_history(source_id, oldest=timestamp).body["messages"]

    return [
        SlackMessage(
            user_id=msg["user"],
            timestamp=msg["ts"],
            text=msg["text"]
        )
        for msg in history
    ]


def user_by_id(user_id: str) -> SlackUser:
    """
    Find a slack user by Slack ID.
    """
    user = _SLACK.users.info(user_id).body["user"]

    return SlackUser(
        id=user["id"],
        name=user["name"]
    )


def channel_by_name(name: str) -> SlackChannel:
    """
    Find a Slack channel by name.
    """
    channels = _SLACK.channels.list(exclude_archived=True).body["channels"]

    try:
        channel, *_ = [
            c for c in channels
            if c["name"].casefold() == name.casefold()
        ]

        return SlackChannel(
            id=channel["id"],
            name=channel["name"],
            users=[user_by_id(slack_id) for slack_id in channel["members"]]
        )

    except ValueError:
        raise slacker.Error("Channel not found.")
