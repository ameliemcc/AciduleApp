import streamlit as st
from streamlit import components
import warnings
import sqlite3
warnings.filterwarnings("ignore", category=DeprecationWarning)
from gensim.models import TfidfModel
from textAnalysis.gensim_lda_model import html_string
from Recherche_par_mot import handle_go_to

st.components.v1.html(html_string, width=1200, height=600, scrolling=True)
conn = sqlite3.connect("/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker"
                       "/AciduleDB.db")
cursor = conn.cursor()


cursor.execute("""
    SELECT titre
    FROM emission
    WHERE topics LIKE '%(1, %'
""")
emission_1 = cursor.fetchall()

cursor.execute("""
    SELECT titre
    FROM emission
    WHERE topics LIKE '%(2, %'

""")
emission_2 = cursor.fetchall()

cursor.execute("""
    SELECT titre
    FROM emission
    WHERE topics LIKE '%(3, %'

""")
emission_3 = cursor.fetchall()


#st.markdown(f'<iframe srcdoc="{html_string}" width="800" height="600" style="transform: scale(0.8);"></iframe>', unsafe_allow_html=True)
st.write('---')
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
    with col2:
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")
        with st.expander('Emissions thème 1 ', expanded=False):
            for row in emission_1:
                titre = row[0]
                st.write(titre)
                st.write("---")



