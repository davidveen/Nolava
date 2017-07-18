"""
Nuhhhnuhnhnuhnuhnuhnuhnuuuhhhnuhhnuhhnuhhnuhh can't mute this!
"""


from typing import List, NamedTuple


class SlackUser(NamedTuple):
    name: str
    id_: str


class SlackChannel(NamedTuple):
    name: str
    id_: str
    users: List[SlackUser]


class SlackMessage(NamedTuple):
    channel: SlackChannel
    user: SlackUser
    text: str
    timestamp: str


class Command(NamedTuple):
    source: str
    user: SlackUser
    payload: str


class Player(NamedTuple):
    id_: str
    name: str
    role: int
    position: int


class Game(NamedTuple):
    id_: str
    position: int
    state: int
    mission: int
    proposal: int

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
