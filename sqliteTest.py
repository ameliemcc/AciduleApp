import sqlite3
from sqlite3 import Error
import os
import re

# table in which emissions are stored
CREATE_EMISSION_TABLE = """CREATE TABLE IF NOT EXISTS emission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fichier_nom TEXT,
            titre TEXT,
            date_diffusion TEXT,
            duree TEXT,
            transcription_id INTEGER NOT NULL,
            FOREIGN KEY (transcription_id)
                   REFERENCES transcription (id) 
        );"""

# table in which transcriptions are stored
CREATE_TRANSCRIPTION_TABLE = """ CREATE TABLE IF NOT EXISTS transcription (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT,
            emission_id INTEGER NOT NULL,
            FOREIGN KEY(emission_id) 
                REFERENCES emission(id)
        );"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_emission(conn, emission):
    """
    Create a new emission into the emission table
    :param conn:
    :param project:
    :return: project id
    """
    sql = """INSERT INTO emission (
        fichier_nom, titre, date_diffusion, duree, transcription_id) 
        VALUES (?, ?, ?, ?, ?)"""
    cur = conn.cursor()
    cur.execute(sql, emission)
    conn.commit()
    return cur.lastrowid


def create_transcription(conn, transcription):
    """
    Create a new transcription into the transcription table
    """
    sql = """INSERT INTO transcription (
        texte, emission_id) 
        VALUES (?, ?)"""
    cur = conn.cursor()
    cur.execute(sql, transcription)
    conn.commit()
    return cur.lastrowid


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"transcriptions.db"

    # create a database connection
    conn = create_connection(database)
    c = conn.cursor()

   # c.execute("""DROP TABLE emission;""")
   # c.execute("""DROP TABLE transcription;""")

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, CREATE_EMISSION_TABLE)
        create_table(conn, CREATE_TRANSCRIPTION_TABLE)

    else:
        print("Error! cannot create the database connection.")

    with conn:
        path_of_audio_files = 'audio_files'
        for filename in os.listdir(path_of_audio_files):
            fichier_nom = os.path.join(path_of_audio_files, filename)
            titre = str(re.findall("(?:S\d+_P\d+_)(\w+)_\d{4}_\d{2}_\d{2}\.mp3", filename))
            date_diffusion = str(re.findall("(?:S\d+_P\d+_)\w+_(\d{4}_\d{2}_\d{2})\.mp3", filename))
            print(date_diffusion)
            print(type(date_diffusion))
            print(titre)
            print(type(titre))
            duree = 0
            transcription_id = 1
            fichier_audio = fichier_nom

        # create a new emission
        emission = (fichier_nom, titre, date_diffusion, duree, transcription_id)
        project_id = create_emission(conn, emission)
        transcriptiontexte = ("a", 4)
        new = create_transcription(conn, transcriptiontexte)

    x = c.execute("SELECT * FROM emission")
    #c.execute("PRAGMA foreign_keys = ON;")
    z = c.execute("SELECT * FROM transcription")

    for y in x.fetchall():
        print(y)

    for y in z.fetchall():
        print(y)


if __name__ == '__main__':
    main()
