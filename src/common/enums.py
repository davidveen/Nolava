
from enum import IntEnum, auto


class MessageType(IntEnum):

    # Game message
    GAME_START = 100
    GAME_RESUME = 101  # template not made, no back-end implementation
    PLAYER_JOIN = 110
    PLAYER_LEAVE = 111
    READY_LIST = 120
    GAME_END = 199

    # GameState message
    GAME_STATUS = 200  # template not made, no back-end implementation
    ROUND_START = 201
    PROPOSAL_VOTE_START = 210
    PROPOSAL_NEXT = 211
    PROPOSAL_ACCEPTED_BY_DEFAULT = 218
    PROPOSAL_VOTE_RESULT = 219
    MISSION_VOTE_START = 220
    MISSION_VOTE_RESULT = 229
    ASSASSIN_ALERT = 230
    ASSASSIN_RESULT = 231
    PRIVATE_VOTE_CONFIRMATION = 240
    PUBLIC_VOTE_CONFIRMATION = 241

    # Private message
    ROLE_MESSAGE = 300
    PROPOSAL_VOTE_ALERT = 301
    MISSION_VOTE_ALERT = 302
    ASSASSIN_PRIVATE_ALERT = 303

    # Error
    UNKNOWN_ERROR = 900
    GAME_LOAD_FAIL = 901
    GAME_START_FAIL = 902
    ALREADY_JOINED = 903
    ALREADY_LEFT = 904

    GAME_IN_PROGRESS = 910
    NO_GAME_IN_PROGRESS = 911        
    NOT_ENOUGH_PLAYERS = 912
    TOO_MANY_PLAYERS = 913

    UNEXPECTED_VOTE = 920
    FUCKED_UP_VOTE = 921
    FUCKED_UP_PROPOSAL = 922
    FUCKED_UP_MURDER = 923
    UNEXPECTED_MURDER = 923
    ALREADY_VOTED = 924
    ALREADY_PROPOSED = 925
    ALREADY_MURDERED = 926

    NOT_ENOUGH_PLAYERS_PROPOSAL = 930
    TOO_MANY_PLAYERS_PROPOSAL = 931
    UNEXPECTED_PROPOSAL = 932


class GameState(IntEnum):
    RECRUITING = 1
    TEAM_PROPOSAL = 2
    TEAM_VOTE = 3
    TEAM_VOTE_COMPLETE = 4
    MISSION_VOTE = 5
    MISSION_VOTE_COMPLETE = 6
    ASSASSINATION = 7
    CONCLUDED = 8
    ABORTED = 99


class MissionStatus(IntEnum):
    PROPOSING = 1
    VOTING_TEAM = 2
    VOTING_MISSION = 3
    CONCLUDED = 9
    ABORTED = 99


class ProposalStatus(IntEnum):
    OPEN = 1
    CLOSED = 2
    ABORTED = 99


class Role(IntEnum):
    MERLIN = 0
    PERCIVAL = 1
    LOYAL_SERVANT = 2
    MORDRED = 3
    ASSASSIN = 4
    OBERON = 5
    MORGANA = 6
    MINION = 7


class CommandType(IntEnum):
    START = auto()
    ABORT = auto()

    LEAVE = auto()
    JOIN = auto()

    VOTE_YES = auto()
    VOTE_NO = auto()
    VOTE_PASS = auto()
    VOTE_FAIL = auto()

    PROPOSE_TEAM = auto()
    ASSASSINATE = auto()
    HELP = auto()
