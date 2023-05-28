"""
Populating the DB with its initial contents
"""
import re
import sqlite3
import os
from collections import Counter
import spacy

nlp = spacy.load("fr_core_news_sm")
file_path = os.path.join("database_maker", "AciduleDB.db")
conn = sqlite3.connect(file_path)
cursor = conn.cursor()

FOLDER_PATH = "../transcriptions"

stopwords = ["beaucoup", "bien", "oui", "non", "bon", "être", "avoir", "pouvoir",
             "faire",  "envoyer", "aller", "prendre", "devoir", "chose" ]
# match repeating numbers
PATTERN_N = r'\b(\d)(?: \1)+\b'
# match repeating ... ... ...
PATTERN_D = r'(\.\.\.)\W{2,}'

def replace_patterns(match):
    return ''

def add_transcription_and_emission(name):
    """Function necessary to add the transcription and emission to the DB"""
    if name.endswith(".txt"):
        file_path = os.path.join(FOLDER_PATH, name)
        with open(file_path, "r") as file:
            content = file.read()

        # Don't add into the DB if the transcription is empty
        if len(content) > 20:
            content = re.sub(PATTERN_N, replace_patterns, content)
            content = re.sub(PATTERN_D, replace_patterns, content)
            # Insert the date
            try:
                dates = re.search(r"\d{4}_\d{2}_\d{2}", name)
                date = dates.group()
            except AttributeError:
                date = None
            # Insert the title
            try:
                #fichier_pattern = r"P\d+_(\w+_\d+_\w+)\.txt"
                fich = re.findall(r"P\d+_(.+)\.txt", name)
                titre = fich[0].replace("_", " ").strip()
            except (AttributeError, IndexError):
                titre = name
            try:
                name_pattern = r"[a-zA-Z]\d+_[a-zA-Z]\d+_([A-Za-z_]+)_" \
                               r"\d{4}_\d{2}_\d{2}(\d{1}|(_[A-Za-z_]+)\.txt|)"
                words = re.findall(name_pattern, name)
                result = [item for item in words[0]]
                if len(result) > 0:
                    if result[-1] == "":
                        em_nom = result[0].replace("_", " ").strip()
                    else:
                        one = result[0].replace("_", " ").strip()
                        two = result[-1].replace("_", " ").strip()
                        em_nom = " : ".join([one, two])
                else:
                    name_pattern2 = r"P\d+_(\w+)_\d+_([^\.]+)\.txt"
                    words = re.findall(name_pattern2, name)
                    result = [item for item in words[0]]
                    if len(result) > 0:
                        if result[-1] == "":
                            title = result[0].replace("_", " ").strip()
                            em_nom = title
                        else:
                            one = result[0].replace("_", " ").strip()
                            two = result[-1].replace("_", " ").strip()
                            em_nom = " : ".join([one, two])


            except (AttributeError, IndexError):
                em_nom = None
            fichier_nom = name

            query_emission = "INSERT INTO emission (date_diffusion, " \
                             "emission_nom, fichier_nom, titre) VALUES (?, ?, ?,?)"
            params_emission = (date, em_nom, fichier_nom, titre)
            cursor.execute(query_emission, params_emission)
            emission_id = cursor.lastrowid

            query_transcription = "INSERT INTO transcription (texte, emission_id) VALUES (?, ?)"
            params_transcription = (content, emission_id)
            cursor.execute(query_transcription, params_transcription)

        else:
            pass


def process_text(text):
    """Function that tokenizes the text, removes the stopwords,
    lemmatizes it and selects desired POS tags"""
    doc = nlp(text)
    processed_tokens = []

    for token in doc:
        if token.is_alpha and not token.is_stop and token.text.lower() not in stopwords:
            lemma = token.lemma_.lower()
            if token.pos_ in ['NOUN', 'ADJ', 'ADV', 'VERB', 'PROPN'] and len(lemma) > 2:
                processed_tokens.append(lemma)

    return processed_tokens

def add_processed_tokens_to_transcription(transcription_id, processed_tokens):
    """Function that adds the processed tokens to the DB"""
    lemmas = " ".join(processed_tokens)

    query_update_lemmas = "UPDATE transcription SET lemmas = ? WHERE id = ?"
    params_update_lemmas = (lemmas, transcription_id)
    cursor.execute(query_update_lemmas, params_update_lemmas)

def process_transcriptions():
    """Insert the most common words into the transcription table"""
    for filename in os.listdir(FOLDER_PATH):
        add_transcription_and_emission(filename)

    cursor.execute("SELECT id, texte FROM transcription")
    transcriptions = cursor.fetchall()

    for transcription in transcriptions:
        transcription_id = transcription[0]
        texte = transcription[1]
        processed_words = process_text(texte)
        top_10 = Counter(processed_words).most_common(10)
        for word, frequency in top_10:
            cursor.execute("INSERT INTO freq (word, frequency) VALUES (?, ?)",
                           (word, frequency))
            word_id = cursor.lastrowid
            cursor.execute("INSERT INTO transcription_freq_word "
                           "(transcription_id, word_id) VALUES (?, ?)",
                           (transcription_id, word_id))
        add_processed_tokens_to_transcription(transcription_id, processed_words)

    conn.commit()

process_transcriptions()

conn.close()
