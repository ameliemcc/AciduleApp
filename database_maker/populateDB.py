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

# enlever si transcription vide

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



def process_text(text):
    doc = nlp(text)
    processed_tokens = []

    for token in doc:
        # Lemmatize and remove punctuation, numerical characters, and stop words

        if token.is_alpha and not token.is_stop:
            lemma = token.lemma_.lower()

            # Filter tokens based on POS tags (noun, adjective, adverb, verb)
            if token.pos_ in ['NOUN', 'ADJ', 'ADV', 'VERB']:
                processed_tokens.append(lemma)

    return processed_tokens

def add_processed_tokens_to_transcription(transcription_id, processed_tokens):
    # Convert the processed tokens list to a string
    lemmas = " ".join(processed_tokens)

    # Update the "lemmas" column in the "transcription" table
    query_update_lemmas = "UPDATE transcription SET lemmas = ? WHERE id = ?"
    params_update_lemmas = (lemmas, transcription_id)
    cursor.execute(query_update_lemmas, params_update_lemmas)

def process_transcriptions():
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
        processed_words = process_text(texte)
        top_10 = Counter(processed_words).most_common(10)
        print(top_10)

        # Insert the frequent words and their frequencies into the "transcription_freq_word" and "freq" tables
        for word, frequency in top_10:
            # Insert into "freq" table
            cursor.execute("INSERT INTO freq (word, frequency) VALUES (?, ?)", (word, frequency))
            word_id = cursor.lastrowid

            # Insert into "transcription_freq_word" table
            cursor.execute("INSERT INTO transcription_freq_word (transcription_id, word_id) VALUES (?, ?)",
                           (transcription_id, word_id))
        add_processed_tokens_to_transcription(transcription_id, processed_words)


    # Commit the changes
    conn.commit()


# Call the function to process transcriptions
process_transcriptions()

# Close the connection
conn.close()

