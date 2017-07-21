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


class Command(NamedTuple):
    command: enums.CommandType
    source: str
    user: SlackUser
    payload: str


class Game(NamedTuple):
    id_: int
    state: enums.GameState
    position: int
    victor: Optional[str]
    mission: int
    proposal: int


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


class Vote(NamedTuple):
    subject_id: int
    player_id: int
    vote: bool
    msg: str

