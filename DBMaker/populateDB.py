import os
import re
from DBMaker.main import c, add_emission, conn

path_of_audio_files = 'audio_files'
for filename in os.listdir(path_of_audio_files):
    fichier_nom = os.path.join(path_of_audio_files,filename)
    titre = str(re.findall("(?:S\d+_P\d+_)(\w+)_\d{4}_\d{2}_\d{2}\.mp3", filename))
    date_diffusion = str(re.findall("(?:S\d+_P\d+_)\w+_(\d{4}_\d{2}_\d{2})\.mp3", filename))
    print(date_diffusion)
    print(type(date_diffusion))
    print(titre)
    print(type(titre))
    duree = 0
    transcription_id = 1
    fichier_audio = fichier_nom


   # create_emission_table()
    add_emission(c, fichier_nom, titre, date_diffusion, duree, transcription_id)
    conn.commit()