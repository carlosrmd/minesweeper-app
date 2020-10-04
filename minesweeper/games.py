from flask import Blueprint
from flask import request, jsonify
from datetime import datetime
from minesweeper.db import get_db
from minesweeper.utils import generate_board, generate_empty_board
from minesweeper.constants import PAUSE_GAME, RESUME_GAME, END_GAME, MOVE, STATUS_ACTIVE, STATUS_FINISHED,\
    STATUS_PAUSED, RESULT_FINISHED_BY_USER, MOVE_QUESTION_MARK,\
    MOVE_CLICK, MOVE_RED_FLAG, flag_cell, MSG_COMMAND_UNRECOGNIZED, MSG_GAME_NOT_FOUND, MSG_MISSING_FIELDS,\
    DATETIME_FORMAT
from minesweeper.MinesweeperPlayer import MinesweeperPlayer
from bson import ObjectId
from bson.errors import InvalidId


bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route("/", methods=["GET"])
def get_games():
    """
    List all games from existing user
    :return: List of game ids
    """
    db = get_db()
    user_name = request.args.get('user_name')
    user_filter = {}
    if user_name:
        user_filter = {"user_name": user_name}
    result = []
    for game_found in db.games.find(user_filter, {"board": 0}):
        game_found["game_id"] = str(game_found["_id"])
        del game_found["_id"]
        result.append(game_found)
    return jsonify(result)


@bp.route("/", methods=["POST"])
def create_game():
    """
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
        return {"msg": MSG_MISSING_FIELDS}, 400

    new_game = {
        "user_name": user_name,
        "board": {
            "covered_board": generate_empty_board(rows=n_rows, columns=n_cols),
            "uncovered_board": generate_board(rows=n_rows, columns=n_cols, mines=n_mines),
            "covered_cells_count": n_rows*n_cols,
            "total_mines": n_mines,
            "total_rows": n_rows,
            "total_columns": n_cols
        },
        "status": STATUS_ACTIVE,
        "started_at": str(datetime.now())
    }
    db = get_db()
    inserted = db.games.insert_one(new_game)
    return {"game_id": str(inserted.inserted_id), "board": new_game["board"]["covered_board"]}


@bp.route("/<game_id>/state", methods=["GET"])
def get_state(game_id):
    """
    Retrieves state of existing game
    :return: game's state
    """
    db = get_db()
    try:
        json_game = db.games.find_one({"_id": ObjectId(game_id)})
    except InvalidId:
        return jsonify({"msg": "Game not found."}), 404
    if json_game is None:
        return jsonify({"msg": "Game not found."}), 404
    response = {
        "board": json_game["board"]["covered_board"],
        "status": json_game["status"]
    }
    if response["status"] == "FINISHED":
        response["result"] = json_game["result"]
        response["total_time"] = json_game["total_time"]
    return jsonify(response)


@bp.route("/<game_id>/<action>", methods=["PUT"])
def game_action(game_id, action):
    """
    Interact with existing non-finished game.
    User could: Pause, Resume, End or Move
    :return: new game's state
    """
    db = get_db()
    current_game = db.games.find_one({"_id": ObjectId(game_id)}, {"status": 1, "started_at": 1})
    if current_game is None:
        return jsonify({"msg": MSG_GAME_NOT_FOUND}), 404
    game_status = current_game["status"]

    if action == PAUSE_GAME:
        if game_status == STATUS_ACTIVE:
            db.games.update_one({"_id": ObjectId(game_id)}, {"$set": {"status": STATUS_PAUSED}})

    elif action == RESUME_GAME:
        if game_status == STATUS_PAUSED:
            db.games.update_one({"_id": ObjectId(game_id)}, {"$set": {"status": STATUS_ACTIVE}})

    elif action == END_GAME:
        if game_status == STATUS_PAUSED or game_status == STATUS_ACTIVE:
            db.games.update_one({"_id": ObjectId(game_id)}, {"$set": {
                "status": STATUS_FINISHED,
                "result": RESULT_FINISHED_BY_USER,
                "total_time": (
                        datetime.now() - datetime.strptime(current_game["started_at"], DATETIME_FORMAT)
                ).total_seconds()
            }
            })

    elif action == MOVE:
        if game_status == STATUS_ACTIVE:
            body = request.json
            try:
                row = body["row"]
                col = body["column"]
                move_type = body["move_type"]
            except KeyError:
                return jsonify({"msg": MSG_MISSING_FIELDS}), 400
            if move_type == MOVE_QUESTION_MARK or move_type == MOVE_RED_FLAG:
                board = db.games.find_one({"_id": ObjectId(game_id)}, {"board": 1})["board"]
                covered_board = board["covered_board"]
                covered_board[row][col] = flag_cell[move_type]
                db.games.update_one({"_id": ObjectId(game_id)}, {'$set': {"board.covered_board": covered_board}})
            elif move_type == MOVE_CLICK:
                mp = MinesweeperPlayer(game_id, db.games)
                mp.load_game_from_db()
                mp.make_move(row, col)
                mp.save_game_to_db()

    else:
        return jsonify({"msg": MSG_COMMAND_UNRECOGNIZED}), 400
    response_game = db.games.find_one({"_id": ObjectId(game_id)}, {
        "status": 1,
        "board": 1,
        "result": 1,
        "total_time": 1
    })
    response = {
        "board": response_game["board"]["covered_board"],
        "status": response_game["status"]
    }
    if response["status"] == "FINISHED":
        response["result"] = response_game["result"]
        response["total_time"] = response_game["total_time"]
    return jsonify(response)
