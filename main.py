import streamlit as st
import sqlite3
import numpy as np

import streamlit as st
import sqlite3

# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db')
cursor = conn.cursor()

# Fetch "fichier_nom" values from the "emission" table
cursor.execute("SELECT fichier_nom FROM emission")
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

    with st.container():
        st.write("This is inside the container")

        # You can call any Streamlit command, including custom components:

    with st.container():
        st.write("This is inside the container")
        col1, col2 = st.columns(2)
        with col1:
            st.write("This is column 1")
        with col2:
            st.write("This is column 2")


if __name__ == '__main__':
    main()






