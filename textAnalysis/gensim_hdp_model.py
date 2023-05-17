from gensim.models import HdpModel
from gensim_preprocessing import corpus, dictionary

# Train the HDP model
#Each line represents a topic, where the first element in the tuple is the topic ID, and the following words with their probabilities represent the main words associated with that topic.
hdp_model = HdpModel(corpus=corpus, id2word=dictionary)
topics = hdp_model.print_topics()
for topic in topics:
    print(topic)

# get topics
# use an other corpus to train de model?