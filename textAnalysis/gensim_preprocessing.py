import os
import spacy
import pprint
import re
import string
from collections import defaultdict
from gensim import corpora


# Define the directory path containing the .txt files
directory = "/Users/mariemccormick/PycharmProjects/AciduleApp/transcriptions"
fr = spacy.load("fr_core_news_sm")
stopwords = list(fr.Defaults.stop_words)

def remove_punctuation(text):
    # Remove punctuation using regular expressions
    text_no_punct = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    return text_no_punct

def remove_numbers(text):
    # Remove numbers using regular expressions
    text_no_numbers = re.sub(r'\d+', '', text)
    return text_no_numbers

def remove_short_words(text):
    words = text.split()
    filtered_words = [word for word in words if len(word) > 2]
    cleaned_text = " ".join(filtered_words)
    return cleaned_text

# Initialize an empty list to store the text content of each file
text_corpus = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as file:
            text = file.read()
            text_corpus.append(text)

# Print the resulting text corpus list

texts = []
for document in text_corpus:
    document = document.replace("'", " ")
    document = remove_punctuation(document)
    document = remove_numbers(document)
    document = remove_short_words(document)
    words = []
    for word in document.lower().split():
        if word not in stopwords:
            words.append(word)
    texts.append(words)


frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# Only keep words that appear more than once
processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
pprint.pprint(processed_corpus)

dictionary = corpora.Dictionary(processed_corpus)
print(dictionary)

corpus = [dictionary.doc2bow(doc) for doc in processed_corpus]
