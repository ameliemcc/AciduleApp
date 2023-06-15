"""
Detecting which language the emission is in and adding the information to the database.
"""
import os
import sqlite3
import spacy
import langcodes
from spacy_language_detection import LanguageDetector
from spacy.language import Language

def get_lang_detector(nlp, name):
    """Function necessary to use the spacy LanguageDetector"""
    return LanguageDetector(seed=42)


def detect_and_update_language():
    """Function to detect the language and add it to the DB"""
    file_path = os.path.join(os.path.dirname(__file__), "AciduleDB.db")
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    nlp_model = spacy.load("fr_core_news_sm")

    Language.factory("language_detector", func=get_lang_detector)
    nlp_model.add_pipe('language_detector', last=True)

    cursor.execute("SELECT e.id, "
                   "t.texte FROM emission e "
                   "JOIN transcription t ON e.id = t.emission_id")
    rows = cursor.fetchall()

    for row in rows:
        emission_id, texte = row

        doc = nlp_model(texte)

        lang = str(doc._.language['language'])
        language = langcodes.Language.make(lang).language_name()

        cursor.execute("UPDATE emission SET langue = ? WHERE id = ?", (language, emission_id))

    conn.commit()

    conn.close()

detect_and_update_language()
