from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer




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
# we add this to remove stopwords, for lower volumes of data stopwords can cause issues
vectorizer_model = CountVectorizer(ngram_range=(1, 2))

# deal with df if needed

model = BERTopic(
    vectorizer_model=vectorizer_model,
    language='french', calculate_probabilities=True,
    verbose=True
)
topics, probs = model.fit_transform(transcriptions)
