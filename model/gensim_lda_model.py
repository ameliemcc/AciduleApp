"""
Training the LDA model and applying it to the emissions that are in french
"""
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


bigrams_phrases = gensim.models.Phrases(texts, min_count=5, threshold=100)
trigram_phrases = gensim.models.Phrases(bigrams_phrases[texts], threshold=100)

bigram = gensim.models.phrases.Phraser(bigrams_phrases)
trigram = gensim.models.phrases.Phraser(trigram_phrases)

def make_bigrams(textss):
    """Define words that go together often"""
    return [bigram[doc] for doc in textss]

def make_trigrams(textss):
    """Define words that go together often (groups of 3)"""
    return [trigram[bigram[doc]] for doc in textss]

data_bigrams = make_bigrams(texts)
data_bigrams_trigrams = make_trigrams(data_bigrams)

# dictionary
id2word = corpora.Dictionary(data_bigrams_trigrams)

texts_removal = data_bigrams_trigrams

# corpus
corpus = [id2word.doc2bow(text) for text in texts_removal]

tfidf = TfidfModel(corpus, id2word=id2word )

LOW_VALUE = 0.03
words = []
words_missing_in_tfidf = []

def process_corpus(corpus_proc):
    """drop words that come back too often (low_value)"""
    for i in range(len(corpus_proc)):
        bow = corpus_proc[i]
        low_value_words = []
        tfidf_ids = [id for id, value in tfidf[bow]]
        bow_ids = [id for id, value in bow]
        low_value_words = [id for id, value in tfidf[bow] if value < LOW_VALUE]
        #drops = low_value_words + words_missing_in_tfidf
        drops = low_value_words
        for item in drops:
            words.append(id2word[item])
        words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids]
        new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in
                   words_missing_in_tfidf]
        corpus_proc[i] = new_bow
    return corpus_proc

corpus = process_corpus(corpus)

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=12,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=15,
                                           alpha="auto")

vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word, mds="mmds", R=30)

html_string = pyLDAvis.prepared_data_to_html(vis)


file_path = os.path.join(os.path.dirname(__file__), "AciduleDB.db")
conn = sqlite3.connect(file_path)
# Connect to the SQLite database

cur = conn.cursor()

# Store the HTML string in a variable
html_string = pyLDAvis.prepared_data_to_html(vis)

# Insert the HTML string into the database
cur.execute("INSERT INTO lda_model_info (html_content) VALUES (?)", (html_string,))
id2word_str = str(id2word)
cur.execute("INSERT INTO lda_model_info (id2word_content) VALUES (?)", (id2word_str,))
lda_model_str = str(lda_model)
cur.execute("INSERT INTO lda_model_info (lda_model_content) VALUES (?)", (lda_model_str,))


cur.execute("""
    SELECT t.emission_id, t.lemmas
    FROM transcription AS t
    JOIN emission AS e ON t.emission_id = e.id
    WHERE e.langue = 'French'
""")
rows = cur.fetchall()


for row in rows:
    emission_id, lemmas = row
    lemma_list = lemmas.split()
    doc_bow = id2word.doc2bow(lemma_list)

    # Get the topics for the document
    doc_topics = lda_model.get_document_topics(doc_bow)
    sorted_data = sorted(doc_topics, key=lambda x: x[1], reverse=True)
    topic_list = [(index, value) for index, value in sorted_data if value > 0.2]
    topic_string = str(topic_list)  # Convert topic_list to a string
    cur.execute("UPDATE emission SET topics = ? WHERE id = ?", (topic_string, emission_id))

# Commit the transaction and close the connection
conn.commit()
conn.close()
