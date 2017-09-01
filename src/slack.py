"""
Compact Slack API client.
"""


import json

from typing import (
    List,
    Union
)

import slacker

from .common.model import (
    SlackChannel,
    SlackMessage,
    SlackUser
)


with open("config/slackbot.json", "r") as config:
    _CONFIG = json.load(config)

_SLACK = slacker.Slacker(_CONFIG["token"])


def post_message(target: str, text: str) -> None:
    """
    Post a message to target (either a Slack User ID or channel name) as
    deepthought.
    """
    _SLACK.chat.post_message(target, text, as_user=True)


def delete_message(message: SlackMessage) -> None:
    """
    Delete message in the target channel that was posted at the given
    timestamp.
    """
    _SLACK.chat.delete(message.channel.id, message.timestamp)


def chat_history(
    channel: Union[SlackChannel, SlackUser],
    private: bool=False,
    timestamp: float=None
) -> List[SlackMessage]:
    """
    Get chat history of either target channel or user (IM).

    Optionally include timestamp from which time on messages will be
    retrieved.
    """
    if private:
        private_channels = _SLACK.im.list().body
        channel_id, *_ = [
            c["id"] for c in private_channels
            if c["user"] == channel.id_
        ]
        history = _SLACK.im.history(channel_id, oldest=timestamp)
    else:
        history = _SLACK.channels.history(channel.id_, oldest=timestamp)

    return [
        SlackMessage(
            channel=channel,
            user=user_by_id(msg["user"]),
            timestamp=msg["ts"],
            text=msg["text"]
        )
        for msg in history
        if msg.get("user", False)
    ]


def user_by_id(user_id: str) -> SlackUser:
    """
    Find a slack user by Slack ID.
    """
    user = _SLACK.users.info(user_id).body["user"]

    return SlackUser(
        id_=user["id"],
        name=user["name"]
    )


def user_by_name(user_name: str) -> SlackUser:
    """
    Find a Slack user by name.
    """
    all_users = _SLACK.users.list().body["members"]

    try:
        user, *_ = [
            u for u in all_users
            if u["name"].casefold() == user_name.casefold()
        ]

        return SlackUser(
            id_=user["id"],
            name=user["name"]
        )

    except ValueError:
        raise slacker.Error(f"Could not find user \"{user_name}\".")


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
            id_=channel["id"],
            name=channel["name"],
            users=[user_by_id(slack_id) for slack_id in channel["members"]]
        )

    except ValueError:
        raise slacker.Error("Channel not found.")
