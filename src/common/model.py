"""
Nuhhhnuhnhnuhnuhnuhnuhnuuuhhhnuhhnuhhnuhhnuhh can't mute this!
"""


from typing import List, NamedTuple


class SlackUser(NamedTuple):
    name: str
    id: str


class SlackChannel(NamedTuple):
    name: str
    id: str
    users: List[SlackUser]


class SlackMessage(NamedTuple):
    channel: SlackChannel
    user: SlackUser
    text: str
    timestamp: str


class CommandData(NamedTuple):
    source: str
    user: SlackUser
    payload: str


# SlackUser = NamedTuple(
#     "SlackUser",
#     [("name", str), ("id", str)]
# )


# SlackChannel = NamedTuple(
#     "SlackChannel",
#     [("name", str), ("id", str), ("users", List[SlackUser])]
# )


# SlackMessage = NamedTuple(
#     "SlackMessage",
#     [("channel", SlackChannel), ("user", SlackUser),
#      ("timestamp", str), ("text", str)]
# )
