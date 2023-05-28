"""
Builds the page within which the user can search by topic
"""
import os
import sqlite3
import warnings
import streamlit as st
from streamlit import components
warnings.filterwarnings("ignore", category=DeprecationWarning)
#from textAnalysis.gensim_lda_model import html_string

file_path = os.path.join("database_maker", "AciduleDB.db")
conn = sqlite3.connect(file_path)

cursor = conn.cursor()

emissions = {}

with st.sidebar.container():
    st.title("AciduleApp")
st.components.v1.html(html_string, width=1200, height=600, scrolling=True)

for i in range(1, 12):
    cursor.execute("""
        SELECT titre
        FROM emission
        WHERE topics LIKE '%({0}, %'
    """.format(i))
    emissions[i] = cursor.fetchall()

st.write('---')
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emissions[1]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 3 : Logement, droits des locataires', expanded=False):
            for row in emissions[3]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 5 : Conseil communal, politique locale', expanded=False):
            for row in emissions[5]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 7 : Politique suisse, vote ', expanded=False):
            for row in emissions[7]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 9 : Médias, droits de '
                         'l\'Homme, informations internationales' , expanded=False):
            for row in emissions[9]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 11 : Lois, gouvernement ', expanded=False):
            for row in emissions[11]:
                titre = row[0]
                st.write(titre)
                st.write("---")
    with col2:
        with st.expander('Emissions thème 2 ', expanded=False):
            for row in emissions[2]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 4 : Sport, compétition, espace', expanded=False):
            for row in emissions[4]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 6 : Russie, politique étrangère', expanded=False):
            for row in emissions[6]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 8 : Vie culturelle lausannoise', expanded=False):
            for row in emissions[8]:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 10 ', expanded=False):
            for row in emissions[10]:
                titre = row[0]
                st.write(titre)
                st.write("---")

conn.close()
