from textAnalysis.gensim_preprocessing import corpus, dictionary, texts
import numpy as np
import json
import glob
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import streamlit as st
## Bigrams and trigrams


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

print(data_bigrams_trigrams[0])



# TF-IDF REMOVAL


from gensim.models import TfidfModel

id2word = corpora.Dictionary(data_bigrams_trigrams)

texts_removal = data_bigrams_trigrams

corpus = [id2word.doc2bow(text) for text in texts_removal]
print(corpus[0][0:20])

tfidf = TfidfModel(corpus, id2word=id2word )

low_value = 0.03
words = []
words_missing_in_tfidf = []



print(texts[0][0:20])


## Vizualizing the data


lda_model = gensim.models.ldamodel.LdaModel(corpus = corpus,
                                           id2word=id2word,
                                           num_topics=15,
                                           random_state = 100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=15,
                                           alpha="auto")

#%%

#pyLDAvis.enable_notebook()
vis=pyLDAvis.gensim.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
html_string = pyLDAvis.prepared_data_to_html(vis)
st.components.v1.html(html_string, width=800, height=600)

