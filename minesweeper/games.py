from flask import Blueprint
from flask import request
from datetime import datetime
from minesweeper.db import get_db
from minesweeper.utils import generate_board, generate_empty_board

bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route("/", methods=["GET"])
def get_games():
    """ TODO: Implement
    List all games from existing user
    :return: List of game ids
    """
    user_id = request.args.get('user_id')
    if user_id:
        #Continue
        return "NOT IMPLEMENTED"
    else:
        return "NOT IMPLEMENTED"


@bp.route("/", methods=["POST"])
def create_game():
    """ TODO: Implement
    Creates new game with given arguments in body
    :return: id for the new game
    """
    content = request.json
    try:
        n_rows = content["n_rows"]
        n_cols = content["n_cols"]
        n_mines = content["n_mines"]
        user_name = content["user_name"]
    except KeyError:
        return {"msg": "Missing required arguments"}, 400

    new_game = {
        "user_name": user_name,
        "board": {
            "covered_board": generate_empty_board(rows=n_rows, columns=n_cols),
            "uncovered_board": generate_board(rows=n_rows, columns=n_cols, mines=n_mines),
            "uncovered_cells_count": n_rows*n_cols,
            "total_mines": n_mines
        },
        "status": "ACTIVE",
        "result": "",
        "started_at": str(datetime.now())
    }
    db = get_db()
    inserted = db.games.insert_one(new_game)
    return {"game_id": str(inserted.inserted_id)}


@bp.route("/<game_id>/state", methods=["GET"])
def get_state():
    """ TODO: Implement
    Retrieves state of existing game
    :return: game's state
    """
    pass


@bp.route("/<game_id>/<action>", methods=["PUT"])
def game_action():
    """ TODO: Implement
    Interact with existing non-finished game.
    User could: Pause, Resume, End or Move
    :return: new game's state
    """
    pass
