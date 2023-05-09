import whisper
import os
import re
import time

from datetime import datetime
start=datetime.now()

options = whisper.DecodingOptions(language= 'fr', fp16=False)
model = whisper.load_model("small")
#result = model.transcribe("S00001_P169_En_depit_du_bon_sens_1989_11_15.mp3")

directory = os.fsencode("/Users/mariemccormick/PycharmProjects/AciduleTranscription/audio_files")

result = model.transcribe("/Users/mariemccormick/PycharmProjects/AciduleTranscription/audio_files/S00004_P169_Nuit_du_logement_1990_04_17_1.mp3")
print(result["text"])


with open("transcriptions/S00004_P169_Nuit_du_logement_1990_04_17_1.txt", "a") as o:
    o.write(result["text"])


'''for root, directories, files in os.walk(directory):
    for filename in files:
            filepath = os.path.join(root, filename)
            result = model.transcribe(filepath, fp16=False)
            name = re.search("\S+?(?=\.\w+$)", filename).group(0)
            with open('transcriptions/' + name + '.txt', "a") as o:
                o.write(result["text"])
            continue
    else:
        continue'''



'''for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".mp3") :
        # print(os.path.join(directory, filename))
        print(str(directory) + '/' + str(filename))
        print(file)
        result = model.transcribe(str(file), fp16=False)

        name = re.search("\S+?(?=\.\w+$)", filename).group(0)
        print(name)
        print(result["text"])

        print('transcriptions/' + name + '.txt')
        with open('transcriptions/' + name + '.txt', "a") as o:
            o.write(result["text"])
        continue
    else:
        continue'''




'''print(result["text"])


with open("transcriptions/S00001_P169_small.txt", "a") as o:
    o.write(result["text"])'''





#Statements

print(datetime.now()-start)
