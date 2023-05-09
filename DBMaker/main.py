from createDB import create_connection, create_table


def main():
    database = r"Acidule.db"
    CREATE_EMISSION_TABLE = """CREATE TABLE IF NOT EXISTS emission (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fichier_nom TEXT,
                titre TEXT,
                date_diffusion TEXT,
                duree TEXT,
                transcription_id INTEGER,
                FOREIGN KEY(transcription_id) REFERENCES transcription(id)

            );"""

    CREATE_TRANSCRIPTION_TABLE = """ CREATE TABLE IF NOT EXISTS transcription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texte TEXT,
                emission_id INTEGER,
                FOREIGN KEY(emission_id) REFERENCES emission(id)
            );"""

    CREATE_TOPIC_TABLE = """ CREATE TABLE IF NOT EXISTS topic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                frequency_rank  INTEGER
            );"""

    CREATE_TRANSCRIPTION_TOPIC_TABLE = """CREATE TABLE IF NOT EXISTS transcription_topic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transcription_id INTEGER,
                topic_id INTEGER,
                FOREIGN KEY(transcription_id) REFERENCES transcription(id),
                FOREIGN KEY(topic_id) REFERENCES topic(id)
            );"""

    CREATE_FREQ_WORD_TABLE = """ CREATE TABLE IF NOT EXISTS freq_word (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT,
                frequency_rank INTEGER
            );"""

    CREATE_TRANSCRIPTION_FREQ_WORD_TABLE = """CREATE TABLE IF NOT EXISTS transcription_freq_word (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transcription_id INTEGER,
                freq_word_id INTEGER,
                FOREIGN KEY(transcription_id) REFERENCES transcription(id),
                FOREIGN KEY(freq_word_id) REFERENCES freq_word(id)
            );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, CREATE_EMISSION_TABLE)
        create_table(conn, CREATE_TOPIC_TABLE)
        create_table(conn, CREATE_TRANSCRIPTION_TOPIC_TABLE)
        create_table(conn, CREATE_FREQ_WORD_TABLE)
        create_table(conn, CREATE_TRANSCRIPTION_FREQ_WORD_TABLE)
        create_table(conn, CREATE_TRANSCRIPTION_TABLE)

        print("Tables created!")
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
'''

    INSERT_EMISSION = """INSERT INTO emission (
            fichier_nom, titre, date_diffusion, duree, transcription_id) 
            VALUES (?, ?, ?, ?, ?)"""


    def add_emission(connection, fichier_nom, titre, date_diffusion, duree, transcription_id):
        with connection:
            connection.execute(INSERT_EMISSION, (fichier_nom, titre, date_diffusion, duree, transcription_id)
                               )


    def create_emission_table():

        c.execute(CREATE_EMISSION_TABLE)

'''

# c.execute(CREATE_EMISSION_TABLE)

# c.execute(INSERT_EMISSION)
#c.execute("""DROP TABLE emission;""")



'''c.execute("SELECT * FROM emission; ")
print(c.fetchall())'''

'''
# commits the changes
conn.commit()

conn.close()

INSERT_EMISSION = """INSERT INTO emission VALUES (12, 'fichier_test.mp4', 'Fichier Test')"""

GET_ALL_EMISSIONS = "SELECT * FROM emission;"

GET_EMISSION_BY_NAME = "SELECT * FROM emission WHERE fichier_nom = ?;"

CREATE_EMISSION_TABLE = """CREATE TABLE emission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fichier_nom TEXT,
            titre TEXT,
            date_diffusion TEXT,
            duree TEXT,
            transcription_id INTEGER,
            fichier_audio BLOB,
            FOREIGN KEY(transcription_id) REFERENCES transcription(id)
        );"""

'''
