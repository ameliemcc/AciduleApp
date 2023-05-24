import streamlit as st
import sqlite3
from visualisation.bubble import BubbleChart
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import streamlit.components.v1 as components

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
    st.markdown(open('htmlStyle.html').read(), unsafe_allow_html=True)
    st.title("Radio Acidule")

    html_style = open('htmlStyle.html').read()
    selected_fichier_nom = st.sidebar.selectbox("Select Fichier Nom", emission_noms)

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

