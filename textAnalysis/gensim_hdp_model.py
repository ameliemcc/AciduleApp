from gensim.models import HdpModel
from gensim_preprocessing import corpus, dictionary

# Train the HDP model
#Each line represents a topic, where the first element in the tuple is the topic ID, and the following words with their probabilities represent the main words associated with that topic.
hdp_model = HdpModel(corpus=corpus, id2word=dictionary)
topics = hdp_model.print_topics()
for topic in topics:
    print(topic)

'''topic_assignments = [hdp_model.infer(doc) for doc in corpus]
for i, doc_topics in enumerate(topic_assignments):
    print(f"Document {i}: {doc_topics}")'''


for document in corpus:
    topic_distribution = hdp_model.get_document_topics(document)
    print(topic_distribution)