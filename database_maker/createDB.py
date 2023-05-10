import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("AciduleDB.db")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS emission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fichier_nom TEXT,
            titre TEXT,
            date_diffusion TEXT,
            lien TEXT,
            transcription_id INTEGER,
            FOREIGN KEY(transcription_id) REFERENCES transcription(id)
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS transcription (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT,
            emission_id INTEGER,
            FOREIGN KEY(emission_id) REFERENCES emission(id)
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS topic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS transcription_topic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transcription_id INTEGER,
            topic_id INTEGER,
            FOREIGN KEY(transcription_id) REFERENCES transcription(id),
            FOREIGN KEY(topic_id) REFERENCES topic(id)
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS freq_word (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              word TEXT
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS transcription_freq_word (
              transcription_id INTEGER,
              word_freq_id INTEGER,
              FOREIGN KEY(transcription_id) REFERENCES transcription(id),
              FOREIGN KEY(word_freq_id) REFERENCES freq_word(id)
          );""")

cur.execute("""CREATE TABLE IF NOT EXISTS freq (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              frequency INTEGER
            );""")

cur.execute("""CREATE TABLE IF NOT EXISTS freq_word_freq (
              word_freqency_id INTEGER,
              freq_id INTEGER,
              FOREIGN KEY(word_freqency_id) REFERENCES freq_word(id),
              FOREIGN KEY(freq_id) REFERENCES freq(id)
          );""")

conn.commit()
cur.close()
conn.close()

