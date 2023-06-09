"""
Provides the initial database structure
"""

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("AciduleDB.db")
cur = conn.cursor()

# Create "emission" table
cur.execute("""CREATE TABLE IF NOT EXISTS emission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fichier_nom TEXT,
            emission_nom TEXT,
            titre TEXT,
            date_diffusion TEXT,
            lien TEXT,
            langue TEXT,
            topics TEXT,
            transcription_id INTEGER,
            FOREIGN KEY(transcription_id) REFERENCES transcription(id)
            );""")

# Create "transcription" table
cur.execute("""CREATE TABLE IF NOT EXISTS transcription (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT,
            lemmas TEXT,
            emission_id INTEGER,
            FOREIGN KEY(emission_id) REFERENCES emission(id)
            );""")

# Create "transcription_freq_word" table
cur.execute('''CREATE TABLE IF NOT EXISTS transcription_freq_word (
                    id INTEGER PRIMARY KEY,
                    transcription_id INTEGER,
                    word_id INTEGER,
                    FOREIGN KEY(transcription_id) REFERENCES transcription(id),
                    FOREIGN KEY(word_id) REFERENCES freq(id)
                )''')

# Create "freq" table
cur.execute('''CREATE TABLE IF NOT EXISTS freq (
                    id INTEGER PRIMARY KEY,
                    word TEXT,
                    frequency INTEGER
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS lda_model_info (
                    id INTEGER PRIMARY KEY,
                    html_content TEXT,
                    id2word_content TEXT,
                    lda_model_content TEXT
                )''')

# Commit the changes and close the cursor and connection
conn.commit()
cur.close()
conn.close()
