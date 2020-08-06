import sqlite3
from sqlite3 import Error


def _connect(db_file):
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


def _create_table(connection, create_table_sql):
    """Create a table from the create_table_sql statement

    Args:
        connection (sqlite3 connection): Connection to SQLite database
        create_table_sql (str): A SQL 'CRATE TABLE' statement
    """
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
