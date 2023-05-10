# Find 10 most frequent NOUNS in each transcription file and produce bubble plot
import spacy
from collections import Counter
import os
nlp = spacy.load("fr_core_news_sm")
from visualisation.bubble import BubbleChart
import matplotlib.pyplot as plt
directory = os.fsencode("/Users/mariemccormick/PycharmProjects/AciduleApp/transcriptions")


import sqlite3

conn = sqlite3.connect("/Users/mariemccormick/PycharmProjects/AciduleApp/database_maker/AciduleDB.db")
cursor = conn.cursor()

# Retrieve the distinct transcription_id values
cursor.execute("SELECT DISTINCT transcription_id FROM transcription_freq_word")
transcription_ids = cursor.fetchall()

nouns_dict = []

for transcription_id in transcription_ids:
    # Retrieve the word and frequency for the given transcription_id
    print(transcription_id)
    cursor.execute("""
        SELECT f.word, f.frequency
        FROM freq AS f
        INNER JOIN transcription_freq_word AS tfw ON tfw.word_id = f.id
        WHERE tfw.transcription_id = ?
        """, (transcription_id[0],))
    words = cursor.fetchall()
    print(words)

    # Create a dictionary for the transcription_id
    transcription_dict = {
        'transcription_id': transcription_id[0],
        'nouns': [{'word': word[0], 'occurrences': word[1], 'colors': 4} for word in words]
    }
    nouns_dict.append(transcription_dict)
    for word, occurrence in words:
        print(word)
        print(occurrence)
cursor.close()
conn.close()



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