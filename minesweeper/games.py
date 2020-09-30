from flask import Blueprint
from flask import request

bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route("/", methods=["GET"])
def get_games():
    """ TODO: Implement
    List all games from existing user
    :return: List of game ids
    """
    user_id = request.args.get('user_id')
    return "NOT IMPLEMENTED"


@bp.route("/", methods=["POST"])
def create_game():
    """ TODO: Implement
    Creates new game with given arguments in body
    :return: id for the new game
    """
    return "NOT IMPLEMENTED"


@bp.route("/<game_id>/<action>", methods=["GET", "POST"])
def game_action():
    """ TODO: Implement
    Interact with existing non-finished game.
    User could: Pause, Resume, End or Move
    :return: new game's state
    """
    pass
