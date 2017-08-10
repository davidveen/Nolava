
import src.message as message


import src.common.enums as enums
import src.common.model as model


def recruit



# TEAM_PROPOSAL
# check mission number
# get required number of players
# get leader
# post messages

def team_vote(game: model.Game):
    """
    Game is in team_vote status
    send the following notifications:
    PUBLIC
        - PROPOSAL_VOTE_START
    PRIVATE
        - PROPOSAL_VOTE_ALERT
    
    notifications are skipped if proposal is 6th proposal
    """
    pass


def team_vote_complete(game: model.Game):
    """
    Game is in team_vote_complete status
    send the following notifications:
    PUBLIC
        - PROPOSAL_VOTE_RESULT
        OR if 6th proposal
        - PROPOSAL_ACCEPTED_BY_DEFAULT
    """
    pass


def mission_vote(game: model.Game):
    """
    Game is in mission_vote status
    send the following notifications:
    PUBLIC
        - MISSION_VOTE_START
    PRIVATE
        - 
    """   


def assign_player_positions(game_id: int):
    pass


def assign_player_roles(game_id: int):
    pass


def next_leader(game_id: int):
    """
    Rotate leadership to next player position
    """
    pass

