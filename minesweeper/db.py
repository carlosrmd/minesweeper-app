from pymongo import MongoClient
from flask import current_app
from flask import g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = MongoClient(
            current_app.config["MONGO_URI"]
        ).minesweeperdb

    return g.db


