from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim_preprocessing import corpus, dictionary

lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)

# Get keywords for each topic
for topic_id in range(lda_model.num_topics):
    topic_terms = lda_model.get_topic_terms(topic_id, topn=10)  # Adjust 'topn' as needed
    topic_keywords = [dictionary[id] for id, _ in topic_terms]
    print(f"Topic {topic_id+1} keywords: {topic_keywords}")

for i, doc_bow in enumerate(corpus):
    doc_topics = lda_model.get_document_topics(doc_bow)
    print(f"Document {i+1} topics: {doc_topics}")
