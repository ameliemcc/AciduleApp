"""
Provides the code for an HDP model - not used in the final project
"""
from gensim.models import HdpModel
from gensim_preprocessing import corpus, dictionary

# Train the HDP model
hdp_model = HdpModel(corpus=corpus, id2word=dictionary)
topics = hdp_model.print_topics()
for topic in topics:
    print(topic)

