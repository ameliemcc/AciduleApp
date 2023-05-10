import re
import sqlite3
import spacy
from collections import Counter
import os

nlp = spacy.load("fr_core_news_sm")

# Establish a connection to the SQLite database
conn = sqlite3.connect('AciduleDB.db')
cursor = conn.cursor()

folder_path = "/Users/mariemccormick/PycharmProjects/AciduleApp/transcriptions"  # Path to the folder containing the .txt files


def add_transcription_and_emission(name):
    if name.endswith(".txt"):
        file_path = os.path.join(folder_path, name)
        with open(file_path, "r") as file:
            content = file.read()

        # Insert into "emission" table
        query_emission = "INSERT INTO emission (fichier_nom) VALUES (?)"
        params_emission = (name,)
        cursor.execute(query_emission, params_emission)
        emission_id = cursor.lastrowid

        # Insert into "transcription" table
        query_transcription = "INSERT INTO transcription (texte, emission_id) VALUES (?, ?)"
        params_transcription = (content, emission_id)
        cursor.execute(query_transcription, params_transcription)


# Function to filter common nouns
def common_nouns(texte):
    filtered_tokens_nouns = []

    for token in texte:
        if token.is_stop == False and token.text.isalpha() == True and token.pos_ == 'NOUN':
            token.lemma_ = str(token.lemma_).lower()
            filtered_tokens_nouns.append(token.lemma_)

    return filtered_tokens_nouns


# Loop over the files in the folder and add transcriptions and emissions
for filename in os.listdir(folder_path):
    add_transcription_and_emission(filename)

# Retrieve the "texte" column from the "transcription" table
cursor.execute("SELECT id, texte FROM transcription")
transcriptions = cursor.fetchall()

# Process each transcription
for transcription in transcriptions:
    transcription_id = transcription[0]
    texte = transcription[1]

    # Tokenize the text into words and count their frequencies
    doc = nlp(texte)
    words = common_nouns(doc)
    word_frequencies = Counter(words)

    # Select the top 10 most frequent words
    top_10 = word_frequencies.most_common(10)

    # Insert the frequent words and their frequencies into the "transcription_freq_word" and "freq" tables
    for word, frequency in top_10:
        # Insert into "freq" table
        cursor.execute("INSERT INTO freq (word, frequency) VALUES (?, ?)", (word, frequency))
        word_id = cursor.lastrowid

        # Insert into "transcription_freq_word" table
        cursor.execute("INSERT INTO transcription_freq_word (transcription_id, word_id) VALUES (?, ?)",
                       (transcription_id, word_id))

# Commit the changes and close the connection
conn.commit()
conn.close()
