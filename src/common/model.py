"""
Nuhhhnuhnhnuhnuhnuhnuhnuuuhhhnuhhnuhhnuhhnuhh can't mute this!
"""


from typing import List, NamedTuple


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
