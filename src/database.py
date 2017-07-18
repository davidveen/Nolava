"""
Everything to do with data
"""


import src.data_access as boomerdb
import src.common.enums as enums
import src.common.model as model


def add_slack_user(slack_id: str, name: str, super_user: bool) -> None:
    """
    Add Slack user to the database.
    """
    sql = "INSERT INTO SlackUser (SlackID, Name, Participating) VALUES(?, ?, 1)"

    boomerdb.query(sql, slack_id, )


def player_join(client_id: int, slack_id: str) -> None:
    """
    Player will be included the next time a new game is started.
    """
    raise NotImplementedError


def player_leave(client_id: int, slack_id: str) -> None:
    """
    Player will not be included the next time a new game is started.
    """
    raise NotImplementedError


def get_game(client_id: str) -> model.Game:
    """
    Return current game.
    """
    raise NotImplementedError


def new_game(client_id: str) -> model.Game:
    """
    Create a new game.
    """
    raise NotImplementedError


def get_player_by_slack_id(slack_id: str) -> model.Player:
    raise NotImplementedError


def check_player_has_joined(client_id: int, slack_id: int) -> bool:
    raise NotImplementedError


def toggle_player_availability(client_id: int, slack_id: int) -> bool:
    raise NotImplementedError


def get_available_players(client_id: int):
    raise NotImplementedError


def set_game_state(game_id: int, target_state: enums.GameState):
    raise NotImplementedError


def register_proposal(game_id: int):
    raise NotImplementedError


def register_team_vote(
    game_id: int,
    player_id: int,
    vote: bool,
    message: str
) -> bool:
    """
    Register team vote
    Return False if player already voted.
    """
    raise NotImplementedError


def register_mission_vote(
    game_id: int,
    player_id: int,
    vote: bool
) -> bool:
    """
    Register team vote
    Return False if player already voted.
    """
    raise NotImplementedError


def get_player_by_name(game_id: int, player_name: str):
    raise NotImplementedError


def get_game(client_id: int) -> bool:
    # get active game
    # return False if no active game on client
    raise NotImplementedError


def get_next_message():
    raise NotImplementedError


def mark_message_posted(message_id):
    pass


def _get_mission(game_id):
    # get active mission
    raise NotImplementedError


def _get_proposal(mission_id):
    # get active proposal
    raise NotImplementedError


def _get_players(game_id):
    raise NotImplementedError


def get_leader(game_id):
    # get active leader
    raise NotImplementedError


def _get_assassin(game_id):
    # get assassin player id
    raise NotImplementedError
