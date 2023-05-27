"""
Provides the main page structure of the code, the sidebar selectboxes and display of transcriptions
"""

import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from visualisation.bubble import BubbleChart


with open("htmlStyle.html", "r", encoding="utf8") as file:
    html_style = file.read()
st.set_page_config(page_title='Radio Acidule', page_icon="📻", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)

conn = sqlite3.connect("/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker"
                       "/AciduleDB.db")
cursor = conn.cursor()

# Fetch "fichier_nom" values from the "emission" table
cursor.execute("SELECT DISTINCT fichier_nom FROM emission")
fichier_noms = [fichier_nom[0] for fichier_nom in cursor.fetchall()]

# Fetch "lien" values from the "emission" table
cursor.execute("SELECT DISTINCT lien FROM emission")
liens = [lien[0] for lien in cursor.fetchall()]

# Fetch "emission_nom" values from the "emission" table
cursor.execute("SELECT DISTINCT emission_nom FROM emission")
emission_noms = [emission_nom[0] for emission_nom in cursor.fetchall()]

# Fetch "date_diffusion" values from the "emission" table
cursor.execute("SELECT DISTINCT date_diffusion FROM emission")
dates_diffusion = [date_diffusion[0] for date_diffusion in cursor.fetchall()]

cursor.execute("""
            SELECT word, COUNT(*) AS count
            FROM freq
            GROUP BY word
            """)
results = cursor.fetchall()
form_results = [f"{word} ({count})" for word, count in results]


def extract_number(string):
    """Function extracting numbers out of the formated list items. """
    return int(string.split('(')[1].split(')')[0])


if 'check' not in st.session_state:
    st.session_state['check'] = False

if st.session_state.check is True:
    form_results = sorted(form_results, key=extract_number, reverse=True)
    form_results.insert(0, '')

if st.session_state.check is False:
    form_results.insert(0, '')


def make_bubbles(words):
    """Function to make the bubbleplot fig"""
    word, occurrence = zip(*words)
    # Define the colormap and normalize the values
    colormap = plt.cm.get_cmap('summer')
    normalize = mcolors.Normalize(vmin=min(occurrence), vmax=max(occurrence))
    # Generate a color for each number in the list
    colors = [mcolors.to_hex(colormap(normalize(value))) for value in occurrence]
    nouns_dict = {
        'words': list(word),
        'occurrences': list(occurrence),
        'colors': colors
    }

    # Create the bubble chart
    bubble_chart = BubbleChart(area=nouns_dict['occurrences'], bubble_spacing=0.1)
    bubble_chart.collapse()
    fig_bubble, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    bubble_chart.plot(ax, nouns_dict['words'], nouns_dict['colors'])

    ax.axis("off")
    ax.relim()
    ax.autoscale_view()
    return fig_bubble


def handle_select():
    """Function handling the actions taken when an emission is selected from the selectbox. """
    st.write(st.session_state.select_emission)
    selected_fichier_nom = st.session_state.select_emission
    cursor.execute("SELECT date_diffusion FROM emission WHERE emission_nom = ?",
                   (selected_fichier_nom,))
    date = cursor.fetchone()
    date_form = ''.join(date) if date else ""

    # Query the database to fetch the corresponding "texte" based on the selected "fichier_nom"
    cursor.execute(
        "SELECT t.texte FROM transcription t JOIN emission e ON t.emission_id = e.id WHERE e.emission_nom = ?",
        (selected_fichier_nom,))
    texte = cursor.fetchone()
    cursor.execute("""
            SELECT f.word, f.frequency
            FROM freq AS f
            INNER JOIN transcription_freq_word AS tfw ON tfw.word_id = f.id
            INNER JOIN transcription AS t ON t.id = tfw.transcription_id
            INNER JOIN emission AS e ON e.id = t.emission_id
            WHERE e.emission_nom = ?
            """,
                   (selected_fichier_nom,)
                   )
    words = cursor.fetchall()

    if words:
        fig_bubble = make_bubbles(words)
        st.header(date_form + ', ' + selected_fichier_nom)
        # Display the chart inside a container
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.write("Thèmes")
                #st.components.v1.html(html_code)
            with col2:
                st.write("Mots fréquents")
                st.pyplot(fig=fig_bubble)
    else:
        st.text("No transcription found for the selected Fichier Nom.")
    if texte:
        st.components.v1.html(html_style + """
            <div class="box">
            {}
            </div>
            """.format(texte[0]), scrolling=True, height=300)
        st.download_button(
            label='Télécharger la transcription',
            data=texte[0],
            file_name=selected_fichier_nom
        )
    else:
        st.text("No transcription found for the selected Fichier Nom.")


def handle_search():
    """Function handling the actions taken when a frequent word is selected from the selectbox. """
    selected_value = st.session_state.select_word
    selected_word = selected_value.split()[0]
    cursor.execute("SELECT id FROM freq WHERE word = ?",
                   (selected_word,))
    ids = [row[0] for row in cursor.fetchall()]
    for id_word in ids:
        # Select the corresponding word_id and transcription_id from the transcription_freq_word table
        cursor.execute("SELECT word_id, "
                       "transcription_id FROM transcription_freq_word WHERE word_id = ?",
                       (id_word,))
        # Retrieve the results as a list of tuples (word_id, transcription_id)
        search_results = cursor.fetchall()
        # Display the word and transcription_id
        for word_id, transcription_id in search_results:
            # Get the word corresponding to the word_id from the freq table
            cursor.execute("SELECT word FROM freq WHERE id = ?", (word_id,))
            word = cursor.fetchone()[0]
            cursor.execute("SELECT emission_id FROM transcription WHERE id = ?",
                           (transcription_id,))
            emission_id = cursor.fetchone()[0]
            cursor.execute("SELECT emission_nom FROM emission WHERE id = ?", (emission_id,))
            emission_nom = cursor.fetchone()[0]
            cursor.execute("""
                           SELECT f.word
                           FROM transcription_freq_word AS tfw
                           JOIN freq AS f ON tfw.word_id = f.id
                           WHERE tfw.transcription_id = ? AND tfw.word_id != ?
                           """, (transcription_id, word_id))

            # Retrieve the associated words as a list of strings
            associated_words = [row[0] for row in cursor.fetchall()]
            st.write(word)
            with st.expander(label=str(emission_nom)):
                word_list = []
                for word in associated_words:
                    word_list.append(word)
                words = ' – '.join(word_list)
                st.write("Mots les plus fréquents dans cette émission:", words)
                st.button('Accéder à la transcription de cette émission', key=emission_id)


def sidebar_elements():
    """Function handling the display of sidebar elements"""
    st.checkbox('Trier les mots par fréquence', value=False, key='check')
    st.selectbox('Rechercher un mot fréquent',
                 form_results,
                 on_change=handle_search,
                 key='select_word',
                 index=0
                 )
    st.selectbox('Choisir une émission',
                 emission_noms,
                 on_change=handle_select,
                 key='select_emission'
                 )


def main():
    with st.sidebar.container():
        sidebar_elements()


if __name__ == "__main__":
    main()
