import os
import pyLDAvis.gensim
import pyLDAvis
import gensim
from gensim import corpora
from gensim.models import TfidfModel
from model.gensim_preprocessing import texts
import sqlite3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

file_path = os.path.join(os.path.dirname(__file__), "AciduleDB.db")
conn = sqlite3.connect(file_path)
cur = conn.cursor()


cur.execute("""
    SELECT t.emission_id, t.lemmas
    FROM transcription AS t
    JOIN emission AS e ON t.emission_id = e.id
    WHERE e.langue = 'French'
""")
rows = cur.fetchall()

cur.execute("SELECT id2word_content FROM lda_model_info")
id2word = cur.fetchone()
id2word = id2word[0] if id2word else None

cur.execute("SELECT lda_model_content FROM lda_model_info")
lda_model = cur.fetchone()
lda_model = lda_model[0] if lda_model else None


for row in rows:
    emission_id, lemmas = row
    lemma_list = lemmas.split()
    doc_bow = id2word.doc2bow(lemma_list)

    # Get the topics for the document
    doc_topics = lda_model.get_document_topics(doc_bow)
    sorted_data = sorted(doc_topics, key=lambda x: x[1], reverse=True)
    #print("Emission id : " + emission_id + "Probabilités: " + sorted_data)
    topic_list = [(index, value) for index, value in sorted_data if value > 0.2]
    topic_string = str(topic_list)  # Convert topic_list to a string
   # cur.execute("UPDATE emission SET topics = ? WHERE id = ?", (topic_string, emission_id))


conn.commit()

conn.close()
