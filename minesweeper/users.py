from flask import Blueprint

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def get_users():
    """ TODO: Implement
    List existing users
    :return: List of registered users
    """
    print()
    return "NOT IMPLEMENTED"


@bp.route("/", methods=["POST"])
def register_users():
    """ TODO: Implement
    Create new user
    :return: None
    """
    return "NOT IMPLEMENTED"