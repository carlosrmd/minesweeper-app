from flask import Blueprint, request, jsonify
from minesweeper.db import get_db
from minesweeper.constants import MSG_USER_ALREADY_EXISTS
from pymongo.errors import DuplicateKeyError


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def get_users():
    """ TODO: Implement
    List existing users
    :return: List of registered users
    """
    db = get_db()
    existing_users = []
    for user in db.users.find():
        new_user = {'user_id': str(user['_id']), 'user_name': user['user_name']}
        existing_users.append(new_user)
    return jsonify(existing_users)


@bp.route("/", methods=["POST"])
def register_users():
    """ TODO: Implement
    Create new user
    :return: None
    """
    db = get_db()
    content = request.json
    user_name = content["user_name"]
    try:
        db.users.insert_one({"user_name": user_name})
    except DuplicateKeyError:
        return jsonify({"msg": MSG_USER_ALREADY_EXISTS}), 409
    return jsonify({"msg": "Ok"})
