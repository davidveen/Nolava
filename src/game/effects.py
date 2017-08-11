
import random
import src.message as message
import src.settings
import src.common.enums as enums
import src.common.model as model
import src.database as db
import src.settings

# sequential routine city
# functions represent state action sequences

# TODO:
_PUBLIC_CHANNEL = 'bar'


def recruit(game: model.Game):
    # get available users
    available_users = db.get_available_users(game.client_id)
    num_players = len(available_users)
    # get player roles and randomize positions
    with src.settings.read() as s:
        list_of_roles = []
        for i in range(num_players):
            role = s.get('PREFERENCE', str(i))
            if not s.getboolean('ROLES', role):
                if role in ('merlin', 'percival'):
                    role = 'servant'
                else:
                    role = 'minion'
            try:
                list_of_roles.append(enums.Role[role.upper()])
            except KeyError:
                # role name in settings file differs from enum role name
                # TODO: determine behaviour
                raise NotImplementedError
    random.shuffle(list_of_roles)
    positions = random.shuffle([x for x in range(num_players)])

    # register players
    for i in range(num_players):
        db.register_player(
            game_id=game.id_,
            slack_id=available_users[i].id_,
            role=list_of_roles[i],
            position=positions[i]
        )

    player_order = sorted(
        list(zip(positions, [x.name for x in available_users]))
    )

    # notify the world
    message.post(
        _PUBLIC_CHANNEL,
        enums.MessageType.GAME_START,
        player_order
    )

    # set game state to TEAM_PROPOSAL
    return enums.GameState.TEAM_PROPOSAL


def team_proposal(game: model.Game):
    """
    Game is in team_proposal status
    send the following notifications:
    PUBLIC
        - PROPOSAL_NEXT
    PRIVATE
        - PROPOSAL_PRIVATE_ALERT
    """
    # get the required number of players
    with src.settings.read() as settings:
        num_required = settings.get(
            'PLAYERS_REQUIRED',
            str(game.num_players)
        ).split(',')[game.mission - 1]

    # get the current leader
    leader = db.get_player_by_position(game.position)

    # notify the world
    message.post(
        _PUBLIC_CHANNEL,
        enums.MessageType.PROPOSAL_NEXT,  # TODO: is this the right msg?
        leader.name,
        ', '.join([p.name for p in db.get_players_in_order(game.position)]),
        game.mission,
        game.proposal,
        num_required
    )

    # instruct the leader
    message.post(
        leader.id_,
        enums.MessageType.PROPOSAL_PRIVATE_ALERT,
        game.mission,
        game.proposal,
        num_required
    )


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

