import sqlite3
from . import parsing
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


def _create_pfam(connection, cursor, pfam_values):
    """
    Create a new Pfam entry.

    Args:
        connection (sqlite3 connection): Connection to SQLite database
        pfam_values (tuple(str)): tuple of values to insert
    """

    sql = "INSERT or IGNORE INTO Pfam(accession, id) VALUES(?,?)"
    cursor.execute(sql, pfam_values)


def _create_go(connection, cursor, go_values):
    """
    Create a new GO entry.

    Args:
        connection (sqlite3 connection): Connection to SQLite database
        go_values (tuple(str)): tuple of values to insert
    """

    sql = "INSERT or IGNORE INTO GO(id, name) VALUES(?,?)"
    cursor.execute(sql, go_values)


def _create_go_pfam_relation(connection, cursor, relation_values):
    """
    Create a new PfamGO relation.

    Args:
        connection (sqlite3 connection): Connection to SQLite database
        go_values (tuple(str)): tuple of values to insert
    """

    sql = """INSERT or IGNORE INTO PfamGORelation(
                Pfam_accession,
                GO_id)
                VALUES(?,?)"""
    cursor.execute(sql, relation_values)


def _create_uniprot_entry(connection, cursor, uniprot_values):
    """
    Create a new uniprot entry.

    Args:
        connection (sqlite3 connection): Connection to SQLite database
        uniprot_values (tuple(str)): tuple of values to insert
    """

    sql = """INSERT or IGNORE INTO UniProt(
                accession,
                entry_name)
                VALUES(?,?)"""
    cursor.execute(sql, uniprot_values)


def _create_pfam_uniprot_relation(connection, cursor, relation_values):
    """
    Create a new Pfam to UniProt relation.

    Args:
        connection (sqlite3 connection): Connection to SQLite database
        go_values (tuple(str)): tuple of values to insert
    """

    sql = """INSERT or IGNORE INTO PfamUniProtRelation(
                Pfam_accession,
                UniProt_accession,
                position)
                VALUES(?,?,?)"""
    cursor.execute(sql, relation_values)


def initiate_db(db_path, pfam2go_path, pfam_a_fasta_path):
    tables = []
    tables.append("""CREATE TABLE IF NOT EXISTS Pfam (
                        accession text PRIMARY KEY NOT NULL,
                        id text NOT NULL UNIQUE);""")

    tables.append("""CREATE TABLE IF NOT EXISTS GO (
                        id text PRIMARY KEY NOT NULL,
                        name text NOT NULL UNIQUE);""")

    tables.append("""CREATE TABLE IF NOT EXISTS PfamGORelation(
        Pfam_accession text NOT NULL,
        GO_id text NOT NULL,
        FOREIGN KEY (Pfam_accession) REFERENCES Pfam(accession),
        FOREIGN KEY (GO_id) REFERENCES GO(id),
        UNIQUE (Pfam_accession, GO_id)
    );""")

    tables.append("""CREATE TABLE IF NOT EXISTS UniProt (
        accession text PRIMARY KEY,
        entry_name text NOT NULL UNIQUE
    );""")

    tables.append("""CREATE TABLE IF NOT EXISTS PfamUniProtRelation(
        Pfam_accession text NOT NULL,
        UniProt_accession text NOT NULL,
        position text NOT NULL,
        FOREIGN KEY (Pfam_accession) REFERENCES Pfam(accession),
        FOREIGN KEY (UniProt_accession) REFERENCES UniProt(accession),
        UNIQUE (Pfam_accession, UniProt_accession)
    );""")

    indices = []
    indices.append("""
        CREATE UNIQUE INDEX idx_pfam_accession
        ON Pfam(accession);
        """)
    indices.append("""
        CREATE UNIQUE INDEX idx_go_id
        ON GO(id);
    """)
    indices.append("""
        CREATE UNIQUE INDEX idx_pfam_go_rel
        ON PfamGORelation(Pfam_accession, GO_id);
    """)
    indices.append("""
        CREATE UNIQUE INDEX idx_uniprot_accession
        ON UniProt(accession);
    """)
    indices.append("""
        CREATE UNIQUE INDEX idx_pfam_uniprot_rel
        ON PfamUniProtRelation(Pfam_accession, UniProt_accession, position);
    """)

    # create db
    connection = _connect(db_path)

    if connection is not None:
        with connection:
            cursor = connection.cursor()

            # create tabkes
            for create_table_sql in tables:
                cursor.execute(create_table_sql)

            # create tabkes
            for create_index_sql in indices:
                cursor.execute(create_index_sql)

            cursor.execute('BEGIN TRANSACTION')
            # insert pfam2go mapping data
            for entry in parsing.parse_pfam2go(pfam2go_path):
                curr_pfam_values = (entry.pfam_accession, entry.pfam_id)
                _create_pfam(
                    connection,
                    cursor,
                    curr_pfam_values)
                curr_go_values = (entry.go_id, entry.go_name)
                _create_go(
                    connection,
                    cursor,
                    curr_go_values)
                _create_go_pfam_relation(
                    connection,
                    cursor,
                    (entry.pfam_accession, entry.go_id))
            cursor.execute('COMMIT')

            cursor.execute('BEGIN TRANSACTION')
            # insert UniProt matches of pfam models
            for entry in parsing.parse_pfam_A_fasta(pfam_a_fasta_path):
                # insert only if the domain has a go annotation
                cursor.execute(
                    "SELECT * FROM Pfam WHERE accession = '{}';"
                    .format(entry.pfam_accession))
                matches = cursor.fetchall()
                if matches is not None:
                    _create_uniprot_entry(
                        connection,
                        cursor,
                        (entry.uniprot_accession, entry.uniprot_entry_name))
                    _create_pfam_uniprot_relation(
                        connection,
                        cursor,
                        (
                            entry.pfam_accession,
                            entry.uniprot_accession,
                            entry.location
                        ))
            cursor.execute('COMMIT')
    else:
        print("Error! cannot create the database connection.")
