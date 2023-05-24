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
    SELECT word, SUM(frequency) AS total_frequency
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



conn.close()