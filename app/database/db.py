import sqlite3
from app.config.settings import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)