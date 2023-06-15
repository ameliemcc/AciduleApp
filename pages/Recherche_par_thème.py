"""
Builds the page within which the user can search by topic
"""
import os
import sqlite3
import warnings
import streamlit as st
from streamlit import components
from Recherche_par_mot import handle_go_to
warnings.filterwarnings("ignore", category=DeprecationWarning)

emissions = {}

file_path = os.path.join("model", "AciduleDB.db")
conn = sqlite3.connect(file_path)

cursor = conn.cursor()

cursor.execute("SELECT html_content FROM lda_model_info")
model_html = cursor.fetchone()
model_html = model_html[0] if model_html else None

st.set_page_config(page_title='Radio Acidule', page_icon="📻", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)

with st.sidebar.container():
    st.title("AciduleApp")
    text = "Ce graphique (carte de distance interthématique) est utile pour visualiser les relations entre différents sujets dans l'ensemble des transcriptions du corpus Acidule. Il permet de représenter graphiquement la proximité ou l'éloignement entre les différents thèmes abordés. On peut donc s'en servir pour identifier les regroupements de sujets similaires. "
    st.markdown(f"<p style='text-align: justify;'>{text}</p>", unsafe_allow_html=True)
st.components.v1.html(model_html, width=1200, height=600, scrolling=True)

cached_results = {}

for i in range(1, 12):
    cursor.execute("""
        SELECT titre, id
        FROM emission
        WHERE topics LIKE '%({0}, %'
    """.format(i))
    emissions[i] = cursor.fetchall()


st.write('---')

def display_emissions(expander_label, topic_number, emissions):
    with st.expander(expander_label, expanded=False):
        for row in emissions[topic_number]:

            titre = row[0]
            st.write(titre)
            em_id = row[1]
            key_disp = (str(em_id) + '_' + str(topic_number) )
            button_label = f"Accéder à la transcription de cette émission (ID: {key_disp})"
            if st.button(button_label, key=key_disp):
                # Check if the result is already cached
                if key_disp in cached_results:
                    result = cached_results[key_disp]
                else:
                    # Call handle_go_to and cache the result
                    result = handle_go_to(titre)
                    cached_results[key_disp] = result
                st.write(result)
            st.write("---")

# Call the function for each expander
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        display_emissions('Emissions thème 1', 1, emissions)
        display_emissions('Emissions thème 3: Logement, droits des locataires', 3, emissions)
        display_emissions('Emissions thème 5: Conseil communal, politique locale', 5, emissions)
        display_emissions('Emissions thème 7: Astronomie, administration', 7, emissions)
        display_emissions('Emissions thème 9: Médias, droits de l\'Homme, informations internationales', 9, emissions)
        display_emissions('Emissions thème 11: Lois, gouvernement', 11, emissions)
    with col2:
        display_emissions('Emissions thème 2', 2, emissions)
        display_emissions('Emissions thème 4: Sport, compétition, espace', 4, emissions)
        display_emissions('Emissions thème 6: Russie, politique étrangère', 6, emissions)
        display_emissions('Emissions thème 8: Vie culturelle lausannoise', 8, emissions)
        display_emissions('Emissions thème 10', 10, emissions)

conn.close()
