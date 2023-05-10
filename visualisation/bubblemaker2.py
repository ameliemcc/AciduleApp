import streamlit as st
import sqlite3
from bubble import BubbleChart
import matplotlib.pyplot as plt

# Establish a connection to the SQLite database
conn = sqlite3.connect("/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db")
cursor = conn.cursor()

# Retrieve the distinct "fichier_nom" values from the "emission" table
cursor.execute("SELECT DISTINCT fichier_nom FROM emission")
fichier_noms = cursor.fetchall()
fichier_noms = [fichier_nom[0] for fichier_nom in fichier_noms]

# Close the database connection
cursor.close()
conn.close()

# Create a Streamlit sidebar with the scroll-down menu for "fichier_nom"
selected_fichier_nom = st.sidebar.selectbox("Select fichier_nom", fichier_noms)

# Establish a new connection to the SQLite database
conn = sqlite3.connect("/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db")
cursor = conn.cursor()

# Retrieve the word and frequency from the "freq" table based on the selected "fichier_nom"
cursor.execute("""
    SELECT f.word, f.frequency
    FROM freq AS f
    INNER JOIN transcription_freq_word AS tfw ON tfw.word_id = f.id
    INNER JOIN transcription AS t ON t.id = tfw.transcription_id
    INNER JOIN emission AS e ON e.id = t.emission_id
    WHERE e.fichier_nom = ?
    """, (selected_fichier_nom,))
words = cursor.fetchall()

# Close the database connection
cursor.close()
conn.close()

# Display the selected "fichier_nom" on the right side of the web interface
st.write("Selected fichier_nom:", selected_fichier_nom)

# Display the word and frequency from the "freq" table on the right side of the web interface
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


word, occurence = k,v
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
fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
bubble_chart.plot(
                    ax, nouns_dict['words'], nouns_dict['colors'])
ax.axis("off")
ax.relim()
ax.autoscale_view()
               # titre = str(re.findall("b'(S\d{5}_P\d{3}_\w+_\d{4}_\d{2}_\d{2})\.txt'", str(filename)))
               # print(titre)
plt.show()
st.pyplot(fig=fig)
