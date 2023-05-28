from textAnalysis.gensim_preprocessing import corpus, dictionary, texts
import numpy as np
import json
import glob
from streamlit import components
import sqlite3
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import streamlit as st
from gensim.models import TfidfModel

bigrams_phrases = gensim.models.Phrases(texts, min_count=5, threshold=100)
trigram_phrases = gensim.models.Phrases(bigrams_phrases[texts], threshold=100)

bigram = gensim.models.phrases.Phraser(bigrams_phrases)
trigram = gensim.models.phrases.Phraser(trigram_phrases)

def make_bigrams(textss):
    return [bigram[doc] for doc in textss]

def make_trigrams(textss):
    return [trigram[bigram[doc]] for doc in textss]

data_bigrams = make_bigrams(texts)
data_bigrams_trigrams = make_trigrams(data_bigrams)
#print(data_bigrams_trigrams[0])

# dictionary
id2word = corpora.Dictionary(data_bigrams_trigrams)

texts_removal = data_bigrams_trigrams

# corpus
corpus = [id2word.doc2bow(text) for text in texts_removal]

tfidf = TfidfModel(corpus, id2word=id2word )

low_value = 0.03
words = []
words_missing_in_tfidf = []

def process_corpus(corpus):
    for i in range(len(corpus)):
        bow = corpus[i]
        low_value_words = []
        tfidf_ids = [id for id, value in tfidf[bow]]
        bow_ids = [id for id, value in bow]
        low_value_words = [id for id, value in tfidf[bow] if value < low_value]
        #drops = low_value_words + words_missing_in_tfidf
        drops = low_value_words
        for item in drops:
            words.append(id2word[item])
        words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids]
        new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]
        corpus[i] = new_bow
    return corpus

corpus = process_corpus(corpus)

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=12,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=15,
                                           alpha="auto")

#lda_model.save("models/ldamodel.model")
print('corpus-1')
test_doc = corpus[-1]
print(type(test_doc))
print('test doc')
print(test_doc)
print(lda_model[test_doc])
#print(new_vector)
#pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
html_string = pyLDAvis.prepared_data_to_html(vis)


# Establish a connection to the database
conn = sqlite3.connect("/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db")
cur = conn.cursor()

# Fetch the rows from the transcription table
#cur.execute("SELECT emission_id, lemmas FROM transcription")

cur.execute("""
    SELECT t.emission_id, t.lemmas
    FROM transcription AS t
    JOIN emission AS e ON t.emission_id = e.id
    WHERE e.langue = 'French'
""")
rows = cur.fetchall()

def Sort(sub_li):
    sub_li.sort(key=lambda x: x[1])
    sub_li.reverse()
    return sub_li

for row in rows:
    emission_id, lemmas = row
    lemma_list = lemmas.split()
    # Convert the lemma list to bag-of-words representation
    doc_bow = id2word.doc2bow(lemma_list)

    # Get the topics for the document
    doc_topics = lda_model.get_document_topics(doc_bow)
    sorted_data = sorted(doc_topics, key=lambda x: x[1], reverse=True)

    topic_list = [(index, value) for index, value in sorted_data if value > 0.2]
    print(f"Emission ID: {emission_id}, Topics: {topic_list}")
    topic_string = str(topic_list)  # Convert topic_list to a string
   # cur.execute("UPDATE emission SET topics = ? WHERE id = ?", (topic_string, emission_id))


conn.commit()

conn.close()

