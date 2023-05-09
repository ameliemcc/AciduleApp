import spacy
import os
from bertopic import BERTopic
nlp = spacy.load("fr_core_news_sm")
import chardet
import os

directory = os.fsencode("/Users/mariemccormick/PycharmProjects/AciduleTranscription/transcriptions")
transcriptions = []

for root, directories, files in os.walk(directory):
    for filename in files:
        filepath = os.path.join(root, filename)
        if filename.endswith(".txt".encode('utf-8')) :
            with open(filepath,  encoding="utf8", errors='ignore') as file:
                text = file.read()
                doc = nlp(text)
                transcriptions.append(text)
                continue
        else:
            continue
print(transcriptions)
print(len(transcriptions))

topic_model = BERTopic(language="french", calculate_probabilities=True, verbose=True)
topics, probs = topic_model.fit_transform(transcriptions)

freq = topic_model.get_topic_info(); freq.head(20)

print(topic_model.get_topic(0)) # Select the most frequent topic)

print(freq)

#print(topic_model.topics_[:10])