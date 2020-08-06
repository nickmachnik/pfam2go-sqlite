import sqlite3
from sqlite3 import Error


def connect(db_file):
    """Connect to SQLite database.

    Args:
        db_file (str): SQLite database file

    Returns:
        SQLite connection object or None
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return connection
