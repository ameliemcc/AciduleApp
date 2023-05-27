import re
import sqlite3
import spacy
from collections import Counter
import os
from spacy.symbols import NOUN, ORTH, LEMMA, POS


nlp = spacy.load("fr_core_news_sm")
# this didn't work
nlp.Defaults.noun_rules = { "Madame": [{ORTH: "Madame", LEMMA: "Madame", POS: NOUN}] }
nlp.Defaults.noun_rules = { "madame": [{ORTH: "madame", LEMMA: "madame", POS: NOUN}] }


# Establish a connection to the SQLite database
conn = sqlite3.connect('AciduleDB.db')
cursor = conn.cursor()

#folder_path = "/Users/mariemccormick/PycharmProjects/AciduleApp/transcriptions"  # Path to the folder containing the .txt files
folder_path = "../transcriptions"  # Path to the folder containing the .txt files

stopwords = ["beaucoup", "bien", "oui", "non", "bon", "être", "avoir", "pouvoir", "faire",  "envoyer", "aller", "prendre", "devoir", "chose" ]
# match repeating numbers
patternNumb = r'\b(\d)(?: \1)+\b'
# match repeating ... ... ...
patternDots = r'(\.\.\.)\W{2,}'

def replace_patterns(match):
    return ''

def add_transcription_and_emission(name):
    if name.endswith(".txt"):
        file_path = os.path.join(folder_path, name)
        with open(file_path, "r") as file:
            content = file.read()

        # Don't add into the DB if the transcription is empty
        if len(content) > 20:
            content = re.sub(patternNumb, replace_patterns, content)
            content = re.sub(patternDots, replace_patterns, content)
            # Insert the date
            try:
                date_pattern = r"\d{4}_\d{2}_\d{2}"
                dates = re.search(date_pattern, name)
                date = dates.group()
            except AttributeError:
                date = None
            # Insert the title
            try:
                #fichier_pattern = r"P\d+_(\w+_\d+_\w+)\.txt"
                fichier_pattern = r"P\d+_(.+)\.txt"
                fich = re.findall(fichier_pattern, name)
                titre = fich[0]
                titre = titre.replace("_", " ").strip()
            except (AttributeError, IndexError):
                titre = name
            print(titre)
            #insert fichier nom
            try:
                # https://regex101.com/r/O6P1f2/1
                name_pattern = r"[a-zA-Z]\d+_[a-zA-Z]\d+_([A-Za-z_]+)_\d{4}_\d{2}_\d{2}(\d{1}|(_[A-Za-z_]+)\.txt|)"
                words = re.findall(name_pattern, name)
                result = [item for item in words[0]]
                if len(result) > 0:
                    if result[-1] == "":
                        title = result[0].replace("_", " ").strip()
                        em_nom = title
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
                # ADD a last option for when no regex matches
                #else:
                    #name_pattern

            except (AttributeError, IndexError):
                em_nom = None
            print(em_nom)
            fichier_nom = name

            # Insert into emission table and retrieve the emission_id
            query_emission = "INSERT INTO emission (date_diffusion, emission_nom, fichier_nom, titre) VALUES (?, ?, ?,?)"
            params_emission = (date, em_nom, fichier_nom, titre)
            cursor.execute(query_emission, params_emission)
            emission_id = cursor.lastrowid

            # Insert the text with the corresponding emission_id
            query_transcription = "INSERT INTO transcription (texte, emission_id) VALUES (?, ?)"
            params_transcription = (content, emission_id)
            cursor.execute(query_transcription, params_transcription)

        else:
            pass


def process_text(text):
    doc = nlp(text)
    processed_tokens = []

    for token in doc:
        if token.is_alpha and not token.is_stop and token.text.lower() not in stopwords:
            lemma = token.lemma_.lower()
            if token.pos_ in ['NOUN', 'ADJ', 'ADV', 'VERB', 'PROPN'] and len(lemma) > 2:
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

