import streamlit as st
from streamlit_searchbox import st_searchbox
#st.text_input('Entrez un mot-clé pour afficher la liste des émissions correspondantes:', help = "Musique, eau, garderie,...")
from streamlit_searchbar import streamlit_searchbar
# https://github.com/m-wrzr/streamlit-searchbox
st.caption('Entrez un mot-clé pour afficher la liste des émissions correspondantes:')

# collect all the frequent words
# count how many texts they are frequent words of
# display in searchbox : politique (16)
# on click, show list of emission:
# emission_nom, date_diffusion, fichier_nom,
# Mots fréquents : skjfd - osnfosn - sjbfdisb- celui selectionné en gras
# Thèmes :
# On click, amener à la page comme main pour voir schéma et transcription

import sqlite3

# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db')
cursor = conn.cursor()

# Fetch all unique word entries and calculate the total frequencies
cursor.execute("""
    SELECT word, COUNT(*) AS count
    FROM freq
    GROUP BY word
    """)
# click box for suggestions by most popular or by alphabetical order ?
# Retrieve the results as a list of tuples (word, total_frequency)
results = cursor.fetchall()

form_results = [f"{word} ({count})" for word, count in results]


def search_items(searchterm: str) -> [str]:
    if not searchterm:
        return sorted(form_results)  # Return all items in alphabetical order
    suggestions = [form_results for form_results in form_results if searchterm.lower() in form_results.lower()]
    suggestions.sort()  # Sort the suggestions alphabetically
    return suggestions

# Pass search function to searchbox
selected_value = st_searchbox(
    search_items,
    key="items_searchbox",
)

# Print the selected item
if selected_value:
    st.write("Selected item:", selected_value)

# Fetch fichier_nom values that have the selected frequency word
if selected_value:

    # Fetch all unique word entries and their corresponding emission details
    # Fetch all unique word entries and their corresponding emission details
    cursor.execute("""
        SELECT e.fichier_nom, e.emission_nom, e.date_diffusion, GROUP_CONCAT(f.word) AS freq_words
        FROM emission AS e
        INNER JOIN transcription AS t ON e.id = t.emission_id
        INNER JOIN transcription_freq_word AS tfw ON t.id = tfw.transcription_id
        INNER JOIN freq AS f ON tfw.word_id = f.id
        WHERE f.word = ?
        AND tfw.transcription_id IN (
            SELECT tfw.transcription_id
            FROM transcription_freq_word AS tfw
            INNER JOIN freq AS f ON tfw.word_id = f.id
            WHERE f.word = ?
            AND tfw.word_id != (
                SELECT id
                FROM freq
                WHERE word = ?
            )
        )
        GROUP BY e.fichier_nom
        """, (selected_value.split()[0], selected_value.split()[0],
              selected_value.split()[0]))  # selected_value contains "word (count)"

    # Retrieve the results as a list of tuples (fichier_nom, emission_nom, date_diffusion, freq_words)
    results = cursor.fetchall()

    # Display the results in separate boxes
    for fichier_nom, emission_nom, date_diffusion, freq_words in results:
        st.write("Fichier Nom:", fichier_nom)
        st.write("Emission Nom:", emission_nom)
        st.write("Date Diffusion:", date_diffusion)
        st.write("Associated Freq Words:", freq_words)
        st.write("---")  # Separator between boxes

    # Fetch the IDs from the freq table
    cursor.execute("SELECT id FROM freq WHERE word = ?", (selected_value.split()[0],))
    ids = [row[0] for row in cursor.fetchall()]

    # Iterate over the IDs
    for id in ids:
        # Select the corresponding word_id and transcription_id from the transcription_freq_word table
        cursor.execute("SELECT word_id, transcription_id FROM transcription_freq_word WHERE word_id = ?",
                       (id,))

        # Retrieve the results as a list of tuples (word_id, transcription_id)
        results = cursor.fetchall()

        # Display the word and transcription_id
        for word_id, transcription_id in results:
            # Get the word corresponding to the word_id from the freq table
            cursor.execute("SELECT word FROM freq WHERE id = ?", (word_id,))
            word = cursor.fetchone()[0]

            st.write("Word:", word)
            st.write("Transcription ID:", transcription_id)
            st.write("---")  # Separator between lines
    # Fetch the IDs from the freq table
    cursor.execute("SELECT id FROM freq WHERE word = ?", (selected_value.split()[0],))
    ids = [row[0] for row in cursor.fetchall()]

    # Iterate over the IDs
    for id in ids:
        # Select the corresponding word_id and transcription_id from the transcription_freq_word table
        cursor.execute("SELECT word_id, transcription_id FROM transcription_freq_word WHERE word_id = ?",
                       (id,))

        # Retrieve the results as a list of tuples (word_id, transcription_id)
        results = cursor.fetchall()

        # Iterate over the results
        for word_id, transcription_id in results:
            # Get the word corresponding to the word_id from the freq table
            cursor.execute("SELECT word FROM freq WHERE id = ?", (word_id,))
            word = cursor.fetchone()[0]

            # Select the words associated with the same transcription_id from the transcription_freq_word table
            cursor.execute("""
                SELECT f.word
                FROM transcription_freq_word AS tfw
                JOIN freq AS f ON tfw.word_id = f.id
                WHERE tfw.transcription_id = ? AND tfw.word_id != ?
                """, (transcription_id, word_id))

            # Retrieve the associated words as a list of strings
            associated_words = [row[0] for row in cursor.fetchall()]

            st.write("Word:", word)
            st.write("Word ID:", word_id)
            st.write("Transcription ID:", transcription_id)
            st.write("Associated Words:", associated_words)
            st.write("---")  # Separator between lines

conn.close()