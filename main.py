import streamlit as st
import sqlite3
from visualisation.bubble import BubbleChart
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import streamlit.components.v1 as components
from streamlit_searchbox import st_searchbox

# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db')
cursor = conn.cursor()

# Fetch "fichier_nom" values from the "emission" table
cursor.execute("SELECT DISTINCT fichier_nom FROM emission")
fichier_noms = [fichier_nom[0] for fichier_nom in cursor.fetchall()]

# Fetch "emission_nom" values from the "emission" table
cursor.execute("SELECT DISTINCT emission_nom FROM emission")
emission_noms = [emission_nom[0] for emission_nom in cursor.fetchall()]

# Fetch "date_diffusion" values from the "emission" table
cursor.execute("SELECT DISTINCT date_diffusion FROM emission")
dates_diffusion = [date_diffusion[0] for date_diffusion in cursor.fetchall()]



# Streamlit app
def main():
    last_selected = None

    st.markdown(open('htmlStyle.html').read(), unsafe_allow_html=True)
    st.title("Radio Acidule")

    cursor.execute("""
        SELECT word, COUNT(*) AS count
        FROM freq
        GROUP BY word
        """)

    # Retrieve the results as a list of tuples (word, count)
    results = cursor.fetchall()

    # Create a list of formatted word entries (word (count))
    form_results = [f"{word} ({count})" for word, count in results]

    def search_items(searchterm: str) -> [str]:
        if not searchterm:
            return sorted(form_results)  # Return all items in alphabetical order
        suggestions = [form_results for form_results in form_results if searchterm.lower() in form_results.lower()]
        suggestions.sort()  # Sort the suggestions alphabetically
        return suggestions

    # Display the search bar in the sidebar
    with st.sidebar.container():
        selected_value = st_searchbox(
            search_items,
            placeholder="Search for a word",
            key="items_searchbox",
        )
        if selected_value:
            last_selected = "searchbox"

    # Print the selected item
    if selected_value:
        st.write("Selected item:", selected_value)
        st.write("---")  # Separator between lines

    # Fetch fichier_nom values that have the selected frequency word

    # Print the selected item
    if selected_value:
        st.write("Selected item:", selected_value)
        st.write("---")  # Separator between lines

        # Fetch the IDs from the freq table
        cursor.execute("SELECT id FROM freq WHERE word = ?", (selected_value.split()[0],))
        ids = [row[0] for row in cursor.fetchall()]

        # Iterate over the IDs
        for id in ids:
            # Select the corresponding word_id and transcription_id from the transcription_freq_word table
            cursor.execute("SELECT word_id, transcription_id FROM transcription_freq_word WHERE word_id = ?", (id,))

            # Retrieve the results as a list of tuples (word_id, transcription_id)
            results = cursor.fetchall()

            # Iterate over the results
            for word_id, transcription_id in results:
                # Get the word corresponding to the word_id from the freq table
                cursor.execute("SELECT word FROM freq WHERE id = ?", (word_id,))
                word = cursor.fetchone()[0]
                cursor.execute("SELECT emission_id FROM transcription WHERE id = ?", (transcription_id,))
                emission_id = cursor.fetchone()[0]
                cursor.execute("SELECT emission_nom FROM emission WHERE id = ?", (emission_id,))
                emission_nom = cursor.fetchone()[0]

                # Select the words associated with the same transcription_id from the transcription_freq_word table
                cursor.execute("""
                    SELECT f.word
                    FROM transcription_freq_word AS tfw
                    JOIN freq AS f ON tfw.word_id = f.id
                    WHERE tfw.transcription_id = ? AND tfw.word_id != ?
                    """, (transcription_id, word_id))

                # Retrieve the associated words as a list of strings
                associated_words = [row[0] for row in cursor.fetchall()]

                # Display the emission information and associated words
                st.write("Emission Nom:", emission_nom)
                st.write("Word:", word)
                word_list = []
                for word in associated_words:
                    word_list.append(word)
                words = ' – '.join(word_list)
                st.write("Associated Words:", words)
                st.write("---")  # Separator between lines

    html_style = open('htmlStyle.html').read()
    selected_fichier_nom = st.sidebar.selectbox("Choisir une émission", emission_noms)
    if selected_fichier_nom:
        last_selected = "selectbox"

    st.write("Last selected:", last_selected)

    # Query the database to fetch the corresponding "date_diffusion" based on the selected "fichier_nom"
    cursor.execute("SELECT date_diffusion FROM emission WHERE emission_nom = ?", (selected_fichier_nom,))
    date = cursor.fetchone()
    date_form = ''.join(date) if date else ""

    # Query the database to fetch the corresponding "texte" based on the selected "fichier_nom"
    cursor.execute(
        "SELECT t.texte FROM transcription t JOIN emission e ON t.emission_id = e.id WHERE e.emission_nom = ?",
        (selected_fichier_nom,))
    texte = cursor.fetchone()

    # Query the database to fetch word and frequency from the "freq" table based on the selected "fichier_nom"
    cursor.execute("""
        SELECT f.word, f.frequency
        FROM freq AS f
        INNER JOIN transcription_freq_word AS tfw ON tfw.word_id = f.id
        INNER JOIN transcription AS t ON t.id = tfw.transcription_id
        INNER JOIN emission AS e ON e.id = t.emission_id
        WHERE e.emission_nom = ?
        """, (selected_fichier_nom,))
    words = cursor.fetchall()

    if words:
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
        figBubble, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
        bubble_chart.plot(ax, nouns_dict['words'], nouns_dict['colors'])

        ax.axis("off")
        ax.relim()
        ax.autoscale_view()

        st.header(date_form + ', ' + selected_fichier_nom)

        # Display the chart inside a container
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.write("Thèmes")
            with col2:
                st.write("Mots fréquents")
                st.pyplot(fig=figBubble)
    else:
        st.text("No transcription found for the selected Fichier Nom.")

    # Display the selected "texte" with line-wrap
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

if __name__ == '__main__':
    main()

