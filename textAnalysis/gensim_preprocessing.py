import pprint
from collections import defaultdict
from gensim import corpora
import sqlite3

# Establish a connection to the SQLite database
conn = sqlite3.connect('/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db')
cursor = conn.cursor()

# Retrieve the content of the 'lemmas' column from the 'transcription' table
cursor.execute("SELECT lemmas FROM transcription")
transcriptions = cursor.fetchall()

# Create an empty list to store the lemmas
text_corpus = []

# Loop over the transcriptions and add the lemmas to the text_corpus list
for transcription in transcriptions:
    lemmas = transcription[0]
    text_corpus.append(lemmas)

# Close the connection to the database
conn.close()

# Print the text_corpus list
#print(text_corpus)

# Tokenize the text corpus
texts = []
for document in text_corpus:
    words = document.split()
    texts.append(words)

#print(texts)


def process_corpus(texts):
    # Count the frequency of each word across documents
    word_frequency = defaultdict(int)
    for text in texts:
        unique_words = set(text)
        for token in unique_words:
            word_frequency[token] += 1

    # Determine the maximum allowed occurrence based on the 40% threshold
    max_occurrence = len(texts) * 0.2

    # Only keep words that occur less than or equal to the maximum allowed occurrence
    processed_corpus = [[token for token in text if word_frequency[token] <= max_occurrence] for text in texts]
    return processed_corpus


# Count the frequency of each word
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# Only keep words that appear more than once
#processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
#pprint.pprint(texts)
#texts = process_corpus(texts)
print('---------')
#pprint.pprint(texts)
# Create a dictionary and corpus using Gensim
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(doc) for doc in texts]

print(dictionary)
print(corpus)
print(texts)