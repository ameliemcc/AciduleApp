import os
import re
import sqlite3

# Establish a connection to the SQLite database
conn = sqlite3.connect('AciduleDB.db')
cursor = conn.cursor()



folder_path = "/Users/mariemccormick/PycharmProjects/AciduleApp/transcriptions"  # Path to the folder containing the .txt files

# Loop over the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            content = file.read()
            cursor.execute("INSERT INTO emission (fichier_nom) VALUES (?)", (filename,))
            # Get the last inserted ID (primary key) from "emission" table
            emission_id = cursor.lastrowid
            # Process the filename and content as needed
            cursor.execute("INSERT INTO transcription (texte, emission_id) VALUES (?, ?)",
                           (content, emission_id))

            # Process the filename and content as needed

            print()  # Add a blank line for separation


# Commit the changes and close the connection
conn.commit()
conn.close()









#from database_maker.main import c, add_emission, conn

# loop over the transcriptions
# add them to the db
# at the same time, find correspondin g



'''
path_of_audio_files = '/Users/mariemccormick/PycharmProjects/AciduleApp/transcriptions'
for filename in os.listdir(path_of_audio_files):
    fichier_nom = os.path.join(path_of_audio_files,filename)
    titre = str(re.findall("(?:S\d+_P\d+_)(\w+)_\d{4}_\d{2}_\d{2}\.txt", filename))
    date_diffusion = str(re.findall("(?:S\d+_P\d+_)\w+_(\d{4}_\d{2}_\d{2})\.txt", filename))
    date_diffusion = str(re.findall("(?:S\d+_P\d+_\w+_)(\d{4}_\d{2}_\d{2})\.txt|(\d{4}_\d{2}_\d{2}_\d{1})\.txt", filename))

    print(date_diffusion)
    print(type(date_diffusion))
    print(titre)
    print(type(titre))
    duree = 0
    transcription_id = 1
    fichier_audio = fichier_nom'''

   # create_emission_table()
   # add_emission(c, fichier_nom, titre, date_diffusion, duree, transcription_id)
   # conn.commit()

#/ (?:S\d+_P\d+_)\w + _((\d{4}_\d{2}_\d{2})\.txt | (\d{4}_\d{2}_\d{2}_\d{1})\.txt) / gm

#/(?:S\d+_P\d+_\w+_)(\d{4}_\d{2}_\d{2})\.txt|(\d{4}_\d{2}_\d{2}_\d{1})\.txt/gm