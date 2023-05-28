import pprint
from collections import defaultdict
from gensim import corpora
import sqlite3
import spacy
nlp_model = spacy.load("fr_core_news_sm")

# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db')
cursor = conn.cursor()

# Retrieve the content of the 'lemmas' column from the 'transcription' table

cursor.execute("""
    SELECT t.lemmas
    FROM transcription AS t
    INNER JOIN emission AS e ON t.emission_id = e.id
    WHERE e.langue = 'French'
""")

# Fetch the results
transcriptions = cursor.fetchall()

# Create an empty list to store the lemmas
text_corpus = []
exclude_words = ['you', 'all', 'yeah', 'that', 'and', 'pain', 'lover', 'baby', 'monsieur']

def get_lemma_language(lemma):
    # Process the lemma using the language-specific model
    doc = nlp_model(lemma)
    # Access the language code of the model
    language = nlp_model.meta["lang"]
    return language
# Loop over the transcriptions and add the lemmas to the text_corpus list
for transcription in transcriptions:
    lemmas = transcription[0]
    lang = get_lemma_language(lemmas)
    if lang == 'fr':
        if not any(word in lemmas.split() for word in exclude_words):
            text_corpus.append(lemmas)
        #text_corpus.append(lemmas)
    else:
        pass

# Close the connection to the database
conn.close()


# Tokenize the text corpus
texts = []
for document in text_corpus:
    words = document.split()
    texts.append(words)


# Count the frequency of each word
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# Only keep words that appear more than once
#processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
#pprint.pprint(texts)
#texts = process_corpus(texts)

#pprint.pprint(texts)
# Create a dictionary and corpus using Gensim
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(doc) for doc in texts]

#print(dictionary)
'''print(corpus)
print(texts)'''
print(texts[0])
