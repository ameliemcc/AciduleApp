import streamlit as st
import sqlite3
from visualisation.bubble import BubbleChart
import matplotlib.pyplot as plt


# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db')
cursor = conn.cursor()

# Fetch "fichier_nom" values from the "emission" table
cursor.execute("SELECT DISTINCT fichier_nom FROM emission")
fichier_noms = cursor.fetchall()
fichier_noms = [fichier_nom[0] for fichier_nom in fichier_noms]


# Streamlit app
def main():
    st.title("Emission Transcriptions")

    # Sidebar with scroll-down menu
    selected_fichier_nom = st.sidebar.selectbox("Select Fichier Nom", fichier_noms)

    # Query the database to fetch the corresponding "texte" based on the selected "fichier_nom"
    cursor.execute(
        "SELECT t.texte FROM transcription t JOIN emission e ON t.emission_id = e.id WHERE e.fichier_nom = ?",
        (selected_fichier_nom,))
    texte = cursor.fetchone()

    # Display the selected "texte" with line-wrap
    if texte:
        st.markdown("<div style='white-space: pre-line;'>Texte:</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='white-space: pre-line;'>{texte[0]}</div>", unsafe_allow_html=True)
    else:
        st.text("No transcription found for the selected Fichier Nom.")

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
    # make this more succint
    wlist = []
    olist = []
    for word, frequency in words:
        st.write("Word:", word)
        st.write("Frequency:", frequency)
        st.write("---")  # Add a separator between each word-frequency pair
        wlist.append(word)
        olist.append(frequency)

    data = list(zip(wlist, olist))
    print(data)
    k, v = [], []
    for word in data:
        k.append(word[0])
        v.append(word[1])

    word, occurence = k, v
    print(word, occurence)
    length = len(word)
    color = '#F0F8FF'
    colors = [color] * length
    nouns_dict = dict({
        'words': word,
        'occurences': occurence,
        'colors': colors
    })

    bubble_chart = BubbleChart(area=nouns_dict['occurences'],
                               bubble_spacing=0.1)
    bubble_chart.collapse()
    figBubble, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    bubble_chart.plot(
        ax, nouns_dict['words'], nouns_dict['colors'])
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()

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






