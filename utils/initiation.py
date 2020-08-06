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


def initiate_db(path):
    sql_create_Pfam = """CREATE TABLE IF NOT EXISTS Pfam (  # noqa: F841
                        accession text PRIMARY KEY NOT NULL,
                        id text NOT NULL UNIQUE,
                    );"""

    sql_create_GO = """CREATE TABLE IF NOT EXISTS GO (
                        id text PRIMARY KEY NOT NULL,
                        name text NOT NULL UNIQUE,
                    );"""

    sql_create_PfamGORelation = """CREATE TABLE IF NOT EXISTS PfamGORelation(
                                    Pfam_accession text NOT NULL,
                                    GO_id text NOT NULL,
                                    FOREIGN KEY (Pfam_accession) REFERENCES Pfam(accession),
                                    FOREIGN KEY (GO_id) REFERENCES GO(id),
                                    UNIQUE (Pfam_accession, GO_id)
                                );"""

    sql_create_uniprot = """CREATE TABLE IF NOT EXISTS UniProt (
                            accession text PRIMARY KEY,
                            entry_name text NOT NULL UNIQUE,
                        );"""

    sql_create_PfamUniProtRelation = """CREATE TABLE IF NOT EXISTS PfamUniProtRelation(
                                    Pfam_accession text NOT NULL,
                                    UniProt_accession text NOT NULL,
                                    position text NOT NULL,
                                    FOREIGN KEY (Pfam_accession) REFERENCES Pfam(accession),
                                    FOREIGN KEY (UniProt_accession) REFERENCES UniProt(accession),
                                    UNIQUE (Pfam_accession, GO_id)
                                );"""

    # create db
    connection = _connect(path)

    # create tables
    if connection is not None:
        pass
    else:
        print("Error! cannot create the database connection.")
