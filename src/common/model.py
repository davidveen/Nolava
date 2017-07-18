"""
Nuhhhnuhnhnuhnuhnuhnuhnuuuhhhnuhhnuhhnuhhnuhh can't mute this!
"""


from typing import List, NamedTuple, Optional
import src.common.enums as enums


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


class Game(NamedTuple):
    state: enums.GameState
    position: int
    victor: Optional[str]


class Player(NamedTuple):
    id_: int
    slack_id: str
    position: int
    role: enums.Role


class Mission(NamedTuple):
    number: int
    status: enums.MissionStatus
    proposal_count: int
    success: bool
