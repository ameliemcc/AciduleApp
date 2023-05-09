# Find 10 most frequent words, excluding stopwords, and 10 most frequent NOUNS in each transcription file

import spacy
from collections import Counter
import os
nlp = spacy.load("fr_core_news_sm")

directory = os.fsencode("/Users/mariemccormick/PycharmProjects/AciduleTranscription/transcriptions")


def ten_common_words(doc):
    filtered_tokens = []
    for token in doc:
        if token.is_stop == False and token.text.isalpha() == True:
            filtered_tokens.append(token.lemma_)
    word_freq = Counter(filtered_tokens)
    common_words = word_freq.most_common(10)
    return common_words


def ten_common_nouns(doc):
    filtered_tokens_nouns = []
    for token in doc:
        if token.is_stop == False and token.text.isalpha() == True and token.pos_ == 'NOUN':
            filtered_tokens_nouns.append(token.lemma_)
    word_freq = Counter(filtered_tokens_nouns)
    common_words = word_freq.most_common(10)
    return common_words


for root, directories, files in os.walk(directory):
    for filename in files:
        filepath = os.path.join(root, filename)
        with open(filepath,  encoding="utf8", errors='ignore') as file:
            text = file.read()
            doc = nlp(text)
            print(filename)
            print(ten_common_words(doc))
            print(ten_common_nouns(doc))
            continue
    else:
        continue
