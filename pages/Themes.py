from textAnalysis.gensim_preprocessing import corpus, dictionary, texts
import numpy as np
import streamlit as st

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

import gensim
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel

from pprint import pprint

import spacy

import pickle
import re
import pyLDAvis
import pyLDAvis.gensim

import matplotlib.pyplot as plt
import pandas as pd

bigram_phrases = gensim.models.Phrases(texts, min_count=5, threshold=100)
trigram_phrases = gensim.models.Phrases(bigram_phrases[texts], threshold=100)

bigram = gensim.models.phrases.Phraser(bigram_phrases)
trigram = gensim.models.phrases.Phraser(trigram_phrases)

def make_bigrams(textss):
    return [bigram[doc] for doc in textss]

def make_trigrams(textss):
    return [trigram[bigram[doc]] for doc in textss]

data_bigrams = make_bigrams(texts)
data_bigrams_trigrams = make_trigrams(data_bigrams)

print(data_bigrams_trigrams[0])

print(data_bigrams)

from gensim.models import TfidfModel

id2word = corpora.Dictionary(data_bigrams_trigrams)

texts_removal = data_bigrams_trigrams

corpus = [id2word.doc2bow(text) for text in texts_removal]
print(corpus[0][0:20])

tfidf = TfidfModel(corpus, id2word=id2word )

low_value = 0.03
words = []
words_missing_in_tfidf = []

lda_model = gensim.models.ldamodel.LdaModel(corpus = corpus,
                                           id2word=dictionary,
                                           num_topics=15,
                                           random_state = 100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=15,
                                           alpha="auto")

pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

pyLDAvis.enable_notebook()
vis=pyLDAvis.gensim.prepare(lda_model, corpus, dictionary, mds="mmds", R=30)
st.show(vis)