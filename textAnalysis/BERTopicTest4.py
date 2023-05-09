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
                n = 700
                docs = [(text[i:i + n]) for i in range(0, len(text), n)]
                transcriptions = transcriptions +docs
                continue
        else:
            continue
print(transcriptions)
print(len(transcriptions))

topic_model = BERTopic(language="french", calculate_probabilities=True, verbose=True)
topics, probs = topic_model.fit_transform(transcriptions)

freq = topic_model.get_topic_info(); freq.head(20)
print(freq)
most = topic_model.get_topic(0)  # Select the most frequent topic
print(most) # Select the most frequent topic)

pred = topic_model.topics_[:10]
print(pred)


fig = topic_model.visualize_topics()
fig.show()

#print(topic_model.topics_[:10])