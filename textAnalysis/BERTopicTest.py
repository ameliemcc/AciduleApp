import spacy
from bertopic import BERTopic
from sklearn.datasets import fetch_20newsgroups



docs = fetch_20newsgroups(subset='all',  remove=('headers', 'footers', 'quotes'))['data']

from bertopic import BERTopic

topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
topics, probs = topic_model.fit_transform(docs)

freq = topic_model.get_topic_info(); freq.head(5)

print(type(docs))
print(len(docs))

print(docs[0:2])
'''
topic_model = BERTopic(embedding_model=nlp)
topics, probs = topic_model.fit_transform(docs)

fig = topic_model.visualize_topics()
fig.show()'''