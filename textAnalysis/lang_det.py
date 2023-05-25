import spacy
import sqlite3
import langcodes

from spacy_language_detection import LanguageDetector
from spacy.language import Language


def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)  # We use the seed 42


def detect_and_update_language():
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db')
    cursor = conn.cursor()

    # Load the Spacy language model for language detection
    nlp_model = spacy.load("fr_core_news_sm")

    # Register the 'language' attribute
    Language.factory("language_detector", func=get_lang_detector)
    nlp_model.add_pipe('language_detector', last=True)

    # Fetch all the emission IDs and texte from the transcription table
    cursor.execute("SELECT e.id, t.texte FROM emission e JOIN transcription t ON e.id = t.emission_id")
    rows = cursor.fetchall()

    for row in rows:
        emission_id, texte = row

        # Detect the language of the texte using Spacy
        doc = nlp_model(texte)

        # Extract the language code and convert it to the language name
        lang = str(doc._.language['language'])
        language = langcodes.Language.make(lang).language_name()

        # Update the lien column of the emission table with the detected language
        cursor.execute("UPDATE emission SET langue = ? WHERE id = ?", (language, emission_id))

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()


# Call the function to detect and update the language
detect_and_update_language()
