# Find 10 most frequent NOUNS in each transcription file and produce bubble plot
import spacy
from collections import Counter
import os
nlp = spacy.load("fr_core_news_sm")
from visualisation.bubble import BubbleChart
import matplotlib.pyplot as plt
directory = os.fsencode("/Users/mariemccormick/PycharmProjects/AciduleTranscription/transcriptions")


def ten_common_nouns(doc):
    filtered_tokens_nouns = []
    for token in doc:
        if token.is_stop == False and token.text.isalpha() == True and token.pos_ == 'NOUN':
            token.lemma_ = str(token.lemma_).lower()
            filtered_tokens_nouns.append(token.lemma_)
    word_freq = Counter(filtered_tokens_nouns)
    common_words = word_freq.most_common(10)
    k, v = [], []
    for word in common_words:
        k.append(word[0])
        v.append(word[1])
    return (k, v)


for root, directories, files in os.walk(directory):
    for filename in files:
        filepath = os.path.join(root, filename)

        try:
            with open(filepath,  encoding="utf8", errors='ignore') as file:
                text = file.read()
                text = text.lower()
                doc = nlp(text)
                word, occurence = ten_common_nouns(doc)
                length = len(word)
                color = '#F0F8FF'
                colors = [color] * length
                nouns_dict = dict({
                    'words' : word,
                    'occurences' : occurence,
                    'colors' :colors
                })
                bubble_chart = BubbleChart(area=nouns_dict['occurences'],
                                           bubble_spacing=0.1)
                bubble_chart.collapse()
                fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
                bubble_chart.plot(
                    ax, nouns_dict['words'], nouns_dict['colors'])
                ax.axis("off")
                ax.relim()
                ax.autoscale_view()
                ax.set_title(filename)
               # titre = str(re.findall("b'(S\d{5}_P\d{3}_\w+_\d{4}_\d{2}_\d{2})\.txt'", str(filename)))
               # print(titre)
                plt.show()
                #plt.savefig("/Users/mariemccormick/PycharmProjects/AciduleTranscription/images/"+ str(titre) + ".png")
                plt.close()
        except ValueError:
            continue
    else:
        continue




