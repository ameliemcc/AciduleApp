import pprint
from collections import defaultdict
from gensim import corpora
import sqlite3

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

# Loop over the transcriptions and add the lemmas to the text_corpus list
for transcription in transcriptions:
    lemmas = transcription[0]
    text_corpus.append(lemmas)

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
#print(corpus)
#print(texts)