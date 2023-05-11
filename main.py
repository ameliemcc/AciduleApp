import streamlit as st
import sqlite3
from visualisation.bubble import BubbleChart
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db')
cursor = conn.cursor()

# Fetch "fichier_nom" values from the "emission" table
cursor.execute("SELECT DISTINCT fichier_nom FROM emission")
fichier_noms = [fichier_nom[0] for fichier_nom in cursor.fetchall()]


# Streamlit app
def main():
    st.markdown(open('htmlStyle.html').read(), unsafe_allow_html=True)

    st.title("Emission Transcriptions")
    html_style = open('htmlStyle.html').read()
    # Sidebar with scroll-down menu
    selected_fichier_nom = st.sidebar.selectbox("Select Fichier Nom", fichier_noms)

    # Query the database to fetch the corresponding "texte" based on the selected "fichier_nom"
    cursor.execute(
        "SELECT t.texte FROM transcription t JOIN emission e ON t.emission_id = e.id WHERE e.fichier_nom = ?",
        (selected_fichier_nom,))
    texte = cursor.fetchone()

    # Display the selected "texte" with line-wrap
    if texte:
        #st.markdown("<div style='white-space: pre-line;'>Texte:</div>", unsafe_allow_html=True)
        #st.markdown(f"<div style='white-space: pre-line;'>{texte[0]}</div>", unsafe_allow_html=True)
        st.components.v1.html(html_style + """ 
        <div class = "box" >
        {}
        </div>
        """.format(texte[0]), scrolling=True, height=300)
    else:
        st.text("No transcription found for the selected Fichier Nom.")

    # Query the database to fetch word and frequency from the "freq" table based on the selected "fichier_nom"
    cursor.execute("""
        SELECT f.word, f.frequency
        FROM freq AS f
        INNER JOIN transcription_freq_word AS tfw ON tfw.word_id = f.id
        INNER JOIN transcription AS t ON t.id = tfw.transcription_id
        INNER JOIN emission AS e ON e.id = t.emission_id
        WHERE e.fichier_nom = ?
        """, (selected_fichier_nom,))
    words = cursor.fetchall()

    # Display the word and frequency from the "freq" table on the right side of the web interface
    word, occurrence = zip(*words)
    colors = ['#F0F8FF'] * len(word)


   # color_palette = ['#FDF6E3', '#FFA07A', '#8FD8D2', '#FFD700']

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

    # Display the chart inside a container
    with st.container():
        st.write("This is inside the container")
        col1, col2 = st.columns(2)
        with col1:
            st.write("This is column 1")
        with col2:
            st.write("This is column 2")
        st.pyplot(fig=figBubble)


if __name__ == '__main__':
    main()
